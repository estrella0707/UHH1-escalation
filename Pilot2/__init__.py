from otree.api import *
import itertools
import random

doc = """
Pilot2 on simplicity and policy preference (vignette) Escalation
"""

# FUNCTION
def creating_session(subsession):
    # Treatment randomization
    initial = itertools.cycle(['complex', 'simple'])
    for player in subsession.get_players():
        player.initial = next(initial)

def cq_bg_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_bg_choices' not in player.participant.vars:
        choices = ['Too much rain is flooding their fields.',
                   'The soil is becoming too acidic, and alien creatures have appeared.',
                   'Robots are taking over farming jobs.',
                   'Crops are growing too fast and causing food waste.']
        random.shuffle(choices)
        player.participant.vars['cq_bg_choices'] = choices
    return player.participant.vars['cq_bg_choices']

def cq_wv_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_wv_choices' not in player.participant.vars:
        choices = ['A rise in solar radiation which affects atmospheric chemistry.',
                   'The acidic waste produced by alien creatures.',
                   'A newly introduced agricultural method.',
                   'The inaction of the government.']
        random.shuffle(choices)
        player.participant.vars['cq_wv_choices'] = choices
    return player.participant.vars['cq_wv_choices']

def cq_bg_error_message(player, value):
    if value != 'The soil is becoming too acidic, and alien creatures have appeared.':
        return "This is not the correct answer. Please read and select again."

def cq_wv_error_message(player, value):
    if player.initial == 'complex':
        if value != "A rise in solar radiation which affects atmospheric chemistry.":
            return "This is not the correct answer. Please read and select again."
    if player.initial == 'simple':
        if value != "The acidic waste produced by alien creatures.":
            return "This is not the correct answer. Please read and select again."

def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, '']],
        label=label,
        widget=widgets.RadioSelect)


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment assignment
    initial = models.StringField()

    # Comprehension check question
    cq_bg = models.StringField(
        label='What changes are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
    )
    cq_wv = models.StringField(
        label='According to the initiative leaflet, what is causing soil acidification on Planet X?',
        widget=widgets.RadioSelect,
    )

    # Manipulation check question
    mq1 = models.IntegerField(choices=range(1, 8))
    mq2 = models.IntegerField(choices=range(1, 8))
    mq3 = models.IntegerField(choices=range(1, 8))
    mq4 = models.IntegerField(choices=range(1, 8))
    mq5 = models.IntegerField(choices=range(1, 8))

    # Engagement check question
    eq = models.IntegerField(choices=range(1, 8))

    # Pretest intention check question
    associate = models.BooleanField()
    associate_des = models.LongStringField(blank=True)
    associate_inf = models.BooleanField(blank=True)

    # Choice
    vote1 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch'],
        initial=''
    )
    confidence1 = models.IntegerField(choices=range(1, 8))
    vote2 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch'],
        initial=''
    )
    confidence2 = models.IntegerField(choices=range(1, 8))
    vote3 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch'],
        initial=''
    )
    confidence3 = models.IntegerField(choices=range(1, 8))

    # Demographic variables
    age = models.IntegerField(
        label='Enter your age. (Please leave this blank if you prefer not to say.)',
        blank=True
    )
    gender = models.StringField(
        widget=widgets.RadioSelect,
        label='Identify your gender',
        choices=['Male', 'Female', 'Non-binary', 'Prefer not to say']
    )
    education = models.StringField(
        widget=widgets.RadioSelect,
        label='Enter your highest education level',
        choices=['No formal education', 'Primary school', 'Secondary school',
                 'University', 'Postgraduate', 'Prefer not to say']
    )
    stand = models.IntegerField(choices=range(1, 8))
    party = models.StringField(
        widget=widgets.RadioSelect,
        label='Which political party do you most closely identify with or support?',
        choices=['Democratic Party', 'Republican Party', 'Other (please describe if you wish)',
                 'I do not support any party', 'Prefer not to say']
    )
    party_other = models.StringField(
        label="Please describe if you wish",
        blank=True,
    )
    # Individual difference variables
    intuition1 = models.IntegerField(
        label='A bat and a ball together cost $110. The bat costs $100 more than the ball. '
              'How much does the ball cost?',
    )
    intuition2 = models.IntegerField(
        label='If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 '
              'machines to make 100 widgets?',
    )
    intuition3 = models.IntegerField(
        label='In a lake, there is a patch of lily pads. Every day, the patch doubles in size. '
              'If it takes 48 days for the patch to cover the entire lake, how many days will '
              'it take for the patch to cover half of the lake?',
    )
    patience = models.IntegerField(choices=range(1, 8))
    scientist = models.IntegerField(choices=range(1, 8))
    religiosity = models.IntegerField(choices=range(1, 8))
    frustration1 = likert1('If my first attempt to solve a problem fails, I keep trying until I succeed.')
    frustration2 = likert1('I am willing to listen and consider alternatives for handling a problem.')
    ethic_new = likert1('It is important to try new and different things in life.')
    ethic_nature = likert1('It is important to care for nature and environment.')
    ethic_secure = likert1('It is important to live in secure and safe surroundings.')
    ethic_creative = likert1('It is important to think new ideas and being creative.')
    ethic_equality = likert1('It is important that people are treated equally and have equal opportunities.')
    ethic_help = likert1('It is important to help people and care for others well-being.')
    scifi = likert1('I enjoy reading science-fiction novels.')


