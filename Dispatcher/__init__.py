from otree.api import *
import itertools
import random

doc = """
Dispatcher app for round-robin assignment
"""


# FUNCTIONS
def creating_session(subsession):
    treatment_cycle = itertools.cycle(['plant', 'creature'])
    for player in subsession.get_players():
        player.treatment = next(treatment_cycle)


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


def cq_bgplant_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_bgplant_choices' not in player.participant.vars:
        choices = ['Too much rain is flooding their fields.',
                   'The soil is becoming too acidic, and plants from other planet have appeared.',
                   'Robots are taking over farming jobs.',
                   'Crops are growing too fast and causing food waste.']
        random.shuffle(choices)
        player.participant.vars['cq_bgplant_choices'] = choices
    return player.participant.vars['cq_bgplant_choices']


def cq_bgplant_error_message(player, value):
    if value != 'The soil is becoming too acidic, and plants from other planet have appeared.':
        return "This is not the correct answer. Please read and select again."


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # AI detection
    answer = models.IntegerField(blank=True)
    aqvideo_attempts = models.IntegerField(initial=0)
    aqvideo = models.BooleanField(initial=0)

    # Treatment assignment
    treatment = models.StringField()

    # Comprehension check question
    cq_bg = models.StringField(
        label='What changes are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
        blank=True
    )
    cq_bgplant = models.StringField(
        label='What changes are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
        blank=True
    )


# PAGES
class Introduction(Page):
    pass


class Consent(Page):
    pass


class ACvideo(Page):
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def error_message(player, values):
        if values['answer'] == 3169:
            return
        player.aqvideo_attempts += 1
        if player.aqvideo_attempts < 2:
            return 'You have typed in wrong digits. Please try again.'

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == 3169:
            player.aqvideo = 1


class ACvideoFail(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.aqvideo != 1


class Background(Page):
    pass


class Q1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'creature'

    form_model = 'player'
    form_fields = ['cq_bg']


class Q1plant(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'plant'

    form_model = 'player'
    form_fields = ['cq_bgplant']


class Instruction(Page):
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.treatment == 'creature':
            return 'EN'
        elif player.treatment == 'plant':
            return 'EN_plant'


page_sequence = [
    Introduction, Consent,
    ACvideo,  # video attention check for bot detection
    ACvideoFail,  # dead end for participants who failed the bot check twice
    Background, Q1, Q1plant, Instruction,
]