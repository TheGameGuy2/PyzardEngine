from game_object_core import*
from collisions import*
from game_mng import GameVars
from GameApp import game_scene
from GameApp import App
from player_movement import player

class TowerBehav(Component):
    #creating new component to add to 'tower' 
    def __init__(self,tower:GameObject):
        #setting name and parent object
        super().__init__("tower_scpt",tower)
        self.tower=tower
        
        #getting collider of the tower object
        self.col:ColliderComponent=tower.get_component("collider")

        #getting collider of player
        self.pl_col:ColliderComponent=player.get_component("collider")

    def on_update(self):
        #logic to execute every frame. on_update is inherit from 'Component'

        if self.col.check_collision(self.pl_col):
            #check if colliding with player
            print("player colliding!!!")

        if self.tower.position.x<0:
            #check if going out of screen, and if, reseting position
            self.tower.position.x=600
        
        #moving 
        self.tower.position.x-=50*GameVars.delta_time

#blk, will be our Block
blk=GameObject(Vector2(600,300),Vector2(40,40),0)
#setting object name is important to not override any other object in scene
blk.name="tower"
#adding sprite
blk.add_component(SpriteComponent(blk,"block.png"))
#adding collider
blk.add_component(ColliderComponent(Vector2(40,40),blk))
#adding our custom component
blk.add_component(TowerBehav(blk))
#adding object to scene and setting update priority so object gets updated
game_scene.add_object(blk)
game_scene.set_priority("tower",0)

        