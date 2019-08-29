/*
Collapsing panel support for TRRF form panels.

Call CollapsingPanels.setUp() on document ready and set .collapsible CSS class on .panel's you want to be collapsible/expandable.

If the page has a .trrf-page-header we also add a collapse/expand all button to the header.
*/

var CollapsingPanels = function() {
    var collapsiblePanelsSelector = "form .panel.collapsible";

    function getAllPanelBodies() {
        return $(collapsiblePanelsSelector +  ' > .panel-body');
    }

    function expandAll() {
        getAllPanelBodies().collapse('show');
    }

    function collapseAll() {
        getAllPanelBodies().collapse('hide');
    }

    function setUpCollapseAllButton() {
        // Adding the collapse button works only if we have one and only one <hx> element in the page header.
        // Otherwise, we might mess up the layout. This can be further customise as needed later on (ie. pass in selector of the button etc.)
        var pageHeader = $('.trrf-page-header > .panel-body > :header');
        if (pageHeader.size() != 1) {
            return;
        }
        var collapseAllToggleBtn = $('<span class="badge pull-right"><span class="glyphicon glyphicon-sort"></span></span>');

        function onCollapseAll() {
            var panelBodies = $(collapsiblePanelsSelector +  ' > .panel-body');
            var allCollapsed = panelBodies.filter('.collapse.in').size() == 0;
            if (allCollapsed) {
                expandAll();
            } else {
                collapseAll();
            }
        }

        collapseAllToggleBtn.on('click', onCollapseAll);
        pageHeader.append(collapseAllToggleBtn);
    }

    function setUpCollapsiblePanel() {
        var panel = $(this);
        var header = panel.children(".panel-heading");
        var body = panel.children(".panel-body");
        var iconParent = header;
        if (header.find(".panel-title").size() == 1) {
            iconParent = header.find(".panel-title");
        }

        header.css("cursor", "pointer");
        body.addClass("collapse");

        header.find("a").each(function() {
            $(this).on('click', function(evt) {
                evt.stopPropagation();
                return true;
            });
        });

        header.on('click', function(evt) {
            body.collapse('toggle');
        })

        function createIconElement(panel) {
            var body = panel.children(".panel-body");
            var isCollapsed = !body.hasClass('in');
            var icon = isCollapsed ? 'glyphicon-triangle-right' : 'glyphicon-triangle-bottom';
            return '<span class="panel-collapse-icon glyphicon ' + icon + '"></span>';
        }

        function toggleIcon() {
            header.find('span[class*="panel-collapse-icon"]').toggleClass('glyphicon-triangle-right glyphicon-triangle-bottom');
        }

        panel.on('hide.bs.collapse', toggleIcon);
        panel.on('show.bs.collapse', toggleIcon);

        iconParent.prepend(createIconElement(panel));
   }


    function setUp() {
        var collapsiblePanels = $(collapsiblePanelsSelector);
        // Apply only when we have more than 1 collapsible panel
        // if (collapsiblePanels.size() <= 1)
        //    return;

        collapsiblePanels.each(setUpCollapsiblePanel);
        setUpCollapseAllButton();
    }

    return {
        setUp: setUp,
        expandAll: expandAll,
        collapseAll: collapseAll
    }
}();

