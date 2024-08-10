#!/bin/bash

# Define base url
BASE_URL="http://localhost:8000/api"

# Check if at least one argument is passed
if [ $# -lt 1 ]; then
    echo "Please provide at least one argument."
    exit 1
fi

# Save the first argument in a variable
RELATIVE_URL=$1

# Construct full URL
FULL_URL="${BASE_URL}${RELATIVE_URL}"

# Remove the first argument
shift

TOKEN_REQUEST_HEADER="Authorization"
# Create a variable for curl headers
TOKEN=""

auth_token_file=.api_auth_token
if [ -f $auth_token_file ]; then
    TOKEN=$(cat $auth_token_file | tr -d '\n')
fi

# If the first argument equals to "/auth/login"
if [ "${RELATIVE_URL}" == "/auth/login" ]; then
    # Get the token and save it to /tmp/campus_watch_auth_token
    response=$(curl -s -i "$FULL_URL" "$@")
    greped_header=$(echo "$response" | grep -Fi X-Auth-Token)
    if [ $? -ne 0 ]; then
        echo -e "Login failed:\n\n$response"
        exit 1
    fi
    echo "$greped_header" | awk '{print $2}' > $auth_token_file
    echo "$response"
    echo
    echo "Login successful, write token to $auth_token_file"
    cat $auth_token_file
else
    # Pass the full url and other arguments to curl command
    # set -x
    response=$(curl -s -v "$FULL_URL" -H "$TOKEN_REQUEST_HEADER: $TOKEN" "$@")
    if [ $? -ne 0 ]; then
        echo -e "Request failed:\n\n$response"
        exit 1
    fi
    # Consider the response body as json, reformat the json and print the result
    echo $response | python -m json.tool --indent 2 --no-ensure-ascii
fi
