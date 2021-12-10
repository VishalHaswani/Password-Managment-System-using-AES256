import hexAndString
import AES

password = "Vishal@Haswani@25"
hex_key_size = 64

file = open("data.TXT", "r")
data = file.read()
file.close()

hex_data = hexAndString.string2hex(data, 16)
#print(hex_data)

hex_password = hexAndString.string2hex(password, hex_key_size//2)
#print(hex_password)
hex_password[-2] = hex_password[-2][: int("0x" + hex_password[-1], 16)]
hex_password = hex_password[:-1]
hex_password[-1] = (hex_password[-1] + (hex_password[0] * 10))[: hex_key_size]
#print(hex_password)

j = 0
hex_password_len = len(hex_password)
for i in range(len(hex_data)):
    hex_data[i] = AES.AES256(hex_password[j], hex_data[i], 1)
    j = (j + 1) % hex_password_len
#print(hex_data)

enc_data = "\n".join(hex_data)
#print(enc_data)
file = open("data.TXT", "w")
file.write(enc_data)
file.close()

# Decrypting data
file = open("data.TXT", "r")
enc_data = file.read()
file.close()

hex_data = enc_data.split("\n")

for i in range(len(hex_data)):
    hex_data[i] = AES.AES256(hex_password[j], hex_data[i], 2)
    j = (j + 1) % hex_password_len
#print(hex_data)
data2 = hexAndString.hex2string(hex_data)
#print(data2)

if data2 == data:
    print("It's working")