#!/bin/bash

shopId=238
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"
customerId="$1"

response=$(curl -s --location "https://sandbox.tekmetric.com/api/v1/repair-orders?shop=$shopId&customer=$customerId&page=0&size=100" \
--header "Authorization: Bearer $accessToken")

repairOrders=$(echo "$response" | jq '.content[]')

if [ -n "$repairOrders" ]; then
    echo "Repair orders found:"
    echo "$repairOrders"
else
    echo "No repair orders found"
fi
