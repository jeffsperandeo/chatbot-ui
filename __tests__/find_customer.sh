#!/bin/bash

shopId=238
accessToken="1c39b602-682c-4100-a7eb-029863bdd191"
page=0
pageSize=100

response=$(curl -s --location "https://sandbox.tekmetric.com/api/v1/customers?shop=$shopId&search=Jeff&page=$page&size=$pageSize" \
--header "Authorization: Bearer $accessToken")

customer=$(echo "$response" | jq '.content[] | select(.lastName == "Sperandeo" and .firstName == "Jeff")')

if [ -n "$customer" ]; then
    echo "Customer found:"
    echo "$customer"
else
    echo "Customer not found"
fi
