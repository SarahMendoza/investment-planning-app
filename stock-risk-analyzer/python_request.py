import requests

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM4OTY0NDcsImlhdCI6MTc0Mzg5Mjg0Nywic3ViIjoidXNlcl9pZCJ9.CMmJZHb1qqTZxN5yYOiAG9IkYG9rs92Q4J40vNh2PA8'
BASE_URL = 'http://localhost:5000/api/v1'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# Analyze single stock
response = requests.get(
    f'{BASE_URL}/analyze/AAPL',
    headers=headers
)
print(response.json())

# Batch analysis
response = requests.post(
    f'{BASE_URL}/analyze/batch',
    headers=headers,
    json={'tickers': ['AAPL', 'GOOGL', 'MSFT']}
)
print(response.json())