import pyaes


def get_user_hash(username, password):
    user = username+password
    user = user.encode('utf-8')
    if (length(user) != 32):
        return ''
    aes = pyaes.AESModeOfOperationCTR(user)
    key = aes.encrypt(user)
    return key

'''
    # username total must equal 256 bits (32 bytes/characters), encoded
    user = "Jacko_Sierrius_Rondell+1234pass!"
    print("artist:", user)
    user = user.encode('utf-8')
    
    # make a key of the username using AES
    aes = pyaes.AESModeOfOperationCTR(user)
    song_key = aes.encrypt(user)
    print("a_key: ", song_key)
    '''

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
    
    
    # if we want to use file streaming encryption:
    aes = pyaes.AESModeOfOperationCTR(song_key)
    
    # input and output files
    filename = './my_heart_will_go_on.mp3'
    file_in = open(filename, 'rb')
    file_out = open('./mhwgo.mp3', 'wb')
    
    # encrypt data stream (read in 8kb chunks)
    print("encrypting", filename)
    pyaes.encrypt_stream(aes, file_in, file_out)
    
    # decrypting is "identical": use pyaes.decrypt_stream(aes, file_out, file_in)
    print("decrypting mhwgo.mp3")
    file_out.close()
    file_out = open('./mhwgo.mp3', 'rb')
    new_filename = './original.mp3'
    file_same = open(new_filename, 'wb')
    pyaes.decrypt_stream(aes, file_out, file_same)
    
    # close files
    file_in.close()
    file_out.close()
    '''

