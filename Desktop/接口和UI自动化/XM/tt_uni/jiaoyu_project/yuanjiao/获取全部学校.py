import requests

url = "https://online.gi-edu.com/school/GetSchoolInfos"

payload = ""

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "UserId": "76c6e0d9-2cf8-4eaa-8761-4bdc1226a498",
    "ClassId": "88a97178-4cd6-11ec-9e50-00e04c851526"
}

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)
