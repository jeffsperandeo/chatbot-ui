#!/bin/bash

# Variables
jobId="$1"
partId="$2"
quantity="$3"
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"

# API Endpoint
url="https://sandbox.tekmetric.com/api/v1/jobs/${jobId}/parts"

# Payload
payload=$(cat <<EOF
{
  "partId": ${partId},
  "quantity": ${quantity}
}
EOF
)

# Make the API request
response=$(curl -s -X POST "$url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $accessToken" \
  -d "$payload")

# Check for success
if echo "$response" | grep -q '"type":"SUCCESS"'; then
  echo "Part added to job successfully:"
  echo "$response"
else
  echo "Failed to add part to job:"
  echo "$response"
fi
