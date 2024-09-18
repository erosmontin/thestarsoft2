import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_ellipsoid(center, radii, rotation, ax=None, color='b', alpha=0.2):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radii[0] * np.outer(np.cos(u), np.sin(v))
    y = radii[1] * np.outer(np.sin(u), np.sin(v))
    z = radii[2] * np.outer(np.ones_like(u), np.cos(v))
    # Apply the rotation matrix to the points on the ellipsoid

    for i in range(len(x)):
        for j in range(len(x)):
            [x[i,j],y[i,j],z[i,j]] = np.dot(rotation, [x[i,j],y[i,j],z[i,j]]) + center

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    ax.plot_surface(x, y, z, color='b', alpha=0.2)

    # Plot the wireframe
    ax.plot_wireframe(x, y, z, color='black', rstride=4, cstride=4, alpha=0.3)
    

def plot_ellipsoidv(center, radii, rotation, ax=None, color='b', alpha=0.2):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radii[0] * np.outer(np.cos(u), np.sin(v))
    y = radii[1] * np.outer(np.sin(u), np.sin(v))
    z = radii[2] * np.outer(np.ones_like(u), np.cos(v))

    ellipsoid = np.array([x, y, z])
    for i in range(len(x)):
        for j in range(len(x)):
            ellipsoid[:, i, j] = np.dot(rotation, ellipsoid[:, i, j])


    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(center[0] + ellipsoid[0],
                    center[1] + ellipsoid[1],
                    center[2] + ellipsoid[2],
                    color=None, alpha=alpha)
    ax.plot_wireframe(x, y, z, color='black', rstride=8, cstride=8,alpha=0.4)
    ax.view_init(elev=0, azim=40)  
    
def plot_axes(ax, origin, rotation, length=1.5):
    """Add axes to the 3D plot."""

    # Define the direction vectors for the axes
    directions = np.eye(3)

    # Apply the rotation matrix to the direction vectors
    directions = np.dot(rotation, directions)

    colors = ['r', 'g', 'b']
    for i in range(3):
        ax.quiver(origin[0], origin[1], origin[2], directions[0,i], directions[1,i], directions[2,i], color=colors[i], length=length)
        
def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define ellipsoid parameters
    center = [0, 0, 0]
    radii = [0.7, 0.3, 0.5]
    # rotation1 = np.eye(3)
    rotation1 = np.array([[0.8, 0.2, 0.1],
                          [-0.1, 0.9, 0.2],
                          [0.1, -0.3, 0.8]])

    # Plot first ellipsoid
    plot_ellipsoid(center, radii, rotation1, ax, color='b')
    plot_axes(ax, center, rotation1, length=1)

    # # Plot second ellipsoid (rotated)
    # plot_ellipsoid(center, radii, rotation2, ax, color='r')
    # plot_axes(ax, center, rotation2, length=1)

    # Set limits and labels
    ax.set_xlim([-1,1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

if __name__ == "__main__":
    main()