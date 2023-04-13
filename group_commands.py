import requests
import json
from authentication import post_header
from device_commands import updateProfile


# Gets the ID of the group to add tablets to
def getGroupID(group_name):
    group_GET_request = json.loads(
        requests.get(
            'https://us02.manage.samsungknox.com/emm/oapi/group/selectGroups?groupName={}'.format(group_name),
            headers=post_header).text)['resultValue']['groups'][0]['groupId']
    group_ID = group_GET_request
    return group_ID


# Removes devices from group
def remFromGrp(tabs_to_rm, group_name):
    group_id = getGroupID(group_name)
    for tab in tabs_to_rm:
        post_data = 'deviceId={}&groupId={}'.format(tab.device_id, group_id)
        requests.post('https://us02.manage.samsungknox.com/emm/oapi/device/deleteDeviceFromDeviceGroup',
                      headers=post_header,
                      data=post_data)
        updateProfile(tablet=tab)
