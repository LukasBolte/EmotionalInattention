import random
import json
import itertools
import math
import re 
import time
import numpy as np
from collections import Counter

from otree.api import *

doc = """
Authors: 
Lukas Bolte (lukas.bolte@outlook.com)
Vlasta Rasocha 
"""



 
# FUNCTIONS 


def create_incremented_array(start, end, increment, callback):
    array = []
    i = start
    while i <= end:
        array.append(callback(i))
        i += increment
    return array

def labels(start,end,increment,callback):
    
    first_array =  create_incremented_array(start, end, increment, callback)

    return ["{:.2f}".format(num) for num in first_array]

def bar_heights(start, end, increment, num_boxes, callback):
    first_array= create_incremented_array(start, end, increment, callback)
    sum_value = sum(first_array)
    ratio = num_boxes / sum_value
    first_array = [value * ratio for value in first_array]
    step = 10
    for i in range(len(first_array)):
            if i %  step == 0:
                first_array[i] = max([1,first_array[i]])

    return manipulate_array(first_array,num_boxes)


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

def create_DE_texts():
    start = 0
    end = 10
    increment = .5
    numbers = np.arange(start + increment , end + increment, increment)
    rightText = [f'Get ${"{:.2f}".format(float(numbers[len(numbers)-1-i]))}' for i in range(len(numbers))] + [f'Get/Pay ${"{:.2f}".format(0)}'] 
    
    start = 0
    end = 8
    increment = .5
    numbers = np.arange(start + increment , end + increment, increment)


    rightText = rightText + [f'Pay ${"{:.2f}".format(float(numbers[i]))}' for i in range(len(numbers))]

    leftText = ['Complete Collabarative Job']*len(rightText)
    return (leftText,rightText)


def likelihood_scale():
    return [
        [1, 'Extremely likely'],
        [2, 'Likely'],
        [3, 'Somewhat likely'],
        [4, 'Somewhat unlikely'],
        [5, 'Unlikely'],
        [6, 'Extremely unlikely']
        ]

class C(BaseConstants):
    NAME_IN_URL = 'question2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MIN_TIME = 5
    MAX_TIME = 10
    MAX_PAY = 20
    NUM_BOXES = 10000
    NUM_DRAWS = 1000
    DELAY = 10
    BALANCE = 8
    PARTICIPATION_FEE = 2
    NUM_PRACTICE = 5
    NUM_FORCED_OPEN = 50
    PAYMENT_PART_2 = .50


    READ_ALL = 'question2/ReadAll.html'
    TWO_PARTS = 'question2/TwoParts.html'
    PAYMENT = 'question2/Payment.html'
    COLLABORATIVE_JOB = 'question2/CollaborativeJob.html'
    TASK_GENERAL = 'question2/TaskGeneral.html'
    BONUS = 'question2/Bonus.html'
    PENALTY = 'question2/Penalty.html'
    SUMMARY = 'question2/Summary.html'
    DEMAND_ELICIATION_INSTRUCTIONS = 'question2/DemandElicitationInstructions.html'

    height_constant = 50000

    START_VALUE = 2
    END_VALUE = 10
    INCREMENT_VALUE = 0.01

    CQ_TASKS = ['CQ_tasks_payment', 'CQ_tasks_demand_elicitation']
    CQ_STATES = ['CQ_states_payment', 'CQ_states_demand_elicitation']
    CQ_TIME_PERIODS = ['CQ_time_periods_payment', 'CQ_time_periods_demand_elicitation']

    LAEBELS = labels(START_VALUE, END_VALUE, INCREMENT_VALUE, lambda i: i)
    BAR_HEIGHTS = bar_heights(START_VALUE, END_VALUE, INCREMENT_VALUE, NUM_BOXES, lambda i: math.exp(-1.75 * i))

    LEFT_TEXT, RIGHT_TEXT = create_DE_texts()

    NUM_DEMAND_ELICITATION_QUESTIONS = len(LEFT_TEXT)
    CONTROL_QUESTIONS = {
        'CQ_tasks_bonus': {
            'CQ_conditions_collaborative_job':(3,'myHint'),
            'CQ_bonus_collabarotive_job_consists': (1,'myHint'),
            'CQ_bonus_collaboartive_job_payment': (3, 'myHint'),
            'CQ_bonus_tentative_bonus': (1, 'myHint'),
            'CQ_bonus_tentative_penalty': (2, 'myHint'),
        },
        'CQ_tasks_penalty': {
            'CQ_conditions_collaborative_job':(3,'myHint'),
            'CQ_penalty_collabarotive_job_consists': (1,'myHint'),
            'CQ_penalty_collaboartive_job_payment': (3, 'myHint'),
            'CQ_penalty_tentative_bonus': (1, 'myHint'),
            'CQ_penalty_tentative_penalty': (2, 'myHint'),
        },


        'CQ_states': {
            'payment':(1,'myHint'),
            'demand_elicitation':(2,'myHint')
        },
        'CQ_time_periods': {
            'payment':(1,'myHint'),
            'demand_elicitation':(2,'myHint')
        }
    }





    
   


