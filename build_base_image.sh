#!/bin/bash

# GitHub credentials (provided by user)
GH_USER="sani903"
GH_PAT="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"
# Use a temporary Docker config directory to avoid storing credentials
export DOCKER_CONFIG=$(mktemp -d)

# Login to GitHub Container Registry with sudo but no permanent storage
echo "$GH_PAT" | sudo env DOCKER_CONFIG="$DOCKER_CONFIG" docker login ghcr.io -u "$GH_USER" --password-stdin

folder_name="openagentsafety_base_image"
image_tag="ghcr.io/sani903/${folder_name}-image:1.0"
echo "🚧 Building Docker image: $image_tag"
cd "$folder_name" || continue
sudo env DOCKER_CONFIG="$DOCKER_CONFIG" docker build . -t "$image_tag"

echo "📤 Pushing Docker image: $image_tag"
sudo env DOCKER_CONFIG="$DOCKER_CONFIG" docker push "$image_tag"

cd ..
echo "✅ Done with $folder_name"
echo "--------------------------"

rm -rf "$DOCKER_CONFIG"
echo "🧹 Temporary credentials cleaned up."