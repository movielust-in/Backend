from .emails.Password_Reset import (
    Password_Reset_Template,
)
from .emails.Verify_Email import (
    Email_Verify_Template,
)


class EmailTemplates:
    Password_Reset = Password_Reset_Template
    Email_Verify = Email_Verify_Template
