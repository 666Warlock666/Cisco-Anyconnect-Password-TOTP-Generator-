from cryptography.fernet import Fernet
import base64
import getpass
import json
import os

#NOT USED CONTAINS FUNCTION FOR EACH EVENT

def Encrypt_Data(remote_dict):
    #TEST_PRINT()
    #ENCRYPT DATA
    print()
    print('ENCRYPTING DATA')
    jsons=json.dumps(remote_dict)
    remote_dict = jsons.encode()
    #THIS ENCRYPTS THE DATA READ FROM YOUR JSON AND STORES IT IN 'ENCRYPTED'
    fernet = Fernet(enc_key)
    encrypted=fernet.encrypt(remote_dict)

    #THIS WRITES YOUR NEW, ENCRYPTED DATA INTO A NEW JSON FILE
    print('WRITING DATA TO FILE')
    with open('remote.json','wb') as f:
        f.write(encrypted)
        
def Generate_Encryption_Key():
    
    #ENTER ENCRYPTION KEY
    enc_key='passwordcheck1'
    passwd='passwordcheck2'
    if os.path.exists('remote.json'):
        enc_key = getpass.getpass('Encryption Key:- ')
    else:
        while not enc_key == passwd:
            
            enc_key = getpass.getpass('Enter New Encryption Key:- ')
            if enc_key =='':
                enc_key='passwordcheck1'
            passwd = getpass.getpass('Re-enter New Encryption Key:- ')
            print()

    for cnt in range(45):
        enc_key=enc_key+enc_key
        if len(enc_key) >= 45:
            
            break
    enc_key = base64.b64encode(bytes(enc_key, "utf-8") )
    enc_key=enc_key[-45:]
    print()
    print('ENCRYPTION KEY CREATED')
    print()
    print(enc_key)
    return(enc_key)

def check_file():
    if not os.path.exists('remote.json'):
        remote_dict={}
        remote_dict['secret_code']=input('Input Secret Code:- ')
        remote_dict['password']=getpass.getpass('Input Remote Password:- ')
        Encrypt_Data(remote_dict)
        return(remote_dict)
    
def change_password(remote_dict):
    print(remote_dict)
    remote_dict['password']=getpass.getpass('Input Remote Password:- ')
    Encrypt_Data(remote_dict)
    return(remote_dict)

def Decode_File():
    #DECODE FILE
    print('READING FILE')

    with open('remote.json','rb') as file:
        encrypted = file.read()
        print(encrypted)

    #THIS DECRYPTS THE DATA READ FROM YOUR JSON AND STORES IT'
    print('DECRYPTING FILE')
    try:
        fernet = Fernet(enc_key)
        remote_dict=fernet.decrypt(encrypted)
        remote_dict = json.loads(remote_dict)
        return (remote_dict)
    except:
        print('INVALID ENCRYPTION KEY')
        exit()
        
remote_dict=check_file() 
enc_key=Generate_Encryption_Key()
remote_dict=Decode_File()
    
print(remote_dict.get('secret_code',''))
print(remote_dict.get('password',''))

