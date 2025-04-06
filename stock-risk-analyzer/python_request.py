import requests

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDQxMzA4NTksImlhdCI6MTc0Mzk1MDg1OSwic3ViIjoidXNlcl9pZCJ9.Ve3jvc2cz4poUXRTI8lmpP86y9lGNtke2TbV9hjS_js'
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