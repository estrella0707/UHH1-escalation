from otree.api import *
import itertools
import random

doc = """
Pilot3 on Escalation, exogenous choice
"""

# FUNCTION
def creating_session(subsession):
    # Treatment randomization
    initial = itertools.cycle(['complex', 'simple'])
    for player in subsession.get_players():
        player.initial = next(initial)
    # question order randomization
    for player in subsession.get_players():
        player.first_logic_then_language = random.choice([True, False])
        player.first_argument_then_policy = random.choice([True, False])

def cq_bg_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_bg_choices' not in player.participant.vars:
        choices = ['Too much rain is flooding their fields.',
                   'The soil is becoming too acidic, and creatures from other planet have appeared.',
                   'Robots are taking over farming jobs.',
                   'Crops are growing too fast and causing food waste.']
        random.shuffle(choices)
        player.participant.vars['cq_bg_choices'] = choices
    return player.participant.vars['cq_bg_choices']

def cq_bg_error_message(player, value):
    if value != 'The soil is becoming too acidic, and creatures from other planet have appeared.':
        return "This is not the correct answer. Please read and select again."

def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, '']],
        label=label,
        widget=widgets.RadioSelect)


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt2ex'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Exclude bots
    AIuse = models.BooleanField(
        label='If you have used any AI tool in completing this study, please tick "Yes". '
              'You will receive the study reward independent of your answer.'
    )

    # Treatment assignment
    initial = models.StringField()
    first_logic_then_language = models.BooleanField()  # randomize the order of questions
    first_argument_then_policy = models.BooleanField()  # randomize the order of questions

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
    mq_logic = models.IntegerField(choices=range(1, 8))
    mq_language = models.IntegerField(choices=range(1, 8))
    mq_fault = models.IntegerField(choices=range(1, 8))

    # Pretest intention check question
    associate = models.BooleanField()
    associate_des = models.LongStringField(blank=True)
    associate_inf = models.BooleanField(blank=True)

    # Choice
    confidence0_argument = models.IntegerField(choices=range(1, 8))
    confidence0_policy = models.IntegerField(choices=range(1, 8))

    vote1 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch'],
        initial=''
    )
    confidence1 = models.IntegerField(choices=range(1, 8))
    why1_argument = models.IntegerField(choices=range(1, 8))
    why1_policy = models.IntegerField(choices=range(1, 8))
    why1 = models.LongStringField(
        label="If you want to elaborate on the reason of your choice, please leave it here. (optional)",
        blank=True
    )

    vote2 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch'],
        initial=''
    )
    confidence2 = models.IntegerField(choices=range(1, 8))
    why2_argument = models.IntegerField(choices=range(1, 8))
    why2_policy = models.IntegerField(choices=range(1, 8))
    why2 = models.LongStringField(
        label="If you want to elaborate on the reason of your choice, please leave it here. (optional)",
        blank=True
    )

    vote3 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch'],
        initial=''
    )
    confidence3 = models.IntegerField(choices=range(1, 8))
    why3_argument = models.IntegerField(choices=range(1, 8))
    why3_policy = models.IntegerField(choices=range(1, 8))
    why3 = models.LongStringField(
        label="If you want to elaborate on the reason of your choice, please leave it here. (optional)",
        blank=True
    )

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
        choices=['Democratic Party', 'Republican Party', 'Independent', 'Prefer not to say']
    )
    immi_attitude = models.IntegerField(
        widget=widgets.RadioSelect,
        label='Which of the following statements most closely reflect your view on the number of <b>legal immigrants</b> '
              'who are permitted to come to the United States to live?',
        choices=[(1, 'The number of legal immigrants today is a very big problem. '
                     'We should ask many legal immigrants to leave the US, '
                     'and stop accepting new immigrants.'),
                 (2, 'The number of legal immigrants today is a big problem. '
                     'We should decrease by a lot the number permitted to come to the US. '),
                 (3, 'The number of legal immigrants today is somewhat of a problem. '
                     'We should try and decrease by a bit the number permitted to come to the US. '),
                 (4, 'The number of legal immigrants today is not a problem. '
                     'We should keep letting in the same number of immigrants to come to the US. '),
                 (5, 'The number of legal immigrants today is not a problem at all. '
                     'We should let even more legal immigrants come to the US. ')
                 ],
    )
    # Individual difference variables
    frustration1 = likert1('If my first attempt to solve a problem fails, I keep trying until I succeed.')
    frustration2 = likert1('I am willing to listen and consider alternatives for handling a problem.')
    ethic_nature = likert1('It is important to care for nature and environment.')
    ethic_secure = likert1('It is important to live in secure and safe surroundings.')


