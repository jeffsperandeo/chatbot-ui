#!/bin/bash

# Variables
customerId="$1"
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"

# API Endpoint
url="https://sandbox.tekmetric.com/api/v1/repair-orders?customer=${customerId}"

# Make the API request
response=$(curl -s --location "$url" \
  --header "Authorization: Bearer $accessToken")

echo "Repair orders found:"
echo "$response" | jq '.content'
