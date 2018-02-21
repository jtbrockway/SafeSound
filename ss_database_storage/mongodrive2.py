import sys
import pymongo

### Create seed data

SEED_DATA = [
    {
        'artist': 'jacko',
        'songs': ['QuadraticFormula'],
        '#key': '',
        'squad': ['sierrius', 'rondell']
    },
    {
        'artist': 'sierrius',
        'songs': ['x=(-b+or-sqrt(b^2-4timesac))/2a'],
        '#key' : '',
        'squad': ['rondell', 'howwy']

    },
    {
        'artist': 'rondell',
        'songs': ['ConspiracyTheory'],
        '#key': '',
        'squad': ['howwy', 'jacko', 'sierrius']
    }
]

### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

uri = '' 

###############################################################################
# main
###############################################################################
client = pymongo.MongoClient(uri)

db = client.get_default_database() ## db as a global reference to the database

def valid_login(usern, passw):
    cursor = db.ugas.find('artist': usern)
    if cursor != None: ## Not sure if this is what it will be.
        if passw==cursor.next()['pass']:
            return True
    return False

def new_user(username):
    cursor = db.artist_list.find('uga': username)
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
    cursor = db.ugas.find('artist':username)
    if not already_uploaded( username, filename):
        #replace with better code.
        new_song_list = cursor.next()['songs'][:]
        new_song_list.append(filename)
        db.ugas.update(
            {'artist':username},
            {$set: { "songs": new_song_list }}
        )
        return True
    return False
# These two functions can be combined into one....
def new_squad_mem( artist, fan):
    new_squad = []
    cursor = db.ugas.find('artist':artist)
    if not in_squad( artist, fan):
        #replace with better code.
        new_squad = cursor.next()['squad'][:]
        new_squad.append(fan)
        db.ugas.update(
            {'artist':username},
            {$set: { "squad": new_squad }}
        )
        return True
    return False

def squad_mem_rmvd(artist, fan):
    new_squad = []
    cursor = db.ugas.find('artist':artist)
    if in_squad( artist, fan):
        #replace with better code.
        new_squad = cursor.next()['squad'][:]
        new_squad.remove(fan)
        db.ugas.update(
            {'artist':username},
            {$set: { "squad": new_squad }}
        )
        return True
    return False

def in_squad(artist, fan): # can use this in conjunction with squad_add and squad_rmv
    cursor = db.ugas.find('artist' : artist)
    if fan in cursor.next()['squad']:
        return True
    return False

### These are for when upload and download happen in smove.py

def already_uploaded(  username, song):
    cursor = db.ugas.find('artist':username)
    if song not in cursor.next()['songs']:
        return False
    return True

def already_downloaded(username, song):
    cursor = db.ugas.find('artist':username)
    if song not in cursor.next()['downloaded']:
        return True
    return True

def clear_ul_history(username):
    db.ugas.update(
        {'artist':username},
        {$set: { 'uploaded': [] }}
    )
    return

def clear_dl_history(username):
    db.ugas.update(
        {'artist':username},
        {$set: { 'downloaded': [] }}
    )
    return

def update_ul_history(username, song):
    cursor = db.ugas.find('artist':username)
    doc_array = cursor.toArray()
    if len(doc_array[0]['uploaded'])+1 > 10:
        clear_ul_history(username)
    new_uls = doc_array[0]['uploaded'][:]
    new_uls.append(song)
    db.ugas.update(
        {'artist':username},
        {$set: { "uploaded": new_uls }}
    )
    return

def update_dl_history(username):
    cursor = db.ugas.find('artist':username)
    doc_array = cursor.toArray()
    if len(cursor.next()['downloaded'])+1 > 20:
        clear_dl_history(username)
    new_dls = doc_array[0]['downloaded'][:]
    new_dls.append(song)
    db.ugas.update(
        {'artist':username},
        {$set: { "downloaded": new_dls }}
    )
    return



def main(args):

    
    
    # First we'll add a few songs. Nothing is required to create the songs 
    # collection; it is created automatically when we insert.
    
    db.drop_collection('ugas')
    ugas = db['ugas']

    # Note that the insert method can take either an array or a single dict.

    ugas.insert_many(SEED_DATA)

    # Then we need to give Boyz II Men credit for their contribution to
    # the hit "One Sweet Day".

    query = {'songs': ['QuadraticFormula']}

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

    ### Only close the connection when your app is terminating

    client.close()


if __name__ == '__main__':
    main(sys.argv[1:])