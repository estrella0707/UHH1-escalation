from otree.api import *
import random

doc = """
Dispatcher app for round-robin assignment
"""


# FUNCTIONS
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


class C(BaseConstants):
    NAME_IN_URL = 'dispatcher'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Comprehension check question
    cq_bg = models.StringField(
        label='What changes are farmers facing on Planet X, according to the information you just read?',
        widget=widgets.RadioSelect,
    )


# Global counter
class GlobalCounter(ExtraModel):
    value = models.IntegerField(default=0)


# PAGES
class Introduction(Page):
    pass


class Consent(Page):
    pass


class Background(Page):
    pass


class Q1(Page):
    form_model = 'player'
    form_fields = ['cq_bg']

    @staticmethod
    def before_next_page(player, timeout_happened):
        counters = GlobalCounter.filter()
        if not counters:
            counter = GlobalCounter.create(value=1)
        else:
            counter = counters[0]
            counter.value += 1
        branch = (counter.value - 1) % 4 + 1
        player.participant.vars['branch'] = branch


    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        branch = player.participant.vars['branch']
        if branch == 1:
            return 'EN'
        elif branch == 2:
            return 'EN_plant'
        elif branch == 3:
            return 'EX'
        elif branch == 4:
            return 'EX_plant'


page_sequence = [
    Introduction, Consent,  # dispatcher
    Background, Q1  # BG and comprehension check
]