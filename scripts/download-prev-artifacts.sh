#!/bin/sh

ARTIFACTS_URL=$(curl -sL https://api.github.com/repos/scriptsmith/gh-actions-test/actions/workflows/ci.yml/runs | jq -r '[.workflow_runs[] | select(.head_branch=="next_release")][0].artifacts_url')
IMAGES_URL=$(curl -L "$ARTIFACTS_URL" | jq -r '[.artifacts[] | select(.name=="build_images")][0].archive_download_url')

echo "Artifacts: $ARTIFACTS_URL"
echo "Images: $IMAGES_URL"

curl -L $IMAGES_URL -o prev_run.zip
unzip prev_run.zip -d prev_run

find prev_run -maxdepth 1 -type f -exec docker load -i {} \; > results.out
