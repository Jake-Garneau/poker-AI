import os
import re
import csv

def parse_archive_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    hands = data.split('\n\n')
    
    parsed_hands = []
    for hand in hands:
        hand_details = {
            'hand_id': '',
            'flop_cards': [],
            'turn_card': [],
            'river_card': [],
            'players': [],
            'hole_cards': {},
            'preflop_actions': [],
            'flop_actions': [],
            'turn_actions': [],
            'river_actions': [],
            'showdown_actions': [],
            'winners': [],
        }
        
        # Extract hand ID
        hand_id = re.search(r'Game ID: (\d+)', hand)
        if hand_id:
            hand_details['hand_id'] = hand_id.group(1)
        
        # Extract community cards
        flop_cards = re.search(r'\*\*\* FLOP \*\*\*:\s*\[(.*?)\]', hand)
        if flop_cards:
            hand_details['flop_cards'] = flop_cards.group(1).split()
        
        turn_card = re.search(r'\*\*\* TURN \*\*\*:\s*\[.*?\] \[(.*?)\]', hand)
        if turn_card:
            hand_details['turn_card'] = [turn_card.group(1)]
        
        river_card = re.search(r'\*\*\* RIVER \*\*\*:\s*\[.*?\] \[(.*?)\]', hand)
        if river_card:
            hand_details['river_card'] = [river_card.group(1)]
        
        # Extract player names
        players = re.findall(r'Seat \d+: ([\w\.\!\?\=\(\)\-\_\s]+?) \(\d+(?:\.\d+)?\)', hand)
        hand_details['players'] = players
        
        for player in players:
            # Use regex to find all card entries for each player
            hole_cards = re.findall(r'Player {} received card: \[(.*?)\]'.format(re.escape(player)), hand)
            if hole_cards:
                # Assuming each player receives exactly 2 hole cards
                hand_details['hole_cards'][player] = hole_cards
        
        # Initialize current stage
        current_stage = 'preflop'
        
        for line in hand.split('\n'):
            if re.match(r'^Player ([\w\.\!\?\=\(\)\-\_\s]+?) raises|Player ([\w\.\!\?\=\(\)\-\_\s]+?) folds|Player ([\w\.\!\?\=\(\)\-\_\s]+?) bets|Player ([\w\.\!\?\=\(\)\-\_\s]+?) calls|Player ([\w\.\!\?\=\(\)\-\_\s]+?) checks|Uncalled bet', line):
                action = parse_action(line)
                if action:
                    if current_stage == 'preflop':
                        hand_details['preflop_actions'].append(action)
                    elif current_stage == 'flop':
                        hand_details['flop_actions'].append(action)
                    elif current_stage == 'turn':
                        hand_details['turn_actions'].append(action)
                    elif current_stage == 'river':
                        hand_details['river_actions'].append(action)

            elif re.match(r'^\*\*\* FLOP \*\*\*', line):
                current_stage = 'flop'
            elif re.match(r'^\*\*\* TURN \*\*\*', line):
                current_stage = 'turn'
            elif re.match(r'^\*\*\* RIVER \*\*\*', line):
                current_stage = 'river'
            elif re.match(r'^\*\*\* SUMMARY \*\*\*', line):
                current_stage = 'summary'
            
            showdown_summary_action = parse_showdown_summary_action(line)
            if showdown_summary_action:
                hand_details['showdown_actions'].append({
                    'player': showdown_summary_action['player'],
                    'cards': showdown_summary_action['cards']
                }) if showdown_summary_action['cards'] != '?? ??' else None
                hand_details['winners'].append(showdown_summary_action['summary'])
        
        parsed_hands.append(hand_details)
    
    return parsed_hands

def parse_action(line):
    match = re.match(r'Player ([\w\.\!\?\=\(\)\-\_\s]+?) (posts small blind|posts big blind|folds|calls|raises|bets|checks)(?: \((\d+(?:\.\d+)?)\))?', line)
    uncalled_bet_match = re.match(r'Uncalled bet \((\d+(?:\.\d+)?)\) returned to ([\w\.\!\?\=\(\)\-\_\s]+?)', line)
    if match:
        action = match.group(2)
        amount = match.group(3) if match.group(3) else ''
        return {
            'player': match.group(1),
            'action': action,
            'amount': amount
        }
    elif uncalled_bet_match:
        return {
            'player': uncalled_bet_match.group(2),
            'action': 'uncalled bet',
            'amount': uncalled_bet_match.group(1)
        }
    return None

def parse_showdown_summary_action(line):
    show_match = re.match(r'\*Player ([\w\.\!\?\=\(\)\-\_\s]+?) shows: .* \[(.*?)\]\. Bets: (\d+(?:\.\d+)?)\. Collects: (\d+(?:\.\d+)?)\..*', line)
    no_show_match = re.match(r'\*Player ([\w\.\!\?\=\(\)\-\_\s]+?) mucks \(does not show cards\)\. Bets: (\d+(?:\.\d+)?)\. Collects: (\d+(?:\.\d+)?)\..*', line)
    if show_match:
        return {
            'player': show_match.group(1),
            'cards': show_match.group(2),
            'summary': f"{show_match.group(1)}: collected {show_match.group(3)} from pot"
        }
    elif no_show_match:
        return {
            'player': no_show_match.group(1),
            'cards': '?? ??',
            'summary': f"{no_show_match.group(1)}: collected {no_show_match.group(2)} from pot"
        }
    return None

def save_to_csv(parsed_hands, csv_file_path):
    no_winners = []
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = [
            'hand_id', 'flop_cards', 'turn_card', 'river_card',
            'players', 'hole_cards', 'preflop_actions', 'flop_actions',
            'turn_actions', 'river_actions', 'showdown_actions', 'winners'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for hand in parsed_hands:
            if hand['hand_id'] == '':
                continue
            if(len(hand['winners']) == 0):
                no_winners.append(hand['hand_id'])
            writer.writerow({
                'hand_id': hand['hand_id'],
                'flop_cards': ' '.join(hand['flop_cards']),
                'turn_card': ' '.join(hand['turn_card']),
                'river_card': ' '.join(hand['river_card']),
                'players': ', '.join(hand['players']),
                'hole_cards': ', '.join([f'{player}: {" ".join(cards)}' for player, cards in hand['hole_cards'].items()]),
                'preflop_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]}'.strip() for action in hand['preflop_actions']]),
                'flop_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]}'.strip() for action in hand['flop_actions']]),
                'turn_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]}'.strip() for action in hand['turn_actions']]),
                'river_actions': ', '.join([f'{action["player"]}: {action["action"]} {action["amount"]}'.strip() for action in hand['river_actions']]),
                'showdown_actions': ', '.join([f'{showdown["player"]}: shows [{showdown["cards"]}]' for showdown in hand['showdown_actions']]),
                'winners': ', '.join(hand['winners']),
                
            })
    print(f'No winners for hands: {no_winners}')
def parse_folder_to_csv(folder_path, output_csv_path):
    all_parsed_hands = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            parsed_hands = parse_archive_txt(file_path)
            all_parsed_hands.extend(parsed_hands)
    
    save_to_csv(all_parsed_hands, output_csv_path)
    print(f'Parsed {len(all_parsed_hands)} hands and saved to {output_csv_path}')

parse_folder_to_csv("../data/archive", "../data/archive_parsed.csv")
