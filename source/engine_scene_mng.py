import pickle
import pygame


class SaveableScene:
    '''used for pickle to save the scene as an .gscn file'''
    def __init__(self,game_objects_,update_objects_,bg_color,name_):
        '''sets properties'''
        self.game_objects=game_objects_
        self.update_objects=update_objects_
        self.background_color=bg_color
        self.name=name_
        
    def save(self,location):
        '''saves file'''
        
        print(self.game_objects)
        for name,ob in self.game_objects.items():
        #this is done so every component is saved, including Sprites

            for name,com in ob.components.items():
                com.on_save()

        with open(f"{location}/{self.name}.gscn","wb") as sf:
            try:

                pickle.dump(self,sf)
                sf.close()
            except Exception as e:
                print(f"Failed to save file: {e}")
    
        


