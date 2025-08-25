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
    # image position randomization
    for player in subsession.get_players():
        player.show_first_image_first = random.choice([True, False])


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
    show_first_image_first = models.BooleanField()  # randomize left/right position

    # Comprehension check question
    cq_bg = models.StringField(
        label='What changes are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
    )

    # Manipulation check question
    mq1_logic = models.IntegerField(choices=range(1, 8))
    mq1_language = models.IntegerField(choices=range(1, 8))
    mq1_time = models.IntegerField(choices=range(1, 8))
    mq2_logic = models.IntegerField(choices=range(1, 8))
    mq2_language = models.IntegerField(choices=range(1, 8))
    mq2_time = models.IntegerField(choices=range(1, 8))

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
    confidence = models.IntegerField(choices=range(1, 8))

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
    form_fields = ['vote', 'confidence']


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
            'show_first_table_first': random.choice([True, False]),
        }

    form_model = 'player'
    form_fields = ['mq1_logic', 'mq1_language', 'mq1_time',
                   'mq2_logic', 'mq2_language', 'mq2_time']


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
    Q2,
    Q3,
    Demographics1,
    Demographics2,
    ProlificCompletion
]