from ..basic_ml_objects import BaseDataProcessing, BasePotentialAlgo

from ....core.utils import log_debug, clear_log_debug

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import random
import gym
import numpy as np
from collections import deque
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.optimizers import Adam, RMSprop

import yfinance as yf
from datetime import datetime, timedelta


import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout


import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from collections import deque

import yfinance as yf
import pandas as pd
from tensorflow.keras import layers


# # Define a simple LSTM model for trading
# def create_rrl_model(input_shape):
#     model = Sequential()
#     model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
#     model.add(Dropout(0.2))
#     model.add(LSTM(50, return_sequences=False))
#     model.add(Dropout(0.2))
#     model.add(Dense(25, activation='relu'))
#     model.add(Dense(3, activation='softmax'))  # 3 actions: buy, sell, hold
#     return model
#
# class GridWorldEnv:
#     def __init__(self, grid_size=5):
#         self.grid_size = grid_size
#         self.reset()
#
#     def reset(self):
#         self.agent_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
#         self.goal_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
#         return self.get_observation()
#
#     def step(self, action):
#         # Actions: 0 = left, 1 = right, 2 = up, 3 = down
#         if action == 0:  # left
#             self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
#         elif action == 1:  # right
#             self.agent_pos[1] = min(self.grid_size - 1, self.agent_pos[1] + 1)
#         elif action == 2:  # up
#             self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
#         elif action == 3:  # down
#             self.agent_pos[0] = min(self.grid_size - 1, self.agent_pos[0] + 1)
#
#         # Reward and termination condition
#         done = self.agent_pos == self.goal_pos
#         reward = 1 if done else -0.1
#         return self.get_observation(), reward, done
#
#     def get_observation(self):
#         # Agent sees a 3x3 grid around it (clipped at boundaries)
#         obs = np.zeros((3, 3))
#         x, y = self.agent_pos
#         for i in range(-1, 2):
#             for j in range(-1, 2):
#                 xi, yj = x + i, y + j
#                 if 0 <= xi < self.grid_size and 0 <= yj < self.grid_size:
#                     obs[i + 1, j + 1] = 1 if [xi, yj] == self.goal_pos else 0
#         return obs
#
#
# class RNN_DQN(nn.Module):
#     def __init__(self, input_dim, hidden_dim, output_dim):
#         super(RNN_DQN, self).__init__()
#         self.fc1 = nn.Linear(input_dim, hidden_dim)
#         self.lstm = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
#         self.fc2 = nn.Linear(hidden_dim, output_dim)
#         self.hidden_dim = hidden_dim
#
#     def forward(self, x, hidden):
#         x = F.relu(self.fc1(x))
#         x, hidden = self.lstm(x.unsqueeze(1), hidden)  # Add sequence dimension
#         x = F.relu(x)
#         x = self.fc2(x.squeeze(1))
#         return x, hidden
#
#     def init_hidden(self, batch_size):
#         # LSTM hidden state initialization
#         return (torch.zeros(1, batch_size, self.hidden_dim),
#                 torch.zeros(1, batch_size, self.hidden_dim))
#
#
# class ReplayBuffer:
#     def __init__(self, capacity):
#         self.buffer = deque(maxlen=capacity)
#
#     def push(self, sequence):
#         self.buffer.append(sequence)
#
#     def sample(self, batch_size):
#         batch = random.sample(self.buffer, batch_size)
#         return batch
#
#     def __len__(self):
#         return len(self.buffer)
#
#
# class DQNAgent:
#     def __init__(self, input_dim, hidden_dim, output_dim, replay_capacity=1000,
#                  gamma=0.99, epsilon=0.1):
#         self.model = RNN_DQN(input_dim, hidden_dim, output_dim)
#         self.target_model = RNN_DQN(input_dim, hidden_dim, output_dim)
#         self.target_model.load_state_dict(self.model.state_dict())
#         self.target_model.eval()
#
#         self.optimizer = optim.Adam(self.model.parameters())
#         self.replay_buffer = ReplayBuffer(replay_capacity)
#         self.gamma = gamma
#         self.epsilon = epsilon
#         self.batch_size = 32
#         self.hidden_dim = hidden_dim
#
#     def select_action(self, state, hidden):
#         if random.random() > self.epsilon:
#             with torch.no_grad():
#                 q_values, hidden = self.model(state.unsqueeze(0), hidden)
#                 return q_values.argmax().item(), hidden
#         else:
#             r = random.randint(0, 3)
#             return r, hidden
#
#     def update(self):
#         if len(self.replay_buffer) < self.batch_size:
#             return
#
#         batch = self.replay_buffer.sample(self.batch_size)
#
#         loss = 0
#         for sequence in batch:
#             states, actions, rewards, next_states, dones = zip(*sequence)
#
#             hidden = self.model.init_hidden(1)  # Initialize LSTM hidden state
#             q_values, hidden = self.model(states[0].unsqueeze(0), hidden)
#             q_value = q_values.gather(1, actions[0].unsqueeze(0))
#
#             next_hidden = self.target_model.init_hidden(1)
#             next_q_values, next_hidden = self.target_model(next_states[0].unsqueeze(0), next_hidden)
#             next_q_value = next_q_values.max(1)[0].detach()
#             expected_q_value = rewards[0] + self.gamma * next_q_value * (1 - dones[0].int())
#             loss += F.mse_loss(q_value, expected_q_value.unsqueeze(0))
#         self.optimizer.zero_grad()
#         loss.backward()
#         self.optimizer.step()
#
#     def update_target(self):
#         self.target_model.load_state_dict(self.model.state_dict())



