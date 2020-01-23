"""
Django Signal related functionality for user_api accounts
"""

from django.dispatch import Signal

# Signal to retire a user from LMS-initiated mailings (course mailings, etc)
USER_RETIRE_MAILINGS = Signal(providing_args=["user"])

# Signal to retire LMS critical information
USER_RETIRE_LMS_CRITICAL = Signal(providing_args=["user"])

# Signal to retire LMS misc information
USER_RETIRE_LMS_MISC = Signal(providing_args=["user"])

# Signal to send email to user when certificate is downloadable
USER_CERTIFICATE_DOWNLOADABLE = Signal(
    providing_args=['first_name', 'display_name', 'certificate_reverse_url', 'user_email'])
