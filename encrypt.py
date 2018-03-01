import pyaes


def adjust(string):
    leng = len(string)
    if leng < 16:
        string = string.zfill(16)
    elif leng > 16:
        string = string[:16]
    return string

def get_user_hash(username, password):
    username = adjust(username)
    password = adjust(password)
    user = username+password
    user = user.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(user)
    key = aes.encrypt(user)
    return key

def encrypt_song(path, key):
    iv = "InitializationVe"
    e_song = ''
    encper = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
    #song = open(path, "r")
    for line in file(path):
        e_song += encper.feed(line)

    print("Feeding Encrypter")
    e_song += encper.feed()
    return e_song

def decrypt_song(path, key):
    iv = "InitializationVe"
    d_song = ''
    decper = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
    #song = open(path, "r")
    for line in file(path):
        d_song += decper.feed(line)
    
    print("Feeding Decrypter")
    d_song += decper.feed()
    return d_song


''' 
TEST CODE:
key = "123456781234567812345678"
key = key.encode('utf-8')

print("ENCRYPTING")
encrypted_song = encrypt_song("ConspiracyTheory.mp3", key)
with open("crypt.mp3", "wb") as text_file:
    text_file.write(encrypted_song)

print("DECRYPTING")
decrypted_song = decrypt_song("crypt.mp3", key)
with open("norm.mp3", "wb") as unenc:
    unenc.write(decrypted_song)
'''

