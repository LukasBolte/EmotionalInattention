import random
import json
import itertools

from collections import Counter

from otree.api import *

doc = """
Authors: 
Lukas Bolte (lukas.bolte@outlook.com)
Vlasta Rasocha 
"""


class C(BaseConstants):
    NAME_IN_URL = 'study'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 8
    MIN_TIME = 5
    MAX_TIME = 10
    NUM_BOXES = 10000
    NUM_DRAWS = 300
    DELAY = 10

    INITIAL_LIST=[2,2,2,2,2,3,3,3,5,10]
    MIN_PAY = min(INITIAL_LIST)
    MAX_PAY = max(INITIAL_LIST)

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    
    
    for player in subsession.get_players():
        if subsession.round_number == 1:
            treatments = itertools.cycle(['bonus', 'penalty'])
            for player in subsession.get_players():
                participant = player.participant
                participant.treatment = next(treatments)
                participant.experiment_sequence = ['Welcome','Consent','Introduction',f"Payment_{participant.treatment}",f"UnderstandingQuestions_{participant.treatment}","Task",'Feedback','Finished']
                new_list = create_list_with_frequency(C.INITIAL_LIST, int(C.NUM_BOXES/len(C.INITIAL_LIST)))
                participant.sequence = json.dumps(random.sample(new_list, C.NUM_DRAWS))
                

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    num_draws = models.StringField()
     
    payment_B = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It is the payment from opening the boxes.'],
            [2, 'It is the payment from opening the boxes minus penalty charge and plus a bonus.']
        ],
        widget=widgets.RadioSelect,
        label='What is the total payment you get for completing this study?'
    )

    bonus = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It corresponds to the largest amount in any of the boxes you have opened.'],
            [2, 'It is the sum of the amounts in the boxes you have opened.'],
            [3, 'It is the amount of the last box you have opened.']
        ],
        widget=widgets.RadioSelect,
        label='How is your payment determined?'
    )
    
    increase_bonus = models.BooleanField(
        blank=True,
        label='It increases.',
        widget=widgets.CheckboxInput
    )

    same_bonus = models.BooleanField(
        blank=True,
        label='It stays the same.',
        widget=widgets.CheckboxInput
    )

    decrease_bonus = models.BooleanField(
        blank=True,
        label='It decreases.',
        widget=widgets.CheckboxInput
    )


    payment_P = models.IntegerField(
        blank=True,
        choices=[
            [1, f'It is the base payment of ${C.MIN_PAY + C.MAX_PAY} minus a penalty.'],
            [2, 'It is the base payment plus a bonus payment minus a penalty.']
        ],
        widget=widgets.RadioSelect,
        label='What is the total payment you get for completing this study?'
    )

    penalty = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It corresponds to the smallest amount in any of the boxes you have opened.'],
            [2, 'It is the sum of the amounts in the boxes you have opened.'],
            [3, 'It is the amount of the last box you have opened.']
        ],
        widget=widgets.RadioSelect,
        label='How is your penalty determined?'
    )
    
    increase_penalty = models.BooleanField(
        blank=True,
        label='It increases.',
        widget=widgets.CheckboxInput
    )

    same_penalty = models.BooleanField(
        blank=True,
        label='It stays the same.',
        widget=widgets.CheckboxInput
    )

    decrease_penalty = models.BooleanField(
        blank=True,
        label='It decreases.',
        widget=widgets.CheckboxInput
    )
    
    feedback = models.LongStringField(blank=True)
    
    
# FUNCTIONS 
# def set_payoffs(group):
#     player1 = group.get_player_by_id(1)
#     player2 = group.get_player_by_id(2)
#     player1.payoff = group.kept
#     player2.payoff = C.ENDOWMENT - group.kept


# PAGES
class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Welcome'


