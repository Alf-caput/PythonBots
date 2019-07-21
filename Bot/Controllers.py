import math
import time
from States import *
from Useful import *
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

def exampleController(agent,target_object,target_speed): #target_object es un objeto tipo obj 
        
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_target = math.atan2(location.data[1],location.data[0])
        
        draw_debug(agent.renderer,target_object.location.data)
        
        current_speed = velocity2D(agent.me)
        #steering
        if abs(angle_to_target)<math.pi/4:
            controller_state.boost = True
            controller_state.handbrake = False
        else:
            controller_state.boost = False
            controller_state.handbrake = True
        controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))

        #throttle
        '''if target_speed > current_speed:
            controller_state.throttle = 1.0
            if target_speed > 1400 and self.start > 2.2 and current_speed < 2250:
                controller_state.boost = True
        elif target_speed < current_speed:
            controller_state.throttle = 0'''
        controller_state.throttle = 1
        '''#dodging
        time_difference = time.time() - self.start
        if time_difference > 2.2 and distance2D(target_object.location, self.me.location) > 1000 and abs(angle_to_ball) < 1.3:
            self.start = time.time()
        elif time_difference <= 0.1:
            controller_state.jump = True
            controller_state.pitch = -1
        elif time_difference >= 0.1 and time_difference <= 0.15:
            controller_state.jump = False
            controller_state.pitch = -1
        elif time_difference > 0.15 and time_difference < 1:
            controller_state.jump = True
            controller_state.yaw = controller_state.steer
            controller_state.pitch = -1'''

        return controller_state

def RushController(agent,target_object,target_speed): #target_object es un objeto tipo obj 
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_target = math.atan2(location.data[1],location.data[0])
        
        draw_debug(agent.renderer,target_object.location.data)
        
        current_speed = velocity2D(agent.me)
        #steering
        if abs(angle_to_target)<math.pi/4:
            controller_state.boost = True
            controller_state.handbrake = False
        else:
            controller_state.boost = False
            controller_state.handbrake = True
        controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))
        #throttle
        controller_state.throttle = 1
        #dodging
        if abs(angle_to_target) < math.pi/4 :#and anglevelocity_to_target= math.atan2(location.data[1],location.data[0]):
            time_difference = time.time() - agent.start
            if time_difference > 2.2 and distance2D(target_object.location, agent.me.location) > 1000 and abs(angle_to_target) < 1.3:
                agent.start = time.time()
            elif time_difference <= 0.4:
                controller_state.jump = True
                controller_state.pitch = 1
                controller_state.use_item = False
            elif time_difference >= 0.4 and time_difference <= 0.5:
                controller_state.jump = False
                controller_state.pitch = -1
                controller_state.use_item = False
            elif time_difference > 0.5 and time_difference < 1:
                controller_state.jump = True
                controller_state.yaw = controller_state.steer
                controller_state.use_item = True
                controller_state.pitch = -1       
        return controller_state




def velocity2D(target_object):
    return math.sqrt(target_object.velocity.data[0]**2 + target_object.velocity.data[1]**2)
    
class Vector3:
    def __init__(self, data):
        self.data = data
    def __sub__(self,value):
        return Vector3([self.data[0]-value.data[0],self.data[1]-value.data[1],self.data[2]-value.data[2]])
    def __mul__(self,value):
        return (self.data[0]*value.data[0] + self.data[1]*value.data[1] + self.data[2]*value.data[2])
    

class obj:
    def __init__(self):
        self.location = Vector3([0,0,0])
        self.velocity = Vector3([0,0,0])
        self.rotation = Vector3([0,0,0])
        self.rvelocity = Vector3([0,0,0])
        
        self.local_location = Vector3([0,0,0])
        self.boost = 0
#
def to_local(target_object,our_object):
    x = (target_object.location - our_object.location) * our_object.matrix[0]
    y = (target_object.location - our_object.location) * our_object.matrix[1]
    z = (target_object.location - our_object.location) * our_object.matrix[2]
    return [x,y,z]

def rotator_to_matrix(our_object):
    r = our_object.rotation.data
    CR = math.cos(r[2])
    SR = math.sin(r[2])
    CP = math.cos(r[0])
    SP = math.sin(r[0])
    CY = math.cos(r[1])
    SY = math.sin(r[1])

    matrix = []
    matrix.append(Vector3([CP*CY, CP*SY, SP]))
    matrix.append(Vector3([CY*SP*SR-CR*SY, SY*SP*SR+CR*CY, -CP * SR]))
    matrix.append(Vector3([-CR*CY*SP-SR*SY, -CR*SY*SP+SR*CY, CP*CR]))
    return matrix

def velocity2D(target_object):
    return math.sqrt(target_object.velocity.data[0]**2 + target_object.velocity.data[1]**2)

def distance2D(target_object, our_object):
    if isinstance(target_object,Vector3):
        difference = target_object - our_object
    else:
        difference = target_object.location - our_object.location
    return math.sqrt(difference.data[0]**2 + difference.data[1]**2)
    

def sign(x):
    if x<=0:
        return -1
    else:
        return 1
