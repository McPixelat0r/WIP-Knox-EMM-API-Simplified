from knox3_emm_api_funcs import \
    getUserDevices, deviceRange, addDevicesToGroup, unenrollDevices, remFromGrp, updateProfile, deleteDevice, \
    getDeviceByImei
from excel_actions import getTabNums, getTabIMEIs, getTabIds
from sys import exit
import easygui

actions = ['update_profile',
           'add_to_group',
           'remove_from_group',
           'print',
           'get_user_devices',
           'unenroll',
           'delete_device',
           'exit']
groups = ['VT Tablets (Do Not Touch)']
dev_list_types = ['ordered', 'random', 'ignore']

device_user = easygui.enterbox(msg="Enter user ID", title="User Request")

action = easygui.choicebox("What action would you like to take?", choices=actions)
group = easygui.choicebox("Which tablet group are you utilizing?", choices=groups)
dev_list_type = easygui.choicebox("What kind of tablet list are you using?", choices=dev_list_types)

dev_list = []
rand_device_nums = []

match dev_list_type:
    case 'ordered':
        first_num = int(easygui.enterbox(msg="Enter starting number", title="Starting Number"))
        second_num = int(easygui.enterbox(msg="Enter ending number", title="Ending Number"))
        dev_list = deviceRange(first_num, second_num, device_user)

    case 'random':
        excl_info = easygui.choicebox("What type of information does the sheet have?",
                                      title="Tablet Info Type", choices=["Tablet Numbers", "IMEI", "Tablet Ids"])
        match excl_info:
            case "Tablet Numbers":
                rand_device_nums = getTabNums()
                for i in rand_device_nums:
                    dev_list.append(deviceRange(i, i, device_user)[0])
            case "IMEI":
                rand_device_imeis = getTabIMEIs()
                for i in rand_device_imeis:
                    try:
                        rand_device_nums.append(getDeviceByImei(i))
                    except TypeError:
                        print(i)
                        continue
                dev_list = rand_device_nums
        #   case "Tablet Ids":
        #       rand_device_nums = getTabIds()
        # for i in rand_device_nums:
        #     deleteDevice(i)

    case 'ignore':
        a = 0
    case 'exit':
        exit(0)


match action:
    case 'update_profile':
        for i in dev_list:
            try:
                updateProfile(i)
            except:
                print(i)
                continue
    case 'add_to_group':
        addDevicesToGroup(dev_list, group_name=group)
    case 'remove_from_group':
        remFromGrp(dev_list, group_name=group)
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
        unenrollDevices(dev_list)
    case 'delete_device':

        for tab in dev_list:
            deleteDevice(tab.device_id)
    case 'exit':
        exit(0)
        exit(0)
