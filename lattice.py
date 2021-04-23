import numpy as np

class Lattice:
    """
        Lattice operations class
    """
    
    def __init__(self, xbins, ndim):
        """
            Create lattice

            xbins  - number of points/bins for each dimension
            ndim   - number of dimensions	    
        """
        # Single-axis discretization
        x_axis = np.linspace(0.0, 1.0, num=xbins)

        # Store important lattice variables
        self.ndim = ndim
        self.xbins = xbins

        # Create lattice array	
        self.xlat = np.tile(x_axis, (ndim,1))
        return 

    def find_nearest(self, Xnodes, xvec):
        """
            Find nearest stored point in Xnodes to point xvec
        """
        # Find square distance     
        dx_2 = np.sum((Xnodes - xvec)**2, axis=1)

        # Identify nearest point
        best_ind = np.argmin(dx_2)
        best_dx = np.sqrt(dx_2[best_ind])
        return Xnodes[best_ind], best_dx, best_ind

    def select_pt(self):
        """
            Randomly select lattice point
        """
        # Randomly select indices on lattice
        xrand = np.random.randint(0, self.xbins, size=self.ndim)

        # Create random point using randomly select indices
        return self.xlat[0, xrand]