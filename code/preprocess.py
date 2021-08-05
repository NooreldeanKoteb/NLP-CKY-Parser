#!/usr/bin/env python

import sys, fileinput
import tree

def run(file):
    # for line in fileinput.input():
    with open(file, 'r') as f:
        trees = []
        for line in f:
            t = tree.Tree.from_str(line)
        
            # Binarize, inserting 'X*' nodes.
            t.binarize()
        
            # Remove unary nodes
            t.remove_unit()
        
            # The tree is now strictly binary branching, so that the CFG is in Chomsky normal form.
        
            # Make sure that all the roots still have the same label.
            assert t.root.label == 'TOP'
            
            trees.append(t)
            print(t)
        return trees
            
        