# PAGES
class Introduction(Page):
    pass


class Background(Page):
    pass


class Q1(Page):
    form_model = 'player'
    form_fields = ['cq_bg']


class Given(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'Pilot2/complex_given.JPG',
            'simple': 'Pilot2/simple_given.JPG',
        }
        return {
            'picture': pictures.get(player.initial)
        }


class Q2(Page):
    form_model = 'player'
    form_fields = ['mq_logic', 'mq_language', 'mq_fault',
                   'confidence0_argument', 'confidence0_policy']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'Pilot2/complex_given.JPG',
            'simple': 'Pilot2/simple_given.JPG',
        }
        return {
            'picture': pictures.get(player.initial)
        }


# R1a, R2a, R3a: display the chosen policy in this round of voting
# R1b, R2b, R3b: if participants switch, ask why they switch
# R0c, R1c, R2c: display that the policy fails
# R0d, R1d, R2d: supporters and opponents explain why the policy fails
class R0c(Page):
    pass


class R0d(Page):
    pass


class Vote1(Page):
    form_model = 'player'
    form_fields = ['vote1', 'confidence1']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'Pilot2/complex_given.JPG',
            'simple': 'Pilot2/simple_given.JPG',
        }
        return {
            'picture': pictures.get(player.initial)
        }


class R1a(Page):
    pass


class R1b(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote1 == 'switch'

    form_model = 'player'
    form_fields = ['why1_argument', 'why1_policy', 'why1']


class R1c(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote1 == 'stick'


class R1d(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote1 == 'stick'


class Vote2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote1 == 'stick'

    form_model = 'player'
    form_fields = ['vote2', 'confidence2']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'Pilot2/complex_vote1.JPG',
            'simple': 'Pilot2/simple_vote1.JPG',
        }
        return {
            'picture': pictures.get(player.initial)
        }


class R2a(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote1 == 'stick'


class R2b(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote2 == 'switch'

    form_model = 'player'
    form_fields = ['why2_argument', 'why2_policy', 'why2']


class R2c(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote2 == 'stick'


class R2d(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote2 == 'stick'


class Vote3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote2 == 'stick'

    form_model = 'player'
    form_fields = ['vote3', 'confidence3']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'Pilot2/complex_vote2.JPG',
            'simple': 'Pilot2/simple_vote2.JPG',
        }
        return {
            'picture': pictures.get(player.initial)
        }


class R3a(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote2 == 'stick'


class R3b(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote3 == 'switch'

    form_model = 'player'
    form_fields = ['why3_argument', 'why3_policy', 'why3']


class Q3(Page):
    form_model = 'player'
    form_fields = ['associate', 'associate_des', 'associate_inf']


class Demographics1(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'stand',
                   'party', 'immi_attitude', 'AIuse']


class Demographics2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['frustration1', 'frustration2', 'ethic_new', 'ethic_nature']
        random.shuffle(survey)
        return survey


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction,
    Background,
    Q1,
    Given,
    Q2,
    R0c, R0d,
    Vote1, R1a, R1b, R1c, R1d,
    Vote2, R2a, R2b, R2c, R2d,
    Vote3, R3a, R3b,
    Q3,
    Demographics1,
    Demographics2,
    ProlificCompletion
]
