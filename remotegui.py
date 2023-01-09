from PyQt5 import QtWidgets, uic, QtGui
from cryptography.fernet import Fernet
import base64
import json
import os
import pyotp
import pyperclip
import sys

# Translate asset paths to useable format for PyInstaller
def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)
  

# Set Global Variables
global enc_key
global remote_dict

# Load GUI Infomation
app = QtWidgets.QApplication([])
gui = uic.loadUi(resource_path("remote.ui"))
gui.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))



def GUI_settings(): # Set GUI Display 
    enc_key=''
    gui.setGeometry(10,60,409,300)
    gui.Frm_Password.setGeometry(10, 60, 391, 171)
    gui.Frm_PasswordEnc.setGeometry(10, 60, 391, 141)
    gui.Frm_Password.hide()
    gui.Frm_PasswordEnc.hide()
    gui.Frm_Main.hide()
    if os.path.exists('remote.enc'):
        gui.Frm_PasswordEnc.show()
    else:
        check()

        
def check():
    global enc_key
    enc_key=''
    change_encryption()

    
        



def change_password(): # GUI Button Action
    gui.lbl_SecretCode.show()
    gui.lineEdit_SecretCode.show()
    if os.path.exists('remote.enc'):
        gui.lbl_SecretCode.hide()
        gui.lineEdit_SecretCode.hide()
    gui.Lbl_Info.setText('')
    gui.Frm_Password.show()
    gui.Frm_Main.hide()
    gui.lbl_Password.setText('New Password')
    gui.lbl_Password2.setText('ReEnter Password')

    
def change_encryption(): # GUI Button Action
    gui.lbl_SecretCode.hide()
    gui.lineEdit_SecretCode.hide()
    gui.Lbl_Info.setText('')
    gui.Frm_Password.show()
    gui.Frm_Main.hide()
    gui.lbl_Password.setText('New Encryption PW')
    gui.lbl_Password2.setText('ReEnter Encryption PW')

    
def cancel(): # GUI Button Action
    gui.Frm_Password.hide()
    gui.Frm_Main.show()
    
def ok(): # GUI Button Action
    global enc_key
    global remote_dict
    gui.Lbl_Info.setText('')
    if gui.lineEdit_Password1.text() == gui.lineEdit_Password2.text():
        gui.Frm_Password.hide()
        gui.Frm_Main.show()
        gui.Lbl_Info.setText("Password Changed")
        if gui.lbl_Password.text() == 'Enter Encryption PW' or gui.lbl_Password.text() == 'New Encryption PW':
            enc_pass = gui.lineEdit_Password1.text()
            Generate_Encryption_Key(enc_pass)
        if not os.path.exists('remote.enc'):
            remote_dict={}
            remote_dict['secret_code']=gui.lineEdit_SecretCode.text()
            remote_dict['password']=gui.lineEdit_Password1.text()
            
        print(remote_dict)
        print(enc_key)
        if not remote_dict.get('secret_code','') =='' and not remote_dict.get('password','') == '':
            Encrypt_Data(remote_dict)
        else:
            gui.lineEdit_Password1.setText('')
            gui.lineEdit_Password2.setText('')
            if not os.path.exists('remote.enc'):
                change_password()
        if gui.lbl_Password.text() == 'New Password':
            remote_dict['password']=gui.lineEdit_Password1.text()
            gui.lineEdit_Password1.setText('')
            gui.lineEdit_Password2.setText('')
    else:
        gui.Lbl_Info.setText("Passwords Don't Match")
    
    
def ok_enc(): # GUI Button Action
    gui.Frm_PasswordEnc.hide()
    gui.Frm_Password.hide()
    enc_pass = gui.lineEdit_PasswordEnc.text()
    Generate_Encryption_Key(enc_pass)
    gui.Frm_Main.show()
    gui.Lbl_Info.setText('Encryption Key Created')
    Decode_File()
    
    #print(gui.lineEdit_PasswordEnc.text())
    
def Checkbox_Show(totp_now):
    if gui.Chk_ShowPassword.isChecked() == True:
        gui.Lbl_Info.setText(remote_dict.get('password','')+totp_now)
    else:
        gui.Lbl_Info.setText('******'+totp_now+ ' - Ready To Paste')
    
    
def code(): # GUI Button Action
    gui.Lbl_Info.setText('Code Generated')
    totp = pyotp.TOTP(remote_dict.get('secret_code',''))
    totp_now = totp.now()
    print("Current OTP:", totp_now)
    Checkbox_Show(totp_now)  
    #gui.Lbl_Info.setText('*******'+totp_now+ ' - Ready To Paste')
    password = remote_dict.get('password','')+ totp_now
    pyperclip.copy(password)
    print('Ready To Paste')
    
def exitprog(): # GUI Button Action
    exit()

# Load GUI Settings
GUI_settings()

# Initialise GUI Buttons
gui.Btn_Exit.clicked.connect(exitprog)
gui.Btn_ChangePassword.clicked.connect(change_password)
gui.Btn_ChangeEncryptionPassword.clicked.connect(change_encryption)
gui.Btn_Cancel.clicked.connect(cancel)
gui.Btn_Ok.clicked.connect(ok)
gui.Btn_OkEnc.clicked.connect(ok_enc)
gui.Btn_CreateCode.clicked.connect(code)
gui.Btn_ExitEnc.clicked.connect(exitprog)

def Generate_Encryption_Key(enc_pass): # Create Encryption Key For Encryption Password
    global enc_key
    enc_key = enc_pass
    #ENTER ENCRYPTION KEY
    for cnt in range(45):
        enc_key=enc_key+enc_key
        if len(enc_key) >= 45:
            break
    enc_key = base64.b64encode(bytes(enc_key, "utf-8") )
    enc_key=enc_key[-45:]
    #print()
    #print('ENCRYPTION KEY CREATED')
    #print()
    #print(enc_key)
    
def Decode_File(): # Decode remote.enc File
    #DECODE FILE
    global remote_dict
    #print('READING FILE')

    with open('remote.enc','rb') as file:
        encrypted = file.read()
        

    #THIS DECRYPTS THE DATA READ FROM YOUR JSON AND STORES IT'
    #print('DECRYPTING FILE')
    try:
        fernet = Fernet(enc_key)
        remote_dict=fernet.decrypt(encrypted)
        remote_dict = json.loads(remote_dict)
        
        return (remote_dict)
    except:
        gui.Lbl_Info.setText('Invalid Encryption Key')
        gui.lineEdit_PasswordEnc.setText('')
        GUI_settings()

def Encrypt_Data(remote_dict): # Encrypt Data When Encryption Password Changes Or New File
    #ENCRYPT DATA
    #print()
    gui.Lbl_Info.setText('Encrypting Data')
    jsons=json.dumps(remote_dict)
    remote_dict = jsons.encode()
    #THIS ENCRYPTS THE DATA READ FROM YOUR JSON AND STORES IT IN 'ENCRYPTED'
    fernet = Fernet(enc_key)
    encrypted=fernet.encrypt(remote_dict)

    #THIS WRITES YOUR NEW, ENCRYPTED DATA INTO A NEW JSON FILE
    gui.Lbl_Info.setText('Writing Data To File')
    with open('remote.enc','wb') as f:
        f.write(encrypted)

def check_file(): # Check If remote.enc File Exist If Not Create 
    if not os.path.exists('remote.enc'):
        remote_dict={}
        change_password()
        remote_dict['secret_code']=input('Input Secret Code:- ')
        remote_dict['password']=getpass.getpass('Input Remote Password:- ')
        Encrypt_Data(remote_dict)
        

# Display GUI
gui.show()
app.exec()