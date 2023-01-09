import pyotp
import pyperclip
import time
from pwinput import pwinput

# optional hardcode of input password
#globalpassword = pwinput(prompt='Enter Global Password:- ', mask='*')
globalpassword = '9s4rXzM!EJp6'


#totp = pyotp.TOTP('AB6TJEFFPNSCS6J5IJYZWZZDOI')
totp = pyotp.TOTP('ADQOBWBBWUXZGQ6BSQTHMSRGL22PWRPNFTAZXSKHLVIR3BRVGVMA')
print("Current OTP:", totp.now())
password = globalpassword+ totp.now()
pyperclip.copy(password)
print('Ready To Paste')
print()
print()
print()
print()
print()
print()
print()
print()
print()
print('                   ',password)
time.sleep(300)
