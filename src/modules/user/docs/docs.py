from core.docs import docs


userDetailsResponses = {
    200: {
        "content": {
             "application/json": {
                 "example": {
                     **docs.baseResponseExample,
                      "message": "account successfully retrieved",
                    "data": {
                        "firstName": "john",
                    }
                 }
             }
        }
    },
    401: docs.unauthorizedResponse
}