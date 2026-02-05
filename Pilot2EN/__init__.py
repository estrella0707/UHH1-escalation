from otree.api import *
import random

doc = """
Pilot2 on simplicity and policy preference (vignette) Escalation, endogenous choice
"""

# FUNCTION
def creating_session(subsession):
    # question order randomization
    for player in subsession.get_players():
        player.complex_left_simple_right = random.choice([True, False])  # image position randomization
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
    NAME_IN_URL = 'pt2en'
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
    first_logic_then_language = models.BooleanField()  # randomize the order of questions
    first_argument_then_policy = models.BooleanField()  # randomize the order of questions
    complex_left_simple_right = models.BooleanField()  # randomize left/right position

    # Comprehension check question
    cq_bg = models.StringField(
        label='What changes are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
    )

    # Manipulation check question
    complex_logic = models.IntegerField(choices=range(1, 8))
    complex_language = models.IntegerField(choices=range(1, 8))
    complex_fault = models.IntegerField(choices=range(1, 8))
    simple_logic = models.IntegerField(choices=range(1, 8))
    simple_language = models.IntegerField(choices=range(1, 8))
    simple_fault = models.IntegerField(choices=range(1, 8))

    # Engagement check question
    eq = models.IntegerField(choices=range(1, 8))

    # Pretest intention check question
    associate = models.BooleanField()
    associate_des = models.LongStringField(blank=True)
    associate_inf = models.BooleanField(blank=True)

    # Choice
    vote0 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['complex', 'simple'],
        initial=''
    )
    confidence0_complex_argument = models.IntegerField(choices=range(1, 8))
    confidence0_complex_policy = models.IntegerField(choices=range(1, 8))
    confidence0_simple_argument = models.IntegerField(choices=range(1, 8))
    confidence0_simple_policy = models.IntegerField(choices=range(1, 8))

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
    ethic_creative = likert1('It is important to think of new ideas and be creative.')
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
    form_model = 'player'
    form_fields = ['vote0']


class Q3(Page):
    form_model = 'player'
    form_fields = ['complex_logic', 'complex_language', 'complex_fault',
                   'confidence0_complex_argument', 'confidence0_complex_policy',
                   'simple_logic', 'simple_language', 'simple_fault',
                   'confidence0_simple_argument', 'confidence0_simple_policy']


# R0a, R1a, R2a, R3a: display the chosen policy in this round of voting
# R1b, R2b, R3b: if participants switch, ask why they switch
# R0c, R1c, R2c: display that the policy fails
# R0d, R1d, R2d: supporters and opponents explain why the policy fails
class R0a(Page):
    pass


class R0c(Page):
    pass


class R0d(Page):
    pass


class C1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote0 == 'complex'

    form_model = 'player'
    form_fields = ['vote1', 'confidence1']


class S1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote0 == 'simple'

    form_model = 'player'
    form_fields = ['vote1', 'confidence1']


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


class C2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote0 == 'complex' and player.vote1 == 'stick'

    form_model = 'player'
    form_fields = ['vote2', 'confidence2']


class S2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote0 == 'simple' and player.vote1 == 'stick'

    form_model = 'player'
    form_fields = ['vote2', 'confidence2']


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


class C3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote0 == 'complex' and player.vote2 == 'stick'

    form_model = 'player'
    form_fields = ['vote3', 'confidence3']


class S3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote0 == 'simple' and player.vote2 == 'stick'

    form_model = 'player'
    form_fields = ['vote3', 'confidence3']


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


class Q4(Page):
    form_model = 'player'
    form_fields = ['eq', 'associate', 'associate_des', 'associate_inf']


class Demographics1(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'stand',
                   'party', 'party_other', 'immi_attitude',
                   'intuition1', 'intuition2', 'intuition3',
                   'patience', 'scientist', 'religiosity', 'AIuse']


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
    R0a, R0c, R0d,
    C1, S1, R1a, R1b, R1c, R1d,
    C2, S2, R2a, R2b, R2c, R2d,
    C3, S3, R3a, R3b,
    Q4,
    Demographics1,
    Demographics2,
    ProlificCompletion
]

