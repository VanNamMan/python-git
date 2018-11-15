import autograd
import autograd.numpy as gnp
import matplotlib.pyplot as plt
import numpy as np

#hello Github

def cost(x,y):
    return (x**2+y-7)**2+(x-y+1)**2






def plot(func,grad=None):
    global CS,ax
    fig,ax = plt.subplots()

    
    x = np.linspace(-6,6,100)
    y = np.linspace(-20,15,100)
    XX,YY = np.meshgrid(x,y)

    lv = np.linspace(-250,250,50)
    Z = cost(XX,YY)
    CS = ax.contour(XX, YY, Z,levels=lv,cmap=plt.cm.Paired)
    cbar = plt.colorbar(CS)

    ax.set_xlim([-6.5,6.5])
    ax.set_ylim([-21.5,16.5])
    plt.show()


plot(cost)
