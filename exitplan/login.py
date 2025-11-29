import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ShoonyaApi-py')))
from api_helper import ShoonyaApiPy
import time, datetime

import hashlib
import json
import pyotp

# User credentials and constants (based on your successful curl command and previous inputs)
userid = "FN166343"
password_raw = "rOnak123456@"  # Use the password as it appeared in the successful curl command
totp_secret = "42666P7R3IF4XBSTD63S672C6J55737O"
api_secret_for_appkey = "ffa516424eb8b0c2ae6543c7e3fcdeae" # API secret derived from the successful curl command's appkey
imei = "abc1234"
vendor_code = "FN166343_U"

def login():
    # 1. Generate current OTP
    totp = pyotp.TOTP(totp_secret)
    current_otp = totp.now()

    api = ShoonyaApiPy()
    ret = api.login(userid=userid, password=password_raw, twoFA=current_otp, vendor_code=vendor_code, api_secret=api_secret_for_appkey, imei=imei)

    if ret is not None and ret.get('stat') == 'Ok':
        print("Login Successful")
        # print(ret)
        return api
    else:
        print("Login Failed")
        print(ret)
        return None

if __name__ == "__main__":
    login()