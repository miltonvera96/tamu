from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from random import randint

class Introduction(Page):
    def is_displayed(self):
            return self.round_number == 1
    
    def vars_for_template(self):

        ten = '10 ECU'

        if self.player.treatment in ['clear_signal_ecu', 'concealed_signal_ecu']:
            ten = '10 ECU'

        return{
            'ten' : ten
        }

class Screen0(Page):
    def is_displayed(self):
            return self.round_number == 1

class Screen1(Page):
    def is_displayed(self):
        return self.round_number == 1
    
    def vars_for_template(self):

        ten = '10 ECU'

        if self.player.treatment in ['clear_signal_ecu', 'concealed_signal_ecu']:
            ten = '10 ECU'

        return{
            'ten' : ten
        }

## INITIAL INSTRUCTIONS FOR PLAYER 1 AND PLAYER 2
class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        one = '1 ECU'
        two = '2 ECU'
        eigth = '8 ECU'
        ten = '10 ECU'
        sub = '10 - 2'
        sub2 = '10 - 8'

        if self.player.treatment in ['clear_signal_ecu', 'concealed_signal_ecu']:
            one = '1 ECU'
            two = '2 ECU'
            eigth = '8 ECU'
            ten = '10 ECU'
            sub = '10 - 2'
            sub2 = '10 - 8'

        return{
            'one' : one,
            'two' : two,
            'eigth' : eigth,
            'ten' : ten,
            'sub' : sub,
            'sub2' : sub2,
        }


