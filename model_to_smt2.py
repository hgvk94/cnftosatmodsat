import sys
from random import randrange
import itertools

def get_lit(lit, randomize=False):
    d = int(lit)
    is_pos = randrange(2) if randomize else d > 0
    v = "v"+str(abs(d))
    if is_pos:
        return v
    else:
        return "(not " + v + ")"

def switch_config(inp):
    return [ "switch"+str(i+1) if s else "(not switch" + str(i+1) +")"  for (i,s) in enumerate(inp)]

def print_clause(args):
    print("(or " + " ".join(args) + ")")

def print_mdl_with_switch(mdl, unsat=False):
    print("(and ")
    for lit in mdl:
        for p in itertools.product([True, False], repeat=2):
            lits = switch_config(p)
            if unsat:
                lits.append(get_lit(lit, True))
            else:
                lits.append(get_lit(lit, (True in p)))
            print_clause(lits)
    print(")")


def print_mdl(mdl):
    print("(and ")
    for lit in mdl:
        print_clause([get_lit(lit, False)])
    print(")")

def model_to_smt2(fname, add_switch, unsat):
    init = True
    with open(fname) as f:
        line = f.readlines()
        for m in line:
            if init:
                assert 's SATISFIABLE' in m
                init = False
                continue
            mdl = m.split(" ")
            assert mdl[0] == "v"
            if add_switch:
                print_mdl_with_switch(mdl[1:-1], unsat)
            else:
                print_mdl(mdl[1:-1])

if __name__ == "__main__":
    model_to_smt2(sys.argv[1], False)
