from fastapi.responses import JSONResponse

SECURITY_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "GET, POST",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "no-referrer",
}

class JsonifyAndAddHeaders:
    @staticmethod
    def jsonify_and_add_headers(data: dict) -> JSONResponse:

        if not isinstance(data, dict):
            raise ValueError("Response data must be a dictionary")
        
        try:
            response = JSONResponse(content=data)
            response.headers.update(SECURITY_HEADERS)
            return response
        except Exception as e:
            raise ValueError(f"Failed to create secure JSONResponse: {e}")

