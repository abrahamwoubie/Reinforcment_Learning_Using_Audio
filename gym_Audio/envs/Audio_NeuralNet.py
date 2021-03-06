import gym
import gym_Audio
import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt


env = gym.make('Audio-v0')
tf.reset_default_graph()


number_of_episodes=[]
number_of_iterations_per_episode=[]

#Define the Placeholder for the Input Data and Variables for the Weights¶
#The activation function is the argmax, which returns the maximum value.

inputs1 = tf.placeholder(shape=[1,400],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([400,4],0,0.01))

Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,1)

#Define next state and error correction techniques
nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)

init = tf.initialize_all_variables()

# Set learning parameters
y = .99
e = 0.1
num_episodes = 2000
#create lists to contain total rewards and steps per episode
jList = []
rList = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        #Reset environment and get first new observation
        s = env.reset()
        #env.render()
        number_of_episodes.append(i)
        rAll = 0
        d = False
        j = 0
        #The Q-Network
        done=False
        while not done:
        #while j < 100:
            j+=1
            #env.render()
            #Choose an action by greedily (with e chance of random action) from the Q-network
            #a,allQ = sess.run([predict,Qout],feed_dict={inputs1:np.identity(16)[s:s+1]})
            a, allQ = sess.run([predict, Qout], feed_dict={inputs1: np.identity(400)[s:s + 1]})
            if np.random.rand(1) < e:
                a[0] = env.action_space.sample()
            #Get new state and reward from environment
            s1,r,d,_ = env.step(a[0])
            #Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout,feed_dict={inputs1:np.identity(400)[s1:s1+1]})
            #Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0,a[0]] = r + y*maxQ1
            #Train our network using target and predicted Q values
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:np.identity(400)[s:s+1],nextQ:targetQ})
            rAll += r
            s = s1
            if d == True:
                #print("Iteration Number {} has finished with {} number of timestamps".format(i, j - 1))
                #Reduce chance of random action as we train the model.
                e = 1./((i/50) + 10)
                break
        #jList.append(j)
        number_of_iterations_per_episode.append(j - 1)
        rList.append(rAll)


percentage_of_successful_episodes=(sum(rList)/num_episodes)*100
print("Reward List",rList)
print ("Percent of successful episodes: ",percentage_of_successful_episodes,"%")

plt.plot(np.arange(len(number_of_episodes)), number_of_iterations_per_episode)
plt.ylabel('Number of Iterations')
plt.xlabel('Episode #')
#plt.grid(True)
#plt.savefig("test.png")
plt.show()

