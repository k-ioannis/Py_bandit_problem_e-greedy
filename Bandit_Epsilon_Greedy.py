import math
import random
import time 
import numpy
from dataclasses import dataclass


#~~ Data structure to store important data ~~# 
@dataclass
class Bandit:
    arms      : list
    visited   : list
    arm_sum   : int 

@dataclass
class Agent:
    rewards   : list 
    machine   : int 
    arm       : int 
    tokens    : int 

    
#Setting the bandit enviroment as dataclasses(structures) inside a list 
def set_Bandits( Machines , Levers ):
    
    #List containing the probability of each arm to be pulled
    arms     = []
    visited  = []
    #List that holds that structures of the bandits 
    nBandits = []
    
    
    for i in range( Machines ):
        
        #loop to store the probabilities of the levers 
        for j in range( Levers ):
            arms.append(  round( random.random(  ) , 2 ) )
            visited.append(0)
        #loop to store the levers of the machines 
        nBandit = Bandit( arms , visited, Levers ) 
        nBandits.append( nBandit )
        print( nBandits[i].arms, nBandits[i].visited )
        
        #clearing the list of the levers
        arms    = []
        visited  = []
        
    return nBandits

#epsilon greeedy algorithm
def eps_Greedy( nBandits , agent , epsilon):
    
     
    while True:
        
        #If the agent runs out of tokens stop the session
        if agent.tokens == 0:
            break
        
        
        #Set condition to explore the first time 
        if agent.machine == -1:
            
            time.sleep( 1 )
            print( "[FIRST TIME IS EXPLORE]" )
            explore_Machine( nBandits , agent  )
        
        #the chances after are based on the epsilon parameter 
        else:
            #Rolling for the Probability to Explore
            roll = round ( random.random() , 2)

            
            if roll <= epsilon:
                
                time.sleep( 2 )
                print( "[ EXPLORING ]" )
                explore_Machine( nBandits , agent  )
            
            else:
                
                time.sleep( 2 )
                print( "[ EXPLOITING ]" )
                exploit_Machine( nBandits , agent  ) 
        agent.tokens -= 1   
        
    
    return 0 

def explore_Machine( nBandits , agent ):
   
    agent.machine = random.randint(1 , Machines)
    print( "    ~EXPLORING MACHINE: " , agent.machine )
    
    
    
    #Getting a random Lever to pull since we Expl
    ind = agent.machine - 1
    upLimit     = nBandits[ ind ].arm_sum

    random_Arm  = random.randint(1,  upLimit)
    roll        = round ( random.random() , 2)
    nBandits[ ind ].visited[ random_Arm - 1 ]   += 1 
    visit       = nBandits[ ind ].visited[ random_Arm - 1 ]

    time.sleep( 1 )
    print("    ~Pulling arm ", random_Arm)
    if (roll >= nBandits[ ind ].arms[ random_Arm - 1] ):
        print("    ~Scored: +1")
        reward = agent.rewards[ ind ][ random_Arm - 1 ] +  1 / visit 
        agent.rewards[ ind ][ random_Arm - 1 ] = round( reward , 2)   
    
    else:
        print("    ~Unlucky didnt score")
        reward = agent.rewards[ ind ][ random_Arm - 1 ] -  1 / visit 
        agent.rewards[ ind ][ random_Arm - 1 ] = round( reward , 2)
        
    print( "    ~Aaverage reward: " ,   agent.rewards[ ind ][ random_Arm - 1 ])
    print( "    ~Times pulled: " , nBandits[ ind ].visited[ random_Arm - 1 ] )
    
    
    
        

    return 0


def exploit_Machine( nBandits , agent  ):
    index         = numpy.argmax(  agent.rewards )
    Machine_index = int(index / len( nBandits ) ) 
    Lever_index   = (index % nBandits[0].arm_sum) 
    nBandits[ Machine_index ].visited[ Lever_index ]   += 1 
    visit         = nBandits[ Machine_index ].visited[ Lever_index ]
    #print(index, Machine_index, Lever_index )
    
    
    
    print("    ~EXPLOITING MACHINE: " , Machine_index + 1)
    print("    ~pulling arm       : " , Lever_index + 1)
    time.sleep( 1 )
    roll        = round ( random.random() , 2)
    if (roll >= nBandits[ Machine_index ].arms[ Lever_index ] ):
        print("    ~Scored: +1")
        reward = agent.rewards[ Machine_index ][ Lever_index ] +  1 / visit 
        agent.rewards[ Machine_index ][ Lever_index ] = round( reward , 2) 
    else:
        print("    ~Unlucky didnt score")
        reward = agent.rewards[ Machine_index ][ Lever_index ] -  1 / visit 
        agent.rewards[ Machine_index ][ Lever_index ] = round( reward , 2) 
    
    print( "    ~Aaverage reward: " ,   agent.rewards[ Machine_index ][ Lever_index ])
    print( "    ~Times pulled: " , nBandits[ Machine_index ].visited[ Lever_index ] )
    return 0 



#~ ~ ~ ~ ~ ~ C A L L S ~ ~ ~ ~ ~ ~ ~ #
Machines = int( input("Enter number of Machines: ") )

Levers   = int( input("Enter number of Levers:   ") )


#Setting the bandits by initializing 
#the Probabilities of each Lever 
nBandits = set_Bandits( Machines , Levers )


#Initilizing the agent 
visited  = []
rewards  = []
temp     = []
machine  = -1
arm      = -1
tokens   = int( input("~ Type number of Tokens to spend: ") )
for i in range( Machines ):
    
    for j in range( Levers ):
        temp.append(0)
    rewards.append( temp )
    temp = []
print( "Machine Reward Lists: ", rewards )
agent    = Agent(rewards , machine , arm, tokens )
#print( agent )


epsilon  = 0.1
eps_Greedy ( nBandits , agent  , epsilon )

