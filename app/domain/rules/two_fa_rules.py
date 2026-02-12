import pyotp


class TwoFaRules:

    @staticmethod
    def generate_totp(two_fa_secret: str) -> pyotp.TOTP:
        return pyotp.TOTP(two_fa_secret)
