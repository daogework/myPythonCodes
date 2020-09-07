import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import animation
 
fig,ax = plt.subplots()
#x = np.linspace(0,2*np.pi,200)
#y = np.sin(x)
x = [1, 2, 3, 4]
y = [1.2, 2.5, 4.5, 7.3]
l = ax.plot(x,y)
dot, = ax.plot([],[],'ro')
 
def init():
    ax.set_xlim(0,2*np.pi)
    ax.set_ylim(-1,1)
    return 1
 
def gen_dot():
    for i in np.linspace(0,2*np.pi,200):
        newdot = [i,np.sin(i)]
        yield newdot
 
def update_dot(newd):
    dot.set_data(newd[0],newd[1])
    return dot,
 
ani = animation.FuncAnimation(fig,update_dot,frames=gen_dot,interval=100,init_func=init)
#ani.save('animation2.gif',writer='imagemagic',fps=30)
plt.show()