# PAGES
class Introduction(Page):
    pass


class Background(Page):
    pass


class Q1(Page):
    form_model = 'player'
    form_fields = ['cq_bg']


class C0(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'complex'


class S0(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'simple'


class Q2(Page):
    form_model = 'player'
    form_fields = ['cq_wv']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'Pilot2/Slide1.JPG',
            'simple': 'Pilot2/Slide5.JPG',
        }
        return {
            'picture': pictures.get(player.initial)
        }


class Q3(Page):
    form_model = 'player'
    form_fields = ['mq1', 'mq2', 'mq3', 'mq4', 'mq5']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'Pilot2/Slide1.JPG',
            'simple': 'Pilot2/Slide5.JPG',
        }
        return {
            'picture': pictures.get(player.initial),
            'show_first_table_first': random.choice([True, False])
        }


class R0(Page):
    form_model = 'player'


class C1(Page):
    form_model = 'player'
    form_fields = ['vote1', 'confidence1']

    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'complex'


class S1(Page):
    form_model = 'player'
    form_fields = ['vote1', 'confidence1']

    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'simple'


class R1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote1 == 'stick'


class C2(Page):
    form_model = 'player'
    form_fields = ['vote2', 'confidence2']

    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'complex' and player.vote1 == 'stick'


class S2(Page):
    form_model = 'player'
    form_fields = ['vote2', 'confidence2']

    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'simple' and player.vote1 == 'stick'


class R2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote2 == 'stick'


class C3(Page):
    form_model = 'player'
    form_fields = ['vote3', 'confidence3']

    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'complex' and player.vote2 == 'stick'


class S3(Page):
    form_model = 'player'
    form_fields = ['vote3', 'confidence3']

    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'simple' and player.vote2 == 'stick'


class R3(Page):
    pass


class Q4(Page):
    form_model = 'player'
    form_fields = ['eq', 'associate', 'associate_des', 'associate_inf']


class Demographics1(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'stand',
                   'party', 'party_other',
                   'intuition1', 'intuition2', 'intuition3',
                   'patience', 'scientist', 'religiosity']


class Demographics2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['frustration1', 'frustration2',
                   'ethic_new', 'ethic_nature', 'ethic_secure',
                   'ethic_creative', 'ethic_equality', 'ethic_help', 'scifi']
        random.shuffle(survey)
        return survey


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction,
    Background,
    Q1,
    C0, S0,
    Q2,
    Q3,
    R0,
    C1, S1, R1,
    C2, S2, R2,
    C3, S3, R3,
    Q4,
    Demographics1,
    Demographics2,
    ProlificCompletion
]