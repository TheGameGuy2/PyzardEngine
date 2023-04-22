'''

    ----__     ____
   |      -----     | 
  --    -           ---
  |          --        |
  |     --             |
  ---___       - _____--
        | __  --|
        |       |
        |       |
        |  _    |
        |       |
        |       |
      _--  | -|_--__
    --_-  - _|_  - _ -

'Behold, the tree of wisdom!'


'''

from tkinter import*
from tkinter import ttk
from tkinter import filedialog
import pygame
from game_object_core import*
import pickle
import os
import threading
import contextlib
import shutil
import json
from pygame.math import Vector2
import pygame
from game_mng import SceneManager

#loading editor colors
with open("editor_colors.json","r") as sf:
    EditorColors=json.load(sf)
    sf.close()

#Data UI ----------------------------------------
def repr_vector2(host,vector:Vector2):
    #UI for representing a Vector
    inf_holder=Frame(host,bg=EditorColors["DetailPanel"])
    inf_holder.pack(fill="x")

    v_x_entr=Entry(inf_holder,width=10,bg=EditorColors["ValueTextBG"])
    v_x_entr.insert(0,f"{vector.x}")
    v_x_entr.pack(anchor="nw",side="left",pady=10,padx=75)
    v_x_entr.bind("<FocusIn>",lambda: v_x_entr.delete(0,"end"))

    v_y_entr=Entry(inf_holder,width=10,bg=EditorColors["ValueTextBG"])
    v_y_entr.insert(0,f"{vector.y}")
    v_y_entr.pack(anchor="nw",side="left",pady=10,padx=10)
    v_y_entr.bind("<FocusIn>",lambda: v_y_entr.delete(0,"end"))
    def set_values():
        try:
            nx=float(v_x_entr.get())
            ny=float(v_y_entr.get())
            vector.x=nx
            vector.y=ny
        except:
            pass
    s_but=Button(inf_holder,text="save",bg=EditorColors["Buttons"],command=set_values)
    s_but.pack(anchor="s",side="bottom")
    #v_x_label=Label(inf_holder,text=f"X: {vector.x}",width=10,bg=EditorColors["ValueTextBG"])
    #v_x_label.pack(anchor="nw",side="left",pady=10,padx=75)
    #v_y_label=Label(inf_holder,text=f"Y: {vector.y}",width=10,bg=EditorColors["ValueTextBG"])
    #v_y_label.pack(anchor="nw",side="left",pady=10,padx=10)
def repr_data(host,name,data):
    #creates label with name: data
    inf_holder=Frame(host,bg=EditorColors["DetailPanel"])
    inf_holder.pack(fill="x")
    v_label=Label(inf_holder,text=f"{name}: {data}",bg=EditorColors["ValueTextBG"])
    v_label.pack(anchor="n")

def detail_header(host,content):
    h_hold_frm=Frame(host,bg=EditorColors["HeaderBG"])
    h_hold_frm.pack(anchor="n",fill="x")
    header=Label(h_hold_frm,text=content,bg=EditorColors["HeaderBG"],font=("Courier", 12))
    header.pack(anchor="n")

def repr_edit_data(host,name,data):
    #creates an entry displaying the data + save button
    inf_holder=Frame(host,bg=EditorColors["DetailPanel"])
    inf_holder.pack(fill="x")
    v_label=Label(inf_holder,text=name,bg=EditorColors["ValueTextBG"])
    v_label.pack(anchor="n",side=LEFT)
    v_entr=Entry(inf_holder,bg=EditorColors["ValueTextBG"])
    v_entr.insert(0,data)
    v_entr.bind("<FocusIn>",lambda:v_entr.delete(0,"end"))
    v_entr.pack(side="left")
    def set_value():
        data=v_entr.get()
    s_but=Button(inf_holder,text="save",bg=EditorColors["Buttons"],command=set_value,height=v_entr.winfo_height())
    s_but.pack()
