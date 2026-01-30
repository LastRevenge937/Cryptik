#!/bin/bash

# Get the shell user
USER_NAME="$USER"
[ -z "$USER_NAME" ] && USER_NAME="authorized_user"

echo ">> Waking Химера as $USER_NAME"
python3 src/main.py "$USER_NAME"
