from otree.api import *

doc = """
Pretest on simplicity and policy preference (vignette)
"""

# FUNCTION
def creating_session(subsession):
    # Treatment randomization
    import itertools
    task = itertools.cycle(['CWV_CP', 'CWV_SP', 'SWV_CP', 'SWV_SP',
                            'SWV_CP_culprit', 'SWV_SP_culprit'])
    for player in subsession.get_players():
        player.task = next(task)

def cq_wv_choices(player):
    import random
    # Shuffle choices
    choices = ['A rise in solar radiation which affects atmospheric chemistry.',
               'The acidic waste produced by the a creature called Tivarns.',
               'A newly introduced agricultural method.',
               'The inaction of the government.']
    random.shuffle(choices)
    return choices

def cq_p_choices(player):
    import random
    # Shuffle choices
    choices = ['Deploying a planet-wide atmospheric mist to filter radiation and stabilize the soil.',
               'Sterilizing cargo ships with a dual-mist system.',
               'Deploying a localized mist over agricultural regions to stabilize soil conditions.',
               'Implementing a robotic fleet and monitoring system to enforce ship sterilization.']
    random.shuffle(choices)
    return choices

def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
        label=label,
        widget=widgets.RadioSelect)


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment assignment
    task = models.StringField()

    # Comprehension check question
    cq_wv = models.StringField(
        label='According to the activists, what is causing soil acidification on Planet X?',
        widget=widgets.RadioSelect,
    )
    cq_p = models.StringField(
        label='According to the activists, how does the proposed policy address this issue?',
        widget=widgets.RadioSelect,
    )

    # Manipulation check question
    mq1 = likert1('world view simplicity')
    mq2 = likert1('fault')
    mq3 = likert1('policy simplicity')
    mq4 = likert1('immediate')
    mq5 = likert1('sustainable')

    # Engagement check question
    eq = likert1('member')

    # Reading time
    reading_time_bg = models.FloatField(blank=True)
    reading_time_wv = models.FloatField(blank=True)
    reading_time_p = models.FloatField(blank=True)

    # Pretest intention check question
    associate = models.BooleanField()
    associate_des = models.LongStringField(blank=True)
    associate_inf = models.BooleanField(blank=True)

    # Choice
    policy_choice = models.StringField(
        widget=widgets.RadioSelect,
        label='What is your opinion on this initiative in the referendum?',
        choices=['I am against it', 'I am in favor of it', 'I abstain']
    )
    policy_votes = likert1('votes')
    policy_confidence = likert1('confidence')

    # Demographic variables
    age = models.IntegerField(
        label='Please enter your age',
        blank=True
    )
    gender = models.StringField(
        widget=widgets.RadioSelect,
        label='Please identify your gender',
        choices=['Male', 'Female', 'Non-binary', 'Other (please describe if you wish)',
                 'Prefer not to say']
    )
    gender_other = models.StringField(
        label="Please describe if you wish",
        blank=True,
    )
    education = models.StringField(
        widget=widgets.RadioSelect,
        label='Please enter your highest education level',
        choices=['No formal education', 'Primary school', 'Secondary school',
                 'University', 'Postgraduate', 'Prefer not to say']
    )
    stand = models.StringField(
        widget=widgets.RadioSelect,
        label='On a scale of 1 to 7, where would you place yourself politically?',
        choices=['1 (Far Left)', '2 (Left)', '3 (Center-Left)', '4 (Central)',
                 '5 (Center-Right)', '6 (Right)', '7 (Far Right)']
    )
    party = models.StringField(
        widget=widgets.RadioSelect,
        label='Which political party do you most closely identify with or support?',
        choices=['Conservative Party', 'Labour Party', 'Other (please describe if you wish)',
                 'I do not support any party', 'Prefer not to say']
    )
    party_other = models.StringField(
        label="Please describe if you wish",
        blank=True,
    )
    intuition = models.StringField(
        widget=widgets.RadioSelect,
        label='Which type of policy explanations would you prefer?',
        choices=['Quick and intuitive', 'Detailed and analytical', 'Depends on the issue']
    )
    populism = models.StringField(
        widget=widgets.RadioSelect,
        label='Which statement do you agree with more?',
        choices=['Experts and academics should guide policy decisions.',
                 'Ordinary people’s common sense should guide policy decisions.',
                 'A mix of both is needed.']
    )
    fullread = models.StringField(
        widget=widgets.RadioSelect,
        label='How often do you read full policy proposals before forming an opinion?',
        choices=['Rarely or never', 'Occasionally', 'Frequently', 'Always']
    )
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
    factcheck = models.StringField(
        widget=widgets.RadioSelect,
        label='When you hear a new policy claim, how often do you fact-check it?',
        choices=['Rarely or never', 'Occasionally', 'Frequently', 'Always']
    )

# PAGES
class Introduction(Page):
    pass


class Background(Page):
    form_model = 'player'
    form_fields = ['reading_time_bg']


class CWV(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.task == "CWV_CP" or player.task == "CWV_SP")

    form_model = 'player'
    form_fields = ['cq_wv', 'reading_time_wv']


class SWV(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.task == "SWV_CP" or player.task == "SWV_SP")

    form_model = 'player'
    form_fields = ['cq_wv', 'reading_time_wv']


class SWVcul(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.task == "SWV_CP_culprit" or player.task == "SWV_SP_culprit")

    form_model = 'player'
    form_fields = ['cq_wv', 'reading_time_wv']


class Q1WV(Page):
    form_model = 'player'
    form_fields = ['mq1', 'mq2']


class CWVCP(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task == "CWV_CP"

    form_model = 'player'
    form_fields = ['cq_p', 'reading_time_p']


class SWVSP(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task == "SWV_SP"

    form_model = 'player'
    form_fields = ['cq_p', 'reading_time_p']


class SWVculSP(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task == "SWV_SP_culprit"

    form_model = 'player'
    form_fields = ['cq_p', 'reading_time_p']


class CWVSP(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task == "CWV_SP"

    form_model = 'player'
    form_fields = ['cq_p', 'reading_time_p']


class SWVCP(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task == "SWV_CP"

    form_model = 'player'
    form_fields = ['cq_p', 'reading_time_p']


class SWVculCP(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task == "SWV_CP_culprit"

    form_model = 'player'
    form_fields = ['cq_p', 'reading_time_p']


class Q2P(Page):
    form_model = 'player'
    form_fields = ['policy_choice', 'policy_votes', 'policy_confidence', 'eq']


class Q3P(Page):
    form_model = 'player'
    form_fields = ['mq3', 'mq4', 'mq5',
                   'associate', 'associate_des', 'associate_inf']


class Demographics(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    form_model = 'player'
    form_fields = ['age', 'gender', 'gender_other', 'education', 'stand',
                   'party', 'party_other', 'intuition', 'populism',
                   'fullread', 'source', 'source_other', 'factcheck']


page_sequence = [
    Introduction,
    Background,
    CWV,
    SWV,
    SWVcul,
    Q1WV,
    CWVCP,
    SWVSP,
    SWVculSP,
    CWVSP,
    SWVCP,
    SWVculCP,
    Q2P,
    Q3P,
    Demographics
]