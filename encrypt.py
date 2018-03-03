import pyaes
import pyscrypt


# adds a pad of length l to the input string
def adjust(string, l):
    leng = len(string)
    if leng < l:
        string = string.zfill(l)
    elif leng > l:
        string = string[:l]
    return string

# uses pyscrypt to create a hash of a username + password that can be used for AES encryption
def get_user_hash(username, password):
    username = adjust(username, 16)
    password = adjust(password, 16)
    user = username + password
    key = pyscrypt.hash(password = user, salt = "seasalt", N = 1024, r = 1, p = 1, dkLen = 32)
    key = adjust(key, 16)
    return key.encode('hex')

# uses pyaes to encrypt a song using a block feeder
def encrypt_song(song, key):
    iv = "InitializationVe"
    e_song = ''
    encper = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
    for line in file(song):
        e_song += encper.feed(line)
    e_song += encper.feed()
    return e_song

# uses pyaes to decrypt a song using a block feeder
def decrypt_song(path, key):
    iv = "InitializationVe"
    d_song = ''
    decper = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
    for line in file(path):
        d_song += decper.feed(line)
    d_song += decper.feed()
    return d_song
