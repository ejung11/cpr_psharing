from otree.api import *


doc = """
This is the Decision app for Part 2 Baseline of 
the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include practice, Harvest, Results, PaymentInfo, rules.
"""

class Constants(BaseConstants):
    name_in_url = 'cpr_baseline_2'
    players_per_group = 8
    num_rounds = 10
    instructions_template = 'cpr_partial_baseline/rules.html'
    endowment = 25
    conversion = 0.005


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_effort_act_b = models.IntegerField()



class Player(BasePlayer):
    # Decision for Activity 2
    effort_act_b = models.IntegerField(
        min=0,
        max=Constants.endowment,
        label="How much effort do you want to allocate to Activity 2?"
    )

    # Guess on others' average decision
    guess_act_b = models.IntegerField(
        min=0,
        max=Constants.endowment,
        label="Your guess on others' average effort allocation to Activity 2"
    )

    others_effort_act_b = models.IntegerField()
    others_avg_effort_act_b = models.FloatField()
    history_accumulated_earnings = models.FloatField()
    period_payoff = models.FloatField()
    period_payoff_int = models.FloatField()

    period_earning_a = models.FloatField()
    period_earning_a_int = models.FloatField()
    period_earning_b = models.FloatField()
    period_earning_b_int = models.FloatField()


#FUNCTIONS
#Round setup
def creating_session(subsession):
    # random matching at the beginning of each games
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)
    #check print, comment out after checking
    #print('in creating session')
    #print('round', subsession.round_number, 'group matrix is', subsession.get_group_matrix())

    #set individual var: total earnings for each participant
    for p in subsession.get_players():
        if subsession.round_number == 1:
            p.participant.vars['totalEarnings_b_float'] = 0
            p.participant.vars['totalEarnings_b'] = 0

#Payoffs
def set_payoffs(g: Group):
    g.total_effort_act_b = sum([p.effort_act_b for p in g.get_players()])

    for p in g.get_players():
        individual_effort = p.effort_act_b
        group_total_effort = g.total_effort_act_b

        # Logically break down the payoff calculation
        base_endowment_value = 5 * Constants.endowment
        individual_extraction = 20 * individual_effort
        externality_cost = 0.1171 * group_total_effort * individual_effort

        earning_act_a = base_endowment_value - (5 * individual_effort)
        earning_act_b = individual_extraction - externality_cost

        p.period_earning_a = float(earning_act_a)
        p.period_earning_a_int = round(p.period_earning_a, 2)

        p.period_earning_b = float(earning_act_b)
        p.period_earning_b_int = round(p.period_earning_b, 2)

        p.period_payoff = float(earning_act_a +
                                earning_act_b
                                )
        p.period_payoff_int = round(p.period_payoff, 2)

        p.participant.vars['totalEarnings_b_float'] += p.period_payoff_int
        p.participant.vars['totalEarnings_b'] = round(p.participant.vars['totalEarnings_b_float'], 2)
        p.history_accumulated_earnings = p.participant.vars['totalEarnings_b']

        p.participant.vars['totalEarnings'] = p.participant.vars['totalEarnings_a'] + p.participant.vars['totalEarnings_b']
        p.participant.vars['totalCash'] = round(p.participant.vars['totalEarnings'] * Constants.conversion, 2)

        # Log effort of others
        p.others_effort_act_b = group_total_effort - individual_effort
        p.others_avg_effort_act_b = round((group_total_effort - individual_effort) / (Constants.players_per_group - 1),
                                          1)





# PAGES
class Harvest(Page):
    form_model = 'player'
    form_fields = ['effort_act_b', 'guess_act_b']



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'



class Results(Page):
    """Players payoff: How much each has earned"""


class PaymentInfo(Page):
    @staticmethod
    def is_displayed(group):
        return group.round_number == Constants.num_rounds

    def vars_for_template(player: Player):
        participant = player.participant
        return dict(redemption_code=participant.label or participant.code)


page_sequence = [
    Harvest,
    ResultsWaitPage,
    Results,
    PaymentInfo,
]