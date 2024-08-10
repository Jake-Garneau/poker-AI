import csv

player_stats = {}
with open('../data/player_stats.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        player = row['Player']
        player_stats[player] = {
            'VPIP': float(row['VPIP']),
            'PFR': float(row['PFR']),
            'Agg': float(row['Agg']),
            'BB_won_per_100': float(row['BB_won_per_100'])
        }


def get_player_stats(player_name):
    if player_name in player_stats:
        stats = player_stats[player_name]
        return [
            round(stats['VPIP'], 2),
            round(stats['PFR'], 2),
            round(stats['Agg'], 2),
            round(stats['BB_won_per_100'], 2)
        ]
    else:
        return []
