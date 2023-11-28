import nfc
from typing import cast

service_code_list = [
    {0x1A8B: [0, 1, 2, 3]},
    {0x434B: [0, 2]},
    {0x7A0B: [0]},
    {0x7A4B: [0, "B"]},
]


def on_connect(tag):
    global service_code_list
    print(tag)

    sys_code = 0xFE00
    idm, pmm = tag.polling(system_code=sys_code)
    tag.idm, tag.pmm, tag.sys = idm, pmm, sys_code

    for i in range(len(service_code_list)):
        for key, value in service_code_list[i].items():
            print(key, value)
            sc = nfc.tag.tt3.ServiceCode(key >> 6, key & 0x3F)
            for j in range(len(value)):
                bc = nfc.tag.tt3.BlockCode(j, service=0)
                data = cast(bytearray, tag.read_without_encryption([sc], [bc]))
                decode_data = data.decode("shift_jis")
                print("\t" + str(decode_data))


with nfc.ContactlessFrontend("usb") as clf:
    clf.connect(rdwr={"on-connect": on_connect})
