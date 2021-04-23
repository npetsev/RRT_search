import numpy as np

class Constraint:
    """Space geometry constraints loaded from a file"""

    def __init__(self, fname):
        """
        Construct a Constraint object from a constraints file

        :param fname: Name of the file to read the Constraint from (string)
        """
        with open(fname, "r") as f:
            lines = f.readlines()
        # Parse the dimension from the first line
        self.n_dim = int(lines[0])

        # Parse the example from the second line
        self.example = [float(x) for x in lines[1].split(" ")[0:self.n_dim]]

        # Run through the rest of the lines and compile the constraints
        self.exprs = []
        for i in range(2, len(lines)):
            # Support comments in the first line
            if lines[i][0] == "#":
                continue
            self.exprs.append(compile(lines[i], "<string>", "eval"))
        return

    def get_example(self):
        """Get the example feasible vector"""
        return self.example

    def get_ndim(self):
        """Get the dimension of the space on which the constraints are defined"""
        return self.n_dim

    def apply(self, x):
        """
        Apply the constraints to a vector, returning True only if all are satisfied

        :param x: list or array on which to evaluate the constraints
        """
        for expr in self.exprs:
            if not eval(expr):
                return False
        return True

    def apply_box(self, x):
        """
        Apply box constraints (points generated on interval [0,1] in all dimensions)
        """
        for xi in x:
            if xi > 1.0 or xi < 0.0:
                return False
        return True

    def find_boundary(self, xnear, dx, growth_rate, epsilon):
        """ 
            Function that finds boundary by shrinking displacement from point xnear
        """
        # Create array of displacement vector magnitudes ranging between epsilon (min) and growth_rate (max)
        vmag = np.linspace(growth_rate, epsilon, num=100)

        # Create array containing test nodes
        dxlist = xnear + vmag[:,None] * dx[None,:] 

        # Check if any of nodes satisfy constraints
        check_array = [self.apply(x) and self.apply_box(x) for x in dxlist]

        # Exit if no valid nodes in test array
        if not np.any(check_array): return False, np.array([])

        # Find indeces of all valid vectors
        best_ind = [i for i, x in enumerate(check_array) if x]
        return True, dxlist[best_ind[0],:]

