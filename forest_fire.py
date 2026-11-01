""" forest fire model
autor: Shlomo Rozenfeld
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

TREE=2
EMPTY=0
FIRE=1
class Forest(object):
    """
    1. An empty cell become accupied with probability p
    2. A cell with tree burns if any of its neighbors is on fire
    3. A cell with tree spontaneusly burns with probability f,
       even if non of its neighbors is on fire
    4. A cell with burning tree becomes empty in the next time step
    """

    def __init__(self, n=100, ro=.5,p=0.0,f=0,setup='column_fire'):
        """Attributes:
        n:   number of rows, columns.
        array:  the numpy array that contains the data.
        ro: tree density
        f: probability for a tree to burn spontaneously
        p: probability of an empty cell to become accupied
        """
        setupfun={'column_fire':self.set_column_fire,'center':self.point_at_center}
        self.n = n
        self.ro=ro
        self.p=p
        self.f=f
        self.array = np.zeros((n+1, n+1), dtype=np.int8)
        self.set_random_tree()
        setupfun[setup]()
        self.count=(self.array==TREE).sum()

    def set_random_tree(self):
        for r in range(1,self.n):
        	for c in range(1,self.n):
        		if np.random.random()<self.ro:
        			self.array[r,c]=TREE
    def set_column_fire(self):
        for r in range(1,self.n):
        	self.array[r,0]=FIRE
        	
    def point_at_center(self):
         self.array[int(self.n/2),int(self.n/2)]=FIRE
                 
    def step(self):
        """Executes one time step."""
        tmp= np.zeros((self.n+1, self.n+1), dtype=np.int8)
        for r in range(1,self.n):
            for c in range(1,self.n):
                if self.array[r,c]==TREE:
                    neighbors=self.get_neighbors(r,c)
                    for neighbor in neighbors:
                        row,col=neighbor
                        fire=self.array[row,col]==FIRE
                        if fire or np.random.random()<self.f:
                            tmp[r,c]=FIRE
                            break 
                        else:
                            tmp[r ,c]=TREE
                elif self.array[r,c]==EMPTY and np.random.random()<self.p:
                    tmp[r ,c]=TREE
        self.array=tmp
        self.count=(self.array==TREE).sum()
        return tmp
    
    def loop(self, steps=1):
        """Executes the given number of time steps."""
        for i in range(steps):
            self.step()
        plt.imshow(self.array,cmap='brg', interpolation='nearest')
        plt.show()
        return self.count
        #return [self.step() for i in xrange(steps)]

    def make_n_steps(self,n):
        for i in range(n):
            self.step()
    
        				        
    def get_neighbors(self,r,c):
        nighbors=[]
        for i in [-1,0,1]:
           for k in [-1,0,1]:
              if i!=0 or k!=0:
                  nighbors.append((r+i,c+k))
        return nighbors

    def animate(self,frames):
        plt.ioff()
        plt.close('all')
        fig = plt.figure()
        ims=[[plt.imshow(self.step(), cmap='brg', interpolation='nearest', animated=True)] for i in range(frames)]
        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=False,repeat_delay=1000)
        print('האנימציה מוכנה, הריצו את התא הבא')
        return ani
        #plt.show()
        #ani.save('dynamic_images.mp4')
        #HTML(ani.to_html5_video())


#if __name__=='__main__':
#   forest=Forest(ro=0.5,n=100)
# print ("ro=%1.2f   trees=%3.1f"%(forest.ro,forest.count))
    
    
