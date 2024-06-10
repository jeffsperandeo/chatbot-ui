#!/bin/bash

# Variables
customerId="$1"
status="$2"
note="$3"
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"

# Fetch repair orders for the customer
response=$(curl -s --location "https://sandbox.tekmetric.com/api/v1/repair-orders?customer=${customerId}" \
  --header "Authorization: Bearer $accessToken")

# Extract the latest job ID (assuming we want to update the latest job)
jobId=$(echo "$response" | jq -r '.content[0].jobs[0].id')

# API Endpoint for updating job status
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
update_response=$(curl -s -X PATCH "$url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $accessToken" \
  -d "$payload")

# Check for success
if echo "$update_response" | grep -q '"type":"SUCCESS"'; then
  echo "Job status updated successfully:"
  echo "$update_response"
else
  echo "Failed to update job status:"
  echo "$update_response"
fi
