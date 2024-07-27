import pandas as pd

df = pd.read_csv("../data/pluribus_test.csv")

player_stats = {}
big_blind = 100
small_blind = 50

def update_stats(player, stat_type, value=1):
    if player not in player_stats:
        player_stats[player] = {
            "total_hands": 0,
            "total_hands_played": 0,
            "hands_vpip": 0,
            "hands_pfr": 0,
            "bets": 0,
            "raises": 0,
            "calls": 0,
            "folds": 0,
            "money_pip": 0,
            "winnings": 0,
            "walks": 0,
            "total_hands_played_counted": False,
            "hands_vpip_counted": False,
            "hands_pfr_counted": False
        }
    player_stats[player][stat_type] += value
    
def update_action_stats(actions):
    for action in actions:
        action_parts = action.split(': ')
        player = action_parts[0]
        action_detail = action_parts[1] if len(action_parts) > 1 else ''
        if('folds' in action_detail):
            update_stats(player, 'folds')
        elif 'bets' in action_detail:
            amount = float(action_detail.split(' ')[1])
            update_stats(player, 'bets')
            update_stats(player, 'money_pip', amount)
        elif 'raises' in action_detail:
            amount = float(action_detail.split(' ')[1])
            update_stats(player, 'raises')
            update_stats(player, 'money_pip', amount)
        elif 'calls' in action_detail:
            amount = float(action_detail.split(' ')[1])
            update_stats(player, 'calls')
            update_stats(player, 'money_pip', amount)
        elif 'uncalled bet' in action_detail:
            amount = float(action_detail.split(' ')[2])
            update_stats(player, 'money_pip', -amount)

for _, row in df.iterrows():
    players = row['players'].split(', ')
    preflop_actions = row['preflop_actions'].split(', ')
    flop_actions = row['flop_actions'].split(', ') if pd.notna(row['flop_actions']) else []
    turn_actions = row['turn_actions'].split(', ') if pd.notna(row['turn_actions']) else []
    river_actions = row['river_actions'].split(', ') if pd.notna(row['river_actions']) else []
    winners = row['winners']
    
    for player in players:
        update_stats(player, 'total_hands')
        player_stats[player]['total_hands_played_counted'] = False
        player_stats[player]['hands_vpip_counted'] = False
        player_stats[player]['hands_pfr_counted'] = False
    
    for action in preflop_actions:
        action_parts = action.split(': ')
        player = action_parts[0]
        action_detail = action_parts[1] if len(action_parts) > 1 else ''
        
        if 'posts' in action_detail:
            if 'small blind' in action_detail:
                update_stats(player, 'money_pip', small_blind)
            else:
                update_stats(player, 'money_pip', big_blind)
            continue
        elif 'folds' in action_detail:
            update_stats(player, 'folds')
        elif 'calls' in action_detail or 'raises' in action_detail:
            amount = float(action_detail.split(' ')[1])
            update_stats(player, 'money_pip', amount)
            if(not player_stats[player]['total_hands_played_counted']):
                update_stats(player, 'total_hands_played')
                player_stats[player]['total_hands_played_counted'] = True
            if(not player_stats[player]['hands_vpip_counted']):
                update_stats(player, 'hands_vpip')
                player_stats[player]['hands_vpip_counted'] = True
            if 'raises' in action_detail:
                if(not player_stats[player]['hands_pfr_counted']):
                    update_stats(player, 'hands_pfr')
                    player_stats[player]['hands_pfr_counted'] = True
                update_stats(player, 'raises')
            if 'calls' in action_detail:
                update_stats(player, 'calls')
                
    update_action_stats(flop_actions)
    update_action_stats(turn_actions)
    update_action_stats(river_actions)
    
    if 'collected' in winners:
        winner_parts = winners.split(': collected ')
        player = winner_parts[0]
        amount = float(winner_parts[1].split(' ')[0])
        update_stats(player, 'winnings', amount)
    
    if len(preflop_actions) == 7 and all(['posts' or 'folds' in action for action in preflop_actions]):
        big_blind_player = preflop_actions[1].split(': ')[0]
        update_stats(big_blind_player, 'walks')

for player, stats in player_stats.items():
    if player == 'MrPink':
        print(stats)
    vpip_hands = stats['total_hands'] - stats['walks']
    agg_div = stats['bets'] + stats['raises'] + stats['calls'] + stats['folds']
    print(player + ' total hands played: ' + str(stats['total_hands_played']))
    vpip = (stats['hands_vpip'] / vpip_hands) * 100 if vpip_hands > 0 else 0
    pfr = (stats['hands_pfr'] / stats['total_hands_played']) * 100 if stats['total_hands_played'] > 0 else 0
    agg = ((stats['bets'] + stats['raises']) / agg_div) * 100 if agg_div > 0 else 0
    bb_won_per_100 = ((stats['winnings'] - stats['money_pip']) / big_blind) / stats['total_hands_played'] if stats['total_hands_played'] > 0 else 0
        
    player_stats[player].update({
        'VPIP': vpip,
        'PFR': pfr,
        'Agg': agg,
        'BB_won_per_100': bb_won_per_100
    })

txt_file_path = '../data/player_stats.txt'

with open(txt_file_path, mode='w') as file:
    for player, stats in player_stats.items():
        file.write(f"Player: {player}\n")
        file.write(f"  VPIP: {stats['VPIP']:.2f}%\n")
        file.write(f"  PFR: {stats['PFR']:.2f}%\n")
        file.write(f"  Agg: {stats['Agg']:.2f}%\n")
        file.write(f"  BB won per 100 hands: {stats['BB_won_per_100']:.2f}\n")
        file.write("\n")