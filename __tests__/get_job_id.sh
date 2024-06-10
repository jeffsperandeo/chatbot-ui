#!/bin/bash

shopId=238
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"
repairOrderId="$1"

response=$(curl -s --location "https://sandbox.tekmetric.com/api/v1/repair-orders/$repairOrderId" \
--header "Authorization: Bearer $accessToken")

jobs=$(echo "$response" | jq '.jobs[]')

if [ -n "$jobs" ]; then
    echo "Jobs found:"
    echo "$jobs"
else
    echo "No jobs found"
fi
