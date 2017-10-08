
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
#$folder_list , File-list
folder_list = []
file_list = []
service=None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.join("","");
    credential_dir = os.path.join(home_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def initiate():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    global service
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list().execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:

        for item in items:
            mime=item['mimeType']
            name=item['name']
            id=item['id']
            if mime=='application/vnd.google-apps.folder':
                #print('Name :{0} Id :({1}) Type :{2}'.format(name,id,"Folder"))
                folder_list.append((name,id))
            else:
                #print ('Name :{0} Id :({1}) Type :{2}'.format(name,id,"File"))
                file_list.append((name,id))

def show_folders() :
    print ("\nFolders:\n")
    for tuple in folder_list:
        print ('Folder :{0} : {1}'.format(tuple[0],tuple[1]))
def show_files() :
    print ("\nFiles:\n")
    for tuple in file_list:
        print ('File :{0} : {1}'.format(tuple[0],tuple[1]))



def create_file(name, mimeType, parents=[]):
    file_meta_data = dict()
    file_meta_data['name'] = name
    file_meta_data['mimeType'] = mimeType
    file_meta_data['parents'] = parents
    file = service.files().create(body=file_meta_data).execute()
    if file['name'] == name:
        print("File Successfully Created")
    else:
        print("Failed To Create File")
    return

#upload_file
def upload_file(local_file_name, mimeType, parents=[]):
    global service
    file_meta_data = dict()
    file_meta_data['name'] = local_file_name
    file_meta_data['mimeType'] = mimeType
    file_meta_data['parents'] = parents
    if os.path.exists(os.path.join('', local_file_name)):
        media = MediaFileUpload(local_file_name, mimeType)
        file = service.files().create(body=file_meta_data, media_body=media).execute()
        if file['name'] == local_file_name:
            print("File Successfully Created")
        else:
            print("Failed To Create File")

    else:
        print("File Doesn't Exist Upload Not Possible")
    return
#close the Upload


if __name__ == '__main__':
    initiate()
    show_files()
    show_folders()
    create_file('client_secret.json','*/*')
file_name = input("Enter File Name For uploading :")

if os.path.exists(os.path.join('', file_name)):
    file_mime_type = input("Enter File mimeType For uploading :")
    upload_file(file_name, mimeType=file_mime_type)

