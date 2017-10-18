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

def get_info(data, debug):
    
    table_card = [Card.new(_[0]+_[1].lower())  for _ in  data['game']['board']] 
    self_card = [Card.new(_[0]+_[1].lower())  for _ in  data['self']['cards']] 
    round_count = data['game']['roundCount']
    n_player = len(data['game']['players'])
    s_player = 0
    s_player_bit = []
    self_bit = data['self']['chips']
    
    for n, i in enumerate(data['game']['players']):
        print i
        if i['isSurvive'] is True:
            s_player+=1
            s_player_bit.append(i['chips'])  
    rank = get_rank(s_player, s_player_bit, self_bit)

    if debug:
        print "======= {r} =======".format(r=round_count)
        print round_count
        print n_player
        print s_player
        print s_player_bit
        Card.print_pretty_cards(table_card + self_card)
        print "======= {r} =======".format(r=round_count)
    return table_card , self_card, rank, s_player, round_count
    
def get_betCount(data):
    return data['game']['betCount']


def ai_action(data, debug = False):

    table_card , self_card, rank, s_player, round_count = get_info(data, debug = debug)
    betCount = get_betCount(data)
    gamma = 0
    beta = 0

    
    if round_count > 5 and rank > 5:
        gamma = 1000
        beta = 2000
    if rank > 7:
        beta = 2000

    print "Survive player : {n}".format(n = s_player)
    print "Sparrow ranking: {n}".format(n = rank)
    
    if len(table_card + self_card) >= 5:
        evaluator = Evaluator()
        pscore = evaluator.evaluate(table_card, self_card)
        pclass = evaluator.get_rank_class(pscore)
        print "Sparrow hand rank = %d (%s)\n" % (pscore, evaluator.class_to_string(pclass))
        
        if pscore > 6000 + beta:
            return "fold"
        elif pscore > 5000 + gamma:
            return "call"
        elif pscore > 2000 + gamma:
            return "raise"
        else:
            return "allin"
            
    elif betCount > 500:
        return "fold"
    else:
        return "call"
    
    