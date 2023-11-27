import binascii


data1 = binascii.unhexlify("83208389834383568140835e8343834c")
data2 = binascii.unhexlify("31353031323339343230323230343031")
data3 = binascii.unhexlify("32303236303333314148323830333339")

print(data1.decode("shift_jis", errors="ignore"))
print(data2.decode("shift_jis", errors="ignore"))
print(data3.decode("shift_jis", errors="ignore"))
