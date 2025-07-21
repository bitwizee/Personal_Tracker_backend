import secrets
import string





class OTPService:


    @staticmethod
    def _generate_otp(length: int = 6):
        digits = string.digits
        return ''.join(secrets.choice(digits) for _ in range(length))