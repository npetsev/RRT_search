import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from constraints import Constraint as clib
from lattice import Lattice as lat
from vertex import Vertex as vtx
from rrt_search import RapidlyExploringRandomTree as rrt

""" 
    Script that loads user input, performs RRT search, and writes output.
   
    Example for running script:
        python rrt_main.py input.txt output.txt nodemax
    
    input.txt     - input file that contains space geometry/constraints (e.g., triangle.txt)
    output.txt    - file where final tree nodes are dumped
    nodemax       - number of nodes that final tree should contain (e.g., 1000)
"""

def count_nodes(X):
    """
        Function that counts how many nodes RRT run has produced
    """
    ncount = [c_obj.apply(xi) and c_obj.apply_box(xi) for xi in X]
    return sum(bool(i) for i in ncount)

def tree_plotter(vtx_list, X):
    """
        Simple function that visualizes the 2D tree generated from RRT run
    """
    # Plot tree node and verteces
    for AB in vtx_list:
        x1 = X[AB[0]][0]; y1 = X[AB[0]][1]
        x2 = X[AB[1]][0]; y2 = X[AB[1]][1]
        fig1 = plt.plot([x1, x2], [y1, y2], marker = 'o')

    plt.xlim([0.0, 1.0]); plt.ylim([0.0, 1.0])
    
    # Plot Voronoi diagram
    vor = Voronoi(X)
    fig2 = voronoi_plot_2d(vor, show_vertices=False, show_points= False, line_colors='black', line_width=1)
    plt.xlim([0.0, 1.0]); plt.ylim([0.0, 1.0])
    plt.show()

# User input
filename = sys.argv[1]
foutname = sys.argv[2]
nodemax = int(sys.argv[3])

# Set RRT hyperparameters
epsilon = 1.0e-05
growth_rate = 0.1

# Set lattice discretization
xbins = 1000

# Load input file with space geometry and create constraints object
c_obj = clib(filename)

# Extract dimensionality
ndim = c_obj.get_ndim()

# Extract starting node
x0 = c_obj.example

# Create lattice
mylat = lat(xbins, ndim)

# Create vertex and node lists
myvtx = vtx(x0)

# Initialize the RRT
rrt_drive = rrt(epsilon, growth_rate, ndim)

# Run RRT search
print("Running RRT search... \nIn case of long runtimes, decrease growth rate.")
vcount = rrt_drive.run(mylat, c_obj, myvtx, nodemax)

# Write output file containing tree nodes
np.savetxt(foutname, np.array(myvtx.node))

# Count generated nodes
print("\n",count_nodes(myvtx.node),"nodes generated")

# Plot results
tree_plotter(myvtx.vert, myvtx.node)
