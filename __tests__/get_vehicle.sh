#!/bin/bash

shopId=238
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"
vin="$1"

response=$(curl -s --location "https://sandbox.tekmetric.com/api/v1/vehicles?shop=$shopId&search=$vin&page=0&size=100" \
--header "Authorization: Bearer $accessToken")

vehicle=$(echo "$response" | jq '.content[] | select(.vin == "'$vin'")')

if [ -n "$vehicle" ]; then
    echo "Vehicle found:"
    echo "$vehicle"
else
    echo "Vehicle not found"
fi
