#!/bin/bash

# Variables
vehicleId="$1"
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"

# API Endpoint
url="https://sandbox.tekmetric.com/api/v1/vehicles/${vehicleId}"

# Make the API request
response=$(curl -s -X GET "$url" \
  -H "Authorization: Bearer $accessToken")

# Check for success
if echo "$response" | grep -q '"id"'; then
  echo "Vehicle details fetched successfully:"
  echo "$response" | jq
else
  echo "Failed to fetch vehicle details:"
  echo "$response"
fi
