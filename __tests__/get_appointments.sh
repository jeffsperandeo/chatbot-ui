#!/bin/bash

shopId=238
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"

response=$(curl -s --location "https://sandbox.tekmetric.com/api/v1/appointments?shop=$shopId&page=0&size=100" \
--header "Authorization: Bearer $accessToken")

appointments=$(echo "$response" | jq '.content[]')

if [ -n "$appointments" ]; then
    echo "Appointments found:"
    echo "$appointments"
else
    echo "No appointments found"
fi