def repr_component(host,component):
    for attr,value in component.__dict__.items():
        if type(value)!=GameObject:
            at_holder=Frame(host,bg=EditorColors["DetailPanel"])
            at_holder.pack(anchor="n",fill="x")
            if type(value)!=Vector2:
                repr_edit_data(at_holder,attr,value)
            else:
                v_t_label=Label(at_holder,bg=EditorColors["HeaderBG"],text=f"{attr}".lower())
                v_t_label.pack(anchor="n")
                repr_vector2(at_holder,value)

#--------------------------------------------------

#Object representation----------------------------
class GameObjectUI:
    #class that represents an object in the editor
     def __init__(self,game_object:GameObject,hirarchie,inf_panel):
        self.game_object=game_object
        self.master=hirarchie
        self.inf_pnl=inf_panel
     
     def redraw_info(self):
        '''draws all components and attributes to the info panel'''
        for wdg in self.inf_pnl.winfo_children():
            wdg.pack_forget()

        transform_holder=Frame(self.inf_pnl,bg=EditorColors["DetailPanel"])
        transform_holder.pack(fill="x",anchor="n")

        detail_header(transform_holder,f"{self.game_object.name}")
        detail_header(transform_holder,"Position")
        repr_vector2(transform_holder,self.game_object.position)
        detail_header(self.inf_pnl,"Scale")
        repr_vector2(self.inf_pnl,self.game_object.scale)
        #creates ui for every component
        for key,com in self.game_object.components.items():
            comp_holder=Frame(self.inf_pnl,bg=EditorColors["DetailPanel"])
           
            comp_holder.pack(anchor="n",fill="x")
            
            #sep=ttk.Separator(comp_holder,orient="horizontal")
            #sep.pack(fill="x")

            detail_header(comp_holder,com.name.upper())
            for attr,value in com.__dict__.items():
                if type(value)!=GameObject:
                    at_holder=Frame(comp_holder,bg=EditorColors["DetailPanel"])
                    at_holder.pack(anchor="n",fill="x")
                    if type(value)!=Vector2:
                        repr_data(at_holder,attr,value)
                    else:
                        v_t_label=Label(at_holder,bg=EditorColors["HeaderBG"],text=f"{attr}".lower())
                        v_t_label.pack(anchor="n")
                        repr_vector2(at_holder,value)
        
     def redraw_ui(self):
        ob_frm=Frame(self.master,bg=EditorColors["ObjectList"])
        ob_frm.pack(anchor="nw",fill="x")
        ob_select=Button(ob_frm,text=self.game_object.name,width=15,height=1,command=self.redraw_info,bg=EditorColors["Buttons"])
        ob_select.pack(anchor="n",)

#--------------------------------------


#Editor class and functions ----------------------------

def draw_object(game_obj,pyg_surface):
    try:
        pyg_surface.blit(game_obj.get_component("sprite").scaled_sprite,game_obj.get_component("sprite").par_rect)
    except:
        game_obj.get_component("sprite").on_load(False,None,None)

def python_file_ui(file,host,row_column:list,image):
    #creates all elements for displaying a python file as a Button
    #todo: open file on click
    if file.endswith(".py"):
        file_frame=Frame(host,bg=EditorColors["FileExplorer"])
        file_frame.grid(row=row_column[0],column=row_column[1])
        pyf_button=Button(file_frame,image=image,width=35,height=35,bg=EditorColors["FileExplorer"])
        pyf_button.pack(pady=3)
        pyf_name_lab=Label(file_frame,text=file,bg=EditorColors["FileExplorer"])
        pyf_name_lab.pack(padx=2)
    else:
        return

