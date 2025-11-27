from otree.api import *
import itertools
import random

doc = """
Pilot 3 Solution"""


# Function
def creating_session(subsession):
    #Treatment randomization
    task = itertools.cycle(['complex_long_simple_long',
                            'complex_long_simple_short',
                            'complex_short_simple_long',
                            'complex_short_simple_short'])
    for player in subsession.get_players():
        player.task = next(task)
    # Order randomization
    for player in subsession.get_players():
        player.complex_left_simple_right = random.choice([True, False]) # image position randomization
        player.first_logic_then_language = random.choice([True, False]) # question order randomization


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


def cq_bg_error_message(player, value):
    if value != 'The soil is becoming too acidic, and alien creatures have appeared.':
        return "This is not the correct answer. Please read and select again."


def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, '']],
        label=label,
        widget=widgets.RadioSelect)


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
    task = models.StringField()
    complex_left_simple_right = models.BooleanField()  # randomize left/right position
    first_logic_then_language = models.BooleanField()  # randomize the order of questions

    # Comprehension check question
    cq_bg = models.StringField(
        label='What changes are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
    )

    # Manipulation check question
    complex_logic = models.IntegerField(choices=range(1, 8))
    complex_language = models.IntegerField(choices=range(1, 8))
    complex_time = models.IntegerField(choices=range(1, 8))
    simple_logic = models.IntegerField(choices=range(1, 8))
    simple_language = models.IntegerField(choices=range(1, 8))
    simple_time = models.IntegerField(choices=range(1, 8))

    # Engagement check question
    eq = models.IntegerField(choices=range(1, 8))

    # Pretest intention check question
    associate = models.BooleanField()
    associate_des = models.LongStringField(blank=True)
    associate_inf = models.BooleanField(blank=True)

    # Choice
    vote = models.StringField(
        widget=widgets.RadioSelect,
        choices=['complex_long',
                 'simple_long',
                 'complex_short',
                 'simple_short'],
        initial=''
    )
    complex_confidence = models.IntegerField(choices=range(1, 8))
    simple_confidence = models.IntegerField(choices=range(1, 8))

    # Demographic variables
    age = models.IntegerField(
        label='Enter your age'
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
    immi_attitude = models.IntegerField(
        widget=widgets.RadioSelect,
        label='Which of the following statements most closely reflect your view on the number of <b>legal immigrants</b> '
              'who are permitted to come to the United Kingdom to live?',
        choices=[(1, 'The number of legal immigrants today is a very big problem. '
                     'We should ask many legal immigrants to leave the UK, '
                     'and stop accepting new immigrants.'),
                 (2, 'The number of legal immigrants today is a big problem. '
                     'We should decrease by a lot the number permitted to come to the UK. '),
                 (3, 'The number of legal immigrants today is somewhat of a problem. '
                     'We should try and decrease by a bit the number permitted to come to the UK. '),
                 (4, 'The number of legal immigrants today is not a problem. '
                     'We should keep letting in the same number of immigrants to come to the UK. '),
                 (5, 'The number of legal immigrants today is not a problem at all. '
                     'We should let even more legal immigrants come to the UK. ')
                 ],
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


class Q2(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image1_map = {
            'complex_long_simple_long': ('Pilot3/Slide2.JPG', 'complex_long'),
            'complex_long_simple_short': ('Pilot3/Slide2.JPG', 'complex_long'),
            'complex_short_simple_long': ('Pilot3/Slide1.JPG', 'complex_short'),
            'complex_short_simple_short': ('Pilot3/Slide1.JPG', 'complex_short'),
        }
        image2_map = {
            'complex_long_simple_long': ('Pilot3/Slide4.JPG', 'simple_long'),
            'complex_long_simple_short': ('Pilot3/Slide3.JPG', 'simple_short'),
            'complex_short_simple_long': ('Pilot3/Slide4.JPG', 'simple_long'),
            'complex_short_simple_short': ('Pilot3/Slide3.JPG', 'simple_short'),
        }
        image1_path, image1_value = image1_map.get(player.task, ('', ''))
        image2_path, image2_value = image2_map.get(player.task, ('', ''))
        return {
            'image1': image1_path,
            'image1_value': image1_value,
            'image2': image2_path,
            'image2_value': image2_value,
        }

    form_model = 'player'
    form_fields = ['vote']


class Q3(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image1 = {
            'complex_long_simple_long': 'Pilot3/Slide2.JPG',
            'complex_long_simple_short': 'Pilot3/Slide2.JPG',
            'complex_short_simple_long': 'Pilot3/Slide1.JPG',
            'complex_short_simple_short': 'Pilot3/Slide1.JPG',
        }
        image2 = {
            'complex_long_simple_long': 'Pilot3/Slide4.JPG',
            'complex_long_simple_short': 'Pilot3/Slide3.JPG',
            'complex_short_simple_long': 'Pilot3/Slide4.JPG',
            'complex_short_simple_short': 'Pilot3/Slide3.JPG',
        }
        return {
            'image1': image1.get(player.task),
            'image2': image2.get(player.task),
        }

    form_model = 'player'
    form_fields = ['complex_logic', 'complex_language', 'complex_time', 'complex_confidence',
                   'simple_logic', 'simple_language', 'simple_time', 'simple_confidence']


class Q4(Page):
    form_model = 'player'
    form_fields = ['eq', 'associate', 'associate_des', 'associate_inf']


class Demographics1(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'stand',
                   'party', 'party_other', 'immi_attitude',
                   'intuition1', 'intuition2', 'intuition3',
                   'patience', 'scientist', 'religiosity']


class Demographics2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['ethic_new', 'ethic_nature', 'ethic_secure',
                  'ethic_creative', 'ethic_equality', 'ethic_help', 'scifi']
        random.shuffle(survey)
        return survey


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction,
    Background,
    Q1,
    Q2,
    Q3,
    Q4,
    Demographics1,
    Demographics2,
    ProlificCompletion
]