class Consent(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Consent'
    

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Introduction'


class Payment_B(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Payment_bonus'


class Payment_P(Page):
    @staticmethod
    def vars_for_template(player):
         return {
             'base_payment':  C.MIN_PAY + C.MAX_PAY
         }
    
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Payment_penalty'


class UnderstandingQuestions_P(Page):
    form_model = 'player'


    form_fields = [ 'payment_P','penalty','increase_penalty', 'same_penalty', 'decrease_penalty']   

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            
            solutions = {'payment_P':1 ,
                             'penalty':1,
                             'increase_penalty':False,
                             'same_penalty':True,
                             'decrease_penalty':True
            }
            hints = {
                'payment_P':f"Your answer is incorrect. Your total payment for completing this study consists of the base payment of ${C.MIN_PAY + C.MAX_PAY} minus a penalty, and no bonus payment.",
                'penalty':'You answer is incorrect. Your penalty corresponds to the smallest amount in any of the boxes you have opened.',
                'decrease_penalty':'You answer is incorrect. When you open another box, two things can happen. When the amount in the new box is more than or equal to the largest amount so far, your potential penalty stays the same. When the amount is less, then your penalty decreases (to the amount in the last box).'
            }
            if 'mistakes' not in player.participant.vars.keys():
                player.participant.mistakes={
                    'payment_P':0,
                    'penalty':0,
                    'penalty_change':0
            }

            error_messages = {}
            for field_name in ['payment_P','penalty']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'
                elif values[field_name] != solutions[field_name]:
                    error_messages[field_name] = hints[field_name]
                    player.participant.mistakes[field_name]+=1            
            penalty=['increase_penalty','same_penalty','decrease_penalty']

            if all([values[field_name]==False for field_name in penalty]):
                error_messages['decrease_penalty']='Please select at least one to answer the question.'
            elif any([values[field_name]!=solutions[field_name] for field_name in ['increase_penalty','same_penalty','decrease_penalty']]):
                error_messages['decrease_penalty']=hints['decrease_penalty']
                player.participant.mistakes['penalty_change']+=1

            return error_messages
        
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'UnderstandingQuestions_penalty'
    

class UnderstandingQuestions_B(Page):
    form_model = 'player'
    form_fields = [ 'payment_B','bonus','increase_bonus', 'same_bonus', 'decrease_bonus']   

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            
            solutions = {
                'payment_B':1 ,
                'bonus':1,
                'increase_bonus':True,
                'same_bonus':True,
                'decrease_bonus':False
            }
            hints = {
                'payment_B':f"Your answer is incorrect. Your total payment for completing this study consists of the payment from opening the boxes, and there is no penalty charge or base payment.",
                'bonus':'You answer is incorrect. Your payment corresponds to the largest amount in any of the boxes you have opened.',
                'decrease_bonus':'You answer is incorrect. When you open another box, two things can happen. When the amount in the new box is less than or equal to the largest amount so far, your potential payment stays the same. When the amount is more, then your payment increases (to the amount in the last box).'
            }
            if 'mistakes' not in player.participant.vars.keys():

                player.participant.mistakes={
                    'payment_B':0,
                    'bonus':0,
                    'bonus_change':0
            }

            error_messages = {}
            for field_name in ['payment_B','bonus']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'
                elif values[field_name] != solutions[field_name]:
                    error_messages[field_name] = hints[field_name]
                    player.participant.mistakes[field_name]+=1            
            bonus=['increase_bonus','same_bonus','decrease_bonus']

            if all([values[field_name]==False for field_name in bonus]):
                error_messages['decrease_bonus']='Please select at least one to answer the question.'
            elif any([values[field_name]!=solutions[field_name] for field_name in ['increase_bonus','same_bonus','decrease_bonus']]):
                error_messages['decrease_bonus']=hints['decrease_bonus']
                player.participant.mistakes['bonus_change']+=1

            return error_messages
        
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'UnderstandingQuestions_bonus'
    


class Task(Page):
    form_model = 'player'
    form_fields = [ 'num_draws']   

    @staticmethod
    def vars_for_template(player):
         return {
             'sequence':  json.dumps(player.participant.sequence)
         }
    

    def before_next_page(player, timeout_happened):

        payoff = json.loads(player.num_draws)
        if payoff==0:
            player.payoff=C.MIN_PAY
        else:
            player.payoff = max(player.participant.sequence[:payoff])

    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Task'
    


class Feedback(Page):
    form_model = 'player'
    form_fields = [ 'feedback']   

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Feedback'
    
class Finished(Page):

    @staticmethod
    def vars_for_template(player):

        part1 = F"You will receive your payment of {player.participant.payoff_plus_participation_fee()}" 
        part2 = ""
        if player.participant.treatment=="penalty":
            part2 = F" consisting of the ${C.MIN_PAY + C.MAX_PAY} base payment minus the penalty of {C.MIN_PAY + C.MAX_PAY - player.participant.payoff_plus_participation_fee()}"
        part3 = " shortly."
        return {'payment_message': part1 + part2 + part3}

    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Finished'


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    def is_displayed(player):
        return player.id_in_group == 1


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        group = player.group

        return dict(payoff=player.payoff, offer=C.ENDOWMENT - group.kept)
    

page_sequence = [
    Welcome,
    Consent,
    Introduction,
    Payment_B,
    Payment_P,
    UnderstandingQuestions_B,
    UnderstandingQuestions_P,
    Task,
    Feedback,
    Finished
]



def create_list_with_frequency(lst, x):
    counter = Counter(lst)  # Count the frequency of elements in the initial list
    max_frequency = max(counter.values())  # Find the maximum frequency

    result = []
    for element, frequency in counter.items():
        num_repeats = x * frequency  # Determine the number of repeats for each element
        result.extend([element] * num_repeats)  # Add the element to the result list

    return result