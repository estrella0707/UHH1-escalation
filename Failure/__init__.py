from otree.api import *
import random

doc = """
Success for the most lucky
"""


# FUNCTIONS
class C(BaseConstants):
    NAME_IN_URL = 'failure'
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
class Failure(Page):
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return 'Survey'


page_sequence = [Failure]