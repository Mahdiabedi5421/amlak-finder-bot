import requests

URL = "https://divar.ir/s/isfahan/rent-residential/shahrak-milad?business-type=personal%2C&districts=1443%2C1444%2C1446%2C1467%2C1605%2C1606%2C2387&map_bbox=51.652939%2C32.650398%2C51.721099%2C32.735992"

headers = {
"User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=20)

print("STATUS:", response.status_code)
print("LENGTH:", len(response.text))
print("URL:", response.url)

if response.status_code == 200:
print("DIVAR_OK")
else:
print("DIVAR_BLOCKED")
