from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from rdrf.models.proms.models import SurveyAssignment
from rdrf.models.proms.models import Survey
from rdrf.models.proms.models import SurveyStates
from rdrf.models.definition.models import Registry
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from rdrf.forms.components import RDRFContextLauncherComponent
from registry.patients.models import Patient
from rdrf.forms.components import RDRFPatientInfoComponent
from rdrf.forms.navigation.locators import PatientLocator
from rdrf.forms.proms_forms import SurveyRequestForm
from rdrf.models.proms.models import SurveyRequest
from rdrf.models.proms.models import SurveyRequestStates
from django.http import JsonResponse
from django.conf import settings
import json
import qrcode
from rdrf.security.security_checks import security_check_user_patient


import logging
logger = logging.getLogger(__name__)


class PromsCompletedPageView(View):
    def get(self, request):
        return render(request, "proms/proms_completed.html", {})


class PromsView(View):
    def get(self, request):
        patient_token = request.session.get("patient_token", None)
        if patient_token is None:
            raise Http404

        survey_assignment = self._get_survey_assignment(patient_token)
        if survey_assignment is None:
            raise Http404

        registry_model = survey_assignment.registry
        survey_name = survey_assignment.survey_name

        survey_model = get_object_or_404(Survey,
                                         registry=registry_model,
                                         name=survey_name)

        survey_questions = survey_model.client_rep

        completed_page = reverse("proms_completed")

        context = {"production": False,
                   "patient_token": patient_token,
                   "registry_code": registry_model.code,
                   "survey_name": survey_name,
                   "completed_page": completed_page,
                   "questions": json.dumps(survey_questions),
                   }

        if hasattr(settings, "PROMS_TEMPLATE"):
            proms_template = settings.PROMS_TEMPLATE
        else:
            proms_template = "proms/proms.html"

        return render(request, proms_template, context)

    def _get_survey_assignment(self, patient_token):
        # patient tokens should be once off so unique to assignments
        try:
            return SurveyAssignment.objects.get(patient_token=patient_token)
        except SurveyAssignment.DoesNotExist:
            logger.error("No survey assignment with patient token %s" % patient_token)
            return None
        except SurveyAssignment.MultipleObjectsReturned:
            logger.error("Multiple survey assignments for patient token %s" % patient_token)
            return None


class PromsLandingPageView(View):
    def get(self, request):
        patient_token = request.GET.get("t", None)
        registry_code = request.GET.get("r", None)
        survey_name = request.GET.get("s", None)
        if not self._is_valid(patient_token,
                              registry_code,
                              survey_name):
            raise Http404

        registry_model = get_object_or_404(Registry, code=registry_code)
        check_login = registry_model.has_feature("proms_landing_login")

        survey_assignment = get_object_or_404(SurveyAssignment,
                                              patient_token=patient_token,
                                              state=SurveyStates.REQUESTED)
        survey_display_name = survey_assignment.survey.display_name
        preamble_text = registry_model.metadata.get("preamble_text")
        context = {
            "preamble_text": preamble_text,
            "survey_name": survey_display_name
        }

        if check_login:
            if request.user.is_anonymous:
                logger.warning(f"User id {request.user.id} not authorised to see survey (user is anonymous)")
                raise Http404
            else:
                from rdrf.helpers.utils import is_authorised
                # NB this will only work if proms on same site
                t = survey_assignment.patient_token
                survey_request = get_object_or_404(SurveyRequest,
                                                   patient_token=t,
                                                   state="requested")
                patient_model = survey_request.patient

                if not is_authorised(request.user, patient_model):
                    logger.warning(f"User id {request.user.id} not authorised to see survey")
                    raise Http404

        return render(request, "proms/preamble.html", context)

    def _is_valid(self, patient_token, registry_code, survey_name):
        return True

    def post(self, request):
        patient_token = request.GET.get("t", None)
        registry_code = request.GET.get("r", None)
        survey_name = request.GET.get("s", None)
        if not self._is_valid(patient_token,
                              registry_code,
                              survey_name):
            raise Http404

        registry_model = get_object_or_404(Registry, code=registry_code)

        # Check survey model exists.
        get_object_or_404(Survey,
                          registry=registry_model,
                          name=survey_name)

        survey_assignment = get_object_or_404(SurveyAssignment,
                                              registry=registry_model,
                                              survey_name=survey_name,
                                              patient_token=patient_token,
                                              state=SurveyStates.REQUESTED)

        survey_assignment.response = "{}"
        survey_assignment.save()
        request.session["patient_token"] = patient_token
        return HttpResponseRedirect(reverse("proms"))


