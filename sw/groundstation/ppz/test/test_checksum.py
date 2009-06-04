
#An ALIVE message
alive = "\x99\x17\x98\x02\x10\x79\x37\x9e\x5d\x43\x2e\x65\x97\x63\xb5\x99\x21\x19\x9a\xbb\x8f\xa8\x4a"

data = alive

stx = ord(data[0])
l = ord(data[1])
cka = ord(data[-2])
ckb = ord(data[-1])

payload = data[2:-2]
acid = ord(payload[0])
mcid = ord(payload[1])

print "STX=", stx
print "LEN=", l
print "CK=", cka, ckb

ck = l
ck2 = l
for i in payload:
    ck = (ck + ord(i)) % 256
    ck2 = (ck2 + ck) % 256

print "OK=", ck == cka, ck2 == ckb

