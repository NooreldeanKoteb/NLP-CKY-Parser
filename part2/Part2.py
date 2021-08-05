# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 14:12:28 2021

@author: Nooreldean Koteb
"""
import Part1 as lib
import preprocess
import unknown
import tree
import postprocess
from collections import defaultdict
from math import log
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import arange
import time

def grammar_prob(rules, rules_prob):
    grammar = {}
    
    for rule in rules.keys():
        grammar[rule] = []
        for sub in rules[rule].keys():
            sub_list = sub.replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(',')
            grammar[rule].append([sub_list, rules_prob[f'{rule} -> {sub}']])
            
    return (grammar)


def gen_table(n):
    table = []
    for i in range(n):
        temp = []
        for j in range(n+1):
            temp.append(set([]))
        table.append(temp)
    return table


def extract_tree(sent, trace, i, j, head):
    n = j-i    
    if n == 1:
        return [head, sent[i]]
    else:
        Y,Z,s = trace[i, j, head]
        return [head, extract_tree(sent, trace, i, s, Y), extract_tree(sent, trace, s, j, Z)]
    

def CKY_parse(grammar, sent):
    sent = sent.split()
    n = len(sent) +1

    table = gen_table(n-1)
    table2 = defaultdict(float)
    trace = {}
    
    for i in range(1, n):
        table[i-1][i-1].add(sent[i-1])
        for rule in grammar.keys():
            for sub in grammar[rule]:
                if len(sub[0]) == 1 and sent[i-1] == sub[0][0]:
                        table2[i-1, i, rule] = log(sub[1], 10)
                        table[i-1][i].add(rule)    
    
    
    for l in range(2, n):
        for i in range(0, n-l):
            k = i+l
            for j in range(i-1, k):
                
                for Y in table[i][j]:
                    for Z in table[j][k]:
                        for rule in grammar.keys():
                            for sub in grammar[rule]:
                                if [Y,Z] == sub[0]:
                                    cur_prob = log(sub[1], 10)
                                    new_prob = cur_prob + table2[i,j,Y] + table2[j,k,Z]
                                    
                                    check_prob = (i,k,rule)
                                    if check_prob in table2.keys():
                                        if new_prob > table2[i,k,rule]:
                                            table2[i,k,rule] = new_prob
                                            trace[i,k,rule] = (Y,Z,j)
                                    else:
                                        table2[i,k,rule] = new_prob
                                        trace[i,k,rule] = (Y,Z,j)
                                    
                                    if check_prob not in trace:
                                        trace[i,k,rule] = (Y,Z,j)
                                        
                                    if rule not in table[i][k]:
                                        table[i][k].add(rule)                            
                
            
    for t in table:
        print(t)
        
    prob = table2[0, n-1, 'TOP']
    
    tree = ''
    if prob:
        tree = extract_tree(sent, trace, 0, n-1, 'TOP')
        tree = str(tree).replace("[", "(").replace("]", ")").replace("'", "").replace(",", "")
        
    return (tree, prob)
    
    
def parse_file(file, grammar):
    with open(file+'.strings', 'r') as f:
        lines = f.readlines()

    parsed_lines = []
    
    x = []
    y = []
    for line in lines:
        x.append(len(line.split()))
        start = time.time()
    
        parsed_lines.append(CKY_parse(grammar, line))
        
        end = time.time()
        y.append(end - start)
    
    with open(file+'.parses', 'w') as f:
        for i in parsed_lines:
            f.write(i[0]+'\n')
        f.close()
    
    return parsed_lines, x, y


def post_proc(dat):
    data = postprocess.run(dat)
    with open(dat+'.post', 'w') as f:
        for i in data:
            f.write(i.__str__()+'\n')
        f.close()
    return data
        
def graph_k(x, y):
    def objective(x, c, k):
    	return c*pow(x,k)
    
    popt, _ = curve_fit(objective, x, y)   
    c, k = popt
    
    x_line = arange(min(x), max(x), 1)
    y_line = objective(x_line, c, k)
    plt.yscale('log')
    plt.xscale('log')
    plt.scatter(x, y)
    plt.plot(x_line, y_line, '--', color='red')
    # return plt.show()    
    return c,k

##########
# Part 2 #
##########
test_strings = '../data/test'
dev_strings = '../data/dev'
trees = lib.read_tree(lib.processed_train_dat_file)
rules, rule_labels = lib.count_rules(trees)
rules_prob = lib.rules_probabilities(rules, rule_labels)
grammar = grammar_prob(rules, rules_prob)

dev_parsed_lines, x, y = parse_file(dev_strings, grammar)
test_parsed_lines, _, _ = parse_file(test_strings, grammar)

post_test = post_proc(test_strings+'.parses')
post_dev = post_proc(dev_strings+'.parses')

print("First 5 Parsed lines of dev.strings:")
for i in dev_parsed_lines[:5]:
    print(f'{i[0]} PROB:{i[1]}\n')

c, k = graph_k(x, y)
    
print("\nFirst 3 Parsed lines of test.strings:")
for i in test_parsed_lines[:3]:
    print(f'{i[0]} PROB:{i[1]}\n')

