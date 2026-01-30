#!/bin/bash

# Ensure script is running from the correct directory
cd "$(dirname "$0")" || exit 1

TEMPLATE="data/users_template.json"
USERS_FILE="data/users.json"

# Step 1: Create users.json from template if it doesn't exist
if [ ! -f "$USERS_FILE" ]; then
    echo "Setting up users.json from template..."
    cp "$TEMPLATE" "$USERS_FILE"
fi

# Step 2: Check if users.json is empty (first run)
if [ ! -s "$USERS_FILE" ]; then
    echo "First-time setup detected!"
    python3 scripts/auth.py -c
fi

# Step 3: Normal login
python3 scripts/auth.py

