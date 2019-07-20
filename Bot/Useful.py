import math
import time
from States import *
from Controllers import *

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

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
