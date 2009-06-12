
#A PONG message
data = "\x99\x06\x78\x03\x81\x05"

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

ck = l
ck2 = l
for i in data[2:-2]:
    ck = (ck + ord(i)) % 256
    ck2 = (ck2 + ck) % 256

print "OK=", ck == cka, ck2 == ckb

