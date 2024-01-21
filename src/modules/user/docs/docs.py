from core.docs import docs


userDetailsResponses = {
    200: {
        "content": {
             "application/json": {
                 "example": {
                     **docs.baseResponseExample,
                      "message": "account successfully retrieved",
                    "data": {
                        "id": 1,
                        "identifier": "4tu333wqypYRydX",
                        "firstName": "John",
                        "lastName": "Doe",
                        "email": "johndoe@example.com"
                    }
                 }
             }
        }
    },
    401: docs.unauthorizedResponse
}