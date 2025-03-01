from otree.api import *
import itertools
import random

doc = """
Pretest on simplicity and policy preference (vignette)
"""

# FUNCTION
def creating_session(subsession):
    # Treatment randomization
    task = itertools.cycle(['CWV_CP', 'CWV_SP', 'SWV_CP', 'SWV_SP',
                            'SWV_CP_culprit', 'SWV_SP_culprit'])
    for player in subsession.get_players():
        player.task = next(task)

def cq_b1_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_b1_choices' not in player.participant.vars:
        choices = ['Too much rain is flooding their fields.',
                   'The soil is becoming too acidic, and strange creatures called Tivarns have appeared.',
                   'Robots are taking over farming jobs.',
                   'Crops are growing too fast and causing food waste.']
        random.shuffle(choices)
        player.participant.vars['cq_b1_choices'] = choices
    return player.participant.vars['cq_b1_choices']

def cq_b2_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_b2_choices' not in player.participant.vars:
        choices = ['Import food and compensate the farmers.',
                   'Remove all the Tivarns immediately.',
                   'Build greenhouses to grow food in space.',
                   'Ban farming to focus on technology.']
        random.shuffle(choices)
        player.participant.vars['cq_b2_choices'] = choices
    return player.participant.vars['cq_b2_choices']

def cq_wv_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_wv_choices' not in player.participant.vars:
        choices = ['A rise in solar radiation which affects atmospheric chemistry.',
                   'The acidic waste produced by the a creature called Tivarns.',
                   'A newly introduced agricultural method.',
                   'The inaction of the government.']
        random.shuffle(choices)
        player.participant.vars['cq_wv_choices'] = choices
    return player.participant.vars['cq_wv_choices']

def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
        label=label,
        widget=widgets.RadioSelect)

def cq_b1_error_message(player, value):
    if value != 'The soil is becoming too acidic, and strange creatures called Tivarns have appeared.':
        return "This is not the correct answer. Please read and select again."

def cq_b2_error_message(player, value):
    if value != 'Import food and compensate the farmers.':
        return "This is not the correct answer. Please read and select again."

def cq_wv_error_message(player, value):
    if player.task in ['CWV_CP', 'CWV_SP']:
        if value != "A rise in solar radiation which affects atmospheric chemistry.":
            return "This is not the correct answer. Please read and select again."
    else:
        if value != "The acidic waste produced by the a creature called Tivarns.":
            return "This is not the correct answer. Please read and select again."


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
    cq_b1 = models.StringField(
        label='What problems are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
    )
    cq_b2 = models.StringField(
        label='How does the government want to handle the crisis, according to the information you just read?',
        widget=widgets.RadioSelect,
    )
    cq_wv = models.StringField(
        label='According to the activists, what is causing soil acidification on Planet X?',
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
    populism1 = likert1('decision')
    populism2 = likert1('lead')
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
    form_model = 'player'
    form_fields = ['reading_time_bg']


class Q1B(Page):
    form_model = 'player'
    form_fields = ['cq_b1', 'cq_b2']


class WV(Page):
    form_model = 'player'
    form_fields = ['reading_time_wv']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures_wv = {
            'CWV_CP': 'Pretest1/Slide1.jpg',
            'CWV_SP': 'Pretest1/Slide1.jpg',
            'SWV_CP': 'Pretest1/Slide2.jpg',
            'SWV_SP': 'Pretest1/Slide2.jpg',
            'SWV_CP_culprit': 'Pretest1/Slide3.jpg',
            'SWV_SP_culprit': 'Pretest1/Slide3.jpg'
        }
        return {
            'picture_wv': pictures_wv.get(player.task)
        }


class Q2WV(Page):
    form_model = 'player'
    form_fields = ['cq_wv']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures_wv = {
            'CWV_CP': 'Pretest1/Slide1.jpg',
            'CWV_SP': 'Pretest1/Slide1.jpg',
            'SWV_CP': 'Pretest1/Slide2.jpg',
            'SWV_SP': 'Pretest1/Slide2.jpg',
            'SWV_CP_culprit': 'Pretest1/Slide3.jpg',
            'SWV_SP_culprit': 'Pretest1/Slide3.jpg'
        }
        return {
            'picture_wv': pictures_wv.get(player.task)
        }


class Q3WV(Page):
    form_model = 'player'
    form_fields = ['mq1', 'mq2']


class P(Page):
    form_model = 'player'
    form_fields = ['reading_time_p']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures_wv = {
            'CWV_CP': 'Pretest1/Slide1.jpg',
            'CWV_SP': 'Pretest1/Slide1.jpg',
            'SWV_CP': 'Pretest1/Slide2.jpg',
            'SWV_SP': 'Pretest1/Slide2.jpg',
            'SWV_CP_culprit': 'Pretest1/Slide3.jpg',
            'SWV_SP_culprit': 'Pretest1/Slide3.jpg'
        }
        pictures_p = {
            'CWV_CP': 'Pretest1/Slide4.jpg',
            'CWV_SP': 'Pretest1/Slide6.jpg',
            'SWV_CP': 'Pretest1/Slide7.jpg',
            'SWV_SP': 'Pretest1/Slide5.jpg',
            'SWV_CP_culprit': 'Pretest1/Slide7.jpg',
            'SWV_SP_culprit': 'Pretest1/Slide5.jpg'
        }
        return {
            'picture_wv': pictures_wv.get(player.task),
            'picture_p': pictures_p.get(player.task)
        }


class Q4P(Page):
    form_model = 'player'
    form_fields = ['policy_choice', 'policy_votes', 'policy_confidence', 'eq']


class Q5P(Page):
    form_model = 'player'
    form_fields = ['mq3', 'mq4', 'mq5',
                   'associate', 'associate_des', 'associate_inf']


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'gender_other', 'education', 'stand',
                   'party', 'party_other',
                   'intuition1', 'intuition2', 'intuition3',
                   'populism1', 'populism2',
                   'source', 'source_other']


page_sequence = [
    Introduction,
    Background,
    Q1B,
    WV,
    Q2WV,
    Q3WV,
    P,
    Q4P,
    Q5P,
    Demographics
]