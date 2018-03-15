# For Google Drive API calls.

from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from apiclient import errors

from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = './credentials/client_secret.json'
APPLICATION_NAME = 'Safe Sound'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = os.path.join('./', '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'client_secret.json')
    print("Checking credentials...")
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("creating new credentials")
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

##### credentials check run globally #####

DL_PATH = "./dlmusic/"
UL_PATH = "./ulmusic/"
#UL_FOLDER = "1sd_Xt-sgMO6uNz8janaTco078D8H20ZP"

### WHEN FINALIZED, WILL NEED TO MOVE TO DIFFERENT DRIVE ACCOUNT AND TAKE OUT THE PARENT CHECKS. ###

def delete_file(drv_service, file_id):
    try:
        drv_service.files().delete(fileId=file_id).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    return

def download(song_name, dl_path):
    # literally download the file into the directories parents
    #file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
    print("======================= DOWNLOAD ===========================")
    file_id = ''
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        #print('Files:')
        for item in items:
            #print('{0} ({1})'.format(item['name'], item['id']))
            if item['name'] == song_name:
                file_id = item['id']
                break

    print("File we are trying to download: %s || %s"%(song_name,file_id))
    request = service.files().get_media(fileId=file_id)

    text = '.txt'
    mp3 = '.mp3'
    file_name = song_name + mp3#text
    
    dl = 'dlc'
    handle = DL_PATH + dl + file_name
    fh = io.FileIO(handle,"wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bDownload progress             : %d%%." % int(status.progress() * 100), end='')

    results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('\nFiles after download completed:')
        for item in items:
            try:
                if UL_FOLDER in item['parents']:
                    print('{0:24} || {1}'.format(item['id'],item['name']))
            except KeyError:
                continue
    print()
    return

def upload(song_name, file_name_path):
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    print("======================== UPLOAD ============================")
    print("New upload. Looking for duplicates...")
    file_metadata = {'name': song_name,
                    'parents':[UL_FOLDER]
    }
    results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            #print('{0} ({1})'.format(item['name'], item['id']))
            if item['name'] == song_name:
                print("Deleting old duplicate '%s' with ID: %s" % (item['name'], item['id']))
                delete_file(service,item['id'])
    # may need to add a variable that is the path to the file. ##
    #media = MediaFileUpload('music/ConspiracyTheory.mp3', mimetype='audio/mpeg')
    print("Uploading new: '%s' "%song_name)
    media = MediaFileUpload(file_name_path, mimetype='audio/mpeg')#text/plain')
    
    file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    print('Done.')

    
    results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files after upload:')
        for item in items:
            try:
                if UL_FOLDER in item['parents']:
                    print('{0:24} || {1}'.format(item['id'],item['name']))
            except KeyError:
                continue
    print()
    return


#### USE MAIN FOR TESTING, PLEASE ####
def main(): 
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Songs in the bank:')
        for item in items:
            try:
                if UL_FOLDER in item['parents']:
                    print('{0:24} || {1}'.format(item['id'],item['name']))
            except KeyError:
                continue
    # upload('test_song2','ulmusic/test_song.txt')
    # upload('ConspiracyTheory','ulmusic/ConspiracyTheory.mp3')
    # download('ConspiracyTheory', DL_PATH)
    return

if __name__ == '__main__':
    main()