## SCREEN 3S - PLAYER 1
class Player1_1(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number == 1

    form_model = 'player'
    form_fields = ['q1']

    def q1_error_message(self, value):
        if value == 'True':
            return 'The answer is False. You can report any amount'
    
    def before_next_page(self):
        self.player.secret_number = randint(1, 10)

class ExtraRoundWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number > Constants.first_rounds

    def after_all_players_arrive(self):
    
        print(Constants.extra_round_t1, Constants.extra_round_t2, Constants.extra_round_t3, Constants.extra_round_t4)
        for p in self.subsession.get_players():
            if p.treatment == 'clear_signal' and Constants.extra_round_t1 <= 25:
                p.selected  = True
            if p.treatment == 'clear_signal_ecu' and Constants.extra_round_t2 <= 25:
                p.selected  = True
            if p.treatment == 'concealed_signal' and Constants.extra_round_t3 <= 25:
                p.selected  = True
            if p.treatment == 'concealed_signal_ecu' and Constants.extra_round_t4 <= 25:
                p.selected  = True


class NewRound(Page):
    def is_displayed(self):
        if(1 < self.round_number <= Constants.first_rounds):
            return True
        else:
            return self.player.selected 

    def vars_for_template(self):
        return{
            'round_number_next': self.round_number,
            'treatment' : self.player.treatment,
            'id_subsession': self.player.id_in_subsession
        }
    pass


## SCREEN 4S - PLAYER 1
class Player1_2(Page):
    def is_displayed(self):
        if(self.round_number <= Constants.first_rounds):
            return self.player.id_in_group == 1
        else:
            return self.player.id_in_group == 1 and self.player.selected

    def vars_for_template(self):

        return {
            'secret_number' : self.player.secret_number,
            'round' : self.round_number,
            'treatment' : self.player.treatment,
            'id_subsession': self.player.id_in_subsession,
            'left_rounds' : Constants.num_rounds - 1
            }

## SCREEN 5S - PLAYER 1
class Player1_3(Page):
    def is_displayed(self):
        if(self.round_number <= Constants.first_rounds):
            return self.player.id_in_group == 1
        else:
            return self.player.id_in_group == 1 and self.player.selected

    form_model = 'player'
    form_fields = ['reported_number']


class PaymentWaitPage(WaitPage):

    def is_displayed(self):
        if(self.round_number <= Constants.first_rounds):
            return True
        else:
            return self.player.selected 

    def after_all_players_arrive(self):
        player1 = self.group.get_player_by_role('player1')
        player2 = self.group.get_player_by_role('player2')

        if player1.reported_number is not None:
            player1.payment = 10 - player1.reported_number
        
        player2.payment = player1.reported_number
        player2.secret_number = player1.secret_number
        player2.reported_number = player1.reported_number
    

## SCREEN 6S - PLAYER 1
class Payment(Page):

    def is_displayed(self):
        if(self.round_number <= Constants.first_rounds):
            return True
        else:
            return self.player.selected 

    def vars_for_template(self):

        left_rounds = Constants.num_rounds - 1
        if(self.player.round_number == Constants.num_rounds):
            left_rounds = Constants.num_rounds

        return {
            'round' : self.round_number,
            'treatment' : self.player.treatment,
            'left_rounds' : left_rounds
            }


class GuessingNumber(Page):
    def is_displayed(self):
        if(self.round_number <= Constants.first_rounds):
            return self.player.id_in_group == 2
        else:
            return self.player.id_in_group == 2 and self.player.selected 

    form_model = 'player'
    form_fields = ['guessing_secret_number', 'guessing_players']

    def guessing_players_error_message(self, value):
        players = int(self.player.session.vars['num_' + self.player.treatment])

        if value > players:
            return 'The number is greater than the actual number of players. You can report any amount'

    def vars_for_template(self):
        players = int(self.player.session.vars['num_' + self.player.treatment])

        return{
            'number_players' : players
        }

class Next(Page):
    def is_displayed(self):
        if(1 < self.round_number <= Constants.first_rounds):
            return True
        else:
            return self.player.selected 

class NewRoundWaitPage(WaitPage):
    wait_for_all_groups = True 

    def is_displayed(self):
        if(self.round_number <= Constants.first_rounds):
            return True
        else:
            return self.player.selected 

    def after_all_players_arrive(self):
        player1_truth = {}
        for i in Constants.treatments:
            player1_truth[i] = 0

        for p in self.subsession.get_players():
            if(p.id_in_group == 1):
                if p.in_round(self.round_number).reported_number == p.in_round(self.round_number).secret_number:
                    player1_truth[p.treatment] = player1_truth[p.treatment] + 1

        print(player1_truth)

        for p in self.subsession.get_players():
            if(p.id_in_group == 2):
                if(p.guessing_players == player1_truth[p.treatment]):
                    p.extra_payment = p.extra_payment + 1
                if(p.guessing_secret_number == p.secret_number):
                    p.extra_payment = p.extra_payment + 1         

        if(self.round_number < Constants.num_rounds):
            for g in self.subsession.get_groups():
                player1 = g.get_player_by_role('player1')
                player1.in_round(self.round_number + 1).get_secret_number()


class FinalPaymentWaitPage(WaitPage):
    wait_for_all_groups = True 

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        print("@@Constants.round_selected_normal:", Constants.round_selected_normal)
        print("@@Constants.round_selected_plus:", Constants.round_selected_plus)

        for p in self.subsession.get_players():
            if p.treatment in ['clear_signal_ecu', 'concealed_signal_ecu']:
                for pr in p.in_all_rounds():
                    print(p.treatment, pr.round_number, p.id_in_group)
                    print(p.final_payment,  pr.payment, pr.extra_payment)
                    p.final_payment = p.final_payment + pr.payment + pr.extra_payment
                p.final_payment = Constants.initial_earning + (p.final_payment * Constants.tax_change) 
            else:
                if p.selected:
                    p.final_payment = Constants.initial_earning + p.in_round(Constants.round_selected_plus).payment + p.in_round(Constants.round_selected_plus).extra_payment
                    p.participant.vars["round_selected"] = Constants.round_selected_plus

                else:
                    p.final_payment = Constants.initial_earning + p.in_round(Constants.round_selected_normal).payment + p.in_round(Constants.round_selected_normal).extra_payment
                    p.participant.vars["round_selected"] = Constants.round_selected_normal
            
            p.participant.vars['final_payment'] = p.final_payment
            p.participant.vars['treatment'] = p.treatment



class FinalPayment(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        return{
            'reported_number' : 10 - self.player.final_payment
        }

class Questions(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    form_model = 'player'
    form_fields = ['q2', 'q3']



page_sequence = [
    Introduction,
    Screen0,
    Screen1,
    Instructions,
    Player1_1,
    ExtraRoundWaitPage,
    NewRound,
    Player1_2,
    Player1_3,
    PaymentWaitPage,
    Payment,
    GuessingNumber,
    Next,
    NewRoundWaitPage,
    FinalPaymentWaitPage,
    Questions
]
