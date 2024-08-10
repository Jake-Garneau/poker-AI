import json

with open('preflop_table.json', 'r') as f:
    table = json.load(f)

def sort_ranks(ranks):
    custom_order = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8,
                     'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    sorted_ranks = sorted(ranks, key=lambda rank: custom_order[rank])
    return sorted_ranks

def hand_to_key(hand):
    rank_mapping = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        'T': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
    }
    suits = {'c': 'C', 'd': 'D', 'h': 'H', 's': 'S'}
    
    cards = hand.split()
    ranks = [rank_mapping[card[0]] for card in cards]
    suits_in_hand = [suits[card[1]] for card in cards]
    
    sorted_ranks = sort_ranks(ranks)
    
    # Ensure that the key for pairs or other hands does not have extra characters
    if len(set(sorted_ranks)) == 1:  # All ranks are the same (pair or more)
        key = ''.join(sorted_ranks)
    else:
        suited = len(set(suits_in_hand)) == 1
        key = ''.join(sorted_ranks) + ('S' if suited else 'O')
    
    return key

def evaluate2(hand):
    key = hand_to_key(hand)
    score = table.get(key, 0)
    if score == 0:
        print(f'Key: {key} not found in table')
    return score
