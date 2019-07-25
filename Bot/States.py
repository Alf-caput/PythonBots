import math
from Useful import* 
from Controllers import *
from rlbot.agents.base_agent import  SimpleControllerState


class exampleATBA:
    def __init__(self):
        self.expired = False

    def execute(self, agent):
        target_object = agent.ball
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball,agent.me)/1.5)
                
        return exampleController(agent,target_object)
        
class CeilingRush:
    def __init__(self):
        self.expired = False

    def execute(self, agent):
        target_object1 = agent.pointA
        target_object2 = agent.pointB
        
        return CeilingRushController(agent,target_object1,target_object2)
        
class Rush:
    def __init__(self):
        self.expired = False

    def execute(self, agent):
        target_object = agent.enemy_goal
        
        return RushController(agent,target_object)

class Wait:
    def __init__(self):
        self.expired = False

    def execute(self, agent):
        target_object = agent.ball_shadow
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball,agent.me)/1.5)
        
        return WaitController(agent,target_object,target_speed)
