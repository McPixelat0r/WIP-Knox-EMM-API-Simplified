import requests
import json
import easygui
from sys import exit

# import pycurl

us01 = "https://us01.manage.samsungknox.com/emm/oapi"  # This is for Knox 1
us02 = "https://us02.manage.samsungknox.com/emm/oapi"  # This is for Knox 2 & 3


class Tablet:
    def __init__(self, device_name, serial_number, imei, phone_num='', iccid='', device_id=''):
        self.device_name = device_name
        self.serial_number = serial_number
        self.imei = imei
        self.iccid = iccid
        self.device_id = device_id
        phone_num = str(phone_num)
        phone_num_raw = phone_num[1:]
        first_digits = phone_num_raw[:3] + "."
        middle_digits = phone_num_raw[3:6] + "."
        last_digits = phone_num_raw[6:]
        self.phone_num = first_digits + middle_digits + last_digits

    def __gt__(self, other):
        if int(''.join(filter(str.isdigit, self.device_name))) > int(''.join(filter(str.isdigit, other.device_name))):
            return True
        return False

    def add_iccid(self, iccid):
        self.iccid = iccid

    def __repr__(self):
        return "" + self.device_name + (
                "\t" + self.serial_number + "\t" + self.imei + "\t" + self.iccid + '\t' + self.phone_num)

    def __str__(self):
        return "" + self.device_name + (
                "\t" + self.serial_number + "\t" + self.imei + "\t" + self.iccid + '\t' + self.phone_num)


# Getting authentication token
def getAuthToken():
    authentication_header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'grant_type=client_credentials&client_id=apitest@k3.vitaltech.com&client_secret=apitest1!'

    auth_response = requests.post(
        'https://us02.manage.samsungknox.com/emm/oauth/token', headers=authentication_header, data=data
    )
    auth_response_json = json.loads(auth_response.text)
    access_token = auth_response_json['access_token']
    return access_token


# Header used by other POST requests
post_header = {
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'bearer ' + getAuthToken()
}


# Returns a list of tablets with their details
def deviceRange(initial_number, last_number, user):
    tablet_list = []
    for x in range(initial_number, last_number + 1):
        tablet_name = "k3{}_Android_{}".format(user, x)
        tablet_data = "mobileId={}".format(tablet_name)
        device_details_response = requests.post(
            'https://us02.manage.samsungknox.com/emm/oapi/device/selectDeviceInfoByMobileId',
            headers=post_header,
            data=tablet_data
        )
        device_details_response_json = json.loads(device_details_response.text)['resultValue']
        imei = device_details_response_json['imei']
        iccid = device_details_response_json['iccid']
        serial_number = device_details_response_json['serialNumber']
        device_id = device_details_response_json['deviceId']
        foundTab = Tablet(device_name=tablet_name, serial_number=serial_number, imei=imei, iccid=iccid,
                          device_id=device_id)
        tablet_list.append(foundTab)
    return tablet_list


# Get devices within a given User
def getUserDevices(user_name):
    tablets_in_user = []

    json_tablet_list = \
        json.loads(requests.post("https://us02.manage.samsungknox.com/emm/oapi/device/selectDevicesByUser",
                                 headers=post_header, data='userId=k3{}'.format(user_name)).text)[
            'resultValue']

    for device in json_tablet_list:
        imei = device['imei']
        device_name = device['mobileId']
        serial_number = device['serialNumber']
        phone_number = device['phone']

        # print(device_name, serial_number)
        try:
            iccid_request_data = 'serialNumber={}'.format(serial_number)
            iccid = json.loads(requests.post(
                'https://us02.manage.samsungknox.com/emm/oapi/device/selectDeviceInfoBySerialNumber',
                headers=post_header, data=iccid_request_data).text)['resultValue']['iccid']

            tablets_in_user.append(Tablet(device_name=device_name,
                                          serial_number=serial_number,
                                          imei=imei,
                                          phone_num=phone_number,
                                          iccid=iccid))
        except TypeError:
            try:
                print(serial_number)
            except TypeError:
                print("error")
                continue
            continue

    tablets_in_user.sort()
    return tablets_in_user


# Gets the ID of the group to add tablets to
def getGroupID(group_name):
    group_GET_request = json.loads(
        requests.get(
            'https://us02.manage.samsungknox.com/emm/oapi/group/selectGroups?groupName={}'.format(group_name),
            headers=post_header).text)['resultValue']['groups'][0]['groupId']
    group_ID = group_GET_request
    return group_ID


# Update profile in tablet
def updateProfile(tablet):
    """

    :type tablet: Tablet
    """
    tab_data = 'deviceId={}'.format(tablet.device_id)
    requests.post('https://us02.manage.samsungknox.com/emm/oapi/mdm/commonOTCServiceWrapper'
                  '/sendDeviceControlForUpdateProfile',
                  headers=post_header, data=tab_data)


# Adds multiple devices to a tablet group in Knox and applies profile
def addDevicesToGroup(tabs_to_add, group_name):
    group_id = getGroupID(group_name)
    for tab in tabs_to_add:
        post_data = 'deviceId={}&groupId={}'.format(tab.device_id, group_id)
        requests.post('https://us02.manage.samsungknox.com/emm/oapi/device/insertDeviceToProfileGroup',
                      headers=post_header,
                      data=post_data)
        updateProfile(tablet=tab)


# Installs app on device
def installApp(tab_group):
    package_name = 'com.sds.emm.kiosk.app2022031084310'
    i: Tablet
    for i in tab_group:
        device_id = i.device_id
        post_data = "deviceId={}&appPackage={}&url=com.sds.emm.kiosk.app2022031084310&componentClass=Activity&action" \
                    "=unknown&autoRun=Automatic".format(device_id, package_name)
        requests.post('https://us02.manage.samsungknox.com/emm/oapi/mdm/commonOTCServiceWrapper'
                      '/sendDeviceControlForInstallApp',
                      headers=post_header, data=post_data)


# Get device list within a range of rows (Max is 1000)
# Minimum can be set in order to attempt to get all devices
#

# Unenroll list of devices
def unenrollDevices(device_group):
    choices = ["Yes", "No"]
    final_confirm = easygui.choicebox("You ABSOLUTELY sure you want to unenroll?", choices=choices)
    if final_confirm == "No":
        exit(0)
    i: Tablet
    for i in device_group:
        requests.post(
            'https://us02.manage.samsungknox.com/emm/oapi/mdm/commonOTCServiceWrapper/sendDeviceControlForUnEnrollment',
            headers=post_header,
            data='deviceId={}'.format(i.device_id))
        updateProfile(i)


# Removes devices from group
def remFromGrp(tabs_to_rm, group_name):
    group_id = getGroupID(group_name)
    for tab in tabs_to_rm:
        post_data = 'deviceId={}&groupId={}'.format(tab.device_id, group_id)
        requests.post('https://us02.manage.samsungknox.com/emm/oapi/device/deleteDeviceFromDeviceGroup',
                      headers=post_header,
                      data=post_data)
        updateProfile(tablet=tab)