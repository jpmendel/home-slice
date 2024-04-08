#!/bin/bash

remote=$1

if [ -z "${remote}" ]; then
    echo "usage: deploy.sh [remote_path]"
    echo "  remote_path: Path to the app location on Raspberry Pi"
    exit 1
fi

echo "Copying to Raspberry Pi..."
rsync -avz --rsh=ssh . "${remote}" --include-from=./deploy/sync_files.txt --delete-excluded
echo "App Uploaded!"
