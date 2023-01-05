# Remote Password+Code Generator

When logging on to Cisco AnyConnect (Homeworker-UK) this requires a your global password and Time-based one-time password combined.
i.e. Pa55W0rd1234567

This program allows a  user to safely store there password and secret code in a small encrypted file that can be unlocked by a users separate password.
(NOTE:- At no time does this encrypted file get decrypted to be able to view human friendly contents)

## Python Install

### Requirements
* cryptography==38.0.3
* pwinput==1.0.2
* pyotp==2.7.0
* pyperclip==1.8.2
* PyQt5==5.15.7
* pyinstaller==5.7.0

``` pip install -r requirements.txt ```

pyinstaller is required to create an executable file (optional)

``` pyinstaller -i 'icon.ico' --onefile --noconsole --add-data 'remote.ui;.' --add-data 'icon.ico;.' .\remotegui.py ```



## Setup
In order to be able to use this the user must know there secret code (usually supplied by IT) ie AB1CDEFGPNSTS4L6IJZZWSSXPH
The user also need to know there global password ie NEC Microsoft password.

When the user first logs on the user is presented to provide an encryption key this just a password or pin that can be used by a user to unlock the encrypted file in future..  Once both passwords match and ok is pressed the used is then pressented to give secret code and global password.

this is then saved and encrypted once the user presses ok

## Usage

when the user loads the generator after setting up the user is asked for there encryption password/pin. If the password/pin provided the user can then taken to the main screen.

### The user has four options:-

- Create Code -  (this generates a code containing global password and TOTP code) this can be pasted directly into Cisco AnyConnect
* Change Password  - This allows the user to change the global Password stored in the encrypted file at anytime when required
* Change Encryption Password/pin - This allows the user to change the encription password at any time (Note there is no min length of password required)
* Exit - Exits Remote Password Generator

## Forgot encryption Password

if the user forgets there encryption password there is no recovery option available. Then user can delete the Remote.enc file and setup there secret code & password again

