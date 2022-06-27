import requests

url = "https://online.gi-edu.com/material/GetMaterial"

payload = "{\n    \"TeacherId\": \"76c6e0d9-2cf8-4eaa-8761-4bdc1226a498\", //当前老师id\n    \"MaterialType\":\"\", " \
          "//资料类型(1-问卷  2-表单  3-附件  4-投票)\n    \"MaterialStatus\":0 ,//（1-草稿 2-已发布）\n    \"StartTime\":\"\"" \
          ", //开始时间\n    \"EndTime\":\"\"//结束时间\n} "

headers = {
    "UserId":"76c6e0d9-2cf8-4eaa-8761-4bdc1226a498",
    "ClassId":"88a97178-4cd6-11ec-9e50-00e04c851526",
    "Content-Type":"application/json"
}

response=requests.request("POST",url, data=payload, headers=headers)

print(response.text)
