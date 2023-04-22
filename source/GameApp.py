from game_mng import*
with open("scenes.txt","r") as f:
    #current scene is getting read from scenes.txt file
    s_name=f.read()
    f.close()
App=Game(SceneManager.loadscene(s_name),600,600)
game_scene=App.scene

def start():
    App.start_app()
