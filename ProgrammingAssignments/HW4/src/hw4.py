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
#var_ranges = []  UNCOMMENT THIS WHEN DONE DEBUGGING
var_ranges = [2, 2, 2, 2, 2]
var_log = False


#
# FACTOR CLASS -- EDIT HERE!
#

def union(list1, list2):
    new_list = list1
    for item in list2:
        if item not in new_list:
            new_list.append(item)
    return new_list

class Factor(dict):
    def __init__(self, scope_, vals_, strides_):
        # Example scope: [1, 3, 4]     -- This indicates a factor over the variables x_1, x_3, and x_4
        self.scope = scope_
        self.vals = vals_
        self.strides = strides_
        # TODO -- ADD EXTRA INITIALIZATION CODE IF NEEDED


    def __mul__(self, other):
        """Returns a new factor representing the product."""
        # TODO -- PUT YOUR MULTIPLICATION CODE HERE!
        # BEGIN PLACEHOLDER CODE -- DELETE THIS!
        var_logging("---------------------------------")
        var_logging("Scopes: " + str(self.scope))
        var_logging("Values: " + str(self.vals))
        var_logging("Strides: " + str(self.strides))
        var_logging("\n")
        var_logging("Other Scopes: " + str(other.scope))
        var_logging("Other Values: " + str(other.vals))
        var_logging("Other Strides: " + str(other.strides))
        var_logging("\n")




        j = 0
        k = 0

        assignments = {}  # Assignments is a list holding the current assignment of each of the variables.  So [0, 1, 0] means x_0 = false, x_1 = true, x_2 = false
        unioned_scopes = union(self.scope, other.scope)
        for l in unioned_scopes:
            assignments[l] = 0

        # for i = 0 ...  |Val(X_1 U X_2)| - 1
        # this loop means to loop through all the values of the X_1 variables
        # in the table and all the values of the X_2 variables in the table
        # For example, if X_1 is binary, and X_2 is binary, then |Val(X_1 U X_2)| should be 4
        numVals = 1

        for item in unioned_scopes:
            numVals *= var_ranges[item]


        psi = []
        var_logging("NumVals: " + str(numVals))

        for i in range(numVals):

            var_logging("j: " + str(j))
            var_logging("k: " + str(k))

            psi.append(self.vals[j] * other.vals[k])
            var_logging("i is: " + str(i))

            for l in unioned_scopes:
                var_logging("l is: " + str(l))
                assignments[l] = assignments[l] + 1
                if assignments[l] == var_ranges[l]:
                    var_logging("entered if statement")
                    assignments[l] = 0
                    j = j - (var_ranges[l] - 1) * self.strides[l]
                    k = k - (var_ranges[l] - 1) * other.strides[l]
                else:
                    var_logging("entered else statement")
                    var_logging("L: " + str(l))
                    j = j + self.strides[l]
                    k = k + other.strides[l]
                    break

        factor_strides = {}
        for factor in unioned_scopes:
            if factor == unioned_scopes[0]:
                factor_strides[factor] = 1 # First stride is always 1
            else:
                factor_strides[factor] = calc_stride(unioned_scopes, factor)

        for num in range(len(var_ranges)):
            if num not in unioned_scopes:
                factor_strides[num] = 0


        var_logging(factor_strides)


        new_scope = self.scope
        new_vals  = self.vals
        new_strides = self.strides
        # END PLACEHOLDER CODE



        var_logging("Unioned Scopes: " + str(unioned_scopes))
#        return Factor(new_scope, new_vals, new_strides)
        return Factor(unioned_scopes, psi, factor_strides)

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
        val = val + str(self.strides) + "\n"
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

def calc_stride(factor_scope, target):
    prod = 1

    if target not in factor_scope:
        raise Exception("Error! The variable " + str(target) + " was no in the scope!")

    for variable in factor_scope:
        if variable == target:
            return prod
        prod *= var_ranges[variable]



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
    var_logging("Factor scopes: " + str(factor_scopes))

    for index in range(len(factor_scopes)):
        factor_strides = {}
        for factor in factor_scopes[index]:
            if factor == factor_scopes[0]:
                factor_strides[factor] = 1 # First stride is always 1
            else:
                factor_strides[factor] = calc_stride(factor_scopes[index], factor)

        for num in range(num_factors):
            if num not in factor_scopes[index]:
                factor_strides[num] = 0
        stride_list.append(factor_strides)

    var_logging(stride_list)

    var_logging("Factor strides calculated")

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
    var_logging("ZIP:" + str(zip(factor_scopes,factor_vals, stride_list)))
    factor_list = [Factor(s,v, stride) for (s,v, stride) in zip(factor_scopes,factor_vals, stride_list)] # We return a list of factors

    for factor in factor_list:
        var_logging("Factor: " + str(factor))
    return factor_list # We return a list of factors


#
# MAIN PROGRAM
#

if __name__ == "__main__":
    var_logging("Beginning program")
    factors = read_model()             #IMPORTANT! UNCOMMENT THIS WHEN DONE DEBUGGING
    '''
    # T1 Network

    f1_strides = {0: 1, 1: 0, 2: 0, 3: 0}
    f2_strides = {0: 0, 1: 1, 2: 2, 3: 0}
    f3_strides = {0: 2, 1: 0, 2: 1, 3: 0}
    f4_strides = {0: 0, 1: 0, 2: 2, 3: 1}

    f1 = Factor([0], [1.5, 1.5], f1_strides)
    f2 = Factor([1, 2], [0.3, 0.7, 2.9, 0.1], f2_strides)
    f3 = Factor([2, 0], [2.8, 1.2, 0.2, 2.8], f3_strides)
    f4 = Factor([3, 2], [1.5, 2.5, 1.1, 0.9], f4_strides)

    factors = [f1, f2, f3, f4]
    '''


    '''
    # T2 Network

    f1_strides = {0: 1, 1: 0, 2: 2, 3: 0, 4: 0}
    f2_strides = {0: 0, 1: 1, 2: 0, 3: 0, 4: 0}
    f3_strides = {0: 0, 1: 0, 2: 1, 3: 0, 4: 0}
    f4_strides = {0: 0, 1: 2, 2: 4, 3: 1, 4: 0}
    f5_strides = {0: 4, 1: 0, 2: 0, 3: 2, 4: 1}

    f1 = Factor([0, 2], [0.05000000, 0.95000000, 1.50000000, 0.50000000], f1_strides)
    f2 = Factor([1], [0.70000000, 2.30000000], f2_strides)
    f3 = Factor([2], [1.10000000, 0.90000000], f3_strides)
    f4 = Factor([3, 1, 2], [0.01000000, 0.99000000, 2.25000000, 3.75000000, 0.50000000, 0.50000000, 0.60000000, 0.40000000], f4_strides)
    f5 = Factor([4, 3, 0], [0.01000000, 4.99000000, 0.10000000, 1.90000000, 0.20000000, 0.80000000, 0.50000000, 0.50000000], f5_strides)


    factors = [f1, f2, f3, f4, f5]
    '''


    # Compute Z by brute force
    var_logging("Factors read...")
    f = reduce(Factor.__mul__, factors)
    z = sum(f.vals)
    print "Z = ",z

