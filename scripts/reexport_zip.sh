#!/bin/bash

echo "Reexporting $1"

COPY="$1.SAVED"
echo "Saving a copy first to $COPY"
cp "$1" "$COPY"

echo "Force-importing $1"
django-admin.py import "$1" --force

echo "Exporting it to $1"
django-admin.py export registry --filename=$1
