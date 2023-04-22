'''
        |
    |   | |
    | | | | |

'Recognise it? Yes, that is indeed grass, go touch some.' 

'''

import pickle 
from game_object_core import*
import pygame
import time
from pygame.math import Vector2
from engine_scene_mng import SaveableScene


class GameVars:
    '''Used to store important Game variables'''
    framerate=60
    window_height=600
    window_width=600
    delta_time=1
    events=[]

class SceneManager:
    '''this class is used for managing scenes, loading , saving etc.'''
    def loadscene(scenefile):
        
        with open(scenefile,"rb") as sf:
            l_scene=pickle.load(sf)
            sf.close()
        
        new_scene=Scene()
        new_scene.background_color=l_scene.background_color
        new_scene.game_objects=l_scene.game_objects
        new_scene.update_objects=l_scene.update_objects
        new_scene.name=l_scene.name
        return new_scene
    
    def save_scene(scene:Scene,path):
        sv_scene=SaveableScene(scene.game_objects,scene.update_objects,scene.background_color,scene.name)
        sv_scene.save(path)
    

class Game:
    '''The application class this represents the App'''
    def __init__(self,scene,window_x:float,window_y:float):
        pygame.init()
        self.scene=scene
        pygame_screen=pygame.display.set_mode((window_x,window_y), vsync=0, flags=pygame.SCALED)
        self.window=pygame._sdl2.Window.from_display_module()
        self.renderer = pygame._sdl2.Renderer.from_window(self.window)
        self.renderer.draw_color=self.scene.background_color
        self.camera=Camera(Vector2(0,0),Vector2(0,0))

    def load_sprites(self,game_objects):
        '''goes through each sprite component and loads it'''
        for ob_name,obj in game_objects.items():
            for comp_name,comp in obj.components.items():
                if comp_name=="sprite":
                    comp.on_load(True,self.renderer,self.camera)
    def reload_update_sprites(self):
        for pr,obs in self.scene.update_objects.items():
            for obj in obs:
                for comp_name,comp in obj.components.items():
                    if comp_name=="sprite":
                         comp.on_load(True,self.renderer,self.camera)
    def start_app(self):
        '''Starts the main gameloop'''
        self.load_sprites(self.scene.game_objects)
        game_clock=pygame.time.Clock()
        while True:
            GameVars.delta_time=game_clock.tick(GameVars.framerate)/1000
            self.update_loop()
            #print(game_clock.get_fps())

    def update_loop(self):
        '''the main gameloop updates each object'''
        self.renderer.clear()
        GameVars.events=pygame.event.get()
        for event in GameVars.events:
             if event.type == pygame.QUIT:
                  self.on_application_quit()
        for i in range(len(self.scene.update_objects.keys())):

            for ob in self.scene.update_objects[i]:
                 
                ob.tech_update()
                ob.update()
        self.renderer.present()







#this code shows how to create a simple scene with 2 objects only using the framework
'''
t=Scene()
t.name="newtestscene"
t.background_color=(10,60,10,255)
foo=GameObject(Vector2(34,20),Vector2(80,80),0)
foo.add_component(ColliderComponent(Vector2(2,3),foo))
foo.name="Object1"
foo.add_component(SpriteComponent(parent_object=foo,sprite="sprite.png"))
bar=GameObject(Vector2(30,30),Vector2(40,40),0)
bar.name="Orange"
bar.add_component(SpriteComponent(bar,"blood_orange.png"))
t.add_object(foo)
t.add_object(bar)
t.set_priority("Orange",0)
t.set_priority("Object1",1)

print(t.update_objects)
SceneManager.save_scene(t,"")
App=Game(SceneManager.loadscene("newtestscene.gscn"),600,600)
App.start_app()
'''