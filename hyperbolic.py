# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.patches import Circle


# %%
#output settings
np.set_printoptions(precision=2)
# get_ipython().run_line_magic('matplotlib', 'qt')


# %%
#Normal polar grid

#grid points
Nr = 100
Nth = 100
#radius of the star
Rs = 1.
#linear grid in each dimension
R, TH = np.linspace(Rs, 2.*Rs, Nr), np.linspace(0., np.pi, Nth)
#corresponding step sizes
dr, dth = (R[-1]-R[0])/Nr, (TH[-1]-TH[0])/Nth
#2d meshgrid
r, th = np.meshgrid(R, TH, indexing='ij')
#transformation to cartesian
x, z = r*np.sin(th), r*np.cos(th)


# %%
#The magnetic field (for which B grad(alpha) = 0)

#dipole flux function
Pdip = np.sin(th)**2/r
#magnetic field components
Br = -2.*np.cos(th)/r**3
Bth = -np.sin(th)/r**3

# Br = 1/r**3
# Bth = 1.

#analytical value of alpha
alpha_an = np.sin(th)/r**0.5


# %%
#numerical calculation of alpha

#initialise
alpha = np.zeros([Nr, Nth])
#assign boundary condition at surface
alpha[0, :] = np.sin(th[0, :])/Rs**0.5

#auxiliar parameters
Cr = Br/dr
Cth = Bth/(r*2*dth)

C = (Bth*dr)/(Br*r*dth*2)

#boundary conditions for theta (zero on the axis)
#not sure if this is necessary
for i in range(0, len(R)):

    alpha[i, 0] = 0.
    alpha[i, Nth-1] = 0.

#calculation of alpha
for i in range(0, len(R)-1):
    for j in range(1, len(TH)-1):

        #try different discretisation schemes because of instabillity
        
        # alpha[i+1, j] = alpha[i,j] - Bth[i,j]*dr/(Br[i,j]*r[i, j]*dth)*(alpha[i,j+1] - alpha[i,j])

        # alpha[i,j] = (Cr[i,j]*alpha[i-1,j] + Cth[i,j]*alpha[i,j-1])/(Cr[i,j] + Cth[i,j]

        # alpha[i+1,j] = (1-C[i,j])*alpha[i,j] + C[i,j]*alpha[i,j-1]

        # alpha[i+1,j] = Cth[i,j]/Cr[i,j]*(alpha[i+1,j-1] - alpha[i+1,j+1]) + alpha[i,j]

        alpha[i+1,j] = alpha[i,j] - C[i,j]/2*(alpha[i,j+1] - alpha[i,j-1]) + C[i,j]**2/2*(alpha[i,j+1] - 2*alpha[i,j] + alpha[i,j-1])
        

# print(alpha)
# print(' ')
# print(alpha_an)


# %%
#plot results
fig = plt.figure()
ax = fig.add_subplot(111)  
#numerical value of alpha
ax.contour(x, z, alpha, levels=10)
#analytical value of alpha
ax.contour(x, z, alpha_an, cmap=cm.inferno, levels=10)
#dipole field for reference
# ax.contour(x, z, Pdip, levels=40, ls='--')


# ax.set_xlim(0., 5.)
# ax.set_ylim(-2.5, 2.5)

#plot parameters
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_aspect('equal')
#add the star
ax.add_patch(Circle((0.,0.), Rs, color='b', zorder=-1))

ax.legend()


# %%
#polar plot to ensure that coordinate transformations do not affect the results
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')

ax.contour(th, r, alpha)
ax.contour(th, r, alpha_an)

#plot parameters to rotate the figure
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')


# %%
#3d plot of the difference between numerical and analytical alpha
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, z, np.abs(alpha-alpha_an))

ax.set_xlabel('x')
ax.set_ylabel('z')

# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)

# ax.set_zlim(top=0.5)

plt.show()
# %%