class Editor:
    def __init__(self,scene,path):
        self.current_scene=scene
        self.current_path=path

        self.engine_window=Tk()
        self.engine_window.title(f"Pyzard Engine - {self.current_scene.name}")
        self.engine_window.iconbitmap("engine_icon.ico")
        self.engine_window.state('zoomed')
        self.images={}
        self.images["python_script_img"]=PhotoImage(master=self.engine_window,file="pythonfile.png")
        self.images["unknown_file_img"]=PhotoImage(master=self.engine_window,file="fileunknown.png")
        self.removed_objects={}
        self.editor_camera=Camera(Vector2(0,0),Vector2(0,0))
        self.default_components={"Sprite":SpriteComponent,"Collider":ColliderComponent}
    def start(self):
        self.load_menu()
        self.load_object_explorer()
        self.load_info()
        self.load_objects()
        self.load_pygame()
        self.load_explorer()
        self.reload_editor()
        self.engine_mainloop()

    def engine_mainloop(self):
        clock=pygame.time.Clock()
        #The engine mainloop, mostly important for pygame
        while True:
            clock.tick(30)
            #engine runs at 30 fps to not be heavy on CPU
            self.pyg_display.fill(self.current_scene.background_color)
            for name,ob in self.current_scene.game_objects.items():
                if ob.get_component("sprite"):
                   draw_object(ob,self.pyg_display)

            self.engine_window.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     quit()
            pygame.display.update()

    def load_objects(self):

        for name,gameobj in self.current_scene.game_objects.items():
            new_ui=GameObjectUI(gameobj,self.object_lib,self.detail_panel)
            new_ui.redraw_ui()

    def load_object_explorer(self):
        
        self.object_inflibs=Frame(self.engine_window,bg=EditorColors["WindowBG"])
        
        self.object_inflibs.pack(fill="x",anchor="n")
        self.object_lib=Frame(self.object_inflibs,bg=EditorColors["ObjectList"],width=280,height=650)
        self.object_lib.propagate(False)
        
        self.object_lib.pack(anchor="nw",side="left")
        #todo: make it scrollable
    def load_menu(self):
         self.toolbar_menu=Menu(self.engine_window)
         self.engine_window.config(menu=self.toolbar_menu)
         self.save_menu=Menu(self.toolbar_menu,tearoff=False)
         self.toolbar_menu.add_cascade(label="Scene",menu=self.save_menu)
         self.save_menu.add_command(label="Save",command=lambda:SceneManager.save_scene(self.current_scene,self.current_path))
    
         self.game_obj_menu=Menu(self.toolbar_menu,tearoff=False)
         self.toolbar_menu.add_cascade(label="Game Objects",menu=self.game_obj_menu)
         self.game_obj_menu.add_command(label="Add",command=self.add_object)
         self.game_obj_menu.add_command(label="Delete",command=self.delete_object)
         self.game_obj_menu.add_command(label="Restore",command=self.restore_object)

         self.opt_menu=Menu(self.toolbar_menu,tearoff=False)
         self.toolbar_menu.add_cascade(label="Options",menu=self.opt_menu)
         self.opt_menu.add_command(label="Add script",command=self.add_script)
         
    def load_info(self):
        
        self.detail_panel=Frame(self.object_inflibs,bg=EditorColors["DetailPanel"],width=400,height=650)
        self.detail_panel.propagate(False)
        self.detail_panel.pack(anchor="ne",side="right")
        #todo: make it scrollable
    def load_pygame(self):
        self.py_window=Frame(self.object_inflibs,height=650,width=1240)
        self.py_window.pack(anchor="n",fill="x",side="left")
        os.environ["SDL_WINDOWID"]=str(self.py_window.winfo_id())
        os.environ["SDL_VIDEODRIVER"]="windib"
        self.pyg_display=pygame.display.set_mode((1240,650))
        self.pyg_display.fill((0,0,0))

    def load_explorer(self):
        self.file_exp=Frame(self.engine_window,bg=EditorColors["FileExplorer"],height=350)
        self.file_exp.propagate(False)
        self.file_exp.grid_propagate(False)
        self.file_exp.pack(anchor="center",fill="x")

    def refresh_explorer(self):
        for ch in self.file_exp.winfo_children():
            ch.pack_forget()
        c_row=0
        c_col=0
        counter=0
        for f in os.listdir(self.current_path):
            if f.endswith(".py"):
                if counter<=10:
                    
                    python_file_ui(f,self.file_exp,[c_row,c_col],self.images["python_script_img"])
                    c_col+=1
                    
                else:
                    counter=0
                    c_col=0
                    c_row+=1
                    python_file_ui(f,self.file_exp,[c_row,c_col],self.images["python_script_img"])
                counter+=1
                
    def refresh_objects(self):
        for w in self.object_lib.winfo_children():
            w.pack_forget()
        
        for name,obj in self.current_scene.game_objects.items():
            new_ui=GameObjectUI(obj,self.object_lib,self.detail_panel)
            new_ui.redraw_ui()
    def refresh_info(self):
        for wdg in self.detail_panel.winfo_children():
            wdg.pack_forget()
        in_lab=Label(self.detail_panel,text="Select Object",bg=EditorColors["DetailPanel"])
        in_lab.pack(anchor="n")
    def reload_editor(self):
        self.refresh_objects()
        self.refresh_info()
        self.refresh_explorer()
    
    def add_script(self):
        n_win=Tk()
        n_win.title("New Script")
        def create_script(name):
            try:
                shutil.copy2("blueprint.py",f"{self.current_path}/{name}.py")
                self.refresh_explorer()
                n_win.destroy()
            except Exception as e:
                print(e)
        hd_label=Label(n_win,text="Name")
        hd_label.pack(anchor="n")
        name_entr=Entry(n_win)
        name_entr.pack(anchor="n")
        crt_but=Button(n_win,text="Create",command=lambda:create_script(name_entr.get()))
        crt_but.pack(anchor="n")
        n_win.mainloop()

    def add_object(self):
        #UI for on object create
        x_pos=0
        y_pos=0
        x_scale=0
        y_scale=0
        name=""

        set_win=Tk()
        set_win.title("New Object")
        set_win.config(bg=EditorColors["WindowBG"])
        nm_lb=Label(set_win,text="Name",bg=EditorColors["WindowBG"])
        nm_lb.pack(anchor="n")

        name_entr=Entry(set_win,width=30,bg=EditorColors["ValueTextBG"])
        name_entr.pack(anchor="n")

        pos_frm=Frame(set_win,bg=EditorColors["WindowBG"])
        pos_frm.pack(fill="x")
        pos_lab=Label(pos_frm,text="Position",bg=EditorColors["WindowBG"])
        pos_lab.pack(anchor="n")
        #make description labels that tell x or y
        set_pos_x=Entry(pos_frm,width=10,bg=EditorColors["ValueTextBG"])
        set_pos_y=Entry(pos_frm,width=10,bg=EditorColors["ValueTextBG"])
        set_pos_x.pack(side="left",pady=10,padx=20)
        set_pos_y.pack(side="left",pady=10,padx=10)
        #scale
        scale_frm=Frame(set_win,bg=EditorColors["WindowBG"])
        scale_frm.pack(fill="x")
        sc_lab=Label(scale_frm,text="Scale",bg=EditorColors["WindowBG"])
        sc_lab.pack(anchor="n")
        set_sc_x=Entry(scale_frm,width=10,bg=EditorColors["ValueTextBG"])
        set_sc_x.pack(side="left",pady=10,padx=20)
        set_sc_y=Entry(scale_frm,width=10,bg=EditorColors["ValueTextBG"])
        set_sc_y.pack(side="left",pady=10,padx=10)
        def get_values():
            x_pos=float(set_pos_x.get())
            y_pos=float(set_pos_y.get())
            x_scale=float(set_sc_x.get())
            y_scale=float(set_sc_y.get())
            name=name_entr.get()
            new_obj=GameObject(Vector2(x_pos,y_pos),Vector2(x_scale,y_scale),0)
            new_obj.name=name
            self.current_scene.add_object(new_obj)
            self.current_scene.set_priority(new_obj.name,0)
            self.refresh_objects()
            set_win.destroy()
        acc_button=Button(set_win,text="Create",command=get_values,bg=EditorColors["Buttons"])
        acc_button.pack(anchor="n",pady=10)

   

    #delete should be a seperate button next to game object button in object list this is a placeholder
    def delete_object(self):
        r_win=Tk()
        r_win.config(bg="#f5756c")
        r_win.title("Delete Object")
        el=Label(r_win,text="Delete Object Name",bg="#f5756c")
        el.pack(anchor="n")
        n_entr=Entry(r_win)
        n_entr.pack(anchor="n")
        def del_gmobj(name) -> None:
            try:
                self.removed_objects[self.current_scene.game_objects[name].name]=self.current_scene.game_objects[name]
                del self.current_scene.game_objects[name]
                self.refresh_objects()
                r_win.destroy()
            except:
                return
        rem_but=Button(r_win,text="Delete",command=lambda:del_gmobj(n_entr.get()))
        rem_but.pack(anchor="n",pady=2)
        
        warn_lab=Label(r_win,text="Object will be lost forever!",bg="red",fg="#ffffff")
        warn_lab.pack(anchor="n")
        r_win.mainloop()

    def restore_object(self):
        r_win=Tk()
        r_win.title("Restore")
        lb=Label(r_win,text="Restore deleted game object")
        lb.pack(anchor="n")
        n_entr=Entry(r_win)
        n_entr.pack(anchor="n")
        def res_ob(name):
            
            self.current_scene.add_object(self.removed_objects[name])
            self.current_scene.set_priority(self.removed_objects[name].name,0)
            self.refresh_objects()
            r_win.destroy()
            
        r_but=Button(r_win,text="Restore",command=lambda:res_ob(n_entr.get()))
        r_but.pack(anchor="n")
        r_win.mainloop()
