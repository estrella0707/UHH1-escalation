from otree.api import *
import random

doc = """
Dispatcher app for round-robin assignment
"""


# FUNCTIONS
class C(BaseConstants):
    NAME_IN_URL = 'dispatcher'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# Global counter
class GlobalCounter(ExtraModel):
    value = models.IntegerField(default=0)


# PAGES
class Introduction(Page):
    pass


class Consent(Page):
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
    Introduction, Consent
]