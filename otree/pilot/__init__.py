import random
import json
import itertools
import math
import re 
import time
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
    NUM_ROUNDS = 10
    MIN_TIME = 5
    MAX_TIME = 10
    NUM_BOXES = 10000
    NUM_DRAWS = 300
    DELAY = 10

    height_constant = 50000

    START_VALUE = 2
    END_VALUE = 10
    INCREMENT_VALUE = 0.01

# create a function 

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    
    
    for player in subsession.get_players():
        if subsession.round_number == 1:
            treatments = itertools.cycle(['bonus', 'penalty'])
            for player in subsession.get_players():
                participant = player.participant
                participant.treatment = next(treatments)
                participant.experiment_sequence = ['Welcome','Consent','Introduction',f"Payment_{participant.treatment}",f"UnderstandingQuestions_{participant.treatment}","Task","Diagnostic","Demographics",'Feedback','Finished']

                # I have two lists: A and B. They have the same length. I want to create a third list that has element A[i] repeated B[i] times.
                # 

                A = labels(player.subsession)
                B = bar_heights(player.subsession)

                new_list = [a for a, b in zip(A, B) for _ in range(b)]
                participant.sequence = json.dumps(random.sample(new_list, C.NUM_DRAWS))

                


                

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    expected_bonus = models.StringField(
        blank=True
    )

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
            [3, 'It is the amount inside the last box you have opened.']
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
            [1, f'It is the base payment of ${C.START_VALUE + C.END_VALUE} minus a penalty.'],
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
            [3, 'It is the amount inside the last box you have opened.']
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
    

    gender = models.PositiveIntegerField(
        blank=True,
        label='Gender: Which gender identity do you most identify with?',
                                         choices=[[0, 'Female'],
                                                  [1, 'Male'],
                                                  [2, 'Transgender female'],
                                                  [3, 'Transgender male'],
                                                  [4, 'Gender variant/Non-conforming'],
                                                  [5, 'Not listed'],
                                                  [6, 'Prefer not to answer']],
                                         widget=widgets.RadioSelect)
    ethnic = models.PositiveIntegerField(
        blank=True,
        label='Race: Which race do you most identify with?',
                                         choices=[[0, 'White or Caucasian'],
                                                  [1, 'Black or African American'],
                                                  [2, 'Hispanic or Latino'],
                                                  [3, 'Asian or Asian American'],
                                                  [4, 'American Indian or Alaska Native'],
                                                  [5, 'Native Hawaiian or Pacific Islander'],
                                                  [6, 'Other'],
                                                  [7, 'Prefer not to answer']],
                                         widget=widgets.RadioSelect)
    age = models.PositiveIntegerField(
        blank=True,
        label='Age: What is your age?',
        choices=[[0, '18-25 years old'],
                [1, '26-35 years old'],
                [2, '36-45 years old'],
                [3, '46-55 years old'],
                [4, '56-65 years old'],
                [5, 'Above 65 years old'],
                [6, 'Prefer not to answer']],
        widget=widgets.RadioSelect)
    education = models.PositiveIntegerField(
        blank=True,
        label='Education: What is the highest level of school you have completed or the highest degree you have received?',
        choices=[[1, 'Some high school'],
                    [2, 'High school diploma (or equivalent, including GED)'],
                    [3, "Some college"],
                    [4, "Associate's degree in 2-year college"],
                    [5, "Bachelor's degree in 4-year college"],
                    [6, "Master's degree"],
                    [7, "Doctoral degree (PhD)"],
                    [8, "Professional doctorate (JD, MD)"],
                    [9, "Prefer not to answer"]],
        widget=widgets.RadioSelect)
    marital = models.PositiveIntegerField(
        blank=True,
        label='What is your marital status?',
        choices=[
            [0, 'Single, never married'],
            [1, 'Married or domestic partnership'],
            [2, 'Widowed'],
            [3, 'Divorced'],
            [4, 'Separated'],
            [5, 'Prefer not to answer']],
    widget=widgets.RadioSelect)
    income = models.PositiveIntegerField(
        blank=True,
        label='What is the annual income of your household? This includes money from jobs, net income from business, farm or rent, pensions, dividends, interest, social security payments and any other monetary income.',
        choices=[[0, 'Less than $10,000'],
                [1, '$10,000 to $29,999'],
                [2, '$30,000 to $49,999'],
                [3, '$50,000 to $69,999'],
                [4, '$70,000 to $99,999'],
                [5, '$100,000 to $149,999'],
                [6, '$150,000 to $199,999'],
                [7, 'More than $200,000'],
                [8, 'Prefer not to answer']],
        widget=widgets.RadioSelect)
    percentProlific = models.PositiveIntegerField(
        blank=True,
        label='How much of your total personal income comes from work on Prolific?',
        choices=[[0, 'A little bit'],
                [1, 'A substantial share but less than half'],
                [2, 'Most of my income'],
                [3, 'All of my income'],
                [4, 'Prefer not to answer']],
        widget=widgets.RadioSelect)
    
    state = models.PositiveIntegerField(
        blank=True,
        choices=[[0, 'Not USA'], [1, 'Alabama'], [2, 'Alaska'], [3, 'Arizona'], [4, 'Arkansas'], [5, 'California'],
                 [6, 'Colorado'], [7, 'Connecticut'], [8, 'Delaware'], [9, 'Florida'], [10, 'Georgia'], [11, 'Hawaii'],
                 [12, 'Idaho'], [13, 'Illinois'], [14, 'Indiana'], [15, 'Iowa'], [16, 'Kansas'], [17, 'Kentucky'],
                 [18, 'Louisiana'], [19, 'Maine'], [20, 'Maryland'], [21, 'Massachusetts'], [22, 'Michigan'],
                 [23, 'Minnesota'], [24, 'Mississippi'], [25, 'Missouri'], [26, 'Montana'], [27, 'Nebraska'],
                 [28, 'Nevada'], [29, 'New Hampshire'], [30, 'New Jersey'], [31, 'New Mexico'], [32, 'New York'],
                 [33, 'North Carolina'], [34, 'North Dakota'], [35, 'Ohio'], [36, 'Oklahoma'], [37, 'Oregon'],
                 [38, 'Pennsylvania'], [39, 'Rhode Island'], [40, 'South Carolina'], [41, 'South Dakota'],
                 [42, 'Tennessee'], [43, 'Texas'], [44, 'Utah'], [45, 'Vermont'], [46, 'Virginia'], [47, 'Washington'],
                 [48, 'West Virginia'], [49, 'Wisconsin'], [50, 'Wyoming']], label='Which state do you live in?')

    feedback = models.LongStringField(blank=True)
    
    