class PromsClinicalView(View):
    """
    What the clinical system sees
    """

    def get(self, request, registry_code, patient_id):
        registry_model = Registry.objects.get(code=registry_code)
        patient_model = Patient.objects.get(id=patient_id)
        security_check_user_patient(request.user, patient_model)

        context = self._build_context(request.user,
                                      registry_model,
                                      patient_model)

        return render(request, "proms/proms_clinical.html", context)

    def _build_context(self, user, registry_model, patient_model):
        survey_requests = self._get_survey_requests(registry_model,
                                                    patient_model)
        context_launcher = RDRFContextLauncherComponent(user,
                                                        registry_model,
                                                        patient_model,
                                                        "PROMS")

        survey_request_form = self._build_survey_request_form(registry_model,
                                                              patient_model,
                                                              user)

        context = {
            "context_launcher": context_launcher.html,
            "location": "Patient Reported Outcomes",
                        "patient": patient_model,
                        "survey_requests": survey_requests,
                        "patient_link": PatientLocator(registry_model,
                                                       patient_model).link,
                        "patient_info": RDRFPatientInfoComponent(registry_model, patient_model, user).html,
                        "survey_request_form": survey_request_form,

        }

        return context

    def _build_survey_request_form(self, registry_model, patient_model, user):
        initial_data = {
            "patient": patient_model,
            "registry": registry_model,
            "user": user.username,
        }
        # restrict the available survey choices based on the registry config

        surveys = [(s["code"], s["description"]) for s in registry_model.metadata.get("surveys", [])]

        return SurveyRequestForm(initial=initial_data, surveys=surveys)

    def _get_survey_requests(self, registry_model, patient_model):
        return SurveyRequest.objects.filter(registry=registry_model,
                                            patient=patient_model).order_by("-created").all()

    def post(self, request, registry_code, patient_id):
        survey_name = request.POST.get("survey_name")
        patient_id = request.POST.get("patient")
        registry_id = request.POST.get("registry")
        patient_token = request.POST.get("patient_token")
        user = request.POST.get("user")
        registry_model = Registry.objects.get(id=registry_id)
        patient_model = Patient.objects.get(id=patient_id)
        security_check_user_patient(request.user, patient_model)
        communication_type = request.POST.get("communication_type")

        survey_request = SurveyRequest(survey_name=survey_name,
                                       registry=registry_model,
                                       patient=patient_model,
                                       user=user,
                                       state=SurveyRequestStates.REQUESTED,
                                       patient_token=patient_token,
                                       communication_type=communication_type,
                                       )
        survey_request.save()

        survey_request.send()

        return JsonResponse({"patient_token": survey_request.patient_token})


class PromsQRCodeImageView(View):
    def get(self, request, patient_token):
        from django.http import HttpResponse
        try:
            survey_request = SurveyRequest.objects.get(patient_token=patient_token)
        except SurveyRequest.DoesNotExist:
            raise Http404
        except SurveyRequest.MultipleObjectsReturned:
            raise Http404

        link = survey_request.email_link
        image = self._make_image(link)
        response = HttpResponse(content_type='image/png')
        image.save(response)
        return response

    def _make_image(self, data):
        return qrcode.make(data)
