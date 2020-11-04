import pandas as pd
import random

class VideoPoker:
    def __init__(self):
        self.deck = []
        self.bankroll = 0
        self.mise = 0
        self.resultat = 0

    def init_deck(self):
        self.deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']
        return self.deck

    def decks(self):
        return self.deck

    def get_bankroll(self):
        return self.bankroll

    def get_mise(self):
        return self.mise

    def get_resultat(self):
        return self.resultat

    def set_bankroll(self, value):
        self.bankroll = value

    def set_mise(self, value):
        self.mise = value

    def premier_tirage(self):
        tirage = random.sample(self.deck, 5)

        for item in tirage:
            self.deck.remove(item)

        return tirage, self.deck


    def choix_carte(self,tirage):

        remove_card = []

        for item in tirage:
            print('Voulez-vous garder cette carte y/n : ', item)
            bol = input()

            if (bol == 'n'):
                remove_card.append(item)

        for item in remove_card:
            tirage.remove(item)

        return tirage

    def deuxieme_tirage(self,jeu):
        if (len(jeu) < 5):
            remaining = random.sample(self.deck, 5 - len(jeu))
            for item in remaining:
                jeu.append(item)

        return jeu

    def machine(self,choice):
        jeu = self.deuxieme_tirage(choice)

        return jeu

    def is_consecutive(self,jeu):
        return sorted(jeu) == list(range(min(jeu), max(jeu) + 1))

    def set_card(self, card_list):
        for i in range(0, len(card_list)):
            if card_list[i] == 'J':
                card_list[i] = 11

            if card_list[i] == 'Q':
                card_list[i] = 12

            if card_list[i] == 'K':
                card_list[i] = 13

            if (card_list[i] == 'A'):
                card_list[i] = 14

            card_list[i] = int(card_list[i])

    def is_win(self,jeu):
        multiply = 0
        msg = "Vous avez perdu votre mise"
        card_list = []
        color_list = []
        royal = [10, 11, 12, 13, 14]

        for item in jeu:
            card, color = item.split('-')

            card_list.append(card)
            color_list.append(color)

            duplicates_color = pd.Series(color_list).value_counts()
            duplicates_card = pd.Series(card_list).value_counts()

        self.set_card(card_list)

        for i in range(0, len(duplicates_card)):
            if duplicates_card[i]!=1:
                if duplicates_card[i] == 2:  # paire or double paire
                    msg = "Bravo vous avez obtenu un paire"
                    multiply += 1
                    if multiply == 2:
                        multiply += 1
                        msg = "Bien , vous avez un douple paire"


        for item in card_list:

            my_count = card_list.count(item)

            #if my_count == 2:  # paire or double paire
                #msg = "Bravo vous avez obtenu un paire"
                #multiply += 1
                #if multiply == 2:
                    #msg = "Bien , vous avez un douple paire"

            if my_count == 3:  # brelan
                multiply = 3
                msg = "Hola, vous avez eu un brelan"
                if multiply == 1:  # full
                    multiply = 9
                    msg = "Vous avez obtenu un full, continuez à jouer pour de meilleurs gain"

            if my_count == 4:
                multiply = 25
                msg = "Excellent votre carré !!!"

            if max(duplicates_color == 5):  # Flush
                multiply = 6
                msg = "Vous avez gangné, un flush bravo"

            print(card_list)
            if self.is_consecutive(card_list):  # quinte
                multiply = 4
                msg = "Vous venez de realiser un quinte"
                if max(duplicates_color == 5):  # Quinte Flush
                    multiply = 50
                    msg = "Vous venez de realiser un quinte flush"
                    if sorted(royal) == sorted(card_list):
                        multiply = 250
                        msg = "Mon respect mon roi, vous avez le jackpot, quinte flush royal"

        return multiply, msg

    def calcul_gain(self,jeu, mise):
        multiply, msg = self.is_win(jeu)
        return multiply * mise, msg

    def partie(self,hand):

        self.bankroll -= self.mise
        gain, msg = self.calcul_gain(hand, self.mise)
        self.bankroll += gain

        return self.bankroll, msg

    def video_poker(self,hand):

        self.resultat = self.bankroll
        self.bankroll, msg = self.partie(hand)

        return self.resultat, self.bankroll, msg


