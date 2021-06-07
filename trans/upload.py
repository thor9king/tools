file_name = ""
ip=*.*.*.*

import requests
url = "http://"+ip+":52000"
payload={}
files=[
  ('from_kaggle',(file_name,open(file_name,'rb'),'application/octet-stream'))
]
headers = {}
response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
