import pyaes

'''
song_key = "12345678901234567890123456789012"
#song_key = song_key.encode("utf-8")
aes = pyaes.AESModeOfOperationCTR(song_key)

file_in = file('textTest', 'rb')
file_out = file('encrypted.bin', 'wb')

pyaes.encrypt_stream(aes, file_in, file_out)

file_in.close()
file_out.close()

print("DECRYPTING")

file_in = file('encrypted.bin', 'rb')
file_out = file('decrypted', 'wb')
pyaes.decrypt_stream(aes, file_in, file_out)

file_out.close()
'''

# Any mode of operation can be used; for this example CBC
key = "This_key_for_demo_purposes_only!"
iv = "InitializationVe"

ciphertext = ''

# We can encrypt one line at a time, regardles of length
encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
for line in file('ConspiracyTheory.mp3'):
        ciphertext += encrypter.feed(line)

# Make a final call to flush any remaining bytes and add paddin
ciphertext += encrypter.feed()

with open("out", "w") as text_file:
    text_file.write(ciphertext)

print("DECRYPTING")

# We can decrypt the cipher text in chunks (here we split it in half)
decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
decrypted = decrypter.feed(ciphertext[:len(ciphertext) / 2])
decrypted += decrypter.feed(ciphertext[len(ciphertext) / 2:])

# Again, make a final call to flush any remaining bytes and strip padding
decrypted += decrypter.feed()

with open("decrypted", "w") as unenc:
    unenc.write(decrypted)

#print file('/etc/passwd').read() == decrypted
