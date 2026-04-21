from otree.api import *
import random

doc = """
exogenous
"""

# FUNCTION
def creating_session(subsession):
    # Treatment randomization
    for player in subsession.get_players():
        player.first_logic_then_language = random.choice([True, False])
        player.first_argument_then_policy = random.choice([True, False])
        player.initial = random.choice(['complex', 'simple'])


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'ex'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment assignment
    initial = models.StringField()
    first_logic_then_language = models.BooleanField()  # randomize the order of questions
    first_argument_then_policy = models.BooleanField()  # randomize the order of questions

    # Manipulation check question
    mq_logic = models.IntegerField(choices=range(1, 8))
    mq_language = models.IntegerField(choices=range(1, 8))
    mq_fault = models.IntegerField(choices=range(1, 8))

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


# PAGES
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


class Instruction(Page):
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

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return 'Survey'


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

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return 'Survey'


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

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return 'Survey'


class R3b(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote3 == 'switch'

    form_model = 'player'
    form_fields = ['why3_argument', 'why3_policy', 'why3']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return 'Survey'


page_sequence = [
    Given,
    Q2,
    R0c, R0d,
    Instruction, Vote1, R1a, R1b, R1c, R1d,
    Vote2, R2a, R2b, R2c, R2d,
    Vote3, R3a, R3b,
]
