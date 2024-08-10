import pandas as pd

file_path = '../data/pluribus_parsed.csv'
data = pd.read_csv(file_path)

# Function to count actions in a given column
def count_actions(column):
    if pd.notna(column):
        return len(column.split(', '))
    return 0

# Function to calculate average actions
def calculate_average_actions(data):
    # Count actions in each action column
    data['preflop_actions_count'] = data['preflop_actions'].apply(count_actions)
    data['flop_actions_count'] = data['flop_actions'].apply(count_actions)
    data['turn_actions_count'] = data['turn_actions'].apply(count_actions)
    data['river_actions_count'] = data['river_actions'].apply(count_actions)
    data['showdown_actions_count'] = data['showdown_actions'].apply(count_actions)
    
    # Calculate total actions and average actions per game
    data['total_actions'] = (data['preflop_actions_count'] +
                             data['flop_actions_count'] +
                             data['turn_actions_count'] +
                             data['river_actions_count'] +
                             data['showdown_actions_count'])
    
    average_actions = data['total_actions'].mean()
    return average_actions

# Calculate and print the average number of actions
average_actions = calculate_average_actions(data)
print(f'Average number of actions: {average_actions}')
