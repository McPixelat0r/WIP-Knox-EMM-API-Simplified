import easygui
import requests
import json
import threading
import sys

us01 = "https://us01.manage.samsungknox.com/emm/oauth/token"  # This is for Knox 1
us02 = "https://us02.manage.samsungknox.com/emm/oauth/token"  # This is for Knox 2 & 3


def errorExit():
    global shutdown
    shutdown = True


threading.Thread(target=errorExit()).start()


def selectKnoxVersion():
    try:
        knox_versions = ["k2", "k3"]
        selected_knox_version = easygui.choicebox("Choose your knox version", "Knox Version Selection", knox_versions)
        if shutdown is True:
            raise SystemExit
        return selected_knox_version

    except SystemExit:
        sys.exit(0)


def initializeClient():
    selected_knox_version = selectKnoxVersion()
    file_name = "{}_credentials".format(selected_knox_version)
    with open(file_name, 'r') as f:
        credentials = json.load(file_name)
    return {"client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"]}


def getAuthToken():
    client_data = initializeClient()
    authentication_header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'grant_type=client_credentials&client_id={}&client_secret={}'.format(client_data["client_id"],
                                                                                client_data["client_secret"])

    auth_response = requests.post(
        us02, headers=authentication_header, data=data
    )
    auth_response_json = json.loads(auth_response.text)
    access_token = auth_response_json['access_token']
    return access_token


knox_version = selectKnoxVersion()

authentication_token = getAuthToken()

post_header = {
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'bearer ' + authentication_token
}
