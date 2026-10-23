from otree.api import *
import random

doc = """
endogenous
"""

# FUNCTION
def creating_session(subsession):
    # question order randomization
    for player in subsession.get_players():
        player.complex_left_simple_right = random.choice([True, False])  # image position randomization
        player.first_argument_then_policy = random.choice([True, False])


def perform_success_draw(player):
    # Luck draw for 0.1% probability to solve the problem
    draw = random.randint(1, 1000)
    player.success = 1 if draw == 1 else 0


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'en'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment assignment
    first_logic_then_language = models.BooleanField()  # randomize the order of questions
    first_argument_then_policy = models.BooleanField()  # randomize the order of questions
    complex_left_simple_right = models.BooleanField()  # randomize left/right position

    # Manipulation check question
    complex_fault = models.IntegerField(choices=range(1, 8))
    complex_familiar = models.IntegerField(choices=range(1, 8))
    complex_ethical = models.IntegerField(choices=range(1, 8))
    complex_immediate = models.IntegerField(choices=range(1, 8))
    simple_fault = models.IntegerField(choices=range(1, 8))
    simple_familiar = models.IntegerField(choices=range(1, 8))
    simple_ethical = models.IntegerField(choices=range(1, 8))
    simple_immediate = models.IntegerField(choices=range(1, 8))

    # Choice
    vote0 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['complex', 'simple', 'abstain'],
        initial=''
    )
    chance0_complex_argument = models.IntegerField(choices=range(1, 8))
    chance0_complex_policy = models.IntegerField(choices=range(1, 8))
    chance0_simple_argument = models.IntegerField(choices=range(1, 8))
    chance0_simple_policy = models.IntegerField(choices=range(1, 8))

    vote1 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch', 'abstain'],
        initial=''
    )
    chance1 = models.IntegerField(choices=range(1, 8))
    why1_argument = models.IntegerField(choices=range(1, 8))
    why1_policy = models.IntegerField(choices=range(1, 8))
    why1 = models.LongStringField(
        label="If you want to elaborate on the reason of your choice, please leave it here. (optional)",
        blank=True
    )

    vote2 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch', 'abstain'],
        initial=''
    )
    chance2 = models.IntegerField(choices=range(1, 8))
    why2_argument = models.IntegerField(choices=range(1, 8))
    why2_policy = models.IntegerField(choices=range(1, 8))
    why2 = models.LongStringField(
        label="If you want to elaborate on the reason of your choice, please leave it here. (optional)",
        blank=True
    )

    vote3 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['stick', 'switch', 'abstain'],
        initial=''
    )
    chance3 = models.IntegerField(choices=range(1, 8))
    why3_argument = models.IntegerField(choices=range(1, 8))
    why3_policy = models.IntegerField(choices=range(1, 8))
    why3 = models.LongStringField(
        label="If you want to elaborate on the reason of your choice, please leave it here. (optional)",
        blank=True
    )

    # whether the chosen policy succeeds
    success = models.IntegerField(initial=0)


# PAGES
class Vote0(Page):
    form_model = 'player'
    form_fields = ['vote0']


class Q2(Page):
    form_model = 'player'
    form_fields = ['complex_fault', 'complex_familiar', 'complex_ethical',
                   'complex_immediate',
                   'chance0_complex_argument', 'chance0_complex_policy',
                   'simple_fault', 'simple_familiar', 'simple_ethical',
                   'simple_immediate',
                   'chance0_simple_argument', 'chance0_simple_policy']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.vote0 == 'abstain':
            return 'Survey'


# R0a, R1a, R2a, R3a: display the chosen policy in this round of voting
# R1b, R2b, R3b: if participants switch, ask why they switch
# R0c, R1c, R2c: display that the policy fails
# R0d, R1d, R2d: supporters and opponents explain why the policy fails
class R0a(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        perform_success_draw(player)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.success == 1:
            return 'Success'


class R0c(Page):
    pass


class R0d(Page):
    pass


class Vote1(Page):
    form_model = 'player'
    form_fields = ['vote1']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'complex/vote0.JPG',
            'simple': 'simple/vote0.JPG',
        }
        return {
            'picture': pictures.get(player.vote0)
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.vote1 == 'abstain':
            return 'Survey'


class R1a(Page):
    form_model = 'player'
    form_fields = ['chance1']

    @staticmethod
    def before_next_page(player, timeout_happened):
        perform_success_draw(player)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.success == 1 and player.vote1 == 'stick':
            return 'Success'


class R1b(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote1 == 'switch'

    form_model = 'player'
    form_fields = ['why1_argument', 'why1_policy', 'why1']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.success == 1:
            return 'Success'
        else:
            return 'Failure'


class R1c(Page):
    pass


class R1d(Page):
    pass


class Vote2(Page):
    form_model = 'player'
    form_fields = ['vote2']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'complex/vote1.JPG',
            'simple': 'simple/vote1.JPG',
        }
        return {
            'picture': pictures.get(player.vote0)
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.vote2 == 'abstain':
            return 'Survey'


class R2a(Page):
    form_model = 'player'
    form_fields = ['chance2']

    @staticmethod
    def before_next_page(player, timeout_happened):
        perform_success_draw(player)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.success == 1 and player.vote2 == 'stick':
            return 'Success'


class R2b(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.vote2 == 'switch'

    form_model = 'player'
    form_fields = ['why2_argument', 'why2_policy', 'why2']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.success == 1:
            return 'Success'
        else:
            return 'Failure'


class R2c(Page):
    pass


class R2d(Page):
    pass


class Vote3(Page):
    form_model = 'player'
    form_fields = ['vote3']

    @staticmethod
    def vars_for_template(player):
        # Map treatment groups to the right picture
        pictures = {
            'complex': 'complex/vote2.JPG',
            'simple': 'simple/vote2.JPG',
        }
        return {
            'picture': pictures.get(player.vote0)
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.vote3 == 'abstain':
            return 'Survey'


class R3a(Page):
    form_model = 'player'
    form_fields = ['chance3']

    @staticmethod
    def before_next_page(player, timeout_happened):
        perform_success_draw(player)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.success == 1 and player.vote3 == "stick":
            return 'Success'
        elif player.success == 0 and player.vote3 == "stick":
            return 'Failure'


class R3b(Page):
    form_model = 'player'
    form_fields = ['why3_argument', 'why3_policy', 'why3']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.success == 1:
            return 'Success'
        else:
            return 'Failure'


page_sequence = [
    Vote0,
    Q2,
    R0a, R0c, R0d,
    Vote1, R1a, R1b, R1c, R1d,
    Vote2, R2a, R2b, R2c, R2d,
    Vote3, R3a, R3b,
]
