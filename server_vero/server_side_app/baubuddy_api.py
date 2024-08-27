import requests

class BaubuddyAPI:


    # Login credentials and headers for authorization
    payload = {
        "username": "365",
        "password": "1"
    }
    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }

    def __init__(self):
        # baubuddy APIs

        self.url_login = "https://api.baubuddy.de/index.php/login"
        self.url_vehicles = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
        self.url_labels = "https://api.baubuddy.de/dev/index.php/v1/labels/"
        self.token = self._get_access_token()

    # Function to get the access token
    def _get_access_token(self):
        response = requests.post(self.url_login, json=self.payload, headers=self.headers)
        access_token = response.json().get("oauth", {}).get("access_token")
        return access_token

    # Function to fetch vehicle data from the external API
    def fetch_vehicle_data(self):
        auth_headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(self.url_vehicles, headers=auth_headers)
        return response.json()

    # Function to resolve color codes for labelIds
    def resolve_color_codes(self,label_ids):
        auth_headers = {
            "Authorization": f"Bearer {self.token}"
        }
        color_codes = []
        for label_id in label_ids:
            response = requests.get(f"{self.url_labels}{label_id}", headers=auth_headers)
            color_code = response.json().get("colorCode")
            if color_code:
                color_codes.append(color_code)
        print(color_codes)
        return color_codes

    def token_available(self):
        if(self.token):
            return True