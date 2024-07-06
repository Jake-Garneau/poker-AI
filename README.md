# Analyzing Poker Hand Data and Developing a Poker Playing Neural Network

## Team Members:

- Rusheel Dasari (rdasari2)
- Jake Garneau (jgarneau)

## Overview:

This project aims to analyze poker game data and develop a neural network model capable of playing no-limit Texas hold’em (NLHE) poker. We will use a dataset of tracked poker games released by the Pluribus (Poker bot built by Facebook's AI Lab and Carnegie Mellon University) research team to train and evaluate our model.

## Background:

Poker is a popular card game that combines skill, strategy, and luck. There have been various attempts to develop AI systems capable of playing poker at a high level. Notable projects include Libratus and Deepstack, an AI that defeated top human players in heads-up (2 player) NLHE. We are using a dataset from Pluribus AI, a competitive poker bot trained in 6 player NLHE, and the first bot to beat humans in a complex multiplayer competition.

## Statement Of Work:

### Datasets:

1. **[UCI Machine Learning Repository - Poker Hand Dataset](https://archive.ics.uci.edu/dataset/158/poker+hand)**

   - Contains 1,025,010 instances of poker hands with 11 attributes: 10 for the cards and 1 for the hand class.
   - Already partitioned into training and test sets.
   - Preliminary inspection indicates that the dataset includes labeled data for classification, where each class represents a different poker hand rank.
   - We will perform preprocessing steps such as normalization and data augmentation to enhance the model's performance.

2. **[Pluribus AI Hands Dataset](http://kevinwang.us/lets-analyze-pluribuss-hands/)**

   - Comprises 10,000 recorded games from Pluribus, an advanced poker AI.
   - Includes detailed information on player actions, betting rounds, positions, stack sizes, and game outcomes.
   - Provides a rich contextual basis for training a poker AI, capturing dynamic game scenarios and strategic decisions.
   - We will perform preprocessing steps such as data normalization, feature engineering (e.g., calculating hand strength, pot odds), and data augmentation to enhance the model's performance.

3. **[Kaggle - Poker Hold’em Games Dataset](https://www.kaggle.com/datasets/smeilz/poker-holdem-games/data)**
   - Similar dataset of recorded multiplayer NLHE games, but cannot view other players’ cards.
   - Can be used as additional data for performance evaluation.

- After downloading the datasets, ensure they are placed in the `data/` directory to match the expected file structure.

### Method:

#### Data Analysis and Preprocessing:

- Normalize and clean the datasets.
- Engineer features such as hand strength, pot odds, and betting patterns.
- Split the data into training, validation, and test sets.

#### Model Development:

- Develop a baseline neural network model to predict player actions based on the game state.
- Explore advanced techniques, including convolutional neural networks (CNN) for feature extraction and reinforcement learning for strategy optimization.

#### Model Training and Evaluation:

- Train the baseline model using the training set.
- Evaluate the model using standard metrics (e.g., accuracy, F1-score) and poker-specific metrics (e.g., win rate, average returns).
- Implement and test advanced models, comparing their performance to the baseline.

#### Simulation and Testing:

- Simulate poker games using the trained models to evaluate performance in realistic scenarios.
- Analyze the AI’s decision-making and strategic behavior in various game contexts.

### Outcome and Performance Evaluation:

We anticipate developing a model that can accurately classify poker hands and make strategic decisions in a simulated poker environment. The success of the project will be measured by the model's classification accuracy, computational efficiency, and its performance in simulated poker games against other AI opponents. We will use metrics such as win rate and average returns to evaluate the AI's poker-playing performance.

## Project Plan:

### Links:

- Git repo: https://github.com/Jake-Garneau/poker-AI
- Task board: https://trello.com/b/u0MGmloA/poker-ai

### By July 13:

- Set up project environment
- Define project objectives and methodology
- Preprocess dataset (normalization, feature engineering)

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

## References:

- https://ai.meta.com/blog/pluribus-first-ai-to-beat-pros-in-6-player-poker/
- https://www.youtube.com/watch?v=2dX0lwaQRX0
- https://www.science.org/doi/10.1126/science.aay2400

## Contributions:

- **Rusheel**: Contributed to the proposal writing, including sections on background, dataset, method, and project plan. Prepared the initial draft of the proposal prompt.
- **Jake**: Researched initial datasets and methodology, defined the project scope. Ensured overall structure of the proposal, aligns with the rubric. Finalized proposal draft.
