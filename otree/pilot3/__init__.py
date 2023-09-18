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
    numeric = [numbers[-1-i] for i in range(len(numbers))]+ [0]
    start = 0
    end = 8
    increment = .5
    numbers = np.arange(start + increment , end + increment, increment)
    rightText = rightText + [f'Pay ${"{:.2f}".format(float(numbers[i]))}' for i in range(len(numbers))]
    leftText = ['Complete Collabarative Job']*len(rightText)
    numeric = numeric + [-el for el in numbers]

    return (leftText,rightText,numeric)


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
    NAME_IN_URL = 'pilot3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MIN_TIME = 5
    MAX_TIME = 10
    AVERAGE_TIME = 15
     
    NUM_BOXES = 10000
    NUM_BOXES_SEQUENCE = 1000
    DELAY = 10
    BALANCE = 8
    PARTICIPATION_FEE = 2.50
    NUM_PRACTICE = 5
    NUM_FORCED_OPEN = 50
    PAYMENT_PART_2 = "0.50"
    PROBABILITY_PART_1 = .05
    START_VALUE = 2
    END_VALUE = 10
    INCREMENT_VALUE = 0.01

    START_VALUE_PENALTY = END_VALUE + START_VALUE
    MAX_PAY = BALANCE + END_VALUE - START_VALUE
    
    READ_ALL = 'pilot3/ReadAll.html'
    TWO_PARTS = 'pilot3/TwoParts.html'
    PAYMENT = 'pilot3/Payment.html'
    COLLABORATIVE_JOB = 'pilot3/CollaborativeJob.html'
    TASK_GENERAL = 'pilot3/TaskGeneral.html'
    BONUS = 'pilot3/Bonus.html'
    PENALTY = 'pilot3/Penalty.html'
    SUMMARY = 'pilot3/Summary.html'
    DEMAND_ELICIATION_INSTRUCTIONS = 'pilot3/DemandElicitationInstructions.html'
    PART2_INSTRUCTIONS = 'pilot3/Part2Instructions.html'

    height_constant = 50000

    CQ_TASKS = ['CQ_tasks_payment', 'CQ_tasks_demand_elicitation']
    CQ_STATES = ['CQ_states_payment', 'CQ_states_demand_elicitation']
    CQ_TIME_PERIODS = ['CQ_time_periods_payment', 'CQ_time_periods_demand_elicitation']

    LAEBELS = labels(START_VALUE, END_VALUE, INCREMENT_VALUE, lambda i: i)
    BAR_HEIGHTS = bar_heights(START_VALUE, END_VALUE, INCREMENT_VALUE, NUM_BOXES, lambda i: math.exp(-1.75 * i))

    LEFT_TEXT, RIGHT_TEXT, NUMERIC_WTP = create_DE_texts()

    NUM_DEMAND_ELICITATION_QUESTIONS = len(LEFT_TEXT)
    CONTROL_QUESTIONS = {
        'CQ_tasks_bonus': {
            'CQ_conditions_collaborative_job':(3,'Sorry, that is incorrect. You will complete the Job only if you decide to complete it, AND Part 1 is chosen for payment.'),
            'CQ_bonus_collabarotive_job_consists': (1,'Sorry, that is incorrect. The Collaborative Job consists of a bonus task completed by you, AND a penalty task completed by a computer.'),
            'CQ_bonus_collaboartive_job_payment': (3, 'Sorry, that is incorrect. If you complete the Collaborative Job, the bonus you earn in the bonus task will be added to your Part 1 payment, AND the penalty the computer earns in the penalty task will be taken away from this payment.'),
            'CQ_bonus_tentative_own': (1, 'Sorry, that is incorrect. Your tentative bonus can increase (if the bonus inside the box is larger than your current tentative bonus). Or it can stay the same (if the bonus inside the box is smaller than your current tentative bonus).'),
            'CQ_bonus_tentative_other': (2, 'Sorry, that is incorrect. Its tentative penalty can decrease (if the penalty inside the box is smaller than its current tentative penalty). Or it can stay the same (if the penalty inside the box is larger than its current tentative penalty).'),
        },
        'CQ_tasks_penalty': {
            'CQ_conditions_collaborative_job':(3,'Sorry, that is incorrect. You will complete the Job only if you decide to complete it, AND Part 1 is chosen for payment.'),
            'CQ_penalty_collabarotive_job_consists': (1,'Sorry, that is incorrect. The Collaborative Job consists of a penalty task completed by you, AND a bonus task completed by a computer.'),
            'CQ_penalty_collaboartive_job_payment': (3, 'Sorry, that is incorrect. If you complete the Collaborative Job, the penalty you earn in the penalty task will be taken away from your Part 1 payment, AND the bonus the computer earns in the bonus task will be added to this payment.'),
            'CQ_penalty_tentative_own': (2, 'Sorry, that is incorrect. Your tentative penalty can decrease (if the penalty inside the box is smaller than your current tentative penalty). Or it can stay the same (if the penalty inside the box is larger than your current tentative penalty).'),
            'CQ_penalty_tentative_other': (1, 'Sorry, that is incorrect. Its tentative bonus can increase (if the bonus inside the box is larger than its current tentative bonus). Or it can stay the same (if the bonus inside the box is smaller than its current tentative bonus).'),
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
                participant.anti_valence = [el for el in bonus_penalty if el != participant.valence][0]
                participant.high_payoff = participant.treatment[2]
                random_draw = random.random()
                participant.part_payment = 'Part 2'
                if C.PROBABILITY_PART_1 > random_draw:
                    participant.part_payment = 'Part 1'

                A = C.LAEBELS
                B = C.BAR_HEIGHTS

                new_list = [a for a, b in zip(A, B) for _ in range(b)]
                participant.sequence = {'penalty':json.dumps(random.sample(new_list, C.NUM_BOXES_SEQUENCE)),
                                        'bonus':json.dumps(random.sample(new_list, C.NUM_BOXES_SEQUENCE))}

                new_list = [a for a, b in zip(A, B) for _ in range(b)]
                participant.practice_sequence = {'penalty':json.dumps(random.sample(new_list, C.NUM_PRACTICE)),
                                        'bonus':json.dumps(random.sample(new_list, C.NUM_PRACTICE))}
                
                new_list = [a for a, b in zip(A, B) for _ in range(b)]
                participant.part2_sequence = {'penalty':json.dumps(random.sample(new_list, C.NUM_FORCED_OPEN)),
                                        'bonus':json.dumps(random.sample(new_list, C.NUM_FORCED_OPEN))}

                
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    confused_binary = models.StringField(
        blank=True,
        choices=[
            [1, 'Yes'],
            [0, 'No'],
        ],
        widget=widgets.RadioSelect,
        label='Was the procedure on the previous page confusing in any way?'
    )
        
    confused_text = models.LongStringField(blank=True)
     
    CQ_conditions_collaborative_job = models.IntegerField(
        blank=True,
        choices=[
            [1, 'If Part 1 is chosen for payment, I will complete the Job for sure regardless of my other decisions.'],
            [2, 'If I decide to complete the Job, I will complete it regardless of whether Part 1 is chosen for payment.'],
            [3, 'I will complete the Job only if I decide to complete it AND Part 1 is chosen for payment.'],
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
            [1, 'The bonus I earn in the bonus task will be added to my Part 1 payment.'],
            [2, 'The penalty the computer earns in the penalty task will be taken away from my Part 1 payment.'],
            [3, 'The bonus I earn in the bonus task will be added to my Part 1 payment, AND the penalty the computer earns in the penalty task will be taken away from this payment.'],
        ],
        widget=widgets.RadioSelect,
        label='How does completing the Collaborative Job affect your payment from Part 1?'
    )

    CQ_penalty_collaboartive_job_payment = models.IntegerField(
        blank=True,
        choices=[
            [1, 'The penalty I earn in the penalty task will be taken away from my Part 1 payment.'],
            [2, 'The bonus the computer earns in the bonus task will be added to my Part 1 payment.'],
            [3, 'The penalty I earn in the penalty task will be taken away from my Part 1 payment, AND the bonus the computer earns in the bonus task will be added to my Part 1 payment.'],
        ],
        widget=widgets.RadioSelect,
        label='How does completing the Collaborative Job affect your payment from Part 1?'
    )

    CQ_bonus_tentative_own = models.IntegerField(
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

    CQ_penalty_tentative_own = models.IntegerField(
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

    CQ_bonus_tentative_other = models.IntegerField(
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

    CQ_penalty_tentative_other = models.IntegerField(
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

    practice_data = models.StringField(blank=True)
    actual_data = models.StringField(blank=True)

    wtp = models.StringField(blank=True)
   
    feedback = models.LongStringField(blank=True)

    feedbackDifficulty = models.IntegerField(
        label="How clear were the instructions? Please answer on a scale of 1 to 10, with 10 being the clearest.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
        )
    
    feedbackUnderstanding = models.IntegerField(
        label="How well did you understand what you were asked to do? Please answer on a scale of 1 to 10, with 10 being the case when you understood perfectly.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
        )
    
    feedbackSatisfied = models.IntegerField(
        label="How satisfied are you with this study overall? Please answer on a scale of 1 to 10, with 10 being the most satisfied.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
        )
    
    feedbackPay = models.IntegerField(
        label="How appropriate do you think the payment for this study is relative to other ones on Prolific? Please answer on a scale of 1 to 10, with 10 being the most appropriate.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
        )
    
    sports = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='Your favorite sports team loses a game. How likely are you to actively avoid watching the match highlights and talking to your friends about the game?'
        )

    car = models.IntegerField(
        blank=True,
        choices=likelihood_scale(),
        widget=widgets.RadioSelect,
        label='After buying a car, your bank account balance is low. If you know that you have enough money to cover your day-to-day expenses, how likely are you to actively avoid checking your bank balance?'
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
        player.participant.times['time_started'] = time.time()
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
                question = field_name.split(f'CQ_{domain}_')[-1]
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'
                elif int(values[field_name]) != control_questions[question][0]:
                    error_messages[field_name] = control_questions[question][1]
                    player.participant.mistakes[field_name]+=1  

            return error_messages


class TransitionPractice(Page):
    pass


class Task(Page):
    form_model = 'player'  
    form_fields = ['practice_data']

    @staticmethod
    def vars_for_template(player):
        valence = player.participant.valence
        myLabels = json.dumps(C.LAEBELS)
        myHeights = json.dumps(C.BAR_HEIGHTS)
        reversed_dividedBarHeights = json.dumps(C.BAR_HEIGHTS[::-1])

        return {
            'top_labels':myLabels,
            'top_dividedBarHeights': myHeights,
            'bottom_labels':myLabels,
            'bottom_dividedBarHeights': reversed_dividedBarHeights,     
            'sequence':  json.dumps(player.participant.practice_sequence[valence])
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        practice_payoff = json.loads(player.practice_data)['tentative_bonus']
        player.participant.practice_payoff = practice_payoff


class TransitionDemandElicitation0(Page):
    @staticmethod
    def vars_for_template(player):
        valence = player.participant.valence
        anti_valence = player.participant.anti_valence

        # own_payoff = float(max(json.loads(player.participant.practice_sequence[valence])[:C.NUM_PRACTICE]))
        # computer_payoff = float(max(json.loads(player.participant.practice_sequence[anti_valence])[:C.NUM_PRACTICE]))

        own_payoff = player.participant.practice_payoff

        if valence == 'bonus':
            # computer_payoff = C.START_VALUE + C.END_VALUE - computer_payoff
            pass
        else:
            own_payoff = C.START_VALUE + C.END_VALUE - own_payoff   
            new_balance = C.START_VALUE_PENALTY - own_payoff


        
        # computer_payoff = "{:.2f}".format(computer_payoff)
        
        if type(own_payoff) != str:
            own_payoff = str(own_payoff)
        print(type(own_payoff),own_payoff) 
        if valence == 'bonus':
            text = "<p>In this practice round of the bonus task, <b>you found a tentative bonus of $" + own_payoff + " after opening " + str(C.NUM_PRACTICE) + " boxes</b>.</p> <p>Remember, Part 1 will be affect your balance of $0 for sure. Thus, your balance would have increased to $" + own_payoff +" if this was the real task. </p> <p>You will next do the real bonus task which will affect your balance. There, you can choose when to stop opening boxes.</p>"
        else:
            text = "<p>In this practice round of the penalty task, <b>you found a tentative penalty of $" + own_payoff + " after opening " + str(C.NUM_PRACTICE) + " boxes</b>.</p> <p>Remember, Part 1 will be affect your balance of $"+str(C.START_VALUE_PENALTY) + " for sure. Thus, your balance would have decreased to $" + f'{new_balance:.2f}' +" if this was the real task. Additionally, we will randomly choose whether Part 2 or Part 3 will affect your balance.</p> <p>You will next do the real penalty task which will affect your balance. There, you can choose when to stop opening boxes.</p>"
            
        return {
            'text':  text
        }


class TaskActual(Page):
    form_model = 'player'  
    form_fields = ['actual_data']

    @staticmethod
    def vars_for_template(player):
        valence = player.participant.valence
        myLabels = json.dumps(C.LAEBELS)
        myHeights = json.dumps(C.BAR_HEIGHTS)
        reversed_dividedBarHeights = json.dumps(C.BAR_HEIGHTS[::-1])

        return {
            'top_labels':myLabels,
            'top_dividedBarHeights': myHeights,
            'bottom_labels':myLabels,
            'bottom_dividedBarHeights': reversed_dividedBarHeights,     
            'sequence':  json.dumps(player.participant.sequence[valence])
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        actual_payoff = json.loads(player.actual_data)['tentative_bonus']
        player.participant.actual_payoff = actual_payoff
        


class TransitionDemandElicitation(Page):
    @staticmethod
    def vars_for_template(player):
        valence = player.participant.valence
        anti_valence = player.participant.anti_valence

        # own_payoff = float(max(json.loads(player.participant.practice_sequence[valence])[:C.NUM_PRACTICE]))
        # computer_payoff = float(max(json.loads(player.participant.practice_sequence[anti_valence])[:C.NUM_PRACTICE]))

        own_payoff = player.participant.actual_payoff
        
        if valence == 'bonus':
            # computer_payoff = C.START_VALUE + C.END_VALUE - computer_payoff
            pass
        else:
            own_payoff = C.START_VALUE + C.END_VALUE - own_payoff   
            new_balance = C.START_VALUE_PENALTY - own_payoff


        
        if type(own_payoff) != str:
            own_payoff = str(own_payoff)

        if valence == 'bonus':
            text = "<p>Your final tentative bonus is $" + own_payoff + "</b>.</p> <p>This bonus is now added to your balance of $0. Thus, your balance is now $" + own_payoff +".</p>"
        else:
            text = "<p>Your final tentative penalty is $" + own_payoff + "</b>.</p> <p>This penalty is now taken away from your balance of $"+str(C.START_VALUE_PENALTY)+". Thus, your balance is now $" + f'{new_balance:.2f}' +".</p>"
        return {
            'text':  text
        }


class TransitionDemandElicitation2(Page):

    @staticmethod
    def vars_for_template(player):
        myLabels = json.dumps(C.LAEBELS)
        myHeights = json.dumps(C.BAR_HEIGHTS)
        reversed_dividedBarHeights = json.dumps(C.BAR_HEIGHTS[::-1])

        return {
            'top_labels':myLabels,
            'top_dividedBarHeights': myHeights,
            'bottom_labels':myLabels,
            'bottom_dividedBarHeights': reversed_dividedBarHeights,     
            }


class DemandElicitation(Page):
    form_model = 'player'
    form_fields = ['wtp']

    @staticmethod
    def vars_for_template(player):
        myLabels = json.dumps(C.LAEBELS)
        myHeights = json.dumps(C.BAR_HEIGHTS)
        reversed_dividedBarHeights = json.dumps(C.BAR_HEIGHTS[::-1])
        numeric_WTP = json.dumps(C.NUMERIC_WTP)
        
        return {
            'leftText':  json.dumps(C.LEFT_TEXT),
            'rightText': json.dumps(C.RIGHT_TEXT),
            'top_labels':myLabels,
            'top_dividedBarHeights': myHeights,
            'bottom_labels':myLabels,
            'bottom_dividedBarHeights': reversed_dividedBarHeights,   
            'numeric_WTP': numeric_WTP
        }
    
    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            print(values)
            if values['wtp']=='':

                return {'wtp':'Please make your choices by clicking on the table below.'}


    @staticmethod
    def before_next_page(player, timeout_happened):
        wtp = json.loads(player.wtp)
        cutoff = wtp['cutoff']
        parts = cutoff.split(":")
        side = parts[0]
        row = int(parts[1])

        if side == "right":
            row = row +1
 
        large_number = 1
        if row <=0:
            player.participant.wtp = C.NUMERIC_WTP[0] + large_number
        elif row > len(C.NUMERIC_WTP) - 1:
            player.participant.wtp = C.NUMERIC_WTP[-1] - large_number
        else:
            player.participant.wtp = (C.NUMERIC_WTP[row] + C.NUMERIC_WTP[row-1])/ 2
        
        rows = [i for i in range(len(C.NUMERIC_WTP))]
        player.participant.random_row = random.choice(rows)
        player.participant.collaborative_job = (C.NUMERIC_WTP[player.participant.random_row] < player.participant.wtp) and (player.participant.part_payment == 'Part 1')

        question = 'Do you prefer <b>complete the Collaborative Job</b> OR <b>'+C.RIGHT_TEXT[player.participant.random_row]+'</b>?'
        player.participant.question = question
        player.participant.right_option = C.RIGHT_TEXT[player.participant.random_row]


class TransitionUnincentivized(Page):
    form_model = 'player'
    form_fields = [ 'confused_binary','confused_text']   

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            if values['confused_binary'] is None:

                return {'confused_binary': 'Please answer the question.'}

 
class UnincentivizedInstructions(Page):
    pass


class Unincentivized1(Page):
    form_model = 'player'
    form_fields = ['sports','car', 'illness','will']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            error_messages = {}
            questions = ['sports','car', 'illness','will']
            for field_name in questions:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'

            return error_messages


class Unincentivized2(Page):
    form_model = 'player'
    form_fields = ['vacation','lottery','date','portfolio']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            error_messages = {}
            questions = ['vacation','lottery','date','portfolio']
            for field_name in questions:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'

            return error_messages
        

class Unincentivized3(Page):
    form_model = 'player'
    form_fields = ['summary_bad','summary_good']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            error_messages = {}
            questions = ['summary_bad','summary_good']
            for field_name in questions:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'

            return error_messages


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        payment_text = player.participant.right_option 
        payment_text = payment_text.lower()
        return {'payment_text':payment_text}
    


class Feedback(Page):
    form_model = 'player'
    form_fields = [ 'feedback']   

    form_model = 'player'
    form_fields = ['feedback', 'feedbackDifficulty', 'feedbackUnderstanding', 'feedbackSatisfied', 'feedbackPay']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['dev_mode']:
            error_messages = {}
            for field_name in ['feedback', 'feedbackDifficulty', 'feedbackUnderstanding', 'feedbackSatisfied',
                               'feedbackPay']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question.'
            return error_messages


class TaskRandomlyChosen(Page):
    form_model = 'player'  

    @staticmethod
    def vars_for_template(player):
        valence = player.participant.valence
        return {
            'sequence':  json.dumps(player.participant.sequence[valence])
        }
    

    @staticmethod
    def is_displayed(player):
        return player.participant.collaborative_job


class AfterTaskRandomlyChosen(Page):
    form_model = 'player'  

    @staticmethod
    def vars_for_template(player):
        valence = player.participant.valence
        anti_valence = player.participant.anti_valence

        own_payoff = float(max(json.loads(player.participant.sequence[valence])[:C.NUM_FORCED_OPEN]))
        computer_payoff = float(max(json.loads(player.participant.sequence[anti_valence])[:C.NUM_FORCED_OPEN]))

        if valence == 'bonus':
            computer_payoff = C.START_VALUE + C.END_VALUE - computer_payoff
        else:
            own_payoff = C.START_VALUE + C.END_VALUE - own_payoff   

        own_payoff = "{:.2f}".format(own_payoff)
        computer_payoff = "{:.2f}".format(computer_payoff)

        player.participant.payoff = float(C.PARTICIPATION_FEE) + float(C.BALANCE)
        if valence =='bonus':
            player.participant.payoff += float(own_payoff) - float(computer_payoff)
        else:
            player.participant.payoff += float(computer_payoff) - float(own_payoff)

        if valence == 'bonus':
            text = "<p>You have completed the Collaborative Job. The bonus you earned is $" + own_payoff + ". In the meantime, the computer earned a penalty of $" + computer_payoff + ".</p> <p>Since Part 1 is chosen, you also get a balance of $" + str(C.BALANCE) + ". Including the participation fee of $" + str(C.PARTICIPATION_FEE) + ", your total payment for the study is thus <b>$" + str(player.participant.payoff) + "</b>.</p>"
        else:
            text = "<p>You have completed the Collaborative Job. The penalty you earned is $" + own_payoff + ". In the meantime, the computer earned a bonus of $" + computer_payoff + ".</p> <p>Since Part 1 is chosen, you also get a balance of $" + str(C.BALANCE) + ". Including the participation fee of $" + str(C.PARTICIPATION_FEE) + ", your total payment for the study is thus <b>$" +  str(player.participant.payoff) + "</b>.</p>"
        
        return {
            'text':  text
        }
    
    @staticmethod
    def is_displayed(player):
        return player.participant.collaborative_job


class Finished(Page):
    @staticmethod
    def vars_for_template(player):
        
    
        if player.participant.part_payment == 'Part 2': 
            player.participant.payoff = C.PARTICIPATION_FEE + float(C.PAYMENT_PART_2)

        player.participant.bonus_payment = player.participant.payoff - C.PARTICIPATION_FEE
        return {}

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.times['time_finished'] = time.time()
        player.participant.finished = True 
        pass


class Redirect(Page):
    pass
    

page_sequence = [
    Welcome,
    Consent,
    Instructions,
    UnderstandingQuestions,
    TransitionPractice,
    Task,
    TransitionDemandElicitation0,
    TaskActual,
    TransitionDemandElicitation,
    TransitionDemandElicitation2,
    TransitionDemandElicitation3,
    DemandElicitation,
    TransitionUnincentivized,
    UnincentivizedInstructions,
    Unincentivized1,
    Unincentivized2,
    Unincentivized3,
    Results, 
    TaskRandomlyChosen,
    AfterTaskRandomlyChosen,
    Feedback,
    Finished,
    Redirect
]