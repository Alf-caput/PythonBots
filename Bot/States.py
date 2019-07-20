import math
from Useful import* 
from rlbot.agents.base_agent import  SimpleControllerState


class exampleATBA:
    def __init__(self):
        self.expired = False

    def execute(self, agent):
        target_object = agent.ball
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball,agent.me)/1.5)
        
        self.controller_state = exampleController(agent,self,target_object,target_speed)
        
        return agent.exampleController(target_object, target_speed)
        
class Rush:
    def __init__(self):
        self.expired = False

    def execute(self, agent):
        target_object = agent.enemy_goal
        target_speed = 1000
        
        self.controller_state = exampleController(agent,self,target_object,target_speed)
        
        return agent.exampleController(target_object, target_speed)
