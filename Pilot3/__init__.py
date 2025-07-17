from otree.api import *
import itertools
import random

doc = """
Pilot 3 Solution"""


# Function
def creating_session(subsession):
    #Treatment randomization
    initial = itertools.cycle(['clsl',  # Complex Long-term, Simple Long-term
                               'csss',  # Complex Short-term, Simple Short-term
                               'clss',  # Complex Long-term, Simple Short-term
                               'cssl'])  # Complex Short-term, Simple Long-term
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

# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt3'
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

# Engagement check question
    eq = models.IntegerField(choices=range(1, 8))

# Pretest intention check question
    associate = models.BooleanField()
    associate_des = models.LongStringField(blank=True)
    associate_inf = models.BooleanField(blank=True)

 # Choice
    vote_clsl = models.StringField(
        widget=widgets.RadioSelect,
        choices=['cl', 'sl'],
        initial=''
    )
    confidence_clsl = models.IntegerField(choices=range(1, 8))
    vote_csss = models.StringField(
        widget=widgets.RadioSelect,
        choices=['cs', 'ss'],
        initial=''
    )
    confidence_csss = models.IntegerField(choices=range(1, 8))
    vote_clss = models.StringField(
        widget=widgets.RadioSelect,
        choices=['cl', 'ss'],
        initial=''
    )
    confidence_clss = models.IntegerField(choices=range(1, 8))
    vote_cssl = models.StringField(
        widget=widgets.RadioSelect,
        choices=['cs', 'sl'],
        initial=''
    )
    confidence_cssl = models.IntegerField(choices=range(1, 8))

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
    intuition1 = models.IntegerField(
        label='A bat and a ball together cost $110. The bat costs $100 more than the ball. '
              'How much does the ball cost? (Please enter an integer only)',
    )
    intuition2 = models.IntegerField(
        label='If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 '
              'machines to make 100 widgets? (Please enter an integer only)',
    )
    intuition3 = models.IntegerField(
        label='In a lake, there is a patch of lily pads. Every day, the patch doubles in size. '
              'If it takes 48 days for the patch to cover the entire lake, how many days will '
              'it take for the patch to cover half of the lake? (Please enter an integer only)',
    )
    populism1 = models.IntegerField(choices=range(1, 8))
    populism2 = models.IntegerField(choices=range(1, 8))
    source = models.StringField(
        widget=widgets.RadioSelect,
        label='Where do you primarily get your political news?',
        choices=['Social media', 'Traditional media (e.g., BBC, Fox, CNN)',
                 'Newspapers / magazines', 'Other (please describe if you wish)']
    )
    source_other = models.StringField(
        label="Please describe if you wish",
        blank=True,
    )


# PAGES
class Introduction(Page):
    pass


class Background(Page):
    pass


class Q1(Page):
    form_model = 'player'
    form_fields = ['cq_bg']


class CLSL(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'clsl'

    form_model = 'player'
    form_fields = ['vote_clsl', 'confidence_clsl']


class CSSS(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'csss'

    form_model = 'player'
    form_fields = ['vote_csss', 'confidence_csss']


class CLSS(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'clss'

    form_model = 'player'
    form_fields = ['vote_clss', 'confidence_clss']


class CSSL(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.initial == 'cssl'

    form_model = 'player'
    form_fields = ['vote_cssl', 'confidence_cssl']


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'stand',
                   'party', 'party_other',
                   'intuition1', 'intuition2', 'intuition3',
                   'populism1', 'populism2',
                   'source', 'source_other']


class ProlificCompletion(Page):
    pass

page_sequence = [
    Introduction,
    Background,
    Q1,
    CLSL,
    CSSS,
    CLSS,
    CSSL,
    Demographics,
    ProlificCompletion
]