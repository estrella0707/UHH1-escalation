from otree.api import *

doc = """
Survey
"""

# FUNCTION
def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, '']],
        label=label,
        widget=widgets.RadioSelect)


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # feedback question
    DEMAND = [
        dict(name='believe', label='I made up my mind in which of the options I believed most and then ticked it.'),
        dict(name='against', label='I made up my mind about which of the options the researchers wanted me to tick '
                                   'and then ticked something else.'),
        dict(name='conform', label='I made up my mind about which of the options the researchers wanted me to tick '
                                   'and then ticked it.'),
        dict(name='random', label='I just made a random guess, like mentally flipping a coin.')
    ]


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

    # Pretest intention check question
    associate = models.BooleanField()
    associate_des = models.LongStringField(blank=True)
    associate_inf = models.BooleanField(blank=True)

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
    patience = models.IntegerField(choices=range(1, 8))
    risk = models.IntegerField(choices=range(1, 8))
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
                     'We should keep letting the same number of legal immigrants to come to the US. '),
                 (5, 'The number of legal immigrants today is not a problem at all. '
                     'We should let even more legal immigrants come to the US. ')
                 ],
    )

    # Individual difference variables
    frustration1 = likert1('If my first attempt to solve a problem fails, I keep trying until I succeed.')
    frustration2 = likert1('I am willing to listen and consider alternatives for handling a problem.')
    ethic_nature = likert1('It is important to care for nature and environment.')
    ethic_secure = likert1('It is important to live in secure and safe surroundings.')

    # Attention check question
    aq = models.BooleanField(
        label='',
        choices=[(True, 'Yes, I have devoted full attention to the questions so far and '
                        'I think you should use my responses for your study.'),
                 (False, 'No, I have NOT devoted full attention to the questions so far and '
                         'I think you should NOT use my responses for your study.')],
        widget=widgets.RadioSelect
    )

    # Experimenter demand
    believe = models.BooleanField(blank=True, initial=0)
    against = models.BooleanField(blank=True, initial=0)
    conform = models.BooleanField(blank=True, initial=0)
    random = models.BooleanField(blank=True, initial=0)


# PAGES
class Q3(Page):
    form_model = 'player'
    form_fields = ['associate', 'associate_des', 'associate_inf']


class Demographics1(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'stand', 'patience', 'risk',
                   'party', 'immi_attitude', 'AIuse', 'aq']


class Demographics2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['frustration1', 'frustration2', 'ethic_secure', 'ethic_nature']
        random.shuffle(survey)
        return survey


class Q4(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [demand['name'] for demand in C.DEMAND]


class ProlificCompletion(Page):
    pass


page_sequence = [
    Q3, Demographics1, Demographics2, Q4,
    ProlificCompletion
]
