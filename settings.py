from os import environ


SESSION_CONFIGS = [
    dict(
        name='EX',
        display_name="Pilot3EX",
        app_sequence=['EX'],
        num_demo_participants=20,
    ),
    dict(
        name='EN',
        display_name="Pilot3EN",
        app_sequence=['EN'],
        num_demo_participants=20,
    )
]


SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=0.00)
PARTICIPANT_FIELDS = ['task_rounds']
SESSION_FIELDS = []
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3080418250966'

INSTALLED_APPS = ['otree']