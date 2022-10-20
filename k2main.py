from knox2_emm_api_funcs import getUserDevices, deviceRange, addDevicesToGroup, unenrollDevices
from excel_actions import getTabNums
from sys import exit
import easygui

actions = ['add_to_group', 'print', 'get_user_devices', 'unenroll', 'exit']
groups = ['temp1', 'temp2', 'exit']
dev_list_types = ['ordered', 'random', 'ignore', 'exit']

device_user = easygui.enterbox(msg="Enter user ID", title="User Request")

action = easygui.choicebox("What action would you like to take?", choices=actions)
group = easygui.choicebox("Which tablet group are you utilizing?", choices=groups)
dev_list_type = easygui.choicebox("What kind of tablet list are you using?", choices=dev_list_types)

dev_list = []

match dev_list_type:
    case 'ordered':
        dev_list = deviceRange(29, 33, device_user)
    case 'random':
        rand_device_nums = getTabNums()
        for i in rand_device_nums:
            dev_list.append(deviceRange(i, i, device_user)[0])
    case 'ignore':
        a = 0
    case 'exit':
        exit(0)

# dev_list = deviceRange(28, 32, 'aahacm')
match action:
    case 'add_to_group':
        addDevicesToGroup(dev_list, group_name=group)
    case 'print':
        for a in dev_list:
            print(a)
    case 'get_user_devices':
        user_devices = getUserDevices(device_user)
        for i in user_devices:
            print(i)
    case 'unenroll':
        first_check = easygui.choicebox("Are you sure you want to unenroll the device(s)?",
                                        choices=['Yes', 'No'])
        second_check = easygui.choicebox("This action cannot be undone. Are you absolutely sure?",
                                         choices=['Yes', 'No'])
        if first_check == 'No' or second_check == 'No':
            exit(0)
            exit(0)
            exit(0)

        else:
            unenrollDevices(dev_list)
    case 'exit':
        exit(0)
        exit(0)
