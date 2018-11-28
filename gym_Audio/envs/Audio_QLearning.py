import gym
import gym_Audio
import numpy as np
env = gym.make('Audio-v0')

#Initialize table with all zeros
Q = np.zeros([env.observation_space.n,env.action_space.n])

# Set learning parameters
lr = .8
y = .95
num_episodes = 2000

#create lists to contain total rewards and steps per episode
#jList = []

rList = []
for i in range(num_episodes):
    print("*******************************************************************")
     #Reset environment and get first new observation
    s = env.reset()
    env.render()
    rAll = 0
    d = False
    j = 0
    #The Q-Table learning algorithm
    while j < 200:
        env.render()
        j+=1
        #Choose an action by greedily picking from Q table
        a = np.argmax(Q[s,:] + np.random.randn(1,env.action_space.n)*(1./(i+1)))
        #Get new state and reward from environment
        s1,r,d,_ = env.step(a)
        #Update Q-Table with new knowledge
        Q[s,a] = Q[s,a] + lr*(r + y*np.max(Q[s1,:]) - Q[s,a])
        rAll += r
        s = s1
        if d == True:
            print("Iteration Number {} has finished with {} number of timestamps".format(i,j))
            break
    #jList.append(j)
    rList.append(rAll)
percentage_of_successful_episodes=(sum(rList)/num_episodes)*100
print("Reward List",rList)
print ("Percent of succesful episodes: ",percentage_of_successful_episodes, "%")

