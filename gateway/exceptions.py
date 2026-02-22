# gateway/exceptions.py
from fastapi import HTTPException, status

class ServiceNotFoundException(HTTPException):
    def __init__(self, service: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": 404,
                "error": "ServiceNotFound",
                "message": f"Service '{service}' is not registered in the API Gateway"
            }
        )

class DownstreamServiceUnavailableException(HTTPException):
    def __init__(self, service: str, url: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status_code": 503,
                "error": "ServiceUnavailable",
                "message": f"Unable to reach {service} service at {url}"
            }
        )

class DownstreamTimeoutException(HTTPException):
    def __init__(self, service: str):
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={
                "status_code": 504,
                "error": "GatewayTimeout",
                "message": f"Request to {service} service timed out"
            }
        )

class InvalidPayloadException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status_code": 400,
                "error": "InvalidPayload",
                "message": "Invalid or empty JSON payload"
            }
        )

class DownstreamErrorException(HTTPException):
    def __init__(self, service: str, path: str, error: dict | str, status_code: int):
        super().__init__(
            status_code=status_code,
            detail={
                "service": service,
                "path": path,
                "error": error
            }
        )