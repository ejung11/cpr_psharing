from otree.api import *


doc = """
This is the intro app for Part 2 - Low Treatment (30% sharing) of 
the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include Instructions, Example, KnowledgeCheck Pages.
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro_tr30'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # KnowledgeCheck questions

    kc1 = models.StringField(
        choices=[['False', 'A.  Remain the same'], ['True', 'B.  Mixed'],],
        label='1. Will your group (Part 1) remain the same or be mixed in Part 2?',
        widget=widgets.RadioSelect,
    )

    kc2 = models.StringField(
        choices=[['False', 'A.  5'], ['True', 'B.  10'], ['False', 'C.  15'], ['False', 'D.  20'], ],
        label='2. How many rounds will you play in Part 2?',
        widget=widgets.RadioSelect,
    )

    kc3 = models.StringField(
        choices=[['True', 'A.  30%'], ['False', 'B.  60%'], ['False', 'C.  90%'], ['False', 'D.  100%'], ],
        label='3. How much do you have to share returns from Activity B with your group members?',
        widget=widgets.RadioSelect,
    )

    kc4 = models.StringField(
        choices=[['False', 'A.  Return from Activity A'],
                 ['False', 'B.  Return from Activity B'],
                 ['False', 'C.  Earning from group sharing'],
                 ['True', 'D.  All of Above'], ],
        label='4. What is your payoff for each round?',
        widget=widgets.RadioSelect,
    )

    kc5 = models.StringField(
        choices=[['True', 'A.  The sum of your earnings from both Part 1 and Part 2.'],
                 ['False', 'B.  The earnings from Part 2.'],
                 ['False', 'C.  A random Part will be selected, and only the earnings from that Part.'],
                 ['False', 'D.  A fixed amount of money, regardless of your performance.'],
                 ],
        label='5. How will your final payoff be calculated?',
        widget=widgets.RadioSelect,
    )


# PAGES
class Instructions(Page):
    pass



class KnowledgeCheck(Page):
    form_model = 'player'
    form_fields = [
        'kc1',
        'kc2',
        'kc3',
        'kc4',
        'kc5',
                   ]

    @staticmethod
    def error_message(player, values):
        solution = dict(
            kc1='True',
            kc2='True',
            kc3='True',
            kc4='True',
            kc5='True',
        )

        # Define specific error messages for each question
        error_messages = dict(
            kc1="The group will be reassigned randomly at the beginning of Part 2",
            kc2="There are 10 rounds in this part.",
            kc3="You are sharing 30% of returns from Activity B wih the group members.",
            kc4="Three sources of earnings are returns from 1. Activity A, 2. Activity B, 3. Group share ",
            kc5="Your final earnings will be the sum of the earnings from both parts.",
        )

        # Prepare the final error messages for display if a wrong answer is selected
        final_errors = {}
        for field_name, correct_value in solution.items():
            if values[field_name] != correct_value:
                final_errors[field_name] = error_messages[field_name]

        return final_errors


page_sequence = [
    Instructions,
    KnowledgeCheck,
]
