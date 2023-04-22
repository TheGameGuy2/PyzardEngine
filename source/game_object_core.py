'''
 
     ____
    |    |
 ---  - - ---     -------
        ------   --
    ---     ___|>_
-    ----   \____/   ----
   -----    -------
 ---    ---     -----

'What a beautiful sunset' 

by @random_dev1 / Andre  B.

'''

from collisions import Collider
import pygame
import pygame._sdl2
import pickle
from pygame.math import Vector2


class GameObject:
    '''basic game-object'''
    def __init__(self,position:Vector2,scale:Vector2,rotation):
        self.name:str="New_Game_Object"
        #name is used as an 'id' for the object

        self.tags:list=[]
        #tags are only to be used by the user, just a helpful feature

        self.components={}
        self.position:Vector2=position
        self.scale:Vector2=scale
        
        self.rotation:float=rotation
        self.start()

    def start(self):
        '''is called on object init'''
        pass
    def tech_update(self):
        '''updates components'''
        for key, value in self.components.items():
            value.on_update()
        self.update()
    def destroy(self):
        del self
    def update(self):
        '''update will be called every frame <- thats a lie, it will be never called'''
        pass
    def add_component(self,component_class):
        '''adds the component'''
        self.components[component_class.name]=component_class

    def get_component(self,component_name):
        '''returns the component'''
        try:
            return self.components[component_name]
        except:
            return False

class Scene:
    '''Holds all game objects acts like a 'World' '''
    def __init__(self):

        self.name="New_Scene"
        self.game_objects={}

        #objects get added like this: [update_priority]=object
        self.update_objects={}
        self.background_color=(0,0,0,0)
        
    def add_object(self,game_object):
        '''Adds object to all objects'''
        self.game_objects[game_object.name]=game_object
        
    def set_priority(self,object_name,priority):
        '''Adds object to update que'''
        if priority in self.update_objects.keys():
            self.update_objects[priority].append(self.game_objects[object_name])
        else:
            self.update_objects[priority]=[self.game_objects[object_name]]
    def swith_priority(self,obj_name,current_priority,new_priority,end_at):
        '''used to switch the priority of an object. if current priority is not set will search through all objects
        end_at specifies how many objects to switch if object has same name
        '''
        t_obs=end_at
        if current_priority==None:
            for pr,ob_list in self.update_objects.items():
                for ob in ob_list:
                    if ob.name==obj_name:
                        if t_obs>0:
                            t_obs-=1
                            self.set_priority(ob.name,new_priority)
                            ob_list.remove(ob)
                        else:
                            break
        else:
            for ob in self.update_objects[current_priority]:
                if ob.name==obj_name:
                    if t_obs > 0:
                        t_obs-=1
                        self.set_priority(ob.name,new_priority)
                        ob_list.remove(ob)
                    else:
                        break

    def get_object(self,name) -> GameObject:
        '''returns found object'''
        return self.game_objects[name]







class Component:
    '''The main component class wich all other components inherit from'''
    def __init__(self,name,parent_object):
        self.name=name
        self.parent_object=parent_object
   
    def on_update(self):
        pass
    def on_save(self):
        pass
    


class SpriteComponent(Component):
    '''The sprite of an Object'''
    def __init__(self,parent_object,sprite,custom_init=[False]):
        '''custom_init: [use_custominit:bool,current_renderer,cur_camera] 
        This should be used to initialize the sprite component during runtime
        '''
        super().__init__("sprite", parent_object)

        
        self.current_renderer=None
        self.sprite_location=sprite
        if custom_init[0]==True:
            self.on_custom_load(True,custom_init[1],custom_init[2])
    def on_load(self,use_sdl2,current_renderer,cur_camera):
        '''sets up sprite for rendering, is needed because pygame.Surface is not saveable'''
        self.camera=cur_camera
        
        self.base_sprite=pygame.image.load(self.sprite_location).convert_alpha()
        self.scaled_sprite=pygame.transform.scale(self.base_sprite,(self.parent_object.scale.x,self.parent_object.scale.y))
        self.par_rect=pygame.Rect(self.parent_object.position.x,self.parent_object.position.y,self.parent_object.scale.x,self.parent_object.scale.y)
        if use_sdl2:
            self.current_renderer=current_renderer
            self.texture=pygame._sdl2.Texture.from_surface(self.current_renderer,self.scaled_sprite)

    def load_sprite(self,sprite_name):
        '''loads the sprite and prepares it for rendering'''
        self.base_sprite=pygame.image.load(sprite_name).convert_alpha()
        self.scaled_sprite=pygame.transform.scale(self.base_sprite,(self.parent_object.scale.x,self.parent_object.scale.y))
        return self.scaled_sprite
    def on_custom_load(self,use_sdl2,current_renderer,cur_camera):
        '''loads everything except the sprite'''
        self.par_rect=pygame.Rect(self.parent_object.position.x,self.parent_object.position.y,self.parent_object.scale.x,self.parent_object.scale.y)
        if use_sdl2:
            self.current_renderer=current_renderer
            self.texture=pygame._sdl2.Texture.from_surface(self.current_renderer,self.scaled_sprite)

    def on_update(self):
        '''Operations every frame'''
        self.par_rect.x=self.parent_object.position.x-self.camera.position.x
        self.par_rect.y=self.parent_object.position.y-self.camera.position.y
        self.par_rect.width=self.parent_object.scale.x - self.camera.scale.x
        self.par_rect.height=self.parent_object.scale.y - self.camera.scale.y
        self.current_renderer.blit(self.texture,self.par_rect)

    def on_save(self):
        '''removes all unsaveable attributes'''
        self.camera=None
        self.current_renderer=None
        self.base_sprite=None
        self.scaled_sprite=None
        self.par_rect=None



class ColliderComponent(Component):
    '''used for detecting collisions'''
    def __init__(self,size:Vector2,parent_object):
        super().__init__("collider",parent_object)
        self.size=size
        self.position_offset=Vector2(0,0)
        self.box=Collider([self.size.x,self.size.y],[self.parent_object.position.x+self.position_offset.x,self.parent_object.position.y+self.position_offset.y])
        
       
    def on_update(self):
        
        self.box.set_pos(self.parent_object.position.x+self.position_offset.x,self.parent_object.position.y+self.position_offset.y)
           

    def check_side_collision(self,other):
        '''uses custom collider to check wich side is coliding'''
        return self.box.is_colliding(other.box)
    def check_collision(self,other):
        '''checks only for collision, is faster then checking for sides'''
        return self.box.is_colliding_simple(other.box)



class Camera:
    '''just a position and scale'''
    def __init__(self,position:Vector2,zoom:Vector2):
        self.position=position
        self.scale=zoom