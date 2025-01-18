import random
import time
from django.core.cache import cache

# Manual management of OTP with expiration
otp_expiry = {}  # Dictionary to store OTP expiry times

def send_otp_to_mobile(mobile_num, user_obj):
    current_time = time.time()  # Get the current time

    # Check if OTP exists and if it's still valid
    if mobile_num in otp_expiry and otp_expiry[mobile_num] > current_time:
        remaining_time = int(otp_expiry[mobile_num] - current_time)
        return False, remaining_time

    try:
        otp_to_send = random.randint(1000, 9999)
        cache.set(mobile_num, otp_to_send, timeout=60)  # Cache OTP for 60 seconds
        otp_expiry[mobile_num] = current_time + 60  # Set expiry time
        # Create Instance
        user_obj.otp = otp_to_send 
        user_obj.save()
        return True, 0  

    except Exception as e:
        print(e)
        # Handle errors gracefully
        return False, 0 