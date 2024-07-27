import os
import re
import csv

def parse_pluribus_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    hands = data.split('\n\n')
    
    parsed_hands = []
    for hand in hands:
        hand_details = {
            'hand_id': '',
            'flop_cards': [],
            'turn_cards': [],
            'river_cards': [],
            'players': [],
            'hole_cards': {},
            'preflop_actions': [],
            'flop_actions': [],
            'turn_actions': [],
            'river_actions': [],
            'showdown_actions': [],
            'winners': []
        }
        
        hand_id = re.search(r'PokerStars Hand #(\d+):', hand)
        if hand_id:
            hand_details['hand_id'] = hand_id.group(1)
        
        flop_cards = re.search(r'\*\*\* FLOP \*\*\* \[(.*?)\]', hand)
        if flop_cards:
            hand_details['flop_cards'] = flop_cards.group(1).split()
            
        turn_card = re.search(r'\*\*\* TURN \*\*\* \[.*?\] \[(.*?)\]', hand)
        if turn_card:
            hand_details['turn_cards'] = [turn_card.group(1)]
        
        river_card = re.search(r'\*\*\* RIVER \*\*\* \[.*?\] \[.*?\] \[(.*?)\]', hand)
        if river_card:
            hand_details['river_cards'] = [river_card.group(1)]
        
        players = re.findall(r'Seat \d+: (\w+) \(\d+ in chips\)', hand)
        hand_details['players'] = players
        
        hole_cards = re.findall(r'Dealt to (\w+) \[(.*?)\]', hand)
        hand_details['hole_cards'] = {player: cards.split() for player, cards in hole_cards}
        
        lines = hand.split('\n')
        current_stage = 'preflop'
        collecting_showdown = False
        
        for line in lines:
            if re.match(r'^\*\*\* FLOP \*\*\*', line):
                current_stage = 'flop'
            elif re.match(r'^\*\*\* TURN \*\*\*', line):
                current_stage = 'turn'
            elif re.match(r'^\*\*\* RIVER \*\*\*', line):
                current_stage = 'river'
            elif re.match(r'^\*\*\* SHOWDOWN \*\*\*', line):
                current_stage = 'showdown'
                collecting_showdown = True
            elif re.match(r'^\*\*\* SUMMARY \*\*\*', line):
                current_stage = 'summary'
                collecting_showdown = False
            else:
                match = re.match(r'(\w+): (posts small blind|posts big blind|folds|calls|raises|bets|checks) ?(\d+)? ?(to \d+)?', line)
                uncalled_bet_match = re.match(r'Uncalled bet \((\d+)\) returned to (\w+)', line)
                if match or uncalled_bet_match:
                    if match:
                        action = {
                            'player': match.group(1),
                            'action': match.group(2),
                            'amount': match.group(3) if match.group(3) else '',
                            'to': match.group(4) if match.group(4) else ''
                        }
                    else:
                        action = {
                            'player': uncalled_bet_match.group(2),
                            'action': 'uncalled bet',
                            'amount': uncalled_bet_match.group(1),
                            'to': ''
                        }
                    if current_stage == 'preflop':
                        hand_details['preflop_actions'].append(action)
                    elif current_stage == 'flop':
                        hand_details['flop_actions'].append(action)
                    elif current_stage == 'turn':
                        hand_details['turn_actions'].append(action)
                    elif current_stage == 'river':
                        hand_details['river_actions'].append(action)
                    elif current_stage == 'showdown':
                        hand_details['showdown_actions'].append(action)

                if collecting_showdown:
                    match_showdown = re.match(r'(\w+): shows \[(.*?)\]', line)
                    if match_showdown:
                        hand_details['showdown_actions'].append({'player': match_showdown.group(1), 'cards': match_showdown.group(2)})
                
                match_winner = re.match(r'(\w+) collected (\d+\.?\d*) from pot', line)
                if match_winner:
                    hand_details['winners'].append({'player': match_winner.group(1), 'amount': match_winner.group(2)})
        
        parsed_hands.append(hand_details)
    
    return parsed_hands

def save_to_csv(parsed_hands, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = [
            'hand_id', 'flop_cards', 'turn_cards', 'river_cards',
            'players', 'hole_cards', 'preflop_actions', 'flop_actions',
            'turn_actions', 'river_actions', 'showdown_actions', 'winners'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for hand in parsed_hands:
            writer.writerow({
                'hand_id': hand['hand_id'],
                'flop_cards': ' '.join(hand['flop_cards']),
                'turn_cards': ' '.join(hand['turn_cards']),
                'river_cards': ' '.join(hand['river_cards']),
                'players': ', '.join(hand['players']),
                'hole_cards': ', '.join([f'{player}: {" ".join(cards)}' for player, cards in hand['hole_cards'].items()]),
                'preflop_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]} {action["to"]}'.strip() for action in hand['preflop_actions']]),
                'flop_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]} {action["to"]}'.strip() for action in hand['flop_actions']]),
                'turn_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]} {action["to"]}'.strip() for action in hand['turn_actions']]),
                'river_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]} {action["to"]}'.strip() for action in hand['river_actions']]),
                'showdown_actions': ', '.join([f'{showdown["player"]}: shows [{showdown["cards"]}]' for showdown in hand['showdown_actions']]),
                'winners': ', '.join([f'{winner["player"]}: collected {winner["amount"]} from pot' for winner in hand['winners']])
            })

def parse_folder_to_csv(folder_path, output_csv_path):
    all_parsed_hands = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            parsed_hands = parse_pluribus_txt(file_path)
            all_parsed_hands.extend(parsed_hands)
    
    save_to_csv(all_parsed_hands, output_csv_path)
    print(f'Parsed {len(all_parsed_hands)} hands and saved to {output_csv_path}')

parse_folder_to_csv("../data/pluribus_converted_logs", "../data/pluribus_parsed.csv")
