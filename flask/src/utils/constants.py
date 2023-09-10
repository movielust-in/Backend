import re


class Constants:
    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    SPECIAL_CHARS = re.compile(
        r"[@_!#$%^&*()<>?/\|}{~:]"
    )


OTP_TYPES = ["SIGNUP", "PASSWORDRESET"]
