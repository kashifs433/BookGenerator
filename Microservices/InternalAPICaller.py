import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Microservices")))
import requests
from ConfigReader import ConfigReader

default_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

class InternalAPICaller:
    @staticmethod
    def make_request(method, service_name, endpoint_path="", headers=None, payload=None, params=None):
        if not method or not service_name:
            raise ValueError("Both 'method' and 'service_name' are required.")

        service_config = ConfigReader.get_value("APIEnginesConfig", "APIEngines", service_name)

        if not service_config:
            raise ValueError(f"Service '{service_name}' not found in APIEnginesConfig.")

        base_url = f"http://127.0.0.1:{service_config.get('PortNumber')}"
        api_url = f"{base_url}/{endpoint_path.lstrip('/')}" if endpoint_path else base_url

        request_headers = default_headers.copy()
        if headers:
            request_headers.update({k: v for k, v in headers.items() if k not in default_headers})

        method = method.upper()

        try:
            response = None
            if method == "GET":
                response = requests.get(api_url, headers=request_headers, params=params)
            elif method == "POST":
                response = requests.post(api_url, headers=request_headers, json=payload)
            else:
                raise ValueError("Unsupported HTTP method. Only GET and POST are allowed.")

            return response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text

        except requests.exceptions.RequestException as e:\
            return None


