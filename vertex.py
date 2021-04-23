import numpy as np

class Vertex:
    """ 
        Vertex operations class
    """

    def __init__(self, x0):
        """
            Initialize vertex and node lists

            x0 - initial/starting node
        """
        self.node = []
        self.vert = []

        # Include initial node in node list
        self.node.append(np.array(x0))
        return

    def ccw(self, A, B, C):
        """
            Check if lattice nodes A, B, and C are listed in counterclockwise order
        """
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def intersect(self, A, B, C, D):
        """
            Return TRUE if AB and CD intersect
        """
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    def vertex_cross(self, xnew, ind):
        """
            Return TRUE if there is intersection between new vertex and stored verteces
            New vertex is defined using newly-added node XNEW and existing node with index IND
            Function does not check for colinear verteces
        """
        for AB in self.vert:
            # Avoid intersection flag if verteces share node
            if (np.any(AB == ind)): continue

            # Check if verteces intersect
            if (self.intersect(self.node[AB[0]], self.node[AB[1]], self.node[ind], xnew)):
                return True
        return False