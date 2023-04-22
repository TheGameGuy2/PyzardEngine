class Collider:
    '''A field that registers intersections'''
    def __init__(self,scale,position):
        self.scale=scale
        self.position=position
        self.x=position[0]
        self.y=position[1]
        self.width=scale[0]
        self.height=scale[1]
        self.center=[self.x+self.scale[0]/2,self.y+self.scale[1]/2]
        self.check_sides={"up":True,"down":True,"left":True,"right":True}
    def __repr__(self):
        return f" X: {self.x} Y: {self.y} W: {self.width} H: {self.height}"
    def set_pos(self,x,y):
        '''sets the position of the collider'''
        self.x=x
        self.y=y
        self.position[0]=x
        self.position[1]=y
        self.center=[self.x+self.scale[0]/2,self.y+self.scale[1]/2]
    def rescale(self,w,h):
        '''sets the scale of the collider'''
        self.width=w
        self.height=h
        self.scale[0]=w
        self.scale[1]=h
    def is_colliding_simple(self,other) -> bool:
        '''checks if the collider is intercepting. Returns bool.'''
        if other.x+other.width>self.x and other.x<self.x+self.width and other.y+other.height>self.y and other.y<self.y+self.height:
            return True
        else:
            return False
    def is_colliding(self,other):
        '''checks if the collider is colliding, and on wich side it's colliding. Returns False if no collision, returns dict on collision
        -> collisions{"up":1,"down":0,"left":1,"right":0}
        '''
        collisions={"up":0,"down":0,"left":0,"right":0}
        if other.x+other.width>self.x and other.x<self.x+self.width and other.y+other.height>self.y and other.y<self.y+self.height:
            if self.check_sides["left"]:
                if other.center[0]<=self.center[0]:
                    collisions["left"]=1
            if self.check_sides["right"]:
                if other.center[0]>=self.center[0]:
                    collisions["right"]=1
            if self.check_sides["up"]:
                if other.center[1]<=self.center[1]:
                     collisions["up"]=1
            if self.check_sides["down"]:
                if other.center[1]>=self.center[1]:
                  collisions["down"]=1
            return collisions
        else:
            return False
