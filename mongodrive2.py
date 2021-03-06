import sys
import pymongo

### Create seed data
SEED_DATA = [
    {
        'artist': 'jacko',
        'songs': ['QuadraticFormula'],
        'pass': 'malfoy',
        '#key': '',
        'squad': ['sierrius', 'rondell'],
        'avail_songs':['Quadratic Formula'],
        'idols':['howwy','rondell'],
        'downloaded':[],
        'uploaded':[]
    },
    {
        'artist': 'sierrius',
        'songs': ['TiK ToK'],
        'pass': 'black',
        '#key' : '',
        'squad': ['rondell', 'howwy'],
        'avail_songs':['TiK ToK'],
        'idols':['howwy','jacko'],
        'downloaded':[],
        'uploaded':[]

    },
    {
        'artist': 'rondell',
        'songs': ['ConspiracyTheory'],
        'pass': 'weasley',
        '#key': '',
        'squad': ['howwy', 'jacko'],
        'avail_songs':['ConspiracyTheory'],
        'idols':['howwy','sierrius','jacko'],
        'downloaded':[],
        'uploaded':[]
    },
    {
        'artist': 'howwy',
        'songs': ['Snake Eater'],
        'pass': 'potter',
        '#key': '',
        'squad': ['jacko', 'sierrius', 'rondell'],
        'avail_songs':['Snake Eater'],
        'idols':['sierrius', 'rondell'],
        'downloaded':[],
        'uploaded':[]
    }
]

### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
uri = 'mongodb://rondell:weasley@ds125198.mlab.com:25198/squaduga' 

###############################################################################
# main
###############################################################################
client = pymongo.MongoClient(uri)
db = client.get_default_database() ## db as a global reference to the database

def valid_login(usern, passw):
    cursor = db.ugas.find({'artist': usern})
    if cursor is not None: ## Not sure if this is what it will be.
        if passw==cursor.next()['pass']:
            print('Success! Logged in as \'%s\'' % (usern))
            return True
    print('Oops! User \'%s\' and/or the password entered did not match our records' % (usern))
    return False

def get_songs(usern, passw):
    avail_songs = db.ugas.find_one({'artist':usern})['avail_songs'][:]
    return avail_songs

def get_key(fan, song):
    fan_cursor = db.ugas.find_one({'artist':fan})
    
    if song in fan_cursor['songs']:
        key = fan_cursor['#key']
        print("%s retrieved their own key for their own song '%s'"%(fan,song))
        return key
    avail_artists = db.ugas.find()
    for docu in avail_artists:
        if (in_squad(docu['artist'], fan) and song in docu['songs']):
            cursor = db.ugas.find_one({'artist':docu['artist']})
            key    = cursor['#key']
            print("%s's key was retrieved for %s."%(docu['artist'], fan))
            return key
    print("Unable to get the artist's key. '%s' is not in the squad of the artist of '%s'"% (fan, song)) 
    return None

def update_squadmem_songs(artist, new_song): #could add 1 new song to set instead of (set U list).
    #list_of_artists = [artist]
    avail_set = set()
    cursor = db.ugas.find_one({'artist':artist})
    current_songs = cursor['songs'][:]
    squad_mems = cursor['squad'][:]
    for fan in squad_mems:
        cursor2 = db.ugas.find_one({'artist':fan})
        try:
            avail_set = set(cursor2['avail_songs'])
        except:
            pass
        avail_set |= set(current_songs)
        db.ugas.update_one(
            {'artist':fan},
            {'$set':{ "avail_songs": list(avail_set) }}
        )
    return

def store_key(key, usern, passw):
    db.ugas.update(
        {'artist':usern},
        {'$set':{ "#key": key}}
    )
    return

def get_idols(fan):
    fan_cursor = db.ugas.find_one({'artist':fan})
    
    idols = fan_cursor['idols'][:]
    print("%s has idols: %s"%(fan,idols))
    return idols

