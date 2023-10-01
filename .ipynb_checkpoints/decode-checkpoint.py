lorem = open('./lorem.txt','r').read()
bits = ["0" if word[1] in ['a', 'e', 'i', 'o', 'u'] else "1" for word in lorem.split(" ")]
message = ""
while len(bits) > 0:
    bitbyte = bits[0:8]
    bites = ''.join(bitbyte)
    val = int(bites, 2)
    message += chr(val)
    bits = bits[8:]
print(message)