# --------------------------------------------
# Trading environment using Yahoo Finance data

class TradingEnv(gym.Env):
    def __init__(self, df):
        super(TradingEnv, self).__init__()

        self.df = df
        self.current_step = 0

        self.action_space = gym.spaces.Discrete(3)  # 0: Hold, 1: Buy, 2: Sell
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)

        self.balance = 1000
        self.shares_held = 0
        self.current_price = 0
        self.net_worth = 1000

    def reset(self):
        self.balance = 1000
        self.shares_held = 0
        self.net_worth = 1000
        self.current_step = 0
        return self._next_observation(), {}

    def _next_observation(self):
        self.current_price = self.df.iloc[self.current_step]['Close']
        obs = np.array([
            self.df.iloc[self.current_step]['Open'],
            self.df.iloc[self.current_step]['Low'],
            self.df.iloc[self.current_step]['High'],
            self.current_price,
            self.df.iloc[self.current_step]['Volume'],
            self.df.iloc[self.current_step]['High'] - self.df.iloc[self.current_step]['Low']
        ])
        return obs

    def step(self, action):
        prev_net_worth = self.net_worth

        if action == 1:  # Buy
            if self.balance > self.current_price:
                self.shares_held += 1
                self.balance -= self.current_price
        elif action == 2:  # Sell
            if self.shares_held > 0:
                self.shares_held -= 1
                self.balance += self.current_price

        self.current_step += 1
        self.net_worth = self.balance + self.shares_held * self.current_price

        reward = self.net_worth - prev_net_worth
        done = self.current_step >= len(self.df) - 1

        return self._next_observation(), reward, done, {}

    def render(self):
        profit = self.net_worth - 1000
        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held}')
        print(f'Net worth: {self.net_worth}')
        print(f'Profit: {profit}')


