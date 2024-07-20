import os
import re
import csv

def parse_pluribus_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    hands = data.split('\n\n')
    
    parsed_hands = []
    for hand in hands:
        hand_details = {}
        
        hand_id = re.search(r'PokerStars Hand #(\d+):', hand)
        if hand_id:
            hand_details['hand_id'] = hand_id.group(1)
        
        hand_details['flop'] = []
        hand_details['turn'] = []
        hand_details['river'] = []
        
        community_cards = re.search(r'\*\*\* FLOP \*\*\* \[(.*?)\](?: \*\*\* TURN \*\*\* \[(.*?)\])?(?: \*\*\* RIVER \*\*\* \[(.*?)\])?', hand)
        if community_cards:
            hand_details['flop'] = community_cards.group(1).split() if community_cards.group(1) else []
            hand_details['turn'] = community_cards.group(2).split() if community_cards.group(2) else []
            hand_details['river'] = community_cards.group(3).split() if community_cards.group(3) else []
        
        players = re.findall(r'Seat \d+: (\w+) \(\d+ in chips\)', hand)
        hand_details['players'] = players
        
        hole_cards = re.findall(r'Dealt to (\w+) \[(.*?)\]', hand)
        hand_details['hole_cards'] = {player: cards.split() for player, cards in hole_cards}
        
        actions = []
        lines = hand.split('\n')
        for line in lines:
            if re.match(r'^\*\*\* FLOP \*\*\*', line):
                actions.append({'player': 'Stage', 'action': 'FLOP', 'amount': '', 'to': ''})
            elif re.match(r'^\*\*\* TURN \*\*\*', line):
                actions.append({'player': 'Stage', 'action': 'TURN', 'amount': '', 'to': ''})
            elif re.match(r'^\*\*\* RIVER \*\*\*', line):
                actions.append({'player': 'Stage', 'action': 'RIVER', 'amount': '', 'to': ''})
            else:
                match = re.match(r'(\w+): (posts small blind|posts big blind|folds|calls|raises|bets|checks) ?(\d+)? ?(to \d+)?', line)
                if match:
                    actions.append({
                        'player': match.group(1), 
                        'action': match.group(2), 
                        'amount': match.group(3) if match.group(3) else '', 
                        'to': match.group(4) if match.group(4) else ''
                    })
        
        hand_details['actions'] = actions
        
        winners = []
        showdowns = []
        collecting_showdown = False
        for line in lines:
            if re.match(r'^\*\*\* SHOWDOWN \*\*\*', line):
                collecting_showdown = True
            elif re.match(r'^\*\*\* SUMMARY \*\*\*', line):
                collecting_showdown = False
            
            if collecting_showdown:
                match_showdown = re.match(r'(\w+): shows \[(.*?)\]', line)
                if match_showdown:
                    showdowns.append({'player': match_showdown.group(1), 'cards': match_showdown.group(2)})
                
                match_winner = re.match(r'(\w+) collected (\d+\.?\d*) from pot', line)
                if match_winner:
                    winners.append({'player': match_winner.group(1), 'amount': match_winner.group(2)})
        
        hand_details['showdowns'] = showdowns
        hand_details['winners'] = winners
        
        if not showdowns:
            for line in lines:
                match_winner_summary = re.match(r'(\w+) collected (\d+\.?\d*) from pot', line)
                if match_winner_summary:
                    winners.append({'player': match_winner_summary.group(1), 'amount': match_winner_summary.group(2)})
        
        hand_details['winners'] = winners
        
        parsed_hands.append(hand_details)
    
    return parsed_hands

def save_to_csv(parsed_hands, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['hand_id', 'flop', 'turn', 'river', 'players', 'hole_cards', 'actions', 'showdowns', 'winners']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for hand in parsed_hands:
            writer.writerow({
                'hand_id': hand['hand_id'],
                'flop': ' '.join(hand['flop']),
                'turn': ' '.join(hand['turn']),
                'river': ' '.join(hand['river']),
                'players': ', '.join(hand['players']),
                'hole_cards': ', '.join([f'{player}: {" ".join(cards)}' for player, cards in hand['hole_cards'].items()]),
                'actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]} {action["to"]}'.strip() for action in hand['actions']]),
                'showdowns': ', '.join([f'{showdown["player"]}: shows [{showdown["cards"]}]' for showdown in hand['showdowns']]),
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