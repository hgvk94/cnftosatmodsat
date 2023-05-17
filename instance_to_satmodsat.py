import sys
import re
import model_to_smt2
import cnf_to_smt2

def print_shared_vars(var):
    #Assume that the first 512 variables are for the input
    print("(", end='')
    for i in range(1, 513):
        print(" v%d" % i, end='')
    print(")")


fname = sys.argv[1]
header = re.compile(r'p cnf (\d+) (\d+)')

produceUnsatInstances=True
with open(fname) as f:
        line = f.readline()
        op = header.match(line)
        var = op.group(1)
        clause = op.group(2)
        cnf_to_smt2.print_declare(var)

print("(declare-const switch1 Bool)")
print("(declare-const switch2 Bool)")
print("(satmodsat ")
print_shared_vars(var)
model_to_smt2.model_to_smt2(fname.replace(".cnf", ".mdl"), True, produceUnsatInstances)
cnf_to_smt2.cnf_to_smt2(fname, False)
print("(switch1 switch2) ()")
print(")")