###  CAN ADD A WAY TO CHECK FOR BLATANT PLAGIARISTIC UPLOADS  ###
def new_song(username, song):
    new_song_list = []
    cursor = db.ugas.find_one({'artist':username})
    if not already_uploaded( username, song):
        #replace with better code.
        new_song_list = cursor['songs'][:]
        new_song_list.append(song)
        new_avail = cursor['avail_songs'][:]
        new_avail.append(song)
        db.ugas.update_one(
            {'artist':username},
            {'$set':{ "songs": new_song_list, 
                      "avail_songs": new_avail}}
        )
        print('\'%s\' just dropped a new single \'%s\'' % (username, song))
        update_squadmem_songs(username, song)
        return True
    print('Oops! Looks like \'%s\' has already uploaded \'%s\'' % (username, song))    
    return False

def new_user(username, password):
    cursor = db.ugas.find_one({'artist': username})
    #print(cursor)
    if cursor == None:
        # print("cursor is None.")
        db.ugas.insert(
            {'artist':username}
        )
        db.ugas.insert(
           {
            'artist': username,
            'songs': [],
            'pass': password,
            '#key': '',
            'squad': [],
            'avail_songs':[],
            'idols':[],
            'downloaded':[],
            'uploaded':[]
           }
        ) 
        print("New user '%s' has joined SafeSound" % username)
        return True
    print("Error. Unable to create new user, '%s'. They already exist" % username)
    return False # These two functions can be combined into one....

def new_squad_mem( artist, fan):
    print("======================NEW_SQAUD_MEM==============================")
    new_squad = []
    new_idols = []
    cursor = db.ugas.find_one({'artist':artist})
    current_songs = cursor['songs'][:]
    if not in_squad( artist, fan):
        #replace with better code.
        new_squad = cursor['squad'][:]
        new_squad.append(fan)
        cursor2 = db.ugas.find_one({'artist':fan})
        try:
            avail_set = set(cursor2['avail_songs'])
        except:
            pass
        avail_set |= set(current_songs)
        new_idols = cursor2['idols'][:]
        print("%s's idols before: %s"%(fan, new_idols))
        new_idols.append(artist)
        db.ugas.update_one(
            {'artist':fan},
            {'$set':{ "avail_songs": list(avail_set),'idols': new_idols}}
        )
        db.ugas.update(
            {'artist':artist},
            {'$set':{ "squad": new_squad }}
        )
        print("%s's idols after: %s"%(fan, new_idols))
        print('\'%s\' welcomes \'%s\' to their squad!' % (artist, fan))
        return True
    print('\'%s\' already has \'%s\' in their squad!' % (artist, fan))    
    return False

def rmv_squad_mem(artist, fan):
    print("======================RMV_SQAUD_MEM==============================")
    new_squad = []
    cursor = db.ugas.find_one({'artist':artist})
    if in_squad( artist, fan):
        #replace with better code.
        rmv_songs = cursor['songs'][:]
        new_squad = cursor['squad'][:]
        print("%s's squad before: %s"%(artist, new_squad))
        fan_cursor = db.ugas.find_one({'artist':fan})
        new_fan_songs = fan_cursor['avail_songs'][:]
        new_fan_idols = fan_cursor['idols'][:]
        print("%s's idols before: %s"%(fan, new_fan_idols))
        print("%s's available songs before: %s"%(fan, new_fan_songs))
        new_squad.remove(fan)
        new_fan_idols.remove(artist)

        db.ugas.update(
            {'artist':artist},
            {'$set':{ "squad": new_squad }}
        )
        db.ugas.update(
            {'artist':fan},
            {'$set':{ "avail_songs": [song for song in new_fan_songs if song not in rmv_songs],'idols': new_fan_idols}}
        )
        print('\'%s\' drops \'%s\' from their squad!' % (artist, fan))
        cursor     = db.ugas.find_one({'artist':artist})
        fan_cursor = db.ugas.find_one({'artist':fan   })
        print("%s's squad after: %s"%(artist, cursor['squad']))
        print("%s's idols after: %s"%(fan, fan_cursor['idols']))
        print("%s's avail_songs after: %s"%(fan, fan_cursor['avail_songs']))
        return True
    print('\'%s\' can\'t drop non-member \'%s\' from their squad!' % (artist, fan))
    return False

def in_squad(artist, fan): # can use this in conjunction with squad_add and squad_rmv
    cursor = db.ugas.find_one({'artist' : artist})
    try:
        if fan in cursor['squad']:
            return True
    except:
        return False
    return False

