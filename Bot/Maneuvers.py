import math
import time
from States import *
from Useful import *
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState

def dodging(agent,target_object,controller_state,angle_to_target):
    time_difference = time.time() - agent.start
    if time_difference > 2.2 and distance2D(target_object.location, agent.me.location) > 1300 and abs(angle_to_target) < 1.3 :
        agent.start = time.time()
    elif time_difference <= 0.1:
        controller_state.jump = True
        controller_state.pitch = -1
    elif time_difference >= 0.1 and time_difference <= 0.15:
        controller_state.jump = False
        controller_state.pitch = -1
    elif time_difference > 0.15 and time_difference < 1:
        controller_state.jump = True
        controller_state.yaw = controller_state.steer
        controller_state.pitch = -1
    return controller_state
def shot(agent,target_object,controller_state,angle_to_target):
    #shot
    if abs(angle_to_target) < math.pi/3 and agent.ball.local_location.data[1]>-50:
        time_difference = time.time() - agent.start
        if time_difference > 2.2 and abs(angle_to_target) < 1.3:
            agent.start = time.time()
        elif time_difference <= 0.4:
            controller_state.jump = True
            controller_state.pitch = 1
            controller_state.use_item = False
        elif time_difference >= 0.4 and time_difference <= 1:
            controller_state.jump = False
            controller_state.pitch = -1
            controller_state.use_item = False
        elif time_difference > 1 and time_difference < 1.4:
            controller_state.jump = True
            controller_state.yaw = controller_state.steer
            controller_state.use_item = True
            controller_state.pitch = -1
    return controller_state
