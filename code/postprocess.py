#!/usr/bin/env python

import sys, fileinput
import tree

def run(file):
    with open(file, 'r') as f:
        trees = []
        for line in f:
            try:
                t = tree.Tree.from_str(line)
        
                t.restore_unit()
                t.unbinarize()
                
                trees.append(t)
                print(t)
            except:
                trees.append("")
                print("")
    return trees
        
