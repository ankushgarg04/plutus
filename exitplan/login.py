import sys
import os
import pyotp
from config import USER_ID, PASSWORD, TOTP_SECRET, API_SECRET, IMEI, VENDOR_CODE
from utils.logger import setup_logger

# Add ShoonyaApi-py to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ShoonyaApi-py')))
from api_helper import ShoonyaApiPy
import time, datetime

import hashlib
import json

logger = setup_logger("login")

def login():
    logger.info("Initiating login process...")
    
    try:
        # 1. Generate current OTP
        totp = pyotp.TOTP(TOTP_SECRET)
        current_otp = totp.now()

        api = ShoonyaApiPy()
        ret = api.login(userid=USER_ID, password=PASSWORD, twoFA=current_otp, vendor_code=VENDOR_CODE, api_secret=API_SECRET, imei=IMEI)

        if ret is not None and ret.get('stat') == 'Ok':
            logger.info("Login Successful")
            return api
        else:
            logger.error(f"Login Failed: {ret}")
            return None
            
    except Exception as e:
        logger.critical(f"Login Exception: {e}")
        return None

if __name__ == "__main__":
    login()