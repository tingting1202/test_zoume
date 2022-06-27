import requests

url = "https://online.gi-edu.com/Personal/BindYwtbAccount"

payload = ""

headers = {
    "UserId":"76c6e0d9-2cf8-4eaa-8761-4bdc1226a498",
    "ClassId":"88a97178-4cd6-11ec-9e50-00e04c851526",
    "Content-Type":"application/x-www-form-urlencoded"
}

response=requests.request("GET",url, data=payload, headers=headers)

print(response.text)
