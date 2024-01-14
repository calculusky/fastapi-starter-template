

baseResponseExample = {
    "success": True
}

unauthorizedResponse = {
     "description": "Unauthorized Error",
            "content": {
              "application/json": {
                "example": {
                     "success": False,
                    "message": "Your session is unauthorized",
                },
                "schema": {
                    "properties": {
                        "success": {
                          "type": "boolean",
                          "default": False
                        },
                        "message": {
                          "type":  "string",
                        },
                      },
                    "required": ["success", "message"]
             }
        }
    }
}



validationResponse = {
            "description": "Validation Error",
            "content": {
              "application/json": {
                # "example": {
                #      "success": False,
                #     "message": "Failed Validation",
                #     "details": []
                # },
                "schema": {
                    "properties": {
                        "success": {
                          "type": "boolean",
                          "default": False
                        },
                        "message": {
                          "type":  "string",
                          "default": "Failed Validation"
                        },
                        "errors": {
                            "items": {
                                 "properties": {
                                    "loc": {
                                        "items": {
                                        "anyOf": [
                                            {
                                            "type": "string"
                                            },
                                            {
                                            "type": "integer"
                                            }
                                        ]
                                        },
                                        "type": "array",
                                        "title": "Location"
                                    },
                                    "msg": {
                                        "type": "string",
                                        "title": "Message"
                                    },
                                    "type": {
                                        "type": "string",
                                        "title": "Error Type"
                                    }
                                    },
                                    "type": "object",
                                    "required": ["loc", "msg", "type"],
                                    "title": "ValidationError"
                                },
                            "type": "array",
                            "title": "Detail"
                          }
                        },
                        "required": ["success", "message", "errors"],
                        "type": "object",
                        "title": "HTTPValidationError"
                }
            }
        }
}