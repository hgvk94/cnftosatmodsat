import sys
import re

def print_declare(var):
    for i in range(1, int(var) + 1):
        print("(declare-const v%d Bool)" % i)

def cnf_to_smt2(fname, print_assert = False):
    init = True
    header = re.compile(r'p cnf (\d+) (\d+)')
    with open(fname) as f:
        line = f.readlines()
        for m in line:
            if init:
                op = header.match(m)
                var = op.group(1)
                clause = op.group(2)
                if print_assert:
                    print_declare(var)
                    print("(assert ", end = '')
                print("(and ")
                init = False
                continue
            mdl = m.split(" ")
            if (mdl[0] == 'c'):
                continue
            if (len(mdl) > 2):
                print("(or ", end='')
            for lit in mdl[0:-1]:
                d = int(lit)
                if d > 0:
                    print(" v%d" % (int(d)), end='')
                else:
                    print(" (not v%d)" % (int(abs(d))), end='')
            if (len(mdl) > 2):
                print(")")
            else:
                print()
        if print_assert:
            print(")", end = '')
        print(")")
        if print_assert:
            print("(check-sat)")

if __name__ == "__main__":
    cnf_to_smt2(sys.argv[1], True)