# create a function 

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    
    
    for player in subsession.get_players():
        if subsession.round_number == 1:

            # create a list of treatments
            bonus_penalty = ['bonus','penalty']
            level_treatments = ['low'] # ['high','low']
            task_treatments = [('tasks',item1, item2) for item1 in bonus_penalty for item2 in level_treatments]
            states_treatments = [] # [('states',item1, 'NA') for item1 in bonus_penalty]
            time_treatments = [] # [('time_periods',item1, 'NA') for item1 in bonus_penalty]
            treatments = task_treatments + states_treatments + time_treatments
            random.shuffle(task_treatments)
            treatments = itertools.cycle(treatments)
            for player in subsession.get_players():
                participant = player.participant
                participant.treatment = next(treatments)
                participant.domain = participant.treatment[0]
                participant.valence = participant.treatment[1]
                participant.high_payoff = participant.treatment[2]

                # participant.experiment_sequence = ['Welcome','Consent','Introduction',f"Payment_{participant.treatment}",f"UnderstandingQuestions_{participant.treatment}","Task","Diagnostic","Demographics",'Feedback','Finished']

                # I have two lists: A and B. They have the same length. I want to create a third list that has element A[i] repeated B[i] times.
                # 

                # A = labels(player.subsession)
                # B = bar_heights(player.subsession)

                A = C.LAEBELS
                B = C.BAR_HEIGHTS
                new_list = [a for a, b in zip(A, B) for _ in range(b)]
                
                participant.sequence = json.dumps(random.sample(new_list, C.NUM_DRAWS))

                

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # expected_bonus = models.StringField(
    #     blank=True
    # )

    # num_draws = models.StringField()


    confused_binary = models.StringField(
        blank=True,
        choices=[
            [1, 'Yes.'],
            [0, 'No.'],
        ],
        widget=widgets.RadioSelect,
        label="Was the procedure on the previous page confusing in any way?"
    )
        

    confused_text = models.LongStringField(blank=True)

     
    CQ_conditions_collaborative_job = models.IntegerField(
        blank=True,
        choices=[
            [1, 'If Part 1 is chosen for payment, I will complete the Job for sure regardless of my other decisions.'],
            [2, 'If I decide to complete the Job, I will complete it regardless of whether Part 1 is chosen for payment.'],
            [3, 'I will complete the Job ONLY if I decide to complete it AND Part 1 is chosen for payment.'],
        ],
        widget=widgets.RadioSelect,
        label='What must happen for you to complete the Collaborative Job?'
    )

    CQ_bonus_collabarotive_job_consists = models.IntegerField(
        blank=True,
        choices=[
            [1, 'A bonus task completed by you, AND a penalty task completed by a computer.'],
            [2, 'A penalty task completed by you, AND a bonus task completed by a computer.'],
            [3, 'A bonus task completed by you ONLY.'],
            [4, 'A penalty task completed by a computer ONLY.'],
        ],
        widget=widgets.RadioSelect,
        label='What does the Collaborative Job consist of?'
    )

    CQ_penalty_collabarotive_job_consists = models.IntegerField(
        blank=True,
        choices=[
            [1, 'A penalty task completed by you, AND a bonus task completed by a computer.'],
            [2, 'A bonus task completed by you, AND a penalty task completed by a computer.'],
            [3, 'A penalty task completed by you ONLY.'],
            [4, 'A bonus task completed by a computer ONLY.'],
        ],
        widget=widgets.RadioSelect,
        label='What does the Collaborative Job consist of?'
    )


    CQ_bonus_collaboartive_job_payment = models.IntegerField(
        blank=True,
        choices=[
            [1, 'The bonus I earn in the bonus task ONLY.'],
            [2, 'The penalty the computer earns in the penalty task ONLY.'],
            [3, 'The bonus I earn in the bonus task MINUS the penalty the computer earns in the penalty task.'],
        ],
        widget=widgets.RadioSelect,
        label='What payment will you receive from the Collaborative Job if you complete it?'
    )


    CQ_penalty_collaboartive_job_payment = models.IntegerField(
        blank=True,
        choices=[
            [1, 'The bonus the computer earns in the bonus task ONLY.'],
            [2, 'The penalty I earn in the penalty task ONLY.'],
            [3, 'The bonus the computer earns in the bonus task MINUS the penalty I earn in the penalty task.'],
        ],
        widget=widgets.RadioSelect,
        label='What payment will you receive from the Collaborative Job if you complete it?'
    )





    CQ_bonus_tentative_bonus = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It can increase OR stay the same.'],
            [2, 'It can decrease OR stay the same.'],
            [3, 'It ALWAYS increases.'],
            [4, 'It ALWAYS stays the same.'],
            [5, 'It ALWAYS decreases.'],
        ],
        widget=widgets.RadioSelect,
        label='What can happen to your tentative bonus when you open a box in the bonus task?'
    )


    CQ_penalty_tentative_bonus = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It can increase OR stay the same.'],
            [2, 'It can decrease OR stay the same.'],
            [3, 'It ALWAYS increases.'],
            [4, 'It ALWAYS stays the same.'],
            [5, 'It ALWAYS decreases.'],
        ],
        widget=widgets.RadioSelect,
        label="What can happen to the computer's tentative bonus when it opens a boox in the bonus task?"
    )





    CQ_bonus_tentative_penalty = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It can increase OR stay the same.'],
            [2, 'It can decrease OR stay the same.'],
            [3, 'It ALWAYS increases.'],
            [4, 'It ALWAYS stays the same.'],
            [5, 'It ALWAYS decreases.'],
        ],
        widget=widgets.RadioSelect,
        label="What can happen to the computer's tentative penalty when it opens a box in the penalty task?"
    )



    CQ_penalty_tentative_penalty = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It can increase OR stay the same.'],
            [2, 'It can decrease OR stay the same.'],
            [3, 'It ALWAYS increases.'],
            [4, 'It ALWAYS stays the same.'],
            [5, 'It ALWAYS decreases.'],
        ],
        widget=widgets.RadioSelect,
        label='What can happen to your tentative penalty when your open a box in the penalty task?'
    )

    


    CQ_tasks_payment = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It is the payment from opening the boxes.'],
            [2, 'It is the payment from opening the boxes minus penalty charge and plus a bonus.']
        ],
        widget=widgets.RadioSelect,
        label='What is the total payment you get for completing this study?'
    )

    CQ_tasks_demand_elicitation = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It is the payment from opening the boxes.'],
            [2, 'It is the payment from opening the boxes minus penalty charge and plus a bonus.']
        ],
        widget=widgets.RadioSelect,
        label='What is the total payment you get for completing this study?'
    )


    CQ_states_payment = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It is the payment from opening the boxes.'],
            [2, 'It is the payment from opening the boxes minus penalty charge and plus a bonus.']
        ],
        widget=widgets.RadioSelect,
        label='STATES: What is the total payment you get for completing this study?'
    )

    CQ_states_demand_elicitation = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It is the payment from opening the boxes.'],
            [2, 'It is the payment from opening the boxes minus penalty charge and plus a bonus.']
        ],
        widget=widgets.RadioSelect,
        label='STATES: What is the total payment you get for completing this study?'
    )


    CQ_time_periods_payment = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It is the payment from opening the boxes.'],
            [2, 'It is the payment from opening the boxes minus penalty charge and plus a bonus.']
        ],
        widget=widgets.RadioSelect,
        label='TIME: What is the total payment you get for completing this study?'
    )

    CQ_time_periods_demand_elicitation = models.IntegerField(
        blank=True,
        choices=[
            [1, 'It is the payment from opening the boxes.'],
            [2, 'It is the payment from opening the boxes minus penalty charge and plus a bonus.']
        ],
        widget=widgets.RadioSelect,
        label='TIME: What is the total payment you get for completing this study?'
    )


    wtp = models.StringField(blank=True)



   
    feedback = models.LongStringField(blank=True)


    
    sports = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='Your favorite sports team loses a game. How likely are you to watch the match highlights and talk to your friends about the game?'
    )

    car = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='After buying a car, your bank account balance is low. If you know that you have enough money to cover your day-to-day expenses, how likely are you to check your bank balance?'
    )

    illness = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='You were recently tested for a serious medical illness. How likely are you to try and distract yourself from thinking about the results while you wait for them (for example by binge-watching TV shows)?'
    )

    will = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='Your parents want to discuss their will with you. They are currently in good health. How likely are you to try to avoid the conversation?'
    )

    vacation = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='You are excited to go on a vacation organized by a travel agency in a couple of months. You are familiar with the travel itinerary already. How likely are you to browse through it again?'
    )

    lottery = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='You buy a lottery ticket with a $5 million jackpot. How likely are you to imagine what you would spend the money on if you won?'
    )

    date = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='You go on a first date with someone you really like. How likely are you to daydream about what your potential relationship could look like?'
    )

    portfolio = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='You have an investment portfolio that you cannot alter for another 6 months. You receive a newsletter from your investment manager telling you that, due to good market conditions, the value of your portfolio has increased by 50% over the past month. How likely are you to log into your account to look at the value of your portfolio?'
    )

    summary_bad = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='Some people distract themselves from difficult or painful thoughts, even if there are useful lessons they could learn from them. Others embrace them. How would you describe yourself?'
    )

    summary_good = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='Some people spend a lot of time thinking about pleasant memories and looking forward to brighter prospects. Others focus on the here and know. How would you describe yourself?'
    )



    
   

