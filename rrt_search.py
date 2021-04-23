import numpy as np

class RapidlyExploringRandomTree:
    """ 
        Rapidly-Exploring Random Tree engine
    """

    def __init__(self, epsilon, growth_rate, ndim):
        """
            epsilon - controls minimum allowed displacement from existing point
            growth_rate - controls maximum allowed displacement from point
        """
        # Check that we have 2D problem (note: higher dims can work without vertex cross check)
        assert(ndim == 2)

        # Check that we have reasonable parameter choice
        assert(growth_rate > epsilon)

        # Store RRT model hyperparameters 
        self.epsilon = epsilon
        self.growth_rate = growth_rate
        return

    def printprog(self, i, ntot, barLength = 20):
        """
            Function for displaying progress of RRT search
        """
        percent = float(i) * 100 / ntot
        arrow   = '-' * int(percent/100 * barLength - 1) + '>'
        spaces  = ' ' * (barLength - len(arrow))
        print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

    def iterate(self, mylat, c_obj, myvtx, vcount):
        """
            Run single iteration for Rapidly Exploring Random Tree (RRT)
        """  
        # Select random point
        xrand = mylat.select_pt()

        # Find nearest point
        xnear, dx, ind = mylat.find_nearest(myvtx.node, xrand)

        # Find displacement vector from nearest point
        deltaX = xrand - xnear

        # Normalize adjusted displacement vector
        dX_mag = np.linalg.norm(deltaX)
        deltaX /= dX_mag
        deltaX *= self.growth_rate

        # Cap maximum displacement at growth rate	
        fac = dX_mag
        if (dx > self.growth_rate): fac = self.growth_rate

        # Identify boundary, skip displacement attempt if no boundary found
        check1, xnew = c_obj.find_boundary(xnear, deltaX, self.growth_rate, self.epsilon)
        if not check1: return vcount

        # If there is only one node, add 2nd node without checking for vertex intersection
        if vcount == 1:
            myvtx.node.append(xnew)
            myvtx.vert.append([0, 1])
            return 2

        # Store newly-generated node/vertex if there is no intersection
        check2 = myvtx.vertex_cross(xnew, ind)
        if not check2:
            myvtx.node.append(xnew)
            myvtx.vert.append([vcount, ind])
            vcount += 1
        return vcount

    def run(self, mylat, c_obj, myvtx, nodemax):
        """
            Primary RRT loop - repeats until we have generated 'nodemax' number of nodes
        """
        vcount = 1
        while vcount < nodemax:   
            vcount = self.iterate(mylat, c_obj, myvtx, vcount)

            # Print progress
            self.printprog(vcount, nodemax)
        return vcount