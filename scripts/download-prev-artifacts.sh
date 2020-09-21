#!/bin/bash

# Run in GitHub actions to download previous workflow run docker images to speed up build
#
# DEFAULT_BRANCH: The name of the branch to find workflow runs in
# GITHUB_REPOSITORY: The repository to search for artifacts in
# GITHUB_WORKFLOW_CODE: The name of the GitHub Workflow

ARTIFACTS_URLS=$(curl -sL "https://api.github.com/repos/$GITHUB_REPOSITORY/actions/workflows/$GITHUB_WORKFLOW_CODE.yml/runs" | jq -r '.workflow_runs[] | select(.head_branch="next_release") | .artifacts_url')
ARTIFACTS_URL=""

while IFS= read -r url; do
    echo "$url"
    count=$(curl -L "$url" | jq -r '.total_count')
    if [[ "$count" != "0" ]]; then
        ARTIFACTS_URL="$url"
        break
    fi
done <<< "$ARTIFACTS_URLS"

if [[ "$ARTIFACTS_URL" == "" ]]; then
    echo "No runs with images available"
    exit 1
fi

IMAGES_URL=$(curl -L "$ARTIFACTS_URL" | jq -r '[.artifacts[] | select(.name=="build_images")][0].archive_download_url')

echo "Artifacts: $ARTIFACTS_URL"
echo "Images: $IMAGES_URL"

if [[ "$IMAGES_URL" == "null" ]]; then
    echo "No previous run"
    exit 0
fi

curl -L $IMAGES_URL -o /tmp/prev_run.zip
unzip /tmp/prev_run.zip -d /tmp/prev_run

find /tmp/prev_run -maxdepth 1 -type f -exec docker load -i {} \;