# LSTM model for stock trading
def create_lstm_model(input_shape, output_shape, dropout_rate=0.2):
    model = tf.keras.Sequential([
        layers.LSTM(64, return_sequences=True, input_shape=input_shape),
        layers.Dropout(dropout_rate),
        layers.LSTM(64),
        layers.Dropout(dropout_rate),
        layers.Dense(32, activation='relu'),
        layers.Dense(output_shape, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='mse')
    return model


# Trading Agent with LSTM
class TradingAgent:
    def __init__(self, env, model_path=None,
                 target_update_freq=1,
                 epsilon=0.1, min_epsilon=0.01, epsilon_decay = 0.99):
        self.env = env
        if model_path and os.path.exists(model_path):
            print(f"Loading model from {model_path}")
            self.model = load_model(model_path)
        else:
            print("Creating new model")
            self.model = create_lstm_model((1, 6), env.action_space.n)


        self.target_model = create_lstm_model((1, 6), env.action_space.n)
        self.update_target_model()

        self.target_update_freq = target_update_freq
        # Notice: epsilon is not use due to the choose function
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        # --------------------------------

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def choose_action(self, state):
        state = state.reshape((1, 1, 6))  # Reshape for LSTM input
        probabilities = self.model.predict(state, verbose=0)[0]
        action = np.random.choice(self.env.action_space.n, p=probabilities)
        return action

    def train(self, episodes, file_name):

        for episode in range(episodes):
            print("E", episode)

            state, _= self.env.reset()
            # print("F", state)
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                # print("h", next_state)
                # print("kk", self.model.predict(next_state.reshape((1, 1, 6))))
                target = reward + (0.99 * np.max(self.model.predict(next_state.reshape((1, 1, 6)), verbose=0)))
                # print("i", target)
                target_f = self.model.predict(state.reshape((1, 1, 6)), verbose=0)
                target_f[0][action] = target
                self.model.fit(state.reshape((1, 1, 6)), target_f, epochs=1, verbose=0)

                state = next_state
                total_reward += reward

            if (episode + 1) % self.target_update_freq == 0:
                self.update_target_model()

            if (episode + 1) % 2 == 0:
                self.save(file_name)

            # Notice Decay epsilon has no effect. see choose function
            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay
                self.epsilon = max(self.min_epsilon, self.epsilon)

            print(f'Episode {episode + 1}/{episodes}, Total Reward: {total_reward}')
            print(next_state)


    def test(self):

        state, _= self.env.reset()
        done = False
        total_reward = 0
        while not done:
            action = self.choose_action(state)
            next_state, reward, done, _ = self.env.step(action)
            # print("h", next_state)
            # print("kk", self.model.predict(next_state.reshape((1, 1, 6))))
            target = reward + (0.99 * np.max(self.model.predict(next_state.reshape((1, 1, 6)), verbose=0)))

            # print("i", target)
            target_f = self.model.predict(state.reshape((1, 1, 6)), verbose=0)
            target_f[0][action] = target

            self.model.fit(state.reshape((1, 1, 6)), target_f, epochs=1, verbose=0)

            state = next_state
            total_reward += reward
        print("Total Reward", str(total_reward))

    def load(self, name):
        self.model = load_model(name)

    def save(self, file_name):
        self.model.save(file_name)

# Function to pull stock data using yfinance
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]

# --------------------------------------------


class RRLAlgo(object):
    def __init__(self, dic):
        # print("90567-8-000 Algo\n", dic, '\n', '-'*50)
        try:
            super(RRLAlgo, self).__init__()
        except Exception as ex:
            print("Error 9057-010 Algo:\n"+str(ex), "\n", '-'*50)
        # print("MLAlgo\n", self.app)
        # print("90004-020 Algo\n", dic, '\n', '-'*50)
        self.app = dic["app"]


# https://chatgpt.com/c/66e0947c-6714-800c-9ef3-3aa45026ed5a
class RRLDataProcessing(BaseDataProcessing, BasePotentialAlgo, RRLAlgo):
    def __init__(self, dic):
        # print("90567-010 DataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)

        self.PATH = os.path.join(self.TO_OTHER, "rrl")
        os.makedirs(self.PATH, exist_ok=True)
        print(f'{self.PATH}')

        self.days_of_investment = 30
        self.now_date = datetime.now()
        # -----
        self.end_date_1 = self.now_date - timedelta(days=self.days_of_investment-1)

        self.end_date = self.now_date - timedelta(days=self.days_of_investment)
        self.start_date = self.end_date - timedelta(days=365)

        print("self.now_date", self.now_date, "self.end_date", self.end_date,
              "self.end_date_1", self.end_date_1, "self.start_date", self.start_date)

    def train(self, dic):
        print("90199-RLL: \n", "="*50, "\n", dic, "\n", "="*50)

        # Load stock data using Yahoo Finance
        ticker = 'AAPL'  # Example: Apple stock
        df = yf.download(ticker, self.start_date, self.end_date)

        # print(df)
        env = TradingEnv(df)
        file_name_ = f'{self.PATH}pickles/{"rrl.pkl"}'
        # print(file_name_)
        agent = TradingAgent(env, model_path=file_name_, target_update_freq=1)
        agent.train(episodes=100, file_name=file_name_)

        print("Training is done")

        result = {"status": "ok"}
        return result

    def test(self, dic):
        print("90222-RLL: \n", "="*50, "\n", dic, "\n", "="*50)

        ticker = 'AAPL'  # Example: Apple stock
        df = yf.download(ticker, self.end_date_1, self.now_date)
        print(df)

        env = TradingEnv(df)
        # Create and train the trading agent
        file_name_ = f'{self.PATH}/pickles/{"rrl.pkl"}'
        agent = TradingAgent(env, model_path=file_name_, target_update_freq=1)

        agent.test()

        result = {"status": "ok"}
        return result


    def train2(self, dic):
        print("90199-RLL: \n", "="*50, "\n", dic, "\n", "="*50)
        episodes = int(dic["episodes"])

        env = GridWorldEnv(grid_size=5)
        agent = DQNAgent(input_dim=9, hidden_dim=128, output_dim=4)
        target_update_freq = 10

        for episode in range(episodes):
            state = torch.tensor(env.reset(), dtype=torch.float32).view(-1)
            hidden = agent.model.init_hidden(1)
            done = False
            sequence = []

            while not done:
                action, hidden = agent.select_action(state, hidden)
                next_state, reward, done = env.step(action)
                next_state = torch.tensor(next_state, dtype=torch.float32).view(-1)

                # print((state, torch.tensor([action]), torch.tensor([reward]), next_state, torch.tensor([done])))
                sequence.append((state, torch.tensor([action]), torch.tensor([reward]), next_state, torch.tensor([done])))
                if len(sequence) >= 10:  # Store only last 10 steps
                    agent.replay_buffer.push(sequence)
                    sequence = []
                state = next_state

            agent.update()

            if episode % target_update_freq == 0:
                agent.update_target()

        result = {"status": "ok"}
        return result


    def train1(self, dic):
        print("90155-dqn: \n", "="*50, "\n", dic, "\n", "="*50)

        # ticker_ = "GOOG" # dic["ticker"]
        # end_date = datetime.now()
        # start_date = end_date - timedelta(days=5000)
        # df = yf.download(ticker_, start_date, end_date)
        # # print("A\n", df)
        # df = df.drop('Close', 1).rename(columns={"Adj Close": "Close"})
        # # print("B\n", df)
        # df = df.reset_index()
        # print(df)

        # =====
        # Example data dimensions
        n_timesteps = 60  # Lookback window of 60 days
        n_features = 5  # e.g., OHLC and volume

        # Create the model
        model = create_rrl_model((n_timesteps, n_features))

        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy')

        # Example of running the model (for simplicity, using random data)
        X = np.random.rand(1000, n_timesteps, n_features)  # Simulated stock data
        y = np.random.randint(0, 3, size=(1000,))  # Random actions (buy/sell/hold)

        # Train the model (replace with actual market data and actions)
        model.fit(X, tf.keras.utils.to_categorical(y), epochs=10, batch_size=64)

        result = {"status": "ok"}
        return result