# FUNCTIONS 

def create_incremented_array(start, end, increment, callback):
    array = []
    i = start
    while i <= end:
        array.append(callback(i))
        i += increment
    return array

def labels(subsession):
    first_array =  create_incremented_array(C.START_VALUE, C.END_VALUE, C.INCREMENT_VALUE, lambda i: i)
    return ["{:.2f}".format(num) for num in first_array]

def bar_heights(subsession):
    first_array= create_incremented_array(C.START_VALUE, C.END_VALUE, C.INCREMENT_VALUE, lambda i: math.exp(-1 * i))
    sum_value = sum(first_array)
    target_mass = 1-len(first_array)/C.NUM_BOXES
    ratio = target_mass / sum_value
    first_array = [value * ratio for value in first_array]
    added_mass = 1/C.NUM_BOXES
    first_array = [value +added_mass for value in first_array]
    return manipulate_array(first_array,C.NUM_BOXES)


def manipulate_array(array, total_sum):
    # Step 1: Calculate the sum of all elements
    sum_value = sum(array)

    # Step 2: Calculate the ratio
    ratio = total_sum / sum_value

    # Step 3: Multiply each element by the ratio
    multiplied_array = [value * ratio for value in array]

    # Step 4: Round each element to the nearest integer
    rounded_array = [round(value) for value in multiplied_array]

    # Step 5: Adjust rounding errors
    rounded_sum = sum(rounded_array)
    difference = total_sum - rounded_sum

    if difference > 0:
        # Rounded sum is too small, find elements where rounded number is the most smaller than the actual number
        rounding_errors = [value - rounded_array[index] if value > rounded_array[index] else 0 for index, value in enumerate(multiplied_array)]
        adjustment = 1
    elif difference < 0:
        # Rounded sum is too large, find elements where rounded number is the most larger than the actual number
        rounding_errors = [rounded_array[index] - value if value < rounded_array[index] else 0 for index, value in enumerate(multiplied_array)]
        adjustment = -1
    else:
        # Rounded sum is already equal to total_sum, no adjustment needed
        return rounded_array

    # Sort rounding errors in descending order and find the indices of the largest ones
    largest_rounding_error_indices = sorted(range(len(rounding_errors)), key=lambda i: rounding_errors[i], reverse=True)[:abs(difference)]

    # Split the difference equally among the elements with the largest rounding errors
    adjusted_array = [value + (adjustment if index in largest_rounding_error_indices else 0) for index, value in enumerate(rounded_array)]

    return adjusted_array


