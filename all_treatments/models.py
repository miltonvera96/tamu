from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from random import randint
from random import shuffle

author = 'Milton Aldair Vera Guzmán'

doc = """
“Experiment TAMU 2” developed by Human Behavior Lab of Texas A&M university (United States). 
"""


class Constants(BaseConstants):
    name_in_url = 'all_treatments'
    players_per_group = 2
    
    # Number of extra round that are going to be played 
    extra_rounds = 1

    # Number of first rounds that are going to be played 
    first_rounds = 2

    # total round to be played
    num_rounds = first_rounds + extra_rounds

    #Amount that will be paid for guessing the correct answer
    payment_correct_answer = 1

    #Amount that will be paid for participating in the experiment
    initial_earning = 10

    #treatmens that will 
    treatments = ['clear_signal', 'clear_signal_ecu', 'concealed_signal', 'concealed_signal_ecu']
    
    ## round when the player have been selected to play the extra round
    round_selected_plus = randint(1, num_rounds)
    ## round when the player have been selected to play the extra round
    round_selected_normal = randint(1, first_rounds)

    #This value is only used on treatments with the ECU treatments
    tax_change = 0.05    

    extra_round_t1 = randint(1,100)
    extra_round_t2 = randint(1,100)
    extra_round_t3 = randint(1,100)
    extra_round_t4 = randint(1,100)


class Subsession(BaseSubsession):


    def creating_session(self):

        groups = self.get_groups()
        count_groups = len(groups)

        index = 0

        #setting treatment to group accodind group_per_treatment variable
        for i in range(count_groups):
            if(index == len(Constants.treatments)):
                index = 0
            
            groups[i].treatment = Constants.treatments[index]
            index = index + 1

        # inside each treatment
        # index 0: player1
        # index 1: player2
        dic = {}
        for i in Constants.treatments:
            dic[i] = [[],[]]

        # matrix = self.get_group_matrix()
        for g in groups:
            if g.treatment in dic:
                # print("Get in ")
                for player in g.get_players():
                    player.treatment = g.treatment
                    dic[g.treatment][player.id_in_group - 1].append(player.id_in_subsession)
        
        new_structure = []

        print(dic)
        for key in dic:
            # print(dic[key])
            shuffle(dic[key][0])
            shuffle(dic[key][1])
            self.session.vars['num_' + key] = len(dic[key][0])

            for i in range(len(dic[key][0])):
                new_structure.append([dic[key][0][i], dic[key][1][i]])

        print("New Structure \n", new_structure)        
        self.set_group_matrix(new_structure)


        # self.group_randomly(fixed_id_in_group=True)


class Group(BaseGroup):
    treatment = models.StringField()
    pass    


class Player(BasePlayer):

    treatment = models.StringField()

    ## VARIABLES
    payment = models.IntegerField(initial=0,min=0, max=10)
    secret_number = models.IntegerField(initial=0, min=0, max=10)

    ## VARIABLES THAT ARE ASK TO PLAYERS
    reported_number = models.IntegerField(min=0, max=10)
    guessing_secret_number = models.IntegerField(min=0, max=10)
    guessing_players = models.IntegerField(min=0)

    selected = models.BooleanField(initial=False)

    final_payment = models.FloatField(initial=0.0, min=0)

    extra_payment = models.IntegerField(initial=0)

    num_players_by_treatment = models.IntegerField(initial=0)

    q1 = models.StringField(
        choices=['True', 'False'],
        doc="""First question from test of player 1""",
        widget=widgets.RadioSelect
    )

    q2 = models.LongStringField ()
    q3 = models.LongStringField()

    def role(self):
        if self.id_in_group == 1:
            return 'player1'
        else:
            return 'player2'


    def get_secret_number(self):
        number  = randint(1, 10)
        self.secret_number = number
