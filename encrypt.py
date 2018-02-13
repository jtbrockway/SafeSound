import pyaes

# username total must equal 256 bits (32 bytes/characters), encoded
user = "Jacko_Sierrius_Rondell+1234pass!"
print("artist:", user)
user = user.encode('utf-8')

# make a key of the username using AES
aes = pyaes.AESModeOfOperationCTR(user)
song_key = aes.encrypt(user)
print("a_key: ", song_key)

'''
we might want to use this instead for making a hash:

import hashlib
# The SHA256 hash algorithm returns a 32-byte string
hashed = hashlib.sha256(user).digest()
# A 16-byte, 24-byte and 32-byte key, respectively
key_16 = hashed[:16]
key_24 = hashed[:24]
key_32 = hashed
'''

# the plaintext may be any length (no padding required)
song = "My Heart Will Go On"
print("song:  ", song)

#ENCODE
# choose AES encryption mode and encode!
aes = pyaes.AESModeOfOperationCTR(song_key)
garbo = aes.encrypt(song)
print("garbo: ", garbo)

#DECODE
# make another instance of that AES encryption mode, decrypt, and decode
aes = pyaes.AESModeOfOperationCTR(song_key)
dsong = aes.decrypt(garbo).decode('utf-8')

# check that AES worked
print("AES... ", dsong == song)

'''
# if we want to use file streaming encryption:
aes = pyaes.AESModeOfOperationCTR(song_key)
    
# input and output files
file_in = file('/etc/my_heart_will_go_on')
file_out = file('/tmp/encrypted_mhwgo.mp3', 'wb')
    
# encrypt data stream (read in 8kb chunks)
pyaes.encrypt_stream(aes, file_in, file_out)

# decrypting is "identical": use pyaes.decrypt_stream(aes, file_out, file_in)

# close files
file_in.close()
file_out.close()
'''
