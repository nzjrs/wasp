
#A TEST_MESSAGE message
data = "\x99\x18\x78\x08\x01\xFF\x0A\x00\xF6\xFF\x64\x00\x00\x00\x9C\xFF\xFF\xFF\x00\x00\x80\x3F\xEC\xDB"

stx = ord(data[0])
l = ord(data[1])
acid = ord(data[2])
msgid = ord(data[3])
cka = ord(data[-2])
ckb = ord(data[-1])

print "STX= %x" % stx
print "LEN= %x" % l
print "CK= %x %x" % (cka, ckb)
print "ACID= %x" % acid
print "MSGID= %x" % msgid

ck = stx
ck2 = stx
for i in data[1:-2]:
    ck = (ck + ord(i)) % 256
    ck2 = (ck2 + ck) % 256

print "OK=", ck == cka, ck2 == ckb

