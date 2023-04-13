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
