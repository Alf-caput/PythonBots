import math
import time
from States import *
from Useful import *
from Maneuvers import *
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

def exampleController(agent,target_object,target_speed): #target_object es un objeto tipo obj 
        
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_target = math.atan2(location.data[1],location.data[0])
        angle_velocity = math.atan2(agent.me.velocity.data[1],agent.me.velocity.data[1])
        draw_debug(agent.renderer,target_object.location.data)
        
        current_speed = velocity2D(agent.me)
        #steering
        if abs(angle_to_target)<math.pi/4:
            if agent.me.has_wheel_contact == True:
                controller_state.boost = True 
            controller_state.handbrake = False
        else:
            controller_state.boost = False
            controller_state.handbrake = True
        controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))

        #throttle
        '''if target_speed > current_speed:
            controller_state.throttle = 1.0
            if target_speed > 1400 and agent.start > 2.2 and current_speed < 2250:
                controller_state.boost = True
        elif target_speed < current_speed:
            controller_state.throttle = .5'''
        controller_state.throttle = 1
        
        #dodging 
        if  abs(angle_to_target) < math.pi/2 and abs(angle_velocity) < math.pi/3:
            dodging(agent,target_object,controller_state,angle_to_target)
        return controller_state

def RushController(agent,target_object,target_speed): #target_object es un objeto tipo obj 
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_target = math.atan2(location.data[1],location.data[0])
        angle_velocity = math.atan2(agent.me.velocity.data[1],agent.me.velocity.data[1])
        draw_debug(agent.renderer,target_object.location.data)
        
        current_speed = velocity2D(agent.me)
        #steering
        if abs(angle_to_target) < math.pi/4:
            controller_state.boost = True
            controller_state.handbrake = False
        elif abs(angle_to_target) < math.pi and abs(angle_to_target) > math.pi/2:
            controller_state.boost = False
            controller_state.handbrake = True
        controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))
        #throttle
        controller_state.throttle = 1
        #shot
        if abs(angle_velocity) < math.pi/2 :
            shot(agent,target_object,controller_state,angle_to_target)
        
        return controller_state





