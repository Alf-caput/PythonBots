import math
import time
from States import *
from Useful import *

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket



class Gosling(BaseAgent):

    def initialize_agent(self):
        self.me = obj()
        self.ball = obj()
        self.enemy_goal = obj()
        self.start = time.time()
        #self.state = exampleATBA()
        
        
    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        controller_state = SimpleControllerState()
        self.preprocess(game)
        return self.state.execute(self)

    def exampleController(self,target_object,target_speed): #target_object es un objeto tipo obj 
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_target = math.atan2(location.data[1],location.data[0])
        
        draw_debug(self.renderer,target_object.location.data)
        
        current_speed = velocity2D(self.me)
        #steering
        if abs(angle_to_target)<math.pi/4:
            controller_state.boost = True
            controller_state.handbrake = False
        else:
            controller_state.boost = False
            controller_state.handbrake = True
        controller_state.steer = sign(angle_to_target)*min(1,abs(2*angle_to_target))
        
            #controller.Steer = Math.Sign(relativeBotToTargetAngle.Z) * Math.Min(1, Math.Abs(2f * relativeBotToTargetAngle.Z));

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

    def preprocess(self,game):
        self.me.location.data = [game.game_cars[self.index].physics.location.x,game.game_cars[self.index].physics.location.y,game.game_cars[self.index].physics.location.z]
        self.me.velocity.data = [game.game_cars[self.index].physics.velocity.x,game.game_cars[self.index].physics.velocity.y,game.game_cars[self.index].physics.velocity.z]
        self.me.rotation.data = [game.game_cars[self.index].physics.rotation.pitch,game.game_cars[self.index].physics.rotation.yaw,game.game_cars[self.index].physics.rotation.roll]
        self.me.rvelocity.data = [game.game_cars[self.index].physics.angular_velocity.x,game.game_cars[self.index].physics.angular_velocity.y,game.game_cars[self.index].physics.angular_velocity.z]
        self.me.matrix = rotator_to_matrix(self.me)
        self.me.boost = game.game_cars[self.index].boost
        
        self.ball.location.data = [game.game_ball.physics.location.x,game.game_ball.physics.location.y,game.game_ball.physics.location.z]
        self.ball.velocity.data = [game.game_ball.physics.velocity.x,game.game_ball.physics.velocity.y,game.game_ball.physics.velocity.z]
        self.ball.rotation.data = [game.game_ball.physics.rotation.pitch,game.game_ball.physics.rotation.yaw,game.game_ball.physics.rotation.roll]
        self.ball.rvelocity.data = [game.game_ball.physics.angular_velocity.x,game.game_ball.physics.angular_velocity.y,game.game_ball.physics.angular_velocity.z]

        self.ball.local_location.data = to_local(self.ball,self.me)
        
        self.enemy_goal.location.data = [0,-sign(game.game_cars[self.index].team)*5120,0]
        self.enemy_goal.local_location.data = to_local(self.enemy_goal,self.me)
        
        if distance2D(self.ball,self.me)<200:
            self.state = Rush()
        else:
            self.state = exampleATBA()



