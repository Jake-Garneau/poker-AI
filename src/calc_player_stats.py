import pandas as pd
import re

df = pd.read_csv('../data/pluribus_parsed.csv')

print("Columns in the DataFrame:", df.columns)

player_stats = {}

def init_player_stats(player_name):
    return {
        "VPIP_count": 0,
        "PFR_count": 0,
        "total_hands": 0,
        "aggression_count": 0,
        "post_flop_actions": 0,
        "winnings": 0
    }

for index, row in df.iterrows():
    if "players" in row:
        players = row["players"].split(", ")
        actions = row["actions"]
        winner_info = row["winners"]

        for player in players:
            if player not in player_stats:
                player_stats[player] = init_player_stats(player)
            player_stats[player]["total_hands"] += 1

        pre_flop_actions = re.findall(r"([a-zA-Z]+): (raises|calls|bets|folds|checks|posts)", actions)

        for action in pre_flop_actions:
            player, move = action
            if player in player_stats:
                if move in ["raises", "calls", "bets"]:
                    player_stats[player]["VPIP_count"] += 1
                if move == "raises":
                    player_stats[player]["PFR_count"] += 1

        post_flop_actions = re.findall(r"Stage: [A-Z]+, ([a-zA-Z]+): (bets|raises|folds|checks|calls)", actions)
        
        for action in post_flop_actions:
            player, move = action
            if player in player_stats:
                player_stats[player]["post_flop_actions"] += 1
                if move in ["bets", "raises"]:
                    player_stats[player]["aggression_count"] += 1

        if winner_info:
            winner_match = re.match(r"([a-zA-Z]+): collected ([\d\.]+)", winner_info)
            if winner_match:
                winner, amount = winner_match.groups()
                amount = float(amount)
                player_stats[winner]["winnings"] += amount

with open('../data/player_stats_output.txt', 'w') as file:
    for player, stats in player_stats.items():
        total_hands = stats["total_hands"]
        vpip = (stats["VPIP_count"] / total_hands) * 100 if total_hands > 0 else 0
        pfr = (stats["PFR_count"] / total_hands) * 100 if total_hands > 0 else 0
        aggression_factor = (stats["aggression_count"] / stats["post_flop_actions"]) * 100 if stats["post_flop_actions"] > 0 else 0
        bb_won_per_100_hands = (stats["winnings"] / (total_hands * 100)) * 100 if total_hands > 0 else 0

        file.write(f"Player: {player}\n")
        file.write(f"VPIP: {vpip:.2f}%\n")
        file.write(f"PFR: {pfr:.2f}%\n")
        file.write(f"Aggression Factor: {aggression_factor:.2f}%\n")
        file.write("\n")