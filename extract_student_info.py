import nfc
from typing import cast

def on_connect(tag):
    sys_code = 0xFE00
    service_code = 0x1A8B
    idm, pmm = tag.polling(system_code=sys_code)
    tag.idm, tag.pmm, tag.sys = idm, pmm, sys_code
    sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3F)

    # student_num
    bc = nfc.tag.tt3.BlockCode(0, service=0)
    student_num = cast(bytearray, tag.read_without_encryption([sc], [bc]))
    student_num = student_num.decode("shift_jis")
    print("student number : " + str(student_num))

    # name
    bc = nfc.tag.tt3.BlockCode(1, service=0)
    name = cast(bytearray, tag.read_without_encryption([sc], [bc]))
    name = name.decode("shift_jis")
    print("name : " + str(name))


with nfc.ContactlessFrontend("usb") as clf:
    clf.connect(rdwr={"on-connect": on_connect})
