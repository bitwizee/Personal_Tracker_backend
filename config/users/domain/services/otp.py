import secrets
import string
from django.db import transaction
from ...models import OTP, Customer
from ..selector.customer import CustomerSelector
from django.utils import timezone
from datetime import timedelta

class OTPService:


    @staticmethod
    def _generate_otp(length: int = 6):
        digits = string.digits
        return ''.join(secrets.choice(digits) for _ in range(length))
    


    @staticmethod
    @transaction.atomic
    def _store_otp_in_db(*, otp_code: str, eamil: str) -> tuple[Customer, OTP]:
        customer, craeted = CustomerSelector.get_or_create(email=eamil)
        OTP.objects.filter(
            customer=customer, is_expired=False
        ).update(
            is_expired=True, expired_at = timezone.now()
        )
        otp = OTP.objects.create(
            customer=customer,
            otp=otp_code,
            expired_at = timezone.now() + timedelta(minutes=5)
        )
        return customer, otp