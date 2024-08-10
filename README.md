# Analyzing Poker Hand Data and Developing a Poker Playing Neural Network

## Overview:

This project aims to analyze poker game data and develop a neural network model capable of playing no-limit Texas hold’em (NLHE) poker. We will use a dataset of tracked poker games released by the Pluribus (Poker bot built by Facebook's AI Lab and Carnegie Mellon University) research team to train and evaluate our model, and then a similar Kaggle dataset of recorded poker games to further validate its performance.

## Background:

Poker is a popular card game that combines skill, strategy, and luck. There have been various attempts to develop AI systems capable of playing poker at a high level. Notable projects include Libratus and Deepstack, an AI that defeated top human players in heads-up (2 player) NLHE. We are using a dataset from Pluribus AI, a competitive poker bot trained in 6 player NLHE, and the first bot to beat humans in a complex multiplayer competition.

## Statement Of Work:

### Datasets:

1. **[Pluribus AI Hands Dataset](http://kevinwang.us/lets-analyze-pluribuss-hands/)**

   - Comprises 10,000 recorded games from Pluribus, an advanced poker AI.
   - Includes detailed information on player actions, betting rounds, positions, stack sizes, and game outcomes.
   - Provides a rich contextual basis for training a poker AI, capturing dynamic game scenarios and strategic decisions.
   - We will perform preprocessing steps such as data normalization, feature engineering (e.g., calculating hand strength, pot odds), and data augmentation to enhance the model's performance.

2. **[Kaggle - Poker Hold’em Games Dataset](https://www.kaggle.com/datasets/smeilz/poker-holdem-games/data)**
   - Similar dataset of recorded multiplayer NLHE games, but cannot view other players’ cards.

### Method:

#### Data Analysis and Preprocessing:

- Normalize and clean the datasets.
- Engineer features such as hand strength, pot odds, and betting patterns.
- Split the data into training, validation, and test sets.

#### Model Development:

##### Implement Pre-Existing Poker Libraries:

- **[Deuces](https://github.com/worldveil/deuces)**: written for the MIT Pokerbots Competition, used to evaluate poker hands of 2 and 5-7, useful for evaluating Texas Holdem hands from pre-flop to river.
- **[Pokerkit](https://github.com/uoftcprg/pokerkit)**: an open-source software library for simulating games, evaluating hands, and facilitating statistical analysis, developed by the University of Toronto Computer Poker Student Research Group.

##### Using Both Datasets

- Rotate through training and validation sets of both pluribus and kaggle recorded games, so that each is used for training/validation/testing, then average the results

##### Logistic Regression

- Implement a logistic regression model as our initial baseline model.
- Use the scikit-learn library to develop and train this model.

##### Multi-Layer Perceptron (MLP):

- Implement a multi-layer perceptron using TensorFlow library.
- Configure the neural network with an appropriate number of layers and neurons.
- Train the MLP model on the training dataset.

##### Ensemble Method:

- Implement gradient boosting and/or random forest.
- Use the scikit-learn library to develop and train this model.

#### Model Training and Evaluation:

- Train the baseline model using the training set.
- To use as baseline/compare against other AI
  - https://github.com/dickreuter/Poker - poker bot with strategy analyzer and strategy editor
  - https://github.com/fedden/poker_ai - another open-source poker bot
- Evaluate the model using standard metrics (e.g., accuracy, F1-score) and poker-specific metrics (e.g., win rate, average returns).
- Implement and test advanced models, comparing their performance to the baseline.

#### Simulation and Testing:

- Simulate poker games using the trained models and other AI to evaluate performance in realistic scenarios.
- Analyze the AI’s decision-making and strategic behavior in various game contexts.

### Outcome and Performance Evaluation:

We anticipate developing a model that can accurately make strategic decisions in a simulated poker environment. The success of the project will be measured by the model's computational efficiency, and its performance in simulated poker games against other AI opponents and itself. We will use metrics such as win rate and average returns to evaluate the AI's poker-playing performance.

## Project Plan:

### Links:

- Git repo: https://github.com/Jake-Garneau/poker-AI

### By July 13:

- Set up project environment
- Define project objectives and methodology
- Preprocess dataset
- Setup PostgreSQL to store datasets
- Set up poker-specific libraries:

### By July 20 (First Project Report Due):

- Develop baseline neural network model
- Train and evaluate the baseline model
- Prepare first project report

### By August 3:

- Implement advanced techniques (e.g., CNN, reinforcement learning)
- Continue training and evaluating advanced models
- Fine-tune advanced models and conduct extensive evaluations

### By August 5/7:

- Prepare and finalize presentation

### By August 10:

- Complete and submit final report

## Requirements

- After downloading datasets, ensure they are placed in `data/` directory to match the expected file structure
- Create virtual environment: `python -m venv myenv`
- To activate (bash/zsh): `source myenv/Scripts/activate`
- To deactivate: `deactivate`
- In virtual environment: `pip install pandas numpy scikit-learn tensorflow jupyter matplotlib pokerkit deuces keras-tuner`
- Make sure to select venv as Python interpreter

## References:

1. https://ai.meta.com/blog/pluribus-first-ai-to-beat-pros-in-6-player-poker/
2. https://www.youtube.com/watch?v=2dX0lwaQRX0
3. https://www.science.org/doi/10.1126/science.aay2400
4. https://pokercopilot.com/essential-poker-statistics
5. Deuces - https://github.com/worldveil/deuces: written for the MIT Pokerbots Competition, used to evaluate poker hands of 2 and 5-7, useful for evaluating Texas Holdem hands from pre-flop to river.
6. Pokerkit - https://github.com/uoftcprg/pokerkit: an open-source software library for simulating games, evaluating hands, and facilitating statistical analysis, developed by the University of Toronto Computer Poker Student Research Group.
7. https://github.com/dickreuter/Poker - poker bot with strategy analyzer and strategy editor
8. https://github.com/fedden/poker_ai - another open-source poker bot
9. https://neptune.ai/blog/monte-carlo-simulation
10. https://stackoverflow.com/questions/33312405/how-to-speed-up-monte-carlo-simulation-in-python

## Player Statistics from Reference 4

- VPIP (Voluntarily put money in pot before flop): 15%-20% is ideal
- PFR (Pre Flop Raise): 2%-3% less than VPIP is ideal
- Agg (Aggression Factor): 50%-60% is ideal, more than that is excessive bluffing or overplaying speculative/bad hands
- Big blinds won/100 hands: positive = winning over time, negative = losing over time
