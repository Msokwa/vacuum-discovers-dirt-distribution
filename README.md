# vacuum-discovers-dirt-distribution
SE402 Artificial Intelligence assignment implementing a reflex vacuum agent that learns and classifies dirt distribution in Vacuum World.
# Vacuum Discovers Dirt Distribution

## Overview

This project implements a reflex vacuum agent for a Vacuum World
environment as part of an Artificial Intelligence course assignment.

The agent explores the rooms of the environment, collects observations
about how frequently dirt appears, and uses the collected data to classify
the house's dirt distribution.

## Dirt Distributions

The agent identifies three distribution types:

- Random
- Skewed
- Uniform

## How It Works

The vacuum:

1. Moves to the leftmost room.
2. Observes each room for multiple simulation ticks.
3. Counts how often dirt appears.
4. Cleans dirt when it appears.
5. Calculates the dirt rate for each room.
6. Compares the rates between rooms.
7. Predicts the house's dirt distribution.

## Results

The official test used 60 simulations.

- Correct predictions: 46
- Failed predictions: 14
- Accuracy: 76.67%

### Confusion Matrix

| Actual | Random | Skewed | Uniform |
|---|---:|---:|---:|
| Random | 14 | 0 | 10 |
| Skewed | 0 | 17 | 0 |
| Uniform | 4 | 0 | 15 |

## Technologies

- Python
- Object-Oriented Programming
- Artificial Intelligence
- Classification
- Data collection
- Reflex agents

## Running the Project

```bash
python reflex_vacuum_simulation.py --assignment-settings 2.1
