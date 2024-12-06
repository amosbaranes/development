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

from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv


class ReplayBuffer:
    def __init__(self, size):
        self.size = size  # max number of items in buffer
        self.buffer = []  # array to holde buffer
        self.next_id = 0

    def __len__(self):
        return len(self.buffer)

    def add(self, transition):
        # transition = (state, action, reward, next_state, done)
        # item = (state, action, reward, next_state, done)
        if len(self.buffer) < self.size:
            self.buffer.append(transition)
        else:
            self.buffer[self.next_id] = transition
        self.next_id = (self.next_id + 1) % self.size

    def sample(self, batch_size, state_size):
        # idxs = np.random.choice(len(self.buffer), batch_size)
        # samples = [self.buffer[i] for i in idxs]
        # states, actions, rewards, next_states, done_flags = list(zip(*samples))
        # return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(done_flags)

        minibatch = random.sample(self.buffer, min(len(self.buffer), batch_size))
        state = np.zeros((batch_size, state_size))
        next_state = np.zeros((batch_size, state_size))
        action, reward, done = [], [], []

        # do this before prediction
        # for speedup, this could be done on the tensor level
        # but easier to understand using a loop
        for i in range(batch_size):
            state[i] = minibatch[i][0]
            action.append(minibatch[i][1])
            reward.append(minibatch[i][2])
            next_state[i] = minibatch[i][3]
            done.append(minibatch[i][4])
        return state, action, reward, next_state,done

    def is_ready(self):
        if len(self.buffer) >= self.size:
            return True
        else:
            return False

class DQNAgent:
    def __init__(self):
        self.env_id = 'CartPole-v1'
        self.env = gym.make(self.env_id)
        # by default, CartPole-v1 has max episode steps = 500
        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n
        # self.memory = deque(maxlen=2000)

        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.999
        self.batch_size = 64
        self.train_start = 1000

        self.replay_buffer = ReplayBuffer(size = 2000)
        # create main model
        self.model = self.create_model()

    def create_model(self):
        X_input = Input((self.state_size,))
        action_space = self.action_size

        # 'Dense' is the basic form of a neural network layer
        # Input Layer of state size(4) and Hidden Layer with 51  nodes
        X = Dense(512, input_shape=(self.state_size,), activation="relu", kernel_initializer='he_uniform')(X_input)

        # Hidden layer with 256 nodes
        X = Dense(256, activation="relu", kernel_initializer='he_uniform')(X)

        # Hidden layer with 64 nodes
        X = Dense(64, activation="relu", kernel_initializer='he_uniform')(X)

        # Output Layer with # of actions:   nodes (left, right)
        X = Dense(action_space, activation="linear", kernel_initializer='he_uniform')(X)

        model = Model(inputs=X_input, outputs=X, name='CartPole')
        model.compile(loss="mse", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=["accuracy"])

        model.summary()
        return model

    # def update_replay_memory(self, transition):
    #     self.memory.append(transition)
    #     if len(self.memory) > self.train_start:
    #         if self.epsilon > self.epsilon_min:
    #             self.epsilon *= self.epsilon_decay

    def act(self, state):
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            return np.argmax(self.model.predict(state))

    def replay(self):

        # A33
        # # Randomly sample minibatch from the memory
        # minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))
        # state = np.zeros((self.batch_size, self.state_size))
        # next_state = np.zeros((self.batch_size, self.state_size))
        # action, reward, done = [], [], []
        #
        # # do this before prediction
        # # for speedup, this could be done on the tensor level
        # # but easier to understand using a loop
        # for i in range(self.batch_size):
        #     state[i] = minibatch[i][0]
        #     action.append(minibatch[i][1])
        #     reward.append(minibatch[i][2])
        #     next_state[i] = minibatch[i][3]
        #     done.append(minibatch[i][4])

        # do batch prediction to save speed
        state, action, reward, next_state, done = self.replay_buffer.sample(self.batch_size, self.state_size)

        target = self.model.predict(state)
        target_next = self.model.predict(next_state)

        for i in range(self.batch_size):
            # correction on the Q value for the action used
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                # Standard - DQN
                # DQN chooses the max Q value among next actions
                # selection and evaluation of action is on the target Q Network
                # Q_max = max_a' Q_target(s', a')
                target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))

        # Train the Neural Network with batches
        self.model.fit(state, target, batch_size=self.batch_size, verbose=0)

    def load(self, name):
        self.model = load_model(name)

    def save(self, name):
        self.model.save(name)

    def train(self, file_name, episodes):
        clear_log_debug()
        for e in range(episodes):
            log_debug("Episode A: " + str(e))
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            done = False
            i = 0
            log_debug("Episode AA: " + str(e))
            while not done:
                # self.env.render()
                action = self.act(state)
                next_state, reward, done, _ = self.env.step(action)
                next_state = np.reshape(next_state, [1, self.state_size])
                if not done or i == self.env._max_episode_steps - 1:
                    reward = reward
                else:
                    reward = -100

                # A33
                # self.update_replay_memory((state, action, reward, next_state, done))
                self.replay_buffer.add((state, action, reward, next_state, done))
                if self.replay_buffer.is_ready():
                    if self.epsilon > self.epsilon_min:
                        self.epsilon *= self.epsilon_decay
                    self.replay()

                state = next_state
                i += 1
                if done:
                    print("episode: {}/{}, score: {}, e: {:.2}".format(e, episodes, i, self.epsilon))
                    if i == 500:
                        print("Saving trained model as cartpole-dqn.keras")
                        log_debug("file_name: " + file_name)
                        log_debug("Episode Z1: ")
                        self.save(file_name)
                        log_debug("Episode Z2: ")


            log_debug("Episode B: " + str(e))
        log_debug("End Train...")

    def test(self, file_name, episodes):
        clear_log_debug()
        self.load(file_name)
        all_states = []
        for e in range(episodes):
            log_debug("Episode A: " + str(e))
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            episode_states = []
            for time in range(500):
                action = np.argmax(self.model.predict(state))
                next_state, reward, done, _ = self.env.step(action)
                episode_states.append(next_state.tolist())
                state = np.reshape(next_state, [1, self.state_size])
                if done:
                    break
            all_states.append(episode_states)
            log_debug("Episode B: " + str(e))
        log_debug("End Test...")
        return all_states

    def record_video(self, video_folder, video_length):

        # vec_env = DummyVecEnv([lambda: gym.make(self.env_id, render_mode="rgb_array")])
        # # Record the video starting at the first step
        # vec_env = VecVideoRecorder(vec_env, video_folder,
        #                        record_video_trigger=lambda x: x == 0, video_length=video_length,
        #                        name_prefix=f"{type(self).__name__}-{self.env_id}")

        # Initialize DummyVecEnv without render_mode
        vec_env = DummyVecEnv([lambda: gym.make(self.env_id)])

        # Set up VecVideoRecorder to record the video
        vec_env = VecVideoRecorder(vec_env, video_folder,
            record_video_trigger=lambda x: x == 0, video_length=video_length,
            name_prefix=f"{type(self).__name__}-{self.env_id}"
        )

        obs = vec_env.reset()
        for _ in range(video_length + 1):
            # action = np.argmax(self.get_qvalues(obs),axis=-1)
            action = np.argmax(self.model.predict(obs))
            obs, _, _, _ = vec_env.step(action)
        # video filename
        file_path = "./"+video_folder+vec_env.video_recorder.path.split("/")[-1]
        # Save the video
        vec_env.close()
        return file_path

    def play_video(self, file_path):
        mp4 = open(file_path, 'rb').read()
        data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
        return HTML("""
            <video width=400 controls>
                  <source src="%s" type="video/mp4">
            </video>
            """ % data_url)


class DNQAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90567-8-000 DNQAlgo\n", dic, '\n', '-'*50)
        try:
            super(DNQAlgo, self).__init__()
        except Exception as ex:
            print("Error 9057-010 DNQAlgo:\n"+str(ex), "\n", '-'*50)
        # print("MLAlgo\n", self.app)
        # print("90004-020 DNQAlgo\n", dic, '\n', '-'*50)
        self.app = dic["app"]


class DNQDataProcessing(BaseDataProcessing, BasePotentialAlgo, DNQAlgo):
    def __init__(self, dic):
        # print("90567-010 DNQDataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DNQDataProcessing ", self.app)

    def train(self, dic):
        print("90155-dqn: \n", "="*50, "\n", dic, "\n", "="*50)

        # n_timesteps = 60  # Lookback window of 60 days
        # n_features = 5  # e.g., OHLC and volume
        #
        # # Example of running the model (for simplicity, using random data)
        # X = np.random.rand(1000, n_timesteps, n_features)  # Simulated stock data
        # y = np.random.randint(0, 3, size=(1000,))  # Random actions (buy/sell/hold)
        # print(X, "\n\n", X.shape, "\n\n", y)
        #
        #
        # return

        episodes = int(dic["episodes"])
        # ---

        agent = DQNAgent()
        save_to_file = os.path.join(self.TO_OTHER, "cartpole-dqn.keras")
        agent.train(save_to_file, episodes)

        result = {"status": "ok dqn"}
        return result

    def test(self, dic):
        print("90155-dqn: \n", "="*50, "\n", dic, "\n", "="*50)
        episodes = int(dic["episodes"])
        # ---

        agent = DQNAgent()
        read_from_file = os.path.join(self.TO_OTHER, "cartpole-dqn.keras")
        results = agent.test(read_from_file, episodes)
        for i in results:
            print(i)

        result = {"status": "ok dqn", "results": results}
        return result

    def record_video(self, dic):
        print("9034-dqn-video: \n", "="*50, "\n", dic, "\n", "="*50)

        video_folder = self.TO_OTHER
        video_length = 500
        agent = DQNAgent()
        agent.record_video(video_folder, video_length)



        result = {"status": "ok dqn record_video"}
        return result

