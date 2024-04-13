#!/bin/bash

set -o allexport
source .pienv
set +o allexport

echo "Copying to Raspberry Pi..."
rsync -avz --rsh=ssh . "${RPI_REMOTE_USER}@${RPI_REMOTE_HOST}:/home/pi/app" --include-from=./deploy/sync_files.txt
echo "App Uploaded!"
