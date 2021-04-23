# RRT_search
RAPIDLY-EXPLORING RANDOM TREE (RRT)

Author: Nikolai Petsev


DESCRIPTION:

This program uses a rapidly-exploring random tree (RRT) algorithm to search a 2D space with 
geometry/obstacles defined in a user-supplied input file. RRTs represent a Monte Carlo path planning 
approach with bias towards the largest Voronoi regions in a given configuration space. RRTs work by 
iteratively sampling new states, and subsequently growing branches extending from the nearest existing 
nodes towards these new states. After completing the RRT search, the program visualizes the generated 
tree and corresponding Voronoi cells, and writes its nodes to a dump file.


FILES:

- constraints.py
- lattice.py
- rrt_main.py
- rrt_search.py
- vertex.py


REQUIREMENTS:

- Python 3.0 or above
- NumPy
- Matplotlib
- SciPy


GETTING STARTED:

The main program script is executed as:

python rrt_main.py <input file> <output file> <nsamples>
  
In this command:

input file - name of file containing space/obstacle geometry

output file - name of file for dumping final tree nodes

nodemax - the number of nodes that the RRT should generate

  
For example, we can generate a tree with 1000 nodes inside a triangular space using:

python rrt_main.py triangle.txt nodes.txt 1000

The following input files for different geometries are provided:
- square.txt
- triangle.txt
- circle.txt
- circle_full.txt
