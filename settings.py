from os import environ


SESSION_CONFIGS = [
    dict(
        name='experiment',
        display_name="4 conditions rotation",
        app_sequence=['Dispatcher', 'EN', 'EN_plant', 'EX', 'EX_plant', 'Survey'],
        num_demo_participants=20,
    ),
    dict(
        name='experiment1',
        display_name="endogenous",
        app_sequence=['EN'],
        num_demo_participants=20,
    ),
    dict(
        name='experiment2',
        display_name="endogenous plant",
        app_sequence=['EN_plant'],
        num_demo_participants=20,
    ),
    dict(
        name='experiment3',
        display_name="exogenous",
        app_sequence=['EX'],
        num_demo_participants=20,
    ),
    dict(
        name='experiment4',
        display_name="exogenous plant",
        app_sequence=['EX_plant'],
        num_demo_participants=20,
    ),
    dict(
        name='experiment_survey',
        display_name="survey",
        app_sequence=['Survey'],
        num_demo_participants=20,
    )
]


SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=0.00)
PARTICIPANT_FIELDS = ['task_rounds']
SESSION_FIELDS = ['branch']
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