# PAGES
class Welcome(Page):
    @staticmethod
    def vars_for_template(player):
        player.participant.times = {}
        player.participant.times['start'] = time.time()
        pass 


class Consent(Page):
    pass

class Introduction(Page):
    pass


class Instructions(Page):
    @staticmethod
    def vars_for_template(player):
        myLabels = json.dumps(C.LAEBELS)
        myHeights = json.dumps(C.BAR_HEIGHTS)
        reversed_dividedBarHeights = json.dumps(C.BAR_HEIGHTS[::-1])
        print(myHeights)
        print(reversed_dividedBarHeights)
        return {
            'top_labels':myLabels,
            'top_dividedBarHeights': myHeights,
            'bottom_labels':myLabels,
            'bottom_dividedBarHeights': reversed_dividedBarHeights,     
        }

class UnderstandingQuestions(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        domain = player.participant.domain
        valence = player.participant.valence
        control_questions = C.CONTROL_QUESTIONS[f"CQ_{domain}_{valence}"]
        questions = list(control_questions.keys())
        
        return questions

    @staticmethod
    def vars_for_template(player):
        myLabels = json.dumps(C.LAEBELS)
        myHeights = json.dumps(C.BAR_HEIGHTS)
        reversed_dividedBarHeights = json.dumps(C.BAR_HEIGHTS[::-1])
        print(myHeights)
        print(reversed_dividedBarHeights)
        return {
            'top_labels':myLabels,
            'top_dividedBarHeights': myHeights,
            'bottom_labels':myLabels,
            'bottom_dividedBarHeights': reversed_dividedBarHeights,     
        }
    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            domain = player.participant.domain
            valence = player.participant.valence
            control_questions = C.CONTROL_QUESTIONS[f"CQ_{domain}_{valence}"]
            
            questions = list(control_questions.keys())
            

            if 'mistakes' not in player.participant.vars.keys():
                player.participant.mistakes = {question:0 for question in questions}

            error_messages = {}
            for field_name in questions:
                print(control_questions)
                question = field_name.split(f'CQ_{domain}_')[-1]
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'
                elif int(values[field_name]) != control_questions[question][0]:
                    print(type(values[field_name]),type(control_questions[question][0]))
                    error_messages[field_name] = control_questions[question][1]
                    player.participant.mistakes[field_name]+=1    
            return error_messages
        
    # def before_next_page(player, timeout_happened):
    #     player.participant.times['start_task'] = time.time()
    #     pass 



class TransitionPractice(Page):
    pass



# class Payment_B(Page):
#     @staticmethod

#     def vars_for_template(player):
#         myLabels = json.dumps(labels(player.subsession))
#         myHeights = json.dumps(bar_heights(player.subsession))
#         return {
#             'labels':myLabels,
#             'dividedBarHeights': myHeights            
#         }
#     def is_displayed(player: Player):
#         return player.participant.experiment_sequence[player.round_number - 1] == 'Payment_bonus'


# class Payment_P(Page):
#     @staticmethod
#     def vars_for_template(player):
#         myLabels = json.dumps(labels(player.subsession))
#         myHeights = json.dumps(bar_heights(player.subsession))
#         return {
#             'labels':myLabels,
#             'dividedBarHeights': myHeights,
#             'base_payment':  C.START_VALUE + C.END_VALUE
#          }
    
#     def is_displayed(player: Player):
#         return player.participant.experiment_sequence[player.round_number - 1] == 'Payment_penalty'


# class UnderstandingQuestions_P(Page):
#     form_model = 'player'


#     form_fields = [ 'payment_P','penalty','increase_penalty', 'same_penalty', 'decrease_penalty']   

#     @staticmethod
#     def error_message(player, values):
#         if not player.session.config['dev_mode']:
            
#             solutions = {'payment_P':1 ,
#                              'penalty':1,
#                              'increase_penalty':False,
#                              'same_penalty':True,
#                              'decrease_penalty':True
#             }
#             hints = {
#                 'payment_P':f"Your answer is incorrect. Your total payment for completing this study consists of the base payment of ${C.START_VALUE + C.END_VALUE} minus a penalty, and no bonus payment.",
#                 'penalty':'You answer is incorrect. Your penalty corresponds to the smallest amount in any of the boxes you have opened.',
#                 'decrease_penalty':'You answer is incorrect. When you open another box, two things can happen. When the amount in the new box is more than or equal to the largest amount so far, your potential penalty stays the same. When the amount is less, then your penalty decreases (to the amount in the last box).'
#             }
#             if 'mistakes' not in player.participant.vars.keys():
#                 player.participant.mistakes={
#                     'payment_P':0,
#                     'penalty':0,
#                     'penalty_change':0
#             }

#             error_messages = {}
#             for field_name in ['payment_P','penalty']:
#                 if values[field_name] is None:
#                     error_messages[field_name] = 'Please answer the question.'
#                 elif values[field_name] != solutions[field_name]:
#                     error_messages[field_name] = hints[field_name]
#                     player.participant.mistakes[field_name]+=1            
#             penalty=['increase_penalty','same_penalty','decrease_penalty']

#             if all([values[field_name]==False for field_name in penalty]):
#                 error_messages['decrease_penalty']='Please select at least one to answer the question.'
#             elif any([values[field_name]!=solutions[field_name] for field_name in ['increase_penalty','same_penalty','decrease_penalty']]):
#                 error_messages['decrease_penalty']=hints['decrease_penalty']
#                 player.participant.mistakes['penalty_change']+=1

#             return error_messages
        
#     def before_next_page(player, timeout_happened):
#         player.participant.times['start_task'] = time.time()
#         pass 

#     def is_displayed(player: Player):
#         return player.participant.experiment_sequence[player.round_number - 1] == 'UnderstandingQuestions_penalty'
    

# class UnderstandingQuestions_B(Page):
#     form_model = 'player'
#     form_fields = [ 'payment_B','bonus','increase_bonus', 'same_bonus', 'decrease_bonus']   
 
#     @staticmethod
#     def error_message(player, values):
#         if not player.session.config['dev_mode']:
            
#             solutions = {
#                 'payment_B':1 ,
#                 'bonus':1,
#                 'increase_bonus':True,
#                 'same_bonus':True,
#                 'decrease_bonus':False
#             }
#             hints = {
#                 'payment_B':f"Your answer is incorrect. Your total payment for completing this study consists of the payment from opening the boxes, and there is no penalty charge or bonus payment.",
#                 'bonus':'You answer is incorrect. Your payment corresponds to the largest amount in any of the boxes you have opened.',
#                 'decrease_bonus':'You answer is incorrect. When you open another box, two things can happen. When the amount in the new box is less than or equal to the largest amount so far, your potential payment stays the same. When the amount is more, then your payment increases (to the amount in the last box).'
#             }
#             if 'mistakes' not in player.participant.vars.keys():

#                 player.participant.mistakes={
#                     'payment_B':0,
#                     'bonus':0,
#                     'bonus_change':0
#             }

#             error_messages = {}
#             for field_name in ['payment_B','bonus']:
#                 if values[field_name] is None:
#                     error_messages[field_name] = 'Please answer the question.'
#                 elif values[field_name] != solutions[field_name]:
#                     error_messages[field_name] = hints[field_name]
#                     player.participant.mistakes[field_name]+=1            
#             bonus=['increase_bonus','same_bonus','decrease_bonus']

#             if all([values[field_name]==False for field_name in bonus]):
#                 error_messages['decrease_bonus']='Please select at least one to answer the question.'
#             elif any([values[field_name]!=solutions[field_name] for field_name in ['increase_bonus','same_bonus','decrease_bonus']]):
#                 error_messages['decrease_bonus']=hints['decrease_bonus']
#                 player.participant.mistakes['bonus_change']+=1

#             return error_messages
        
#     def before_next_page(player, timeout_happened):
#         player.participant.times['start_task'] = time.time()
#         pass 
#     def is_displayed(player: Player):
#         return player.participant.experiment_sequence[player.round_number - 1] == 'UnderstandingQuestions_bonus'
    


class Task(Page):
    form_model = 'player'  

    @staticmethod
    def vars_for_template(player):
        return {
            'sequence':  json.dumps(player.participant.sequence)
        }
    
    # def before_next_page(player, timeout_happened):

    #     payoff = json.loads(player.num_draws)
    #     if payoff==0:
    #         player.payoff=C.START_VALUE
    #     else:
    #         player.payoff = max(json.loads(player.participant.sequence)[:payoff])
    #     player.participant.times['end_task'] = time.time()
    #     player.participant.num_draws = player.num_draws
    #     player.participant.bonus_payment = player.payoff - C.START_VALUE
    #     pass 

    # def is_displayed(player: Player):
    #     return player.participant.experiment_sequence[player.round_number - 1] == 'Task'
    

# class Diagnostic(Page):
    # form_model = 'player'
    # form_fields = ['expected_bonus']


    # @staticmethod
    # def error_message(player, values):
    #     if not player.session.config['dev_mode']:
        
    #         def is_valid_number_range(string, x, y):
    #             try:
    #                 number = float(string)
    #                 if x <= number <= y:
    #                     decimal_count = len(string.split('.')[-1])
    #                     return decimal_count <= 2
    #             except ValueError:
    #                 return False

    #             return False

   
    #         if values['expected_bonus'] is None:
    #             return {'expected_bonus':'Please answer the question.'}
    #         else:
    #             if is_valid_number_range(values['expected_bonus'], C.START_VALUE, C.END_VALUE):
    #                 return {}
    #             else:
    #                 return {'expected_bonus':f'Please enter a dollar amount  between ${C.START_VALUE} and ${C.END_VALUE} with at most two decimals points.'}
    
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     normalized_bonus = player.expected_bonus
    #     if player.participant.treatment == 'penalty':
    #         normalized_bonus = C.START_VALUE + C.END_VALUE - float(player.expected_bonus)
    #     player.participant.expected_bonus = normalized_bonus    
    #     pass

    # @staticmethod
    # def is_displayed(player: Player):
    #     return player.participant.experiment_sequence[player.round_number - 1] == 'Diagnostic'


class TransitionDemandElicitation(Page):
    pass

class TransitionDemandElicitation2(Page):
    pass

class DemandElicitation(Page):
    form_model = 'player'
    form_fields = ['wtp']


    @staticmethod
    def vars_for_template(player):
        
        

        myLabels = json.dumps(C.LAEBELS)
        myHeights = json.dumps(C.BAR_HEIGHTS)
        reversed_dividedBarHeights = json.dumps(C.BAR_HEIGHTS[::-1])
 
        

        return {
            'leftText':  json.dumps(C.LEFT_TEXT),
            'rightText': json.dumps(C.RIGHT_TEXT),

            'top_labels':myLabels,
            'top_dividedBarHeights': myHeights,
            'bottom_labels':myLabels,
            'bottom_dividedBarHeights': reversed_dividedBarHeights,   
        }
    
    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            print(values)
            if values['wtp']=='':

                return {'wtp':'Please make your choices by clicking on the table below.'}


class TransitionUnincentivized(Page):
    form_model = 'player'
    form_fields = [ 'confused_binary','confused_text']   

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            if values['confused_binary'] is None:
                return {'confused_binary': 'Please answer the question.'}


 
class UnincentivizedInstructions(Page):
    form_model = 'player'
    form_fields = ['confused_binary','confused_text']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            if values['confused_binary'] is None:
                return {'confused_binary': 'Please answer the question.'}



class Unincentivized(Page):
    form_model = 'player'
    form_fields = ['sports','car', 'illness','will','vacation','lottery','date','portfolio','summary_bad','summary_good']


    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            error_messages = {}
            questions = ['sports','car', 'illness','will','vacation','lottery','date','portfolio','summary_bad','summary_good']
            for field_name in questions:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'
            return error_messages
        






class Results(Page):
    pass



class Feedback(Page):
    form_model = 'player'
    form_fields = [ 'feedback']   

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.feedback = player.feedback
        pass






class Finished(Page):

    @staticmethod
    def vars_for_template(player):
        player.participant.times['finished'] = time.time()

        # part1 = F"You will receive your payment of {player.participant.payoff_plus_participation_fee()}" 
        # part2 = ""
        # if player.participant.treatment=="penalty":
        #     part2 = F" consisting of the ${C.START_VALUE + C.END_VALUE} base payment minus the penalty of {C.START_VALUE + C.END_VALUE - player.participant.payoff_plus_participation_fee()}"
        # part3 = " shortly."

        return {'payment_message': 'test'}



# class Demographics(Page):
#     form_model = 'player'
#     form_fields = ['gender', 'ethnic', 'age','education', 'marital', 'income', 'percentProlific','state']

#     @staticmethod
#     def error_message(player, values):
#         if not player.session.config['dev_mode']:
            
#             error_messages = {}pl
#             for field_name in ['gender', 'ethnic', 'age','education', 'marital', 'income', 'percentProlific','state']:
#                 if values[field_name] is None:
#                     error_messages[field_name] = 'Please answer the question.'
                      
#             return error_messages
    
#     @staticmethod
#     def before_next_page(player, timeout_happened):
#         player.participant.demographics = {}
#         for el in ['gender', 'ethnic', 'age','education', 'marital', 'income', 'percentProlific','state']:
#             player.participant.demographics[el] = player.__dict__[el]
            
#     @staticmethod
#     def is_displayed(player: Player):
#         return player.participant.experiment_sequence[player.round_number - 1] == 'Demographics'

# class Offer(Page):
#     form_model = 'group'
#     form_fields = ['kept']

#     def is_displayed(player):
#         return player.id_in_group == 1


# class ResultsWaitPage(WaitPage):
#     after_all_players_arrive = 'set_payoffs'


# class Results(Page):
#     @staticmethod
#     def vars_for_template(player):
#         group = player.group

#         return dict(payoff=player.payoff, offer=C.ENDOWMENT - group.kept)
    

page_sequence = [
    Welcome,
    Consent,
    # Introduction,
    Instructions,
    UnderstandingQuestions,
    TransitionPractice,
    Task,
    TransitionDemandElicitation,
    TransitionDemandElicitation2,
    DemandElicitation,
    TransitionUnincentivized,
    UnincentivizedInstructions,
    Unincentivized,
    Results, 
    Feedback,
    Finished
]
