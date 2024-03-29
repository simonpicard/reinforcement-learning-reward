# Plan-Based Reward Shaping for Multi-Agent Reinforcement Learning

## Quickstart

```
git clone git@github.com:simonpicard/reinforcement-learning-reward.git
cd reinforcement-learning-reward
pip install -r requirements.txt
cd src
python runAllPlot.py
python handlePlot.py
```

## Introduction

Reproducing the results of an article about reinforcement learning.

Reinforcement learning simulation have been written in pure python without any libraries. Running the aboves commands will generate all results used in the article.

Explore the article in `article/example.pdf` or the presentation in `presentation/PBRS_for_MARL.pdf`.

## Research abstract

Reinforcement learning agents don't get future feedback about how good was their decision taken in a precise state. This leads to a temporal problem as the agents will not know immediately which part of their decisions where the good ones. RL, while being simple, presents some issues. The time taken by the agents to learn the right policy grows exponentially while adding new variables to the environment. When the state space is too vast, memory becomes an issue as well as the matrix for each state-action pair becomes too big and too many states need to be updated too frequently slowing down drastically the process. 

A way of improving the converging speed is to provide prior knowledge to the agents through a method called reward shaping. Reward shaping is the addition of domain knowledge to reinforcement learning in a way that will minimize non-optimal behaviours and will fastly converge to the optimal one. In this article we will see how to effectively incorporate reward shaping in MARL using individual and joint plan based plans and we will combine them with a flag based heuristic.

We will show that providing prior knowledge, while not always being possible due to heuristic problems, significantly increases agent's performances and speed of convergence. Plan-based reward shaping will be our main concern for our experiment. It is a particular form of reward shaping that guides agent's through the world regarding predetermined plans. We will be focusing on analysing different plan-based strategies to determine the most efficient one.
