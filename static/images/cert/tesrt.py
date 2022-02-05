import pyotp
import time
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret, interval=425.41)
otp = totp.now()
print(otp)
time.sleep(300)
print(totp.verify(otp))

