
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import email_manager as emailManager


directorio_credenciales = 'credentials_module.json'

# Login in drive
def login():
    """ Login in Google Drive"""
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales


# search Drive files
def search():
    """ Search files in Google Drive"""
    result = []
    credenciales = login()
    lista_archivos = credenciales.ListFile().GetList()
    print('********* Archivos encontrados: *********')
    for f in lista_archivos:
        print('- ' + f['title'])
        is_public = False
        email_owner = ''
        metadata = f.GetPermissions()
        for data in metadata:
            if data.get('type') == 'anyone':
                is_public = True
            if data.get('role') == 'owner':
               email_owner = data.get('emailAddress')


        result.append({'file_name':f['title'],
                        'extension':f['fileExtension'],
                        'owner':email_owner,
                        'visibility':("Público" if is_public  else "Privado"),
                        'last_modified_date': f['modifiedDate'],
                        'permissions':metadata,
                        'embedLink':f['embedLink'],
                        'object':f})
    
    return result

def delete_permissions(file):
    """ Delete permissions of a file"""
    permissions = file.GetPermissions()
    email_owner = ''
    for data in permissions:
        if data.get('role') == 'owner':
            email_owner = data.get('emailAddress')
   
    for permission in permissions:
        if permission.get('type') == 'anyone':
            file.DeletePermission(permission['id'])
            emailManager.send_email( email_owner, 'Se establece estado privado para el sieguiente archivo archivo: ' + file['embedLink'])
            print('Se establece estado privado al archivo: ' + file['title'])

            

