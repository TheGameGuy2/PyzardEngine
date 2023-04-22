from game_object_core import*
from collisions import*
from game_sound import*
from game_mng import GameVars
from GameApp import game_scene
from GameApp import App
# Your logic goes here
#Reminder: import script in assemble.py

#getting player object in scene.
player:GameObject=game_scene.get_object("player")
game_scene.background_color=(30,200,40,255)



class PlayerMov(Component):
    '''player movement. will be added as new component.'''
    def __init__(self,player):
        #setting name and parent object
        super().__init__("pl_mov",player)
        #stting the gravity with wich the player will move down
        self.gravity=80
        self.player=player
        
    def on_update(self):
        #reseting player gravity, 
        self.gravity=80
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            #if space gets pressed, gravity gets inverted
            if self.player.position.y>0:
                self.gravity= -self.gravity*2
        
            
            
        #adding gravity to player
        self.player.position.y+=self.gravity*GameVars.delta_time

#adding sprite to player object
player.add_component(SpriteComponent(player,"sprite.png"))
#adding collider
player.add_component(ColliderComponent(player.scale,player))

#adding our custom component
player.add_component(PlayerMov(player))

