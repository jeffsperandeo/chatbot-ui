#!/bin/bash

shopId=238
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"

response=$(curl -s --location "https://sandbox.tekmetric.com/api/v1/jobs?shop=$shopId&page=0&size=100" \
--header "Authorization: Bearer $accessToken")

jobs=$(echo "$response" | jq '.content[]')

if [ -n "$jobs" ]; then
    echo "Jobs found:"
    echo "$jobs"
else
    echo "No jobs found"
fi