# PAGES
class Welcome(Page):
    @staticmethod
    def vars_for_template(player):
        player.participant.times = {}
        player.participant.times['start'] = time.time()
        pass 

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

    def vars_for_template(player):
        myLabels = json.dumps(labels(player.subsession))
        myHeights = json.dumps(bar_heights(player.subsession))
        return {
            'labels':myLabels,
            'dividedBarHeights': myHeights            
        }
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Payment_bonus'


class Payment_P(Page):
    @staticmethod
    def vars_for_template(player):
        myLabels = json.dumps(labels(player.subsession))
        myHeights = json.dumps(bar_heights(player.subsession))
        return {
            'labels':myLabels,
            'dividedBarHeights': myHeights,
            'base_payment':  C.START_VALUE + C.END_VALUE
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
                'payment_P':f"Your answer is incorrect. Your total payment for completing this study consists of the base payment of ${C.START_VALUE + C.END_VALUE} minus a penalty, and no bonus payment.",
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
        
    def before_next_page(player, timeout_happened):
        player.participant.times['start_task'] = time.time()
        pass 

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
                'payment_B':f"Your answer is incorrect. Your total payment for completing this study consists of the payment from opening the boxes, and there is no penalty charge or bonus payment.",
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
        
    def before_next_page(player, timeout_happened):
        player.participant.times['start_task'] = time.time()
        pass 
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
            player.payoff=C.START_VALUE
        else:
            player.payoff = max(json.loads(player.participant.sequence)[:payoff])
        player.participant.times['end_task'] = time.time()
        player.participant.num_draws = player.num_draws
        pass 

    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Task'
    

class Diagnostic(Page):
    form_model = 'player'
    form_fields = ['expected_bonus']


    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
        
            def is_valid_number_range(string, x, y):
                try:
                    number = float(string)
                    if x <= number <= y:
                        decimal_count = len(string.split('.')[-1])
                        return decimal_count <= 2
                except ValueError:
                    return False

                return False

   
            if values['expected_bonus'] is None:
                return {'expected_bonus':'Please answer the question.'}
            else:
                if is_valid_number_range(values['expected_bonus'], C.START_VALUE, C.END_VALUE):
                    return {}
                else:
                    return {'expected_bonus':f'Please enter a dollar amount  between ${C.START_VALUE} and ${C.END_VALUE} with at most two decimals points.'}
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.expected_bonus = player.expected_bonus
        pass

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Diagnostic'



class Feedback(Page):
    form_model = 'player'
    form_fields = [ 'feedback']   

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.feedback = player.feedback
        pass

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Feedback'
    
class Finished(Page):

    @staticmethod
    def vars_for_template(player):
        player.participant.times['finished'] = time.time()

        part1 = F"You will receive your payment of {player.participant.payoff_plus_participation_fee()}" 
        part2 = ""
        if player.participant.treatment=="penalty":
            part2 = F" consisting of the ${C.START_VALUE + C.END_VALUE} base payment minus the penalty of {C.START_VALUE + C.END_VALUE - player.participant.payoff_plus_participation_fee()}"
        part3 = " shortly."
        return {'payment_message': part1 + part2 + part3}

  

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Finished'

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'ethnic', 'age','education', 'marital', 'income', 'percentProlific','state']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            
            error_messages = {}
            for field_name in ['gender', 'ethnic', 'age','education', 'marital', 'income', 'percentProlific','state']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'
                      
            return error_messages
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.demographics = {}
        for el in ['gender', 'ethnic', 'age','education', 'marital', 'income', 'percentProlific','state']:
            player.participant.demographics[el] = player.__dict__[el]
            
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.experiment_sequence[player.round_number - 1] == 'Demographics'

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
    Diagnostic,
    Demographics,
    Feedback,
    Finished
]
