# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 21:44:40 2017

@author: 69390
"""
import sys
sys.path.append(r"C:\Users\69390\Desktop\texas-holdem")
from deuces import Evaluator
from deuces import Card


def get_rank(s_player, s_player_bit, self_bit):
    xx = sorted(s_player_bit, reverse = True)
    print xx
    print self_bit
    rank = xx.index(self_bit)
    return rank


def get_card(data):
    table_card = [Card.new(_[0]+_[1].lower())  for _ in  data['game']['board']] 
    self_card = [Card.new(_[0]+_[1].lower())  for _ in  data['self']['cards']] 
    return table_card, self_card

def get_player(data):
    
    
    round_count = data['game']['roundCount']
    #n_player = len(data['game']['players'])
    s_player = 0
    s_player_bit = []
    self_bit = data['self']['chips']
    
    for n, i in enumerate(data['game']['players']):
        print i
        if i['isSurvive'] is True:
            s_player+=1
            s_player_bit.append(i['chips'])  
    rank = get_rank(s_player, s_player_bit, self_bit)

    return  rank, s_player, round_count
    
def get_betCount(data):
    return data['game']['betCount']

def get_minBet(data):
    return data['self']['minBet']

def ai_action(data, debug = False):

    rank, s_player, round_count = get_player(data)
    table_card , self_card =  get_card(data)
    betCount = get_betCount(data)
    min_bet = get_minBet(data)
    print "Survive player : {n}".format(n = s_player)
    print "Sparrow ranking: {n}".format(n = rank)    
    print "Total BetCount : {n}".format(n = betCount)    
    print "min_bet        : {n}".format(n = min_bet)
    
    gamma = 0
    beta = 0
    alpha = 0

    if rank < 3:
        alpha = - 1200
        gamma = - 1000
    '''
    if round_count > 5 and rank > 5:
        gamma += 1000
        beta += 1000
    
    if rank > 7:
        beta += 500
    '''
    if  min_bet > 200:
        gamma += -500
        beta += -500
    
    if  min_bet > 400:
        gamma += -1000
        beta += -500


    if len(table_card + self_card) >= 5:
        evaluator = Evaluator()
        pscore = evaluator.evaluate(table_card, self_card)
        pclass = evaluator.get_rank_class(pscore)
        print "Sparrow hand rank = %d (%s)\n" % (pscore, evaluator.class_to_string(pclass))
        
        if pscore > 6000 + beta:
            return "fold"
        elif pscore > 4000 + gamma:
            return "call"
        elif pscore > 2000 + alpha:
            return "raise"
        else:
            return "allin"
            
    elif round_count<10 and min_bet > 300:
        return "fold"
    else:
        return "call"
    
    