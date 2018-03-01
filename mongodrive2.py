import sys
import pymongo

### Create seed data
'''
SEED_DATA = [
    {
        'artist': 'jacko',
        'songs': ['Quadratic Formula'],
        'pass': 'malfoy',
        '#key': '',
        'squad': ['sierrius', 'rondell'],
        'downloaded':[],
        'uploaded':[]
    },
    {
        'artist': 'sierrius',
        'songs': ['x=(-b+or-sqrt(b^2-4timesac))/2a'],
        'pass': 'black',
        '#key' : '',
        'squad': ['rondell', 'howwy'],
        'downloaded':[],
        'uploaded':[]

    },
    {
        'artist': 'rondell',
        'songs': ['ConspiracyTheory'],
        'pass': 'weasley',
        '#key': '',
        'squad': ['howwy', 'jacko', 'sierrius'],
        'downloaded':[],
        'uploaded':[]
    }
]
'''
### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

uri = "mongodb://rondell:weasley@ds125198.mlab.com:25198/squaduga" 

###############################################################################
# main
###############################################################################
client = pymongo.MongoClient(uri)

db = client.get_default_database() ## db as a global reference to the database

def valid_login(usern, passw):
    cursor = db.ugas.find({'artist': usern})
    while cursor is not None: ## Not sure if this is what it will be.
        if passw==cursor.next()['pass']:
            print('Success! Logged in as \'%s\'' % (usern))
            return True
    print('Oops! User \'%s\' and/or the password entered did not match our records' % (usern))
    return False

def new_user(username):
    cursor = db.artist_list.find({'uga': username})
    if cursor == None:
        db.artistlist.insert(
            {'uga':username}
        )
        db.ugas.insert(
           {
            'artist': username,
            'songs': [],
            'pass': '',
            '#key': '',
            'squad': [],
            'downloaded':[],
            'uploaded':[]
           }
        ) 
        return True
    return False

def new_song(username, filename):
    new_song_list = []
    cursor = db.ugas.find_one({'artist':username})
    if not already_uploaded( username, filename):
        #replace with better code.
        new_song_list = cursor['songs'][:]
        new_song_list.append(filename)
        #print(new_song_list)
        db.ugas.update_one(
            {'artist':username},
            {'$set':{ "songs": new_song_list }}
        )
        print('\'%s\' just dropped a new single \'%s\'' % (username, filename))
        cursor = db.ugas.find_one({'artist':username})
        #print(cursor['songs'])
        return True
    print('Oops! Looks like \'%s\' has already uploaded \'%s\'' % (username, filename))    
    return False
# These two functions can be combined into one....
def new_squad_mem( artist, fan):
    new_squad = []
    cursor = db.ugas.find_one({'artist':artist})
    if not in_squad( artist, fan):
        #replace with better code.
        new_squad = cursor['squad'][:]
        new_squad.append(fan)
        db.ugas.update(
            {'artist':artist},
            {'$set':{ "squad": new_squad }}
        )
        print('\'%s\' welcomes \'%s\' to their squad!' % (artist, fan))
        return True
    print('\'%s\' already has \'%s\' in their squad!' % (artist, fan))    
    return False

def rmv_squad_mem(artist, fan):
    new_squad = []
    cursor = db.ugas.find_one({'artist':artist})
    if in_squad( artist, fan):
        #replace with better code.
        new_squad = cursor['squad'][:]
        new_squad.remove(fan)
        db.ugas.update(
            {'artist':artist},
            {'$set':{ "squad": new_squad }}
        )
        print('\'%s\' drops \'%s\' from their squad!' % (artist, fan))
        return True
    print('\'%s\' can\'t drop non-member \'%s\' from their squad!' % (artist, fan))
    return False

def in_squad(artist, fan): # can use this in conjunction with squad_add and squad_rmv
    cursor = db.ugas.find_one({'artist' : artist})
    if fan in cursor['squad']:
        return True
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


'''
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
    # Then we need to give Boyz II Men credit for their contribution to
    # the hit "One Sweet Day".

    query = {'artist': 'jacko'}

    ugas.update(query, {'$set': {'songs': ['Das da wrong melody']}})

    # Finally we run a query which returns all the hits that spent 10 or
    # more weeks at number 1.
    # gte is "greater than or equal to"
    cursor = ugas.find({})

    for doc in cursor:
        print ('%s has songs: %s and %s are the people that can listen to these songs' %
               (doc['artist'], doc['songs'], doc['squad']))
    
    ### Since this is an example, we'll clean up after ourselves.

    #db.drop_collection('ugas')
    valid_login('jacko','malboy')
    valid_login('sierrius', 'white')
    valid_login('rondell', 'weasley')
    ### Only close the connection when your app is terminating

    new_song('jacko','myspaghet')
    new_song('jacko','myspaghet')
    rmv_squad_mem('sierrius', 'jacko')
    new_squad_mem('sierrius', 'jacko')


    cursor = ugas.find({})

    for doc in cursor:
        print ('%s has songs: %s and %s are the people that can listen to these songs' %
               (doc['artist'], doc['songs'], doc['squad']))    

    client.close()


if __name__ == '__main__':
    main(sys.argv[1:])
'''