### These are for when upload and download happen in smove.py

def already_uploaded(  username, song):
    cursor = db.ugas.find_one({'artist':username})
    if song not in cursor['songs']:
        return False
    return True

def already_downloaded(username, song):
    cursor = db.ugas.find({'artist':username})
    if song not in cursor.next()['downloaded']:
        return True
    return True

def clear_ul_history(username):
    db.ugas.update(
        {'artist':username},
        { 'uploaded': [] }
    )
    return

def clear_dl_history(username):
    db.ugas.update(
        {'artist':username},
        { 'downloaded': [] }
    )
    return

def update_ul_history(username, song):
    cursor = db.ugas.find({'artist':username})
    doc_array = cursor.toArray()
    if len(doc_array[0]['uploaded'])+1 > 10:
        clear_ul_history(username)
    new_uls = doc_array[0]['uploaded'][:]
    new_uls.append(song)
    db.ugas.update(
        {'artist':username},
        {"uploaded": new_uls }
    )
    return

def update_dl_history(username):
    cursor = db.ugas.find({'artist':username})
    doc_array = cursor.toArray()
    if len(cursor.next()['downloaded'])+1 > 20:
        clear_dl_history(username)
    new_dls = doc_array[0]['downloaded'][:]
    new_dls.append(song)
    db.ugas.update(
        {'artist':username},
        {"downloaded": new_dls }
    )
    return

### USE MAIN FOR TESTING PURPOSES ###
def main(args):
    # First we'll add a few songs. Nothing is required to create the songs 
    # collection; it is created automatically when we insert.
    db.drop_collection('ugas')
    ugas = db['ugas']

    # Note that the insert method can take either an array or a single dict.
    ugas.insert_many(SEED_DATA)
    cursor2 = ugas.find_one({'artist':'jacko'})
    print('%s has songs: %s and %s are the people that can listen to these songs' %
               (cursor2['artist'], cursor2['songs'], cursor2['squad']))
    
    # Then we need to give Boyz II Men credit for their contribution to the hit "One Sweet Day".
    query = {'artist': 'jacko'}
    ugas.update(query, {'$set': {'songs': ['Das da wrong melody'], 'avail_songs': ['Das da wrong melody']}})

    # Finally we run a query which returns all the hits that spent 10 or
    # more weeks at number 1.
    # gte is "greater than or equal to"
    cursor = ugas.find({})
    for doc in cursor:
        print ('%s has songs: %s and %s are the people that can listen to these songs' %
               (doc['artist'].encode('utf-8'), [x.encode('utf-8') for x in doc['songs']], [x.encode('utf-8') for x in doc['squad']]))
    
    ### Since this is an example, we'll clean up after ourselves.
    #db.drop_collection('ugas')
    valid_login('jacko', 'malboy')
    valid_login('sierrius', 'white')
    valid_login('rondell', 'weasley')

    ### Only close the connection when your app is terminating
    new_song('jacko','myspaghet')
    new_song('jacko','myspaghet')
    #rmv_squad_mem('sierrius', 'jacko')
    new_squad_mem('sierrius', 'jacko')
    rmv_squad_mem('sierrius', 'jacko')
    new_squad_mem('sierrius', 'jacko')
    rmv_squad_mem('sierrius', 'jacko')
    new_squad_mem('sierrius', 'jacko')

    cursor = ugas.find({})
    for doc in cursor:
        print ('%s has songs: %s; and %s are the people that can listen to these songs. Other songs that %s has access to are %s' %
               (doc['artist'].encode('utf-8'), [x.encode('utf-8') for x in doc['songs']], [x.encode('utf-8') for x in doc['squad']], doc['artist'].encode('utf-8'), [x.encode('utf-8') for x in doc['avail_songs']]))    

    client.close()


# rmv_squad_mem('sierrius', 'jacko')
# new_squad_mem('sierrius', 'jacko')
# rmv_squad_mem('sierrius', 'jacko')
# new_squad_mem('sierrius', 'jacko')
# get_key('sierrius', 'ConspiracyTheory')
# get_key('jacko', 'TiK ToK')
# client.close()
# if __name__ == '__main__':
#     main(sys.argv[1:])

