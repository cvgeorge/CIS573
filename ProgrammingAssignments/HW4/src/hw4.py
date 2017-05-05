# CIS 553 - Probabalistic Methods in AI
# Homework #4
# Connor George
# May 2017
#
# This code was adapted from the provided code template
#
# TEMPLATE CODE
import sys
import tokenize
import itertools

# List of variable cardinalities is global, for convenience.
# NOTE: This is not a good software engineering practice in general.
# However, the autograder code currently uses it to set the variable 
# ranges directly without reading in a full model file, so please keep it
# here and use it when you need variable ranges!
var_ranges = []
var_log = True


#
# FACTOR CLASS -- EDIT HERE!
#

def union(list1, list2):
    new_list = list1
    for item in list2:
        if item not in list2:
            new_list.append(item)
    return new_list

class Factor(dict):
    def __init__(self, scope_, vals_, strides_, ranges_):
        # Example scope: [1, 3, 4]     -- This indicates a factor over the variables x_1, x_3, and x_4
        self.scope = scope_
        self.vals = vals_
        self.strides = strides_
        self.ranges = ranges_
        # TODO -- ADD EXTRA INITIALIZATION CODE IF NEEDED


    def __mul__(self, other):
        """Returns a new factor representing the product."""
        # TODO -- PUT YOUR MULTIPLICATION CODE HERE!
        # BEGIN PLACEHOLDER CODE -- DELETE THIS!

        var_logging("Scopes: " + str(self.ranges))
        var_logging("Ranges: " + str(self.ranges))
        var_logging("Values: " + str(self.ranges))
        var_logging("Strides: " + str(self.ranges))
        var_logging("\n")




        j = 0
        k = 0

        assignments = []

        for l in range(len(union(self.scope, other.scope))):
            assignments.append(0)

        # for i = 0 ...  |Val(X_1 U X_2)| - 1
        # this loop means to loop through all the values of the X_1 variables
        # in the table and all the values of the X_2 variables in the table
        # For example, if X_1 is binary, and X_2 is binary, then |Val(X_1 U X_2)| should be 4

        new_scope = self.scope
        new_vals  = self.vals
        new_strides = self.strides
        new_ranges = self.ranges
        # END PLACEHOLDER CODE

        return Factor(new_scope, new_vals, new_strides, new_ranges)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    def __repr__(self):
        """Return a string representation of a factor."""
        rev_scope = self.scope[::-1]
        val = "x" + ", x".join(str(s) for s in rev_scope) + "\n"
        itervals = [range(var_ranges[i]) for i in rev_scope]
        for i,x in enumerate(itertools.product(*itervals)):
            val = val + str(x) + " " + str(self.vals[i]) + "\n"
        return val


#
# READ IN MODEL FILE
#

# Read in all tokens from stdin.  Save it to a (global) buf that we use
# later.  (Is there a better way to do this? Almost certainly.)
curr_token = 0
token_buf = []

def var_logging(to_print):
    if var_log == True:
        print(to_print)

def read_tokens():
    global token_buf
    for line in sys.stdin:
        token_buf.extend(line.strip().split())
    var_logging("Num tokens:" + str(len(token_buf)))

def next_token():
    global curr_token
    global token_buf
    curr_token += 1
    return token_buf[curr_token-1]

def next_int():
    return int(next_token())

def next_float():
    return float(next_token())

# Preamble clarification:
#
# MARKOV     -- Type of network
# 3          -- There are 3 variables (nodes) in the network, x_0, x_1, and x_2
# 2 2 3      -- The first and second variables are binary (0, 1).  The third variable is trinary (0, 1, 2)
# 2          -- There are 2 cliques in the network
# 2 0 1      -- There are 2 variables in this clique, they are x_0 and x_1
# 2 1 2      -- There are 2 variables in this clique, they are x_1 and x_2
#
#
# Function table clarification:
#
#
#
#
#
#



def read_model():
    # Read in all tokens and throw away the first (expected to be "MARKOV")
    var_logging("Reading tokens")
    read_tokens()
    var_logging("Tokens read")
    s = next_token()

    # Get number of vars, followed by their ranges
    num_vars = next_int()
    var_logging("Number of variables is: " + str(num_vars))
    global var_ranges;
    var_ranges = [next_int() for i in range(num_vars)]
    var_logging("Variable ranges/cardinalities calculated")  # Example: If the variable range is 2, it is a binary variable

    # Get number and scopes of factors 
    num_factors = int(next_token())
    var_logging("Number of factors is: " + str(num_factors)) # This is how many tables we will read in as well

    factor_scopes = []                                       # A factor scope simply refers to the variables present in the factor
    for i in range(num_factors):
        scope = [next_int() for i in range(next_int())]
        # NOTE: 
        #   UAI file format lists variables in the opposite order from what
        #   the pseudocode in Koller and Friedman assumes. By reversing the
        #   list, we switch from the UAI convention to the Koller and
        #   Friedman pseudocode convention.
        scope.reverse()
        factor_scopes.append(scope)

    stride_list = []
    print factor_scopes
    for index in range(len(factor_scopes)):
        factor_strides = {}
        for factor_index in range(len(factor_scopes[index])):
            if factor_index == 0:
                factor_strides[factor_scopes[index][0]] = 1 # First stride is always 1
            else:
                prod = 1
                for i in range(0, factor_index):
                    prod *= var_ranges[factor_scopes[index][i]]
                factor_strides[factor_scopes[index][factor_index]] = prod
        stride_list.append(factor_strides)

    print stride_list

    var_logging("Factor strides calculated..... but this code hasn't been tested yet")

    var_logging("Factors aligned with K&F standard")


    # Read in all factor values
    factor_vals = []
    for i in range(num_factors):                             # Factor values are the values in the table
        factor_vals.append([next_float() for i in range(next_int())])

    var_logging("Factor values read")

    # DEBUG
    #print "Num vars: ",num_vars
    #print "Ranges: ",var_ranges
    #print "Scopes: ",factor_scopes
    #print "Values: ",factor_vals
    var_logging("File read!")
    return [Factor(s,v, stride, ranges) for (s,v, stride, ranges) in zip(factor_scopes,factor_vals, stride_list, var_ranges)] # We return a list of factors


#
# MAIN PROGRAM
#

if __name__ == "__main__":
    var_logging("Beginning program")
    factors = read_model()
    # Compute Z by brute force
    var_logging("Factors read...")
    f = reduce(Factor.__mul__, factors)
    z = sum(f.vals)
    print "Z = ",z

