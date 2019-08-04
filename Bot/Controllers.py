import math
import time

from Useful import *
from Maneuvers import *
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

def exampleController(agent,target_object): #target_object es un objeto tipo obj 
        
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_target = math.atan2(location.data[1],location.data[0])
        angle_velocity = math.atan2(agent.me.velocity.data[1],agent.me.velocity.data[1])
        #draw_debug(agent.renderer,location.data)
        draw_debug(agent,agent.renderer,target_object.location.data)
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
        controller_state.throttle=1
        #dodging 
        if  abs(angle_to_target) < math.pi/2 and abs(angle_velocity) < math.pi/3:
            dodging(agent,target_object,controller_state,angle_to_target)
        return controller_state

def CeilingRushController(agent,target_object1,target_object2): #target_object es un objeto tipo obj 
        controller_state = SimpleControllerState()
            
        '''if distance2D(agent.me,agent.pointA)<distance2D(agent.me,agent.pointB) and agent.me.location.data[2]>2800:
            target_object = target_object2
            location = agent.pointB.local_location
            angle_to_target = math.atan2(location.data[1],location.data[0])
        else:
            target_object = target_object1
            location = agent.pointA.local_location
            angle_to_target = math.atan2(location.data[1],location.data[0])'''
        target_object = target_object1
        location = agent.pointA.local_location
        angle_to_target = math.atan2(location.data[1],location.data[0])
        draw_debug(agent,agent.renderer,target_object.location.data)
        angle_velocity = math.atan2(agent.me.velocity.data[1],agent.me.velocity.data[1])
        #draw_debug(agent.renderer,target_object.location.data)
        
        current_speed = velocity2D(agent.me)
        #steering
        if abs(angle_to_target) < math.pi/4:
            controller_state.handbrake = False
        elif abs(angle_to_target) < math.pi and abs(angle_to_target) > math.pi/2:
            controller_state.handbrake = True
        if agent.me.location.data[2]<1800:
            controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))
        else:
            controller_state.steer = 0
        #throttle
        controller_state.throttle = 1
        
        return controller_state

def RushController(agent,target_object): #target_object es un objeto tipo obj 
        controller_state = SimpleControllerState()
        location = target_object.local_location
        angle_to_target = math.atan2(location.data[1],location.data[0])
        
        angle_velocity = math.atan2(agent.me.velocity.data[1],agent.me.velocity.data[1])
        draw_debug(agent,agent.renderer,target_object.location.data)
        #steering
        if abs(angle_to_target) < math.pi/4:
            controller_state.handbrake = False
        elif abs(angle_to_target) < math.pi and abs(angle_to_target) > math.pi/2:
            controller_state.handbrake = True
        controller_state.yaw = controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))
        #throttle
        controller_state.throttle = 1
        #shot
        if True:#abs(angle_velocity) < math.pi/3:
            shot(agent,target_object,controller_state,angle_to_target)
        
        return controller_state

def WaitController(agent,target_object,target_speed):
        current_speed = velocity2D(agent.me)
        controller_state = SimpleControllerState()
        location = target_object.local_location
        angle_to_target = math.atan2(location.data[1],location.data[0])
        draw_debug(agent,agent.renderer,target_object.location.data)
        if abs(angle_to_target) < math.pi/4:
            controller_state.handbrake = False
        elif abs(angle_to_target) < math.pi and abs(angle_to_target) > math.pi/2:
            controller_state.handbrake = True
        
        controller_state.yaw = controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))
        if  distance2D(target_object,agent.me)<100:
            controller_state.throttle = -1
        else:
            controller_state.throttle = 1
        return controller_state




