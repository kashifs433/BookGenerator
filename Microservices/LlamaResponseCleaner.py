import re
import json

class ResponseCleaner():

    @staticmethod
    def Extract_Clean_Json(response_text):
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                json_data = json.loads(json_str)
                pretty_json = json.dumps(json_data, indent=2)
                return pretty_json
            except json.JSONDecodeError:
                return None
        return None

