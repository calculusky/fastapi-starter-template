from core.docs import docs




signupResponses = {
    200: {
        "content": {
             "application/json": {
                 "example": {
                     **docs.baseResponseExample,
                      "message": "signup successful",
                    "data": {
                         "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3WnA5dlBLZzNOZ1pwZiIsImV4cCI6MTcwNDcwMDQ2Nn0.gX_0hMuZVAPRMkARU7U8R1TnM82ChHegDECdFA5qoLE",
                         "tokenType": "bearer"
                    }
                 }
             }
        }
    },
    422: docs.validationResponse
}


loginResponses = {
    200: {
        "content": {
             "application/json": {
                 "example": {
                     **docs.baseResponseExample,
                      "message": "login successful",
                    "data": {
                         "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3WnA5dlBLZzNOZ1pwZiIsImV4cCI6MTcwNDcwMDQ2Nn0.gX_0hMuZVAPRMkARU7U8R1TnM82ChHegDECdFA5qoLE",
                         "tokenType": "bearer"
                    }
                 }
             }
        }
    },
    422: docs.validationResponse
}

verifyEmailResponses = {
    200: {
        "content": {
             "application/json": {
                 "example": {
                     **docs.baseResponseExample,
                      "message": "Email verification successfully sent"
                 }
             }
        }
    },
    422: docs.validationResponse
}