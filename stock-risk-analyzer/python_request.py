import requests

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM5NDA0NjUsImlhdCI6MTc0MzkzNjg2NSwic3ViIjoidXNlcl9pZCJ9.1nPu1rWrV2UzatwRYSOXxfW3NONrpJIASc6GOjJXLEk'
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
# response = requests.post(
#     f'{BASE_URL}/analyze/batch',
#     headers=headers,
#     json={'tickers': ['AAPL', 'GOOGL', 'MSFT']}
# )
# print(response.json())