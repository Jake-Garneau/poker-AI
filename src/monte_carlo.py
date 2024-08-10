import random
from pokerkit import Automation, NoLimitTexasHoldem
from deuces import Card, Deck
import copy
import numpy as np
import sys

sys.path.append('../src')
from get_stats import get_player_stats

PLAYER_ACTIONS_AGG = {
    'TAG': {'call': 15, 'raise': 70, 'fold': 15},
    'LAG': {'call': 25, 'raise': 60, 'fold': 15},
    'TP': {'call': 40, 'raise': 10, 'fold': 50},
    'LP': {'call': 50, 'raise': 10, 'fold': 40},
    'APPF': {'call': 40, 'raise': 30, 'fold': 30}
}

PLAYER_ACTIONS_PASS = {
    'TAG': {'call': 18, 'raise': 82},
    'LAG': {'call': 29, 'raise': 71},
    'TP': {'call': 80, 'raise': 20},
    'LP': {'call': 83, 'raise': 17},
    'APPF': {'call': 57, 'raise': 43}
}

def get_type_temp(player):
    return 'APPF'

def get_type(player):
    stats = get_player_stats(player)
    VPIP = stats[0]
    PFR = stats[1]
    AGG = stats[2]
    
    if VPIP >= 20 and VPIP <= 30 and PFR > 50 and AGG < 30:
        return 'APPF'  # Aggressive Pre-Flop, Passive Post-Flop
    elif VPIP >= 15 and VPIP <= 25 and PFR >= 10 and PFR <= 20 and AGG >= 30 and AGG <= 40:
        return 'TAG'
    elif VPIP >= 25 and VPIP <= 40 and PFR >= 20 and PFR <= 30 and AGG >= 40 and AGG <= 60:
        return 'LAG'
    elif VPIP >= 10 and VPIP <= 20 and PFR >= 5 and PFR <= 10 and AGG >= 10 and AGG <= 20:
        return 'TP'
    elif VPIP >= 30 and VPIP <= 40 and PFR >= 5 and PFR <= 10 and AGG >= 5 and AGG <= 10:
        return 'LP'

def betting_round(players, state):
    actions_taken = [False] * len(players)
    actions_required = [False] * len(players)
    while True:
        for i, p in enumerate(players):
            if players[i] == []:
                actions_taken[i] = True
                actions_required[i] = False
                continue
            if actions_taken[i] and not actions_required[i]:
                continue
            player_type = get_type_temp(p)
            if(actions_required[i]):
                actions = PLAYER_ACTIONS_AGG[player_type]
            else:
                actions = PLAYER_ACTIONS_PASS[player_type]
            action = random.choices(list(actions.keys()), weights=list(actions.values()), k=1)[0]
            if action == 'fold':
                state.fold()
                players[i] = []
            elif action == 'call':
                state.check_or_call()
            elif action == 'raise':
                state.complete_bet_or_raise_to()
                actions_taken = [False] * len(players)  # Reset actions for all players
                actions_required = [True] * len(players)  # Reset actions for all players
            actions_taken[i] = True
            actions_required[i] = False
        if (all(actions_taken) and not all(actions_required)):
            return players

def monte_carlo_1r(players, board):
    players_temp = copy.deepcopy(players)
    state = NoLimitTexasHoldem.create_state(
        (
            Automation.ANTE_POSTING,
            Automation.BET_COLLECTION,
            Automation.BLIND_OR_STRADDLE_POSTING,
            Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
            Automation.HAND_KILLING,
            Automation.CHIPS_PUSHING,
            Automation.CHIPS_PULLING,
            Automation.CARD_BURNING,
        ),
        True,  # Uniform antes?
        0,  # Antes
        (50, 100),  # Blinds or straddles
        300,  # Min-bet
        (10000),  # Starting stacks
        6,  # Number of players
    )

    for p in players_temp:
        state.deal_hole(p)
        
    for p in players_temp:
        state.check_or_call()
                
    state.deal_board(board[0] + board[1] + board[2])
    players_temp = betting_round(players_temp, state)
    
    if state.status:
        state.deal_board(board[3])
        players_temp = betting_round(players_temp, state)
        
    if state.status:
        state.deal_board(board[4])
        players_temp = betting_round(players_temp, state)
    
    return state.stacks
    
    
    

def deuces_random_fill(seat, hand, board, deck):
    hand = hand.split(' ')
    board = board.split(' ')
    
    deck.shuffle()
    for c in hand:
        deck.cards.remove(Card.new(c))
    for c in board:
        deck.cards.remove(Card.new(c))
    
    cards = [None] * 6
    cards[seat-1] = hand[0] + hand[1]
    for i in range(6):
        if i == seat-1:
            continue
        cards[i] = Card.int_to_str(deck.draw(1)) + Card.int_to_str(deck.draw(1))
        
    for i in range(5-len(board)):
        board.append(Card.int_to_str(deck.draw(1)))
    return cards, board

def monte_carlo_single(seat, hand, board, iter_per_hand, deck):
    final_stacks = np.zeros(6)
    for _ in range(iter_per_hand):
        players, full_board = deuces_random_fill(seat, hand, board, deck)
        stacks = monte_carlo_1r(players, full_board)
        final_stacks += stacks
    return final_stacks / iter_per_hand

def monte_carlo(seat, hand, board, total_iter, iter_per_hand):
    final_stacks = np.zeros(6)
    deck = Deck()
    
    for _ in range(total_iter):
        players, full_board = deuces_random_fill(seat, hand, board, deck)
        for _ in range(iter_per_hand):
            stacks = monte_carlo_1r(players, full_board)
            final_stacks += np.array(stacks)
    
    final_stacks = (final_stacks / (total_iter * iter_per_hand)) - 10000
    return np.round(final_stacks, 2)

def run_monte_carlo(args):
    return monte_carlo(*args)

'''
No Multiprocessing:
100,100: Execution time: 19.785251140594482 seconds
1000,100: dnf

With multiprocessing/np
100,100: Execution time: 4.774865388870239 seconds
1000,100: Execution time: 28.339681148529053 seconds

10000, 100: Execution time: 386.6325218677521 seconds
[ 44.5045  20.043  -61.2575  -0.9905  -1.9555  -0.3435]

10000, 50: Execution time: 148.79697823524475 seconds
[ 41.166   22.4975 -66.2135  -1.127    2.101    1.5775]

10000, 20: Execution time: 56.45469069480896 seconds
[ 43.862   21.0685 -64.4705  10.6925  -3.541   -7.611 ]
[ 39.376   24.4895 -62.427    2.8565  -6.4395   2.1415]

10000, 10: Execution time: 27.115662813186646 seconds
[ 38.0975  29.308  -65.817   -1.8495  -4.302    4.558 ]
[ 47.4135  26.902  -75.1895   3.257   -1.3435  -1.0415]

10000, 1: Execution time: 4.668900489807129 seconds
[ 29.7895  40.636  -68.899  -10.089    4.5935   3.969 ]
[ 41.084  42.632 -71.746  -5.106  -4.431  -2.433]
[ 38.8     25.623  -41.6515  -7.0375 -12.1715  -3.5625]

100000, 1: Execution time: 27.864699602127075 seconds
[ 44.4405  22.503  -65.881   -2.65    -2.1035   3.6885]
'''