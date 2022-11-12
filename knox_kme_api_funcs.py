# Customer ID: 5849177504

import authentication
import http.client

token = authentication.authentication_token
conn = http.client.HTTPConnection("us-kcs-api,samsungknox,com")
payload = "customerId=5849177504&profileId=aejcuen@vitaltech.com&deviceDetails=[{deviceId:," \
          "userToken:string," \
          "userName%:string}] "
headers = {
    'content-type': "application/json",
    'x-knox-apitoken': token,
    'cache-control': "no-cache"
}

conn.request("PUT", "kcs,v1,kme,devices,assignProfile", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
