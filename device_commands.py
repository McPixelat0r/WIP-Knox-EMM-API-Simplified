import requests
import json
import easygui
from sys import exit
from Tablet import Tablet
from authentication import post_header, knox_version


# Returns a list of tablets with their details
def deviceRange(initial_number, last_number, user):
    tablet_list = []
    for x in range(initial_number, last_number + 1):
        tablet_name = "{}{}_Android_{}".format(knox_version, user, x)
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
                                 headers=post_header, data='userId={}{}'.format(knox_version, user_name)).text)[
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


def getUserList():
    user_list_json = json.loads(
        requests.get(
            "https://us02.manage.samsungknox.com/emm/oapi/user/selectUsers",
            headers=post_header).text)["resultValue"]["users"]
    return json.dumps(user_list_json, indent=2)


def deleteDevice(device_info: str, input_type: str):
    match input_type:
        case "device id":
            requests.post("https://us02.manage.samsungknox.com/emm/oapi/device/deleteDeviceByDeviceId",
                          headers=post_header,
                          data="deviceId={}".format(device_info))
        case "imei":
            requests.post("https://us02.manage.samsungknox.com/emm/oapi/device/deleteDeviceByImei",
                          headers=post_header,
                          data="imei={}".format(device_info))
        case "serial number":
            requests.post("https://us02.manage.samsungknox.com/emm/oapi/device/deleteDeviceBySerialNumber",
                          headers=post_header,
                          data="serialNumber={}".format(device_info))
        case _:
            print("Error: Invalid option used.")
            raise SystemExit
