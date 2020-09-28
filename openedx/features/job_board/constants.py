"""
Constants for Job Board app
"""

JOB_PARAM_QUERY_KEY = 'query'
JOB_PARAM_COUNTRY_KEY = 'country'
JOB_PARAM_CITY_KEY = 'city'
JOB_PARAM_TRUE_VALUE = '1'

JOB_TYPE_REMOTE_KEY = 'remote'
JOB_TYPE_ONSITE_KEY = 'onsite'

JOB_TYPE_CHOICES = (
    (JOB_TYPE_REMOTE_KEY, 'Remote'),
    (JOB_TYPE_ONSITE_KEY, 'Onsite'),
)

JOB_COMP_VOLUNTEER_KEY = 'volunteer'
JOB_COMP_HOURLY_KEY = 'hourly'
JOB_COMP_SALARIED_KEY = 'salaried'

JOB_COMPENSATION_CHOICES = (
    (JOB_COMP_VOLUNTEER_KEY, 'Volunteer'),
    (JOB_COMP_HOURLY_KEY, 'Hourly'),
    (JOB_COMP_SALARIED_KEY, 'Salaried (Yearly)'),
)

JOB_HOURS_FULLTIME_KEY = 'fulltime'
JOB_HOURS_PARTTIME_KEY = 'parttime'
JOB_HOURS_FREELANCE_KEY = 'freelance'

JOB_HOURS_CHOICES = (
    (JOB_HOURS_FULLTIME_KEY, 'Full Time'),
    (JOB_HOURS_PARTTIME_KEY, 'Part Time'),
    (JOB_HOURS_FREELANCE_KEY, 'Freelance'),
)

DJANGO_COUNTRIES_KEY_INDEX = 0
DJANGO_COUNTRIES_VALUE_INDEX = 1

# Logo image file max allowed file size in bytes
LOGO_IMAGE_MAX_SIZE = 2 * 1024 * 1024  # 2 MB
LOGO_ALLOWED_EXTENSION = ['jpg', 'png']
