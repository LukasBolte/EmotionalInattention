from os import environ

SESSION_CONFIGS = [
        dict(
        name='question2',
        app_sequence=['question2'],
        num_demo_participants=8,
        dev_mode=False
    ),
    dict(
        name='question2_dev_mod',
        app_sequence=['question2'],
        num_demo_participants=8,
        dev_mode=True
    ),
    dict(
        name='pilot',
        app_sequence=['pilot'],
        num_demo_participants=2,
        dev_mode=False
    ),
        dict(
        name='pilot_dev_mod',
        app_sequence=['pilot'],
        num_demo_participants=2,
        dev_mode=True
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['treatment','domain','valence','high_payoff','part_payment','collaborative_job','random_row','question','wtp','experiment_sequence','sequence','mistakes','times','num_draws','bonus_payment','expected_bonus','feedback','demographics']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5047380031882'
