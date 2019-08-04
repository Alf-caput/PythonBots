import math
import time

from States import *
from Useful import *
from Controllers import *

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket



class Bot(BaseAgent):

    def initialize_agent(self):
        self.me = obj()
        self.mate = obj()
        self.ball = obj()
        self.ball_shadow = obj()
        self.enemy_goal = obj()
        self.our_goal = obj()
        self.pointA = obj()
        self.pointB = obj()
        self.start = time.time()
        #self.state = exampleATBA()
        
        
        
    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        controller_state = SimpleControllerState()
        self.preprocess(game)
        return self.state.execute(self)

    

    def preprocess(self,game):
        self.me.location.data = [game.game_cars[self.index].physics.location.x,game.game_cars[self.index].physics.location.y,game.game_cars[self.index].physics.location.z]
        self.me.velocity.data = [game.game_cars[self.index].physics.velocity.x,game.game_cars[self.index].physics.velocity.y,game.game_cars[self.index].physics.velocity.z]
        self.me.rotation.data = [game.game_cars[self.index].physics.rotation.pitch,game.game_cars[self.index].physics.rotation.yaw,game.game_cars[self.index].physics.rotation.roll]
        self.me.rvelocity.data = [game.game_cars[self.index].physics.angular_velocity.x,game.game_cars[self.index].physics.angular_velocity.y,game.game_cars[self.index].physics.angular_velocity.z]
        self.me.matrix = rotator_to_matrix(self.me)
        self.me.boost = game.game_cars[self.index].boost
        self.me.has_wheel_contact = game.game_cars[self.index].has_wheel_contact
        self.me.team = game.game_cars[self.index].team
        
        for i in range(0,game.num_cars):
            if game.game_cars[i].team == self.me.team and i!=self.index:
                self.mate.location.data = [game.game_cars[i].physics.location.x,game.game_cars[i].physics.location.y,game.game_cars[i].physics.location.z]
                self.mate.local_location.data = to_local(self.mate,self.me)
                break
            else:
                self.mate.location.data = [9999,9999,9999]
        
        self.ball.location.data = [game.game_ball.physics.location.x,game.game_ball.physics.location.y,game.game_ball.physics.location.z]
        self.ball.velocity.data = [game.game_ball.physics.velocity.x,game.game_ball.physics.velocity.y,game.game_ball.physics.velocity.z]
        self.ball.rotation.data = [game.game_ball.physics.rotation.pitch,game.game_ball.physics.rotation.yaw,game.game_ball.physics.rotation.roll]
        self.ball.rvelocity.data = [game.game_ball.physics.angular_velocity.x,game.game_ball.physics.angular_velocity.y,game.game_ball.physics.angular_velocity.z]
        self.ball.local_location.data = to_local(self.ball,self.me)
        
        '''ball_prediction = self.get_ball_prediction_struct()

        if ball_prediction is not None:
            for i in range(0, ball_prediction.num_slices):
                prediction_slice = ball_prediction.slices[i]
                location = prediction_slice.physics.location
                self.logger.info("At time {}, the ball will be at ({}, {}, {})"
                                 .format(prediction_slice.game_seconds, location.x, location.y, location.z))'''
        
        
        self.ball_shadow.location.data = [game.game_ball.physics.location.x,game.game_ball.physics.location.y + sign(self.me.team)*3000,game.game_ball.physics.location.z]

        self.ball_shadow.local_location.data = to_local(self.ball_shadow,self.me)
        
        self.enemy_goal.location.data = [0,-sign(game.game_cars[self.index].team)*5120,0]
        self.enemy_goal.local_location.data = to_local(self.enemy_goal,self.me)
        
        self.our_goal.location.data = [0,sign(game.game_cars[self.index].team)*5120,0]
        self.our_goal.local_location.data = to_local(self.our_goal,self.me)
        
        if self.me.location.data[0]>=0:
            self.pointA.location.data = [4000,-sign(self.me.team)*(min(200+self.me.location.data[2],400)),2000]
            self.pointA.local_location.data = to_local(self.pointA,self.me)
            
            self.pointB.location.data = [4000,-sign(self.me.team)*1000,2000]
            self.pointB.local_location.data = to_local(self.pointB,self.me)
        else:
            self.pointA.location.data = [-4000,-sign(self.me.team)*max(-200-self.me.location.data[2],-400),2000]
            self.pointA.local_location.data = to_local(self.pointA,self.me)
            
            self.pointB.location.data = [-4000,-sign(self.me.team)*1000,2000]
            self.pointB.local_location.data = to_local(self.pointB,self.me)
            
        if (self.me.team==1 and self.me.location.data[1]>-400 and self.me.location.data[1]<2500)or(self.me.team==0 and self.me.location.data[1]<400 and self.me.location.data[1]>-2500):
            flag=True
        else:
            flag=False
            
            
        
        if distance2D(self.ball,self.me)>200:
            if distance2D(self.ball,self.mate)>=distance2D(self.ball,self.me) or distance2D(self.me,self.our_goal)<1500:
                self.state = exampleATBA()
            else:
                self.state = Wait()
        elif flag and self.me.has_wheel_contact and distance2D(self.me,self.pointA)<distance2D(self.me,self.enemy_goal) and abs(self.me.location.data[0])>2000:#self.me.location.data[1]<sign(self.me.team)*300 and abs(self.me.location.data[0])>2000:# and self.me.has_wheel_contact:
            self.state = CeilingRush()
        else:
            self.state = Rush()
        
        self.controller_state = self.state


