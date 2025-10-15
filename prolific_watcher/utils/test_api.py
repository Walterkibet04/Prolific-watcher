from cookie_manager import get_valid_cookies
import requests

# Get valid cookies (refreshes if expired)
cookies = get_valid_cookies()

# Set headers for API request
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Cookie": cookies
}

# Make API call to Prolific
response = requests.get("https://internal-api.prolific.com/api/v1/participant/studies/", headers=headers)

# Print results
print("Status code:", response.status_code)
print("Response JSON:", response.json())