#------------------------------------------------------

#editor start/select screen-----------------------------------

def select_scene(window):
    #simply select scene file
    file = filedialog.askopenfile()

    dir=file.name[::-1].split("/",1)[1][::-1]+"/"
    #this, beautiful piece of code gets the path of the file...

    
    scene=SceneManager.loadscene(file.name)
    window.destroy()
    App=Editor(scene,dir)
    App.start()

def create_scene(window):
    # asks for name, then directory, then copys all needed files there
    new_win=Tk()
    name_lb=Label(new_win,text="Name")
    name_lb.pack(anchor="n")
    n_entr=Entry(new_win)
    n_entr.pack(anchor="n")

    def finish(name):
        path=filedialog.askdirectory()
        shutil.copy2("game_object_core.py",path+"/game_object_core.py")
        shutil.copy2("collisions.py",path+"/collisions.py")
        shutil.copy2("game_sound.py",path+"/game_sound.py")
        shutil.copy2("game_mng.py",path+"/game_mng.py")
        shutil.copy2("assemble.py",path+"/assemble.py")
        shutil.copy2("engine_scene_mng.py",path+"/engine_scene_mng.py")
        shutil.copy2("GameApp.py",path+"/GameApp.py")
        n_s=Scene()
        n_s.name=name
        with open(f"{path}/scenes.txt","w") as f:
            f.write(n_s.name+".gscn")
            f.close()
        new_win.destroy()
        App=Editor(n_s,path)

        window.destroy()
        App.start()

    c_butt=Button(new_win,text="Create",command=lambda:finish(n_entr.get()))
    c_butt.pack(anchor="n")
    new_win.mainloop()
#----------------------------------------------------------------

def main():
    
    start_window=Tk()
    start_window.title("Select Scene")
    start_window.iconbitmap("engine_icon.ico")
    start_window.geometry("400x400")

    select_b=Button(start_window,text="Select Scene",command= lambda: select_scene(start_window))
    select_b.pack(anchor="n",pady=25)

    new_b=Button(start_window,text="New Scene",command=lambda:create_scene(start_window))
    new_b.pack(anchor="n",pady=25)
    start_window.mainloop()
if __name__=="__main__":
    main()

