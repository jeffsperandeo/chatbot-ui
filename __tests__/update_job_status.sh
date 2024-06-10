#!/bin/bash

# Variables
jobId="$1"
status="$2"
note="$3"
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"

# API Endpoint
url="https://sandbox.tekmetric.com/api/v1/jobs/${jobId}"

# Payload
payload=$(cat <<EOF
{
  "completed": ${status},
  "note": "${note}"
}
EOF
)

# Make the API request
response=$(curl -s -X PATCH "$url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $accessToken" \
  -d "$payload")

# Check for success
if echo "$response" | grep -q '"type":"SUCCESS"'; then
  echo "Job status updated successfully:"
  echo "$response"
else
  echo "Failed to update job status:"
  echo "$response"
fi
