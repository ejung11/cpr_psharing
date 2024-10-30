from otree.api import *


doc = """
This is the intro app for Part 1 of 
the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include Instructions, Example, KnowledgeCheck Pages.
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro_baseline'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # KnowledgeCheck questions
    kc1 = models.StringField(
        choices=[['False', '2'], ['False', '4'], ['False', '6'], ['True', '8'], ],
        label='1. How many people are in your group during the experiment?',
        widget=widgets.RadioSelect,
    )

    kc2 = models.StringField(
        choices=[['True', 'Remain the same'], ['False', 'Randomly reassigned'],],
        label='2. Will your group remain the same or be randomly reassigned throughout Part 1?',
        widget=widgets.RadioSelect,
    )

    kc3 = models.StringField(
        choices=[['False', '5'], ['True', '10'], ['False', '15'], ['False', '20'], ],
        label='3. How many rounds will you play in Part 1?',
        widget=widgets.RadioSelect,
    )

    kc4 = models.StringField(
        choices=[['False', '10 efforts'],
                 ['False', '15 efforts'],
                 ['False', '20 efforts'],
                 ['True', '25 efforts'],
                 ],
        label='4. How many efforts are you given each round to allocate between activities?',
        widget=widgets.RadioSelect,
    )

    kc5 = models.StringField(
        choices=[['False', 'E$ 2 per effort'],
                 ['False', 'E$ 3 per effort'],
                 ['True', 'E$ 5 per effort'],
                 ['False', 'E$ 10 per effort'],
                 ],
        label='5. What is the return for each effort you allocate to Activity F?',
        widget=widgets.RadioSelect,
    )

    kc6 = models.StringField(
        choices=[['False', 'Your own allocation only'],
                 ['False', 'Others effort allocated to Activity G only'],
                 ['True', 'The total effort allocated to Activity G by the entire group'],
                 ['False', 'The number of rounds played'],
                 ],
        label='6. What affects the return for each effort allocated to Activity G?',
        widget=widgets.RadioSelect,
    )

    kc7 = models.StringField(
        choices=[['True', 'The sum of your earnings from all rounds.'],
                 ['False', 'The earnings from just the final round.'],
                 ['False', 'A random round will be selected, and only the earnings from that round.'],
                 ['False', 'A fixed amount of money, regardless of your performance.'],
                 ],
        label='7. How will your payoff in the Part 1 be calculated?',
        widget=widgets.RadioSelect,
    )


# PAGES
class Instructions(Page):
    pass


class Wait(Page):
    pass



class KnowledgeCheck(Page):
    form_model = 'player'
    form_fields = [
        'kc1',
        'kc2',
        'kc3',
        'kc4',
        'kc5',
        'kc6',
        'kc7',
                   ]

    @staticmethod
    def error_message(player, values):
        solution = dict(
            kc1='True',
            kc2='True',
            kc3='True',
            kc4='True',
            kc5='True',
            kc6='True',
            kc7='True',
        )

        # Define specific error messages for each question
        error_messages = dict(
            kc1="You will be randomly assigned to a group of 8 people.",
            kc2="Your group will remain the same throughout Part 1.",
            kc3="There are 10 rounds in the game.",
            kc4="You are given 25 efforts in every round to allocate between activities.",
            kc5="The return for each effort in Activity A is 5 ECUs.",
            kc6="The return for Activity B is affected by the total effort allocated by the entire group.",
            kc7="Your final payoff will be the sum of your earnings from all rounds."
        )

        # Prepare the final error messages for display if a wrong answer is selected
        final_errors = {}
        for field_name, correct_value in solution.items():
            if values[field_name] != correct_value:
                final_errors[field_name] = error_messages[field_name]

        return final_errors


class BeforePractice(Page):
    pass


page_sequence = [
    Instructions,
    Wait,
    KnowledgeCheck,
    BeforePractice,
]
