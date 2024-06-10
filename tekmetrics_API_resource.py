import os

"""
Ensure you refer to the .env for specific variables customized for this project.

# Tekmetric API Documentation

## GENERAL

### Overview
The Tekmetric API allows shop owners to grant read-only access to their Customer, Vehicle, and Repair Order data to 3rd party applications through a RESTful web service. Our API uses resource-oriented URLs, accepts query strings, returns JSON responses, and uses standard HTTP response codes, authentication, and verbs.

### Authentication
The Tekmetric API uses access tokens to authenticate requests. You can obtain an access token and authenticate requests by following the steps below:
1. Complete the API Application form linked here. Once your application is reviewed, you will be contacted with next steps.
2. Exchange the provided Client ID and Client Secret for an access token using the Token Endpoint.
3. Provide the generated access token as the bearer token value in each request to the API. The token will continue to be valid until it is revoked. If access to additional resources is requested or if access to a resource is removed, the same access token can still be used after authorization to the resource is granted or removed.

Example:
```
-H "Authorization: Bearer 7de937e1-8574-4459-a0cc-bb4505e7803f"
```

### Versioning
The initial release of Tekmetric's API will be versioned as v1. All endpoints will include the API version as part of its URL path, for example:
```
https://sandbox.tekmetric.com/api/v1/customers
```
Future releases that include breaking changes will use a different version in its URL path.

### Environments
Tekmetric provides both a Test and Production environment for its public API. We encourage users to use the Test environment to experiment with and develop against.

| Environment | Hostname                        |
|-------------|---------------------------------|
| Sandbox     | https://sandbox.tekmetric.com   |
| Production  | https://shop.tekmetric.com      |

### Error Codes
Tekmetric uses standard HTTP response codes to indicate the success or failure of an API request.

| HTTP Status Code | Description                                                |
|------------------|------------------------------------------------------------|
| 200              | Everything worked as expected                              |
| 400              | Bad request. Request has invalid parameters.               |
| 401              | Unauthorized. Invalid client credentials or access token provided. |
| 403              | Forbidden. Provided access token does not have sufficient privileges to requested resource. |
| 404              | Requested resource not found.                              |
| 429              | Too many requests. Rate limit exceeded.                    |
| 5xx              | Error on Tekmetric's end.                                  |

Error Types:
- **invalid_token**: Invalid access token provided to API.
- **insufficient_scope**: Provided access token does not have sufficient privileges to requested resource.
- **invalid_client**: Invalid client credentials or grant type provided to API.

Example Error Response:
```json
{
  "error": "insufficient_scope",
  "error_description": "Insufficient scope for this resource",
  "scope": "791"
}
```

### Rate Limiting
To ensure quick responses to API calls, throttling/overload protection is included in the API. Exceeding the quota will return an HTTP status code 429 with an empty body. Default integrations are limited to 600 API calls per minute, while Sandbox accounts are limited to 300 API calls per minute.

Handling 429 Errors:
- Make a request to the API.
- If the request fails, wait 2 + random_number_milliseconds seconds and retry the request.
- If the request fails, wait 4 + random_number_milliseconds seconds and retry the request.
- Continue with exponential backoff up to a maximum backoff time.
- Maximum backoff is typically 60 seconds.

## API

### Access Token
Send your partner credentials to gain an access token to access shop resources.

Request Headers:
- Content-Type: `application/x-www-form-urlencoded;charset=UTF-8`
- Authorization: Provide your credentials using HTTP Basic Auth. `Basic client_id:client_secret`, where client credentials are Base64 encoded

Request Parameters:
- grant_type: `client_credentials`

Example Request:
```bash
curl -X POST 'http://sandbox.tekmetric.com/api/v1/oauth/token' \
-H "Authorization: Basic Njc3OWVmMjBlNzU4MTdiNzk2MDI6Y2xpZW50X3NlY3JldA==" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "grant_type=client_credentials"
```

Example Response:
```json
{
  "access_token": "7de937e1-8574-4459-a0cc-bb4505e7803f",
  "token_type": "bearer",
  "scope": "1 2"
}
```

### Shops
Retrieve a list of shops your token has been granted access to.

Request Headers:
- Authorization: `Bearer access_token`

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/shops' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
[
  {
    "id": 1,
    "name": "Demo Shop 1",
    "nickname": "",
    "phone": "123-4456-7890",
    "email": "demo@tekmetric.com",
    "website": "www.demoshop1.com",
    "address": {
      "id": 79130,
      "address1": "5704 Southwest Freeway",
      "address2": "",
      "city": "Houston",
      "state": "TX",
      "zip": "77057",
      "streetAddress": "5704 Southwest Freeway",
      "fullAddress": "5704 Southwest Freeway, Houston, TX 77057"
    },
    "roCustomLabelEnabled": false
  }
]
```

### Shop
Retrieve details of a specific shop by ID.

Request Headers:
- Authorization: `Bearer access_token`

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/shops/1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "id": 1,
  "name": "Demo Shop 1",
  "nickname": "",
  "phone": "123-4456-7890",
  "email": "demo@tekmetric.com",
  "website": "www.demoshop1.com",
  "address": {
    "id": 79130,
    "address1": "5704 Southwest Freeway",
    "address2": "",
    "city": "Houston",
    "state": "TX",
    "zip": "77057",
    "streetAddress": "5704 Southwest Freeway",
    "fullAddress": "5704 Southwest Freeway, Houston, TX 77057"
  },
  "roCustomLabelEnabled": false
}
```

### Customers
Retrieve a list of customers filtered by the provided search parameters.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- shop: Integer (Search for customers by shop)
- search: String (Search for customers by their name, email, or phone number)
- okForMarketing: Boolean (Filter by customers who are ok for marketing)
- updatedDateStart: Date (Filter by customer updated date)
- updatedDateEnd: Date (Filter by customer updated date)
- deletedDateStart: Date (Filter by customer deleted date)
- deletedDateEnd: Date (Filter by customer deleted date)
- sort: String (Specify the property to sort on, multiple sort parameters permitted)
- customerTypeId: Integer (Search by Customer type)
- sortDirection: String (Specify the sort direction, ASC or DESC)
- size: Integer (Specify the number of results)
- page: Integer (Specify the page of results)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/customers?shop=1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "content": [
    {
      "id": 35680,
      "firstName": "Vince",
      "lastName": "Zulauf",
      "email": "vincezulauf@mail.test",
      "phone": [
        {
          "number": "111-111-1111",
          "type": "Cell",
          "primary": true
        }
      ],
      "customerType": {
        "id": 1,
        "code": "PERSON",
        "name": "Person"
      },
      "address": {
        "address1": "5103 Swift Park",
        "city": "Tyreseview",
        "state": "VT",
        "zip": "48824",
        "fullAddress": "5103 Swift Park, Tyreseview, VT 48824"
      },
      "shopId": 79,
      "okForMarketing": true,
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z"
    }
  ],
  "totalPages": 458,
  "last": false,
  "totalElements": 4571,
  "sort": [
    {
      "direction": "DESC",
      "property": "firstName",
      "ignoreCase": false,
      "nullHandling":

 "NATIVE",
      "ascending": false,
      "descending": true
    }
  ],
  "numberOfElements": 1,
  "first": true,
  "size": 1,
  "number": 0
}
```

### Customer
Retrieve a customer by ID.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (customerId)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/customers/35680' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "id": 35680,
  "firstName": "Vince",
  "lastName": "Zulauf",
  "email": "vincezulauf@mail.test",
  "phone": [
    {
      "number": "111-111-1111",
      "type": "Cell",
      "primary": true
    }
  ],
  "customerType": {
    "id": 1,
    "code": "PERSON",
    "name": "Person"
  },
  "address": {
    "address1": "5103 Swift Park",
    "city": "Tyreseview",
    "state": "VT",
    "zip": "48824",
    "fullAddress": "5103 Swift Park, Tyreseview, VT 48824"
  },
  "shopId": 79,
  "okForMarketing": true,
  "createdDate": "2019-02-27T10:31:59Z",
  "updatedDate": "2019-02-28T10:32:28Z",
  "deletedDate": null
}
```

### Create Customer
Create a new customer.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Attributes:
- shopId: Integer (required, Shop id)
- customerTypeId: Integer (Customer type id: 1 for PERSON (default) 2 for BUSINESS)
- firstName: String (required, First name)
- lastName: String (Last name)
- email: Array<String> (Array of email addresses)
- notes: String (Notes)
- phone: Array<String> (Array of phone numbers)
- address: JSON (Address entity with address1, address2, city, state, zip fields)
- okForMarketing: Boolean (Is customer OK for marketing)

Example Request:
```bash
curl -X POST 'https://sandbox.tekmetric.com/api/v1/customers' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"shopId": 1, "firstName": "John", "lastName": "Smith", "customerTypeId": 1, "email": ["test@tekmetric.com"], "phone": ["1111111122"], "address":{"address1": "1981 Good Luck Rd.", "address2": "Hillway Apartments", "city": "Lanham", "state": "Maryland", "zip": "20744"}, "notes": "notes", "okForMarketing": true }'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Customer created",
  "data": {
    "id": 398340,
    "firstName": "John",
    "lastName": "Smith",
    "email": "test@tekmetric.com",
    "phone": [
      {
        "id": 476665,
        "number": "1111111122",
        "type": "Mobile",
        "primary": true
      }
    ],
    "address": {
      "id": 406619,
      "address1": "1981 Good Luck Rd.",
      "address2": "Hillway Apartments",
      "city": "Lanham",
      "state": "Maryland",
      "zip": "20744",
      "fullAddress": "1981 Good Luck Rd. Hillway Apartments, Lanham, Maryland 20744",
      "streetAddress": "1981 Good Luck Rd. Hillway Apartments"
    },
    "notes": "notes",
    "customerType": {
      "id": 1,
      "code": "PERSON",
      "name": "Person"
    },
    "contactFirstName": null,
    "contactLastName": null,
    "shopId": 1,
    "okForMarketing": true,
    "createdDate": "2021-06-30T17:42:58.193Z",
    "updatedDate": "2021-06-30T17:42:58.193Z",
    "deletedDate": null,
    "birthday": null
  },
  "details": {}
}
```

### Update Customer
Update a customer.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Attributes:
- customerTypeId: Integer (Customer type id: 1 for PERSON (default) 2 for BUSINESS)
- firstName: String (First name)
- lastName: String (Last name)
- notes: String (Notes)
- address: JSON (Address entity with address1, address2, city, state, zip fields)
- okForMarketing: Boolean (Is customer OK for marketing)

Example Request:
```bash
curl -X PATCH 'https://sandbox.tekmetric.com/api/v1/customers/398340' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"customerTypeId": 2 }'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Customer updated",
  "data": {
    "id": 398340,
    "firstName": "John",
    "lastName": "Smith",
    "email": "test@tekmetric.com",
    "phone": [
      {
        "id": 476665,
        "number": "1111111122",
        "type": "Mobile",
        "primary": true
      }
    ],
    "address": {
      "id": 406619,
      "address1": "1981 Good Luck Rd.",
      "address2": "Hillway Apartments",
      "city": "Lanham",
      "state": "Maryland",
      "zip": "20744",
      "fullAddress": "1981 Good Luck Rd. Hillway Apartments, Lanham, Maryland 20744",
      "streetAddress": "1981 Good Luck Rd. Hillway Apartments"
    },
    "notes": "notes",
    "customerType": {
      "id": 2,
      "code": "BUSINESS",
      "name": "Business"
    },
    "contactFirstName": null,
    "contactLastName": null,
    "shopId": 1,
    "okForMarketing": true,
    "createdDate": "2021-06-30T17:42:58.193Z",
    "updatedDate": "2021-06-30T17:42:58.193Z",
    "deletedDate": null,
    "birthday": null
  },
  "details": {}
}
```

### Repair Orders
Retrieve a list of all repair orders filtered by the provided search parameters.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- shop: Integer (Search for repair orders by shop)
- start: Date (Specify a start date to filter by Repair Orders created after the entered value)
- end: Date (Specify an end date to filter by Repair Orders created before the entered value)
- postedDateStart: Date (Filter by repair order posted date)
- postedDateEnd: Date (Filter by repair order posted date)
- updatedDateStart: Date (Filter by repair order updated date)
- updatedDateEnd: Date (Filter by repair order updated date)
- deletedDateStart: Date (Filter by repair order deleted date)
- deletedDateEnd: Date (Filter by repair order deleted date)
- repairOrderNumber: Integer (Specify a specific RO# you want returned)
- repairOrderStatusId: Array<Integer> (Specify a status if you want to filter results to a specific status)
- customerId: Integer (Specify this value to get repairs for a specific customer)
- vehicleId: Integer (Specify this value to get repairs for a specific vehicle)
- search: String (Search for repair orders by RO#, customer name, and vehicle info)
- sort: String (Specify the property to sort on)
- sortDirection: String (Determine the direction to sort your results)
- size: Integer (Specify the number of results)
- page: Integer (Specify the page of results)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/repair-orders?shop=1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "content": [
    {
      "id": 869586,
      "repairOrderNumber": 43,
      "shopId": 1,
      "repairOrderStatus": {
        "id": 2,
        "code": "WORKINPROGRESS",
        "name": "Work In Progress"
      },
      "repairOrderLabel": {
        "id": 12,
        "code": "WORKNOTSTRTD",
        "name": "Work Not Started",
        "status": {
          "id

": 2,
          "code": "WORKINPROGRESS",
          "name": "Work In Progress"
        }
      },
      "repairOrderCustomLabel": {
        "name": "Wash Bay"
      },
      "color": "#1786E8",
      "appointmentStartTime": "2019-02-28T10:31:59Z",
      "customerId": 361186,
      "serviceWriterId": 616,
      "vehicleId": 516457,
      "milesIn": null,
      "milesOut": null,
      "completedDate": "2019-02-28T10:31:59Z",
      "postedDate": "2019-02-28T10:32:28Z",
      "laborSales": 13000,
      "partsSales": 25997,
      "subletSales": 20000,
      "discountTotal": 11650,
      "feeTotal": 8800,
      "taxes": 1960,
      "amountPaid": 0,
      "totalSales": 58107,
      "jobs": [
        {
          "id": 1084138,
          "repairOrderId": 869586,
          "vehicleId": 516457,
          "customerId": 361186,
          "name": "Diagnostic Inspection",
          "authorized": true,
          "authorizedDate": "2019-02-25T16:12:17",
          "selected": true,
          "technicianId": 100,
          "note": "Code 2343 - will need airbag replacement",
          "partsTotal": 25997,
          "laborTotal": 13000,
          "discountTotal": 1650,
          "feeTotal": 4900,
          "subtotal": 42247,
          "createdDate": "2019-02-27T10:31:59Z",
          "updatedDate": "2019-02-28T10:32:28Z",
          "labor": [
            {
              "id": 2563821,
              "name": "Diagnostic Inspection",
              "rate": 13000,
              "hours": 1,
              "complete": false
            }
          ],
          "parts": [
            {
              "id": 2735929,
              "quantity": 1,
              "brand": "AutoCraft Gold",
              "name": "Battery",
              "partNumber": "#35-2",
              "description": "Group size 35, 640 CCA",
              "cost": 15999,
              "retail": 23997,
              "model": null,
              "width": null,
              "ratio": null,
              "diameter": null,
              "constructionType": null,
              "loadIndex": null,
              "speedRating": null,
              "partType": {
                "id": 1,
                "code": "PART",
                "name": "Part"
              }
            },
            {
              "id": 2735928,
              "quantity": 1,
              "brand": "Cooper",
              "name": null,
              "partNumber": null,
              "description": null,
              "cost": 1000,
              "retail": 2000,
              "model": "Tire",
              "width": "105",
              "ratio": 45,
              "diameter": 17,
              "constructionType": "",
              "loadIndex": "",
              "speedRating": "",
              "partType": {
                "id": 2,
                "code": "TIRE",
                "name": "Tire"
              },
              "dotNumbers": [
                "12345678",
                "ASDF5678"
              ]
            }
          ],
          "fees": [
            {
              "id": 685613,
              "name": "Percentage Job Fee",
              "total": 3900
            },
            {
              "id": 685612,
              "name": "Fixed Job Fee",
              "total": 1000
            }
          ],
          "discounts": [
            {
              "id": 125750,
              "name": "Percentage Job Discount",
              "total": 650
            },
            {
              "id": 125748,
              "name": "Fixed Job Discount",
              "total": 1000
            }
          ],
          "laborHours": 0.2,
          "loggedHours": 0.67
        }
      ],
      "sublets": [
        {
          "id": 48802,
          "name": "Custom Sublet",
          "vendor": {
            "id": 2257,
            "name": "NAPA Auto Parts",
            "nickname": "One Broadway CAMBRIDGE, MA 02142-1187",
            "website": null,
            "phone": null
          },
          "authorized": null,
          "selected": true,
          "note": null,
          "items": [
            {
              "id": 48523,
              "name": "Sublet Line Item",
              "cost": 10000,
              "price": 20000,
              "complete": false
            }
          ],
          "price": 20000,
          "cost": 10000
        }
      ],
      "fees": [
        {
          "id": 685614,
          "name": "Shop Supplies",
          "total": 3900
        }
      ],
      "discounts": [
        {
          "id": 125749,
          "name": "RO Discount",
          "total": 10000
        }
      ],
      "customerConcerns": [
        {
          "id": 8241,
          "concern": "NOISE WHEN TURNING LEFT ",
          "techComment": null
        },
        {
          "id": 8242,
          "concern": "CHECK TPMS SENSOR",
          "techComment": null
        }
      ],
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "deletedDate": null
    }
  ],
  "pageable": {
    "sort": {
      "unsorted": false,
      "sorted": true,
      "empty": false
    },
    "offset": 0,
    "pageSize": 10,
    "pageNumber": 0,
    "paged": true,
    "unpaged": false
  },
  "totalPages": 1,
  "totalElements": 1,
  "last": true,
  "size": 10,
  "number": 0,
  "first": true,
  "sort": {
    "unsorted": false,
    "sorted": true,
    "empty": false
  },
  "numberOfElements": 1,
  "empty": false
}
```

### Repair Order
Retrieve a Repair Order by ID.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (repairOrderId)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/repair-orders/869586' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "id": 869586,
  "repairOrderNumber": 43,
  "shopId": 1,
  "repairOrderStatus": {
    "id": 2,
    "code": "WORKINPROGRESS",
    "name": "Work In Progress"
  },
  "repairOrderLabel": {
    "id": 12,
    "code": "WORKNOTSTRTD",
    "name": "Work Not Started",
    "status": {
      "id": 2,
      "code": "WORKINPROGRESS",
      "name": "Work In Progress"
    }
  },
  "repairOrderCustomLabel": {
    "name": "Wash Bay"
  },
  "color": "#1786E8",
  "appointmentStartTime": "2019-02-28T10:31:59Z",
  "customerId": 361186,
  "serviceWriterId": 616,
  "vehicleId": 516457,
  "milesIn": null,
  "milesOut": null,
  "completedDate": "2019-02-28T10:31:59Z",
  "postedDate": "2019-02-28T10:32:28Z",
  "laborSales": 13000,
  "partsSales": 25997,
  "subletSales": 20000,
  "discountTotal": 11650,
  "feeTotal": 8800,
  "taxes": 1960,
  "amountPaid": 0,
  "totalSales": 58107,
  "jobs": [
    {
      "id": 1084138,
      "repairOrderId": 869586,
      "vehicleId": 516457,
      "customerId": 361186,
      "name": "Diagnostic Inspection",
      "authorized": true,
      "authorizedDate": "2019-02-25T16:12:17",
      "selected": true,
      "technicianId": 100,
      "note": "Code 2343 - will need airbag replacement",
      "partsTotal": 25997,
      "laborTotal": 13000,
      "discountTotal": 1650,
      "feeTotal": 4900,
      "subtotal":

 42247,
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "labor": [
        {
          "id": 2563821,
          "name": "Diagnostic Inspection",
          "rate": 13000,
          "hours": 1,
          "complete": false
        }
      ],
      "parts": [
        {
          "id": 2735929,
          "quantity": 1,
          "brand": "AutoCraft Gold",
          "name": "Battery",
          "partNumber": "#35-2",
          "description": "Group size 35, 640 CCA",
          "cost": 15999,
          "retail": 23997,
          "model": null,
          "width": null,
          "ratio": null,
          "diameter": null,
          "constructionType": null,
          "loadIndex": null,
          "speedRating": null,
          "partType": {
            "id": 1,
            "code": "PART",
            "name": "Part"
          }
        },
        {
          "id": 2735928,
          "quantity": 1,
          "brand": "Cooper",
          "name": null,
          "partNumber": null,
          "description": null,
          "cost": 1000,
          "retail": 2000,
          "model": "Tire",
          "width": "105",
          "ratio": 45,
          "diameter": 17,
          "constructionType": "",
          "loadIndex": "",
          "speedRating": "",
          "partType": {
            "id": 2,
            "code": "TIRE",
            "name": "Tire"
          },
          "dotNumbers": [
            "12345678",
            "ASDF5678"
          ]
        }
      ],
      "fees": [
        {
          "id": 685613,
          "name": "Percentage Job Fee",
          "total": 3900
        },
        {
          "id": 685612,
          "name": "Fixed Job Fee",
          "total": 1000
        }
      ],
      "discounts": [
        {
          "id": 125750,
          "name": "Percentage Job Discount",
          "total": 650
        },
        {
          "id": 125748,
          "name": "Fixed Job Discount",
          "total": 1000
        }
      ],
      "laborHours": 0.2,
      "loggedHours": 0.67
    }
  ],
  "sublets": [
    {
      "id": 48802,
      "name": "Custom Sublet",
      "vendor": {
        "id": 2257,
        "name": "NAPA Auto Parts",
        "nickname": "One Broadway CAMBRIDGE, MA 02142-1187",
        "website": null,
        "phone": null
      },
      "authorized": null,
      "selected": true,
      "note": null,
      "items": [
        {
          "id": 48523,
          "name": "Sublet Line Item",
          "cost": 10000,
          "price": 20000,
          "complete": false
        }
      ],
      "price": 20000,
      "cost": 10000
    }
  ],
  "fees": [
    {
      "id": 685614,
      "name": "Shop Supplies",
      "total": 3900
    }
  ],
  "discounts": [
    {
      "id": 125749,
      "name": "RO Discount",
      "total": 10000
    }
  ],
  "customerConcerns": [
    {
      "id": 8241,
      "concern": "NOISE WHEN TURNING LEFT ",
      "techComment": null
    },
    {
      "id": 8242,
      "concern": "CHECK TPMS SENSOR",
      "techComment": null
    }
  ],
  "createdDate": "2019-02-27T10:31:59Z",
  "updatedDate": "2019-02-28T10:32:28Z",
  "deletedDate": null
}
```

### Update Repair Order
Update a Repair Order.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Attributes:
- keyTag: String (KeyTag value on Repair Order)
- milesIn: Integer (Mileage in on Repair Order)
- milesOut: Integer (Mileage out on Repair Order)
- technicianId: Integer (Set default Technician on Repair Order by employeeId)
- serviceWriterId: Integer (Set Service Writer on Repair Order by employeeId)
- customerTimeOut: DateTime (Set Promise Time on Repair Order)

Example Request:
```bash
curl -X PATCH 'https://sandbox.tekmetric.com/api/v1/repair-orders/1104636' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"milesIn": 110463}'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Repair Order Saved",
  "data": {}
}
```

### Jobs
Retrieve a list of all jobs filtered by the provided search parameters.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- shop: Integer (Filter by shop ID)
- vehicleId: Integer (Filter by vehicle ID)
- repairOrderId: Integer (Filter by repair order ID)
- customerId: Integer (Filter by customer ID)
- authorized: Boolean (Filter by authorized jobs)
- authorizedDateStart: Date (Filter by job authorization date)
- authorizedDateEnd: Date (Filter by job authorization date)
- updatedDateStart: Date (Filter by job updated date)
- updatedDateEnd: Date (Filter by job updated date)
- repairOrderStatusId: Array<Integer> (Filter results by repair order status)
- sort: String (Specify the property to sort on)
- sortDirection: String (Determine the direction to sort your results)
- size: Integer (Specify the number of results)
- page: Integer (Specify the page of results)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/jobs?shop=1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "content": [
    {
      "id": 1084138,
      "repairOrderId": 869586,
      "vehicleId": 516457,
      "customerId": 361186,
      "name": "Diagnostic Inspection",
      "authorized": true,
      "authorizedDate": "2019-02-25T16:12:17",
      "selected": true,
      "technicianId": 100,
      "note": "Code 2343 - will need airbag replacement",
      "jobCategoryName": "Heating & Air Conditioning",
      "partsTotal": 25997,
      "laborTotal": 13000,
      "discountTotal": 1650,
      "feeTotal": 4900,
      "subtotal": 42247,
      "archived": false,
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "completedDate": "2019-02-28T11:35:28Z",
      "labor": [
        {
          "id": 2563821,
          "name": "Diagnostic Inspection",
          "rate": 13000,
          "hours": 1,
          "complete": false
        }
      ],
      "parts": [
        {
          "id": 2735929,
          "quantity": 1,
          "brand": "AutoCraft Gold",
          "name": "Battery",
          "partNumber": "#35-2",
          "description": "Group size 35, 640 CCA",
          "cost": 15999,
          "retail": 23997,
          "model": null,
          "width": null,
          "ratio": null,
          "diameter": null,
          "constructionType": null,
          "loadIndex": null,
          "speedRating": null,
          "partType": {
            "id": 1,
            "code": "PART",
            "name": "Part"
          }
        },
        {
          "id": 2735928,
          "quantity": 1,
          "brand": "Cooper",
          "name": null,
          "partNumber": null,
          "description": null,
          "cost": 1000,
          "retail": 2000,
          "model": "Tire",
          "width": "105",
          "ratio": 45,
          "diameter": 17,
          "constructionType": "",
          "loadIndex": "",
          "speedRating": "",
          "partType": {
            "id": 2,
            "code": "TIRE",
            "name": "Tire"
          },
          "dotNumbers": [
            "12345678",
            "ASDF5678"
          ]
        }
      ],
      "fees": [
        {
          "id": 685613,
          "name": "

Percentage Job Fee",
          "total": 3900
        },
        {
          "id": 685612,
          "name": "Fixed Job Fee",
          "total": 1000
        }
      ],
      "discounts": [
        {
          "id": 125750,
          "name": "Percentage Job Discount",
          "total": 650
        },
        {
          "id": 125748,
          "name": "Fixed Job Discount",
          "total": 1000
        }
      ],
      "laborHours": 0.2,
      "loggedHours": 0.67
    }
  ],
  "pageable": {
    "sort": {
      "unsorted": false,
      "sorted": true,
      "empty": false
    },
    "offset": 0,
    "pageSize": 10,
    "pageNumber": 0,
    "paged": true,
    "unpaged": false
  },
  "totalPages": 1,
  "totalElements": 1,
  "last": true,
  "size": 10,
  "number": 0,
  "first": true,
  "sort": {
    "unsorted": false,
    "sorted": true,
    "empty": false
  },
  "numberOfElements": 1,
  "empty": false
}
```

### Job
Retrieve a Job by ID.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (job ID)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/jobs/1084138' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "id": 1084138,
  "repairOrderId": 869586,
  "vehicleId": 516457,
  "customerId": 361186,
  "name": "Diagnostic Inspection",
  "authorized": true,
  "authorizedDate": "2019-02-25T16:12:17",
  "selected": true,
  "technicianId": 100,
  "note": "Code 2343 - will need airbag replacement",
  "jobCategoryName": "Heating & Air Conditioning",
  "partsTotal": 25997,
  "laborTotal": 13000,
  "discountTotal": 1650,
  "feeTotal": 4900,
  "subtotal": 42247,
  "archived": false,
  "createdDate": "2019-02-27T10:31:59Z",
  "updatedDate": "2019-02-28T10:32:28Z",
  "completedDate": "2019-02-28T11:35:28Z",
  "labor": [
    {
      "id": 2563821,
      "name": "Diagnostic Inspection",
      "rate": 13000,
      "hours": 1,
      "complete": false
    }
  ],
  "parts": [
    {
      "id": 2735929,
      "quantity": 1,
      "brand": "AutoCraft Gold",
      "name": "Battery",
      "partNumber": "#35-2",
      "description": "Group size 35, 640 CCA",
      "cost": 15999,
      "retail": 23997,
      "model": null,
      "width": null,
      "ratio": null,
      "diameter": null,
      "constructionType": null,
      "loadIndex": null,
      "speedRating": null,
      "partType": {
        "id": 1,
        "code": "PART",
        "name": "Part"
      }
    },
    {
      "id": 2735928,
      "quantity": 1,
      "brand": "Cooper",
      "name": null,
      "partNumber": null,
      "description": null,
      "cost": 1000,
      "retail": 2000,
      "model": "Tire",
      "width": "105",
      "ratio": 45,
      "diameter": 17,
      "constructionType": "",
      "loadIndex": "",
      "speedRating": "",
      "partType": {
        "id": 2,
        "code": "TIRE",
        "name": "Tire"
      },
      "dotNumbers": [
        "12345678",
        "ASDF5678"
      ]
    }
  ],
  "fees": [
    {
      "id": 685613,
      "name": "Percentage Job Fee",
      "total": 3900
    },
    {
      "id": 685612,
      "name": "Fixed Job Fee",
      "total": 1000
    }
  ],
  "discounts": [
    {
      "id": 125750,
      "name": "Percentage Job Discount",
      "total": 650
    },
    {
      "id": 125748,
      "name": "Fixed Job Discount",
      "total": 1000
    }
  ],
  "laborHours": 0.2,
  "loggedHours": 0.67
}
```

### Update Job
Update a Job.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Attributes:
- completed: Boolean (Indicate if a job has been completed)
- name: String (Name of the job)
- note: String (Notes relevant to the job)
- technicianId: Integer (Set technician on job by employeeId)
- loggedHours: Decimal (Hours logged on job by employee in hours)

Example Request:
```bash
curl -X PATCH 'https://sandbox.tekmetric.com/api/v1/jobs/1197955' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"name": "Brake Job"}'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Job Saved",
  "data": {
    "id": 1084138,
    "repairOrderId": 869586,
    "vehicleId": 516457,
    "customerId": 361186,
    "name": "Diagnostic Inspection",
    "authorized": true,
    "authorizedDate": "2019-02-25T16:12:17",
    "selected": true,
    "technicianId": 100,
    "note": "Code 2343 - will need airbag replacement",
    "partsTotal": 25997,
    "laborTotal": 13000,
    "discountTotal": 1650,
    "feeTotal": 4900,
    "subtotal": 42247,
    "createdDate": "2019-02-27T10:31:59Z",
    "updatedDate": "2019-02-28T10:32:28Z",
    "labor": [],
    "parts": [],
    "fees": [],
    "discounts": []
  }
}
```

### Canned Jobs
Retrieve a list of all canned jobs filtered by the provided search parameters.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- shop: Integer (Filter by shop ID)
- search: String (Filter by job name)
- categories: Array<String> (Filter results by job category codes)
- rates: Array<String> (Filter results by labor rates)
- sort: String (Specify the property to sort on)
- sortDirection: String (Determine the direction to sort your results)
- size: Integer (Specify the number of results)
- page: Integer (Specify the page of results)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/canned-jobs?shop=1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "content": [
    {
      "id": 609280,
      "name": "TIRE PATCH",
      "note": null,
      "totalCost": 3577,
      "jobTemplateType": null,
      "jobCategoryCode": null,
      "laborRates": [
        7331,
        12715
      ],
      "labor": [
        {
          "id": 1482155,
          "name": "PATCH",
          "rate": 7331,
          "hours": 0.3,
          "complete": false
        },
        {
          "id": 1482157,
          "name": "MOUNT AND BALANCE",
          "rate": 12715,
          "hours": 0,
          "complete": false
        }
      ],
      "parts": [
        {
          "id": 1484852,
          "quantity": 1,
          "brand": null,
          "name": "PATCH PLUG KIT",
          "partNumber": "TIRE PPL 710",
          "description": null,
          "cost": 100,
          "retail": 1300,
          "model": null,
          "width": null,
          "ratio": null,
          "diameter": null,
          "constructionType": null,
          "loadIndex": null,
          "speedRating": null,
          "partType": {
            "id": 1,
            "code": "PART",
            "name": "

Part"
          }
        }
      ],
      "discounts": [
        {
          "id": 125748,
          "name": "Fixed Job Discount",
          "total": 1000
        }
      ],
      "fees": [
        {
          "id": 685612,
          "name": "Fixed Job Fee",
          "total": 1000
        }
      ],
      "packagePrice": false
    }
  ],
  "pageable": {
    "sort": {
      "sorted": false,
      "unsorted": true,
      "empty": true
    },
    "pageNumber": 0,
    "offset": 0,
    "pageSize": 10,
    "paged": true,
    "unpaged": false
  },
  "totalElements": 1,
  "totalPages": 1,
  "last": true,
  "first": true,
  "size": 10,
  "number": 0,
  "sort": {
    "sorted": false,
    "unsorted": true,
    "empty": true
  },
  "numberOfElements": 1,
  "empty": false
}
```

### Add Canned Jobs To Repair Order
Add given canned jobs to a repair order.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (repairOrderId)

Example Request:
```bash
curl -X POST 'https://sandbox.tekmetric.com/api/v1/repair-orders/1/canned-jobs' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-H "Content-Type: application/json" \
--data-raw '[609801]'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Job(s) saved",
  "data": {
    "jobs": [
      1089313
    ]
  }
}
```

### Vehicles
Retrieve a list of all vehicles filtered by the provided search parameters.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- shop: Integer (Search for vehicles by shop)
- customerId: Integer (Specify a customerId to receive vehicles for specific customer)
- search: String (Search for vehicles by year, make, or model)
- updatedDateStart: Date (Filter by vehicle updated date)
- updatedDateEnd: Date (Filter by vehicle updated date)
- deletedDateStart: Date (Filter by vehicle deleted date)
- deletedDateEnd: Date (Filter by vehicle deleted date)
- sort: String (Specify the property to sort on)
- sortDirection: String (Determine the direction to sort your results)
- size: Integer (Specify the number of results)
- page: Integer (Specify the page of results)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/vehicles?shop=1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "content": [
    {
      "id": 359093,
      "customerId": 258819,
      "year": 2006,
      "make": "Ford",
      "model": "Escape",
      "subModel": "XLT",
      "engine": "3.0L V6 (1) GAS FI",
      "color": "blue",
      "licensePlate": "tag-no",
      "state": "TX",
      "vin": "",
      "driveType": "AWD",
      "transmission": "Automatic",
      "bodyType": "Wagon",
      "notes": null,
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "deletedDate": "2019-03-28T10:32:28Z"
    },
    {
      "id": 375446,
      "customerId": 258819,
      "year": 2008,
      "make": "Lexus",
      "model": "GX470",
      "subModel": "Base",
      "engine": "4.7L V8 (2UZ-FE) GAS FI",
      "licensePlate": "tag-123",
      "state": "VA",
      "driveType": "AWD",
      "transmission": "Automatic CVT",
      "bodyType": "Sport Utility",
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "deletedDate": "2019-03-28T10:32:28Z"
    },
    {
      "id": 517955,
      "customerId": 258819,
      "year": 2015,
      "make": "Ford",
      "model": "Fusion",
      "subModel": "SE",
      "engine": "2.5L L4 (7) GAS FI",
      "licensePlate": "tag",
      "state": "TX",
      "vin": "sample-vin",
      "driveType": "FWD",
      "transmission": "Manual",
      "bodyType": "Sedan",
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "deletedDate": "2019-03-28T10:32:28Z"
    }
  ],
  "pageable": {
    "sort": {
      "unsorted": false,
      "sorted": true,
      "empty": false
    },
    "offset": 0,
    "pageSize": 10,
    "pageNumber": 0,
    "paged": true,
    "unpaged": false
  },
  "totalPages": 1,
  "totalElements": 3,
  "last": true,
  "size": 10,
  "number": 0,
  "first": true,
  "sort": {
    "unsorted": false,
    "sorted": true,
    "empty": false
  },
  "numberOfElements": 3,
  "empty": false
}
```

### Vehicle
Retrieve a Vehicle by ID.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (vehicleId)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/vehicles/1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "id": 1,
  "customerId": 258819,
  "year": 2006,
  "make": "Ford",
  "model": "Escape",
  "subModel": "XLT",
  "engine": "3.0L V6 (1) GAS FI",
  "color": "blue",
  "licensePlate": "tag-no",
  "state": "TX",
  "vin": "",
  "driveType": "AWD",
  "transmission": "Automatic",
  "bodyType": "Wagon",
  "createdDate": "2019-02-27T10:31:59Z",
  "updatedDate": "2019-02-28T10:32:28Z",
  "deletedDate": "2019-03-28T10:32:28Z"
}
```

### Create Vehicle
Create a new vehicle.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Attributes:
- customerId: Integer (required, Customer id)
- year: Integer (required, Year of Vehicle)
- make: String (required, Make of Vehicle)
- model: String (required, Model of Vehicle)
- subModel: String (SubModel of Vehicle)
- engine: String (Engine of Vehicle)
- color: String (Color of Vehicle)
- licensePlate: String (License Plate of Vehicle)
- state: String (License Plate State of Vehicle)
- vin: String (VIN of Vehicle)
- notes: String (Notes for Vehicle)
- unitNumber: String (Unit Number for Vehicle)

Example Request:
```bash
curl -X POST 'https://sandbox.tekmetric.com/api/v1/vehicles' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"customerId": 228770, "year": 2020, "make": "Nissan", "model": "Pathfinder", "subModel": "LSX", "vin": "WDBSK74F46F114815", "licensePlate": "06GUAVB", "state": "TX"}'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Vehicle created",
  "data": {
    "id": 548052,
    "customerId": 228770,
    "year": 2020,
    "make": "Nissan",
    "model": "Pathfinder",
    "subModel": "LSX",
    "licensePlate": "06GUAVB",
    "state": "TX",
    "createdDate": "2021-06-30T15:40:15.469Z",
    "

updatedDate": "2021-06-30T15:40:15.469Z"
  }
}
```

### Update Vehicle
Update a vehicle.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Attributes:
- year: Integer (Year of Vehicle)
- make: String (Make of Vehicle)
- model: String (Model of Vehicle)
- subModel: String (SubModel of Vehicle)
- engine: String (Engine of Vehicle)
- color: String (Color of Vehicle)
- licensePlate: String (License Plate of Vehicle)
- state: String (License Plate State of Vehicle)
- vin: String (VIN of Vehicle)
- notes: String (Notes for Vehicle)
- unitNumber: String (Unit Number for Vehicle)

Example Request:
```bash
curl -X PATCH 'https://sandbox.tekmetric.com/api/v1/vehicles/643641' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"year": "2006"}'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Vehicle Saved",
  "data": {
    "id": 1,
    "customerId": 258819,
    "year": 2006,
    "make": "Ford",
    "model": "Escape",
    "subModel": "XLT",
    "engine": "3.0L V6 (1) GAS FI",
    "color": "blue",
    "licensePlate": "tag-no",
    "state": "TX",
    "vin": "",
    "driveType": "AWD",
    "transmission": "Automatic",
    "bodyType": "Wagon",
    "createdDate": "2019-02-27T10:31:59Z",
    "updatedDate": "2019-02-28T10:32:28Z",
    "deletedDate": "2019-03-28T10:32:28Z"
  }
}
```

### Appointments
Retrieve a list of all appointments filtered by the provided search parameters.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- shop: Integer (Search for appointments by shop)
- customerId: Integer (Specify a customerId to search appointments)
- vehicleId: Integer (Specify a vehicleId to search appointments)
- start: Date (Specify a start date to filter appointments)
- end: Date (Specify an end date to filter appointments)
- updatedDateStart: Date (Filter by appointment updated date)
- updatedDateEnd: Date (Filter by appointment updated date)
- includeDeleted: Boolean (Filter out deleted appointments)
- sort: String (Specify the property to sort on)
- sortDirection: String (Determine the direction to sort your results)
- size: Integer (Specify the number of results)
- page: Integer (Specify the page of results)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/appointments?shop=1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "content": [
    {
      "id": 1,
      "shopId": 1,
      "customerId": 1,
      "vehicleId": 2,
      "startTime": "2018-02-04T19:54:38",
      "endTime": "2018-02-04T20:24:38",
      "description": "A/C Smells Funny, Oil leak in driveway, Blinker light is out",
      "arrived": null,
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "deletedDate": null,
      "leadSource": null,
      "rideOption": null,
      "dropoffTime": "2018-02-04T17:00:00",
      "pickupTime": "2018-02-04T21:00:00",
      "appointmentOption": null
    },
    {
      "id": 2,
      "shopId": 1,
      "customerId": 1,
      "vehicleId": 2,
      "startTime": "2018-02-06T17:24:52",
      "endTime": "2018-02-06T17:54:52",
      "description": "A/C smell, noise on bumps",
      "arrived": true,
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "deletedDate": "2019-02-28T10:32:28Z",
      "leadSource": "Drive-By",
      "rideOption": {
        "id": 3,
        "code": "NONE",
        "name": "None"
      },
      "dropoffTime": "2018-02-06T12:00:00",
      "pickupTime": "2018-02-06T19:00:00",
      "appointmentOption": {
        "id": 1,
        "code": "STAY",
        "name": "Stay With Vehicle"
      }
    }
  ],
  "pageable": {
    "sort": {
      "sorted": true,
      "unsorted": false,
      "empty": false
    },
    "offset": 0,
    "pageSize": 10,
    "pageNumber": 0,
    "paged": true,
    "unpaged": false
  },
  "totalElements": 73,
  "totalPages": 8,
  "last": false,
  "size": 2,
  "number": 0,
  "first": true,
  "sort": {
    "sorted": true,
    "unsorted": false,
    "empty": false
  },
  "numberOfElements": 2,
  "empty": false
}
```

### Appointment
Retrieve an Appointment by ID.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (appointmentId)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/appointments/1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "id": 1,
  "shopId": 1,
  "customerId": 1,
  "vehicleId": 2,
  "startTime": "2018-02-04T19:54:38",
  "endTime": "2018-02-04T20:24:38",
  "description": "A/C Smells Funny, Oil leak in driveway, Blinker light is out",
  "arrived": null,
  "createdDate": "2019-02-27T10:31:59Z",
  "updatedDate": "2019-02-28T10:32:28Z",
  "deletedDate": null,
  "leadSource": "Drive-By",
  "rideOption": {
    "id": 1,
    "code": "RIDE ",
    "name": "Ride Required"
  },
  "dropoffTime": "2018-02-15:00:00",
  "pickupTime": "2018-02-16T18:00:00",
  "appointmentOption": {
    "id": 2,
    "code": "DROP",
    "name": "Drop-off Vehicle"
  }
}
```

### Create Appointment
Create a new appointment.

Request Headers:
- Content-Type: `application/json`
- Authorization: `Bearer access_token`

Request Attributes:
- shopId: Integer (required, Shop id)
- customerId: Integer (Customer id, not required unless there is a vehicle)
- vehicleId: Integer (Vehicle id, not required unless there is a customer)
- startTime: DateTime (required, Start time of the appointment)
- endTime: DateTime (required, End time of the appointment)
- title: String (required, Title of the appointment)
- description: String (Description)
- color: String (Color which will be shown with the Appointment)
- dropoffTime: DateTime (Vehicle Drop-off time)
- pickupTime: DateTime (Vehicle Pick-up time)
- rideOption: String (Ride option for the appointments that are DROP)

Example Request:
```bash
curl -X POST 'https://sandbox.tekmetric.com/api/v1/appointments' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"shopId":1, "customerId":229769, "startTime": "2020-05-20T16:15:17Z", "endTime": "2020-05-20T16:45:17Z", "title": "appointment title", "description": "appointment description", "color": "yellow" }'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Appointment Saved",
  "data": 1
}
```

### Update Appointment
Update an appointment.

Request Headers:
- Content-Type: `application/json`
- Authorization: `

Bearer access_token`

Request Attributes:
- shopId: Integer (required, Shop id)
- customerId: Integer (Customer id, not required unless there is a vehicle)
- vehicleId: Integer (Vehicle id, not required unless there is a customer)
- startTime: DateTime (required, Start time of the appointment)
- endTime: DateTime (required, End time of the appointment)
- title: String (required, Title of the appointment)
- description: String (Description)
- color: String (Color which will be shown with the Appointment)
- dropoffTime: DateTime (Vehicle Drop-off time)
- pickupTime: DateTime (Vehicle Pick-up time)
- rideOption: String (Ride option for the appointments that are DROP)

Example Request:
```bash
curl -X PATCH 'https://sandbox.tekmetric.com/api/v1/appointments/10613' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15" \
-d '{"customerId":229769, "startTime": "2020-05-20T16:15:17Z", "endTime": "2020-05-20T16:45:17Z" }'
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Appointment Updated",
  "data": {
    "id": 10613,
    "shopId": 1,
    "customerId": 229769,
    "vehicleId": 318807,
    "startTime": "2020-05-20T16:15:17Z",
    "endTime": "2020-05-20T16:45:17",
    "description": "leaking brake fluid\r\n",
    "title": "Title",
    "color": "#33B679",
    "arrived": true,
    "updatedDate": "2020-05-20T12:08:08Z",
    "deletedDate": null,
    "leadSource": "Yelp",
    "rideOption": {
      "id": 2,
      "code": "LOANDER ",
      "name": "Loaner Required"
    },
    "dropoffTime": "2020-05-20T11:00:00Z",
    "pickupTime": "2020-05-20T19:15:00Z",
    "appointmentOption": {
      "id": 2,
      "code": "DROP",
      "name": "Drop-off Vehicle"
    }
  }
}
```

### Delete Appointment
Delete an appointment by ID.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (appointmentId)

Example Request:
```bash
curl -X DELETE 'https://sandbox.tekmetric.com/api/v1/appointments/1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "type": "SUCCESS",
  "message": "Appointment Deleted",
  "data": 1
}
```

### Employees
Retrieve a list of all employees filtered by the provided search parameters.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- shop: Integer (Search for employees by shop)
- search: String (Search for employees by name)
- updatedDateStart: Date (Filter by employee updated date)
- updatedDateEnd: Date (Filter by employee updated date)
- sort: String (Specify the property to sort on)
- sortDirection: String (Determine the direction to sort your results)
- size: Integer (Specify the number of results)
- page: Integer (Specify the page of results)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/employees?shop=1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "content": [
    {
      "id": 780,
      "email": "malindawintheiser@mail.test",
      "firstName": "Malinda",
      "lastName": "Wintheiser",
      "employeeRole": {
        "id": 2,
        "code": "2",
        "name": "Service Advisor"
      },
      "canPerformWork": true,
      "createdDate": "2019-02-27T10:31:59Z",
      "updatedDate": "2019-02-28T10:32:28Z",
      "certificationNumber": "CT2023-12345"
    }
  ],
  "pageable": {
    "sort": {
      "unsorted": false,
      "sorted": true,
      "empty": false
    },
    "offset": 0,
    "pageSize": 10,
    "pageNumber": 0,
    "paged": true,
    "unpaged": false
  },
  "totalPages": 1,
  "totalElements": 3,
  "last": true,
  "size": 10,
  "number": 0,
  "first": true,
  "sort": {
    "unsorted": false,
    "sorted": true,
    "empty": false
  },
  "numberOfElements": 3,
  "empty": false
}
```

### Employee
Retrieve an Employee by ID.

Request Headers:
- Authorization: `Bearer access_token`

Request Parameters:
- id: Integer (employeeId)

Example Request:
```bash
curl -X GET 'https://sandbox.tekmetric.com/api/v1/employees/1' \
-H "Authorization: Bearer dd824dda-c02c-478a-aa84-cd9fdb217c15"
```

Example Response:
```json
{
  "id": 780,
  "email": "malindawintheiser@mail.test",
  "firstName": "Malinda",
  "lastName": "Wintheiser",
  "employeeRole": {
    "id": 2,
    "code": "2",
    "name": "Service Advisor"
  },
  "canPerformWork": true,
  "createdDate": "2019-02-27T10:31:59Z",
  "updatedDate": "2019-02-28T10:32:28Z",
  "certificationNumber": "CT2023-12345"
}
```

## Changelog
### 2019-2023
Tekmetric has made various updates and improvements to the API, ensuring it remains robust and reliable for shop owners and developers.

---
"""