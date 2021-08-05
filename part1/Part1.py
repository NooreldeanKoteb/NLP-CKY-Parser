# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:16:15 2021

@author: Nooreldean Koteb
"""

import preprocess
import unknown
import tree
import postprocess


def pre_unk(dat):
    data = preprocess.run(dat)
    with open(dat+'.pre', 'w') as f:
        for i in data:
            f.write(i.__str__()+'\n')
        f.close()
        
    data = unknown.run(dat+'.pre')
    
    with open(dat+'.pre.unk', 'w') as f:
        for i in data:
            f.write(i.__str__()+'\n')
        f.close()
    
    return data


def read_tree(dat):
    with open(dat, 'r') as f:
        trees = []
        for line in f:
            t = tree.Tree.from_str(line)
        
            # Make sure that all the roots still have the same label.
            assert t.root.label == 'TOP'
            
            trees.append(t)
        return trees


def count_rules_helper(tree, rules, rule_labels):
    children = []
    
    for child in tree.children:
        children.append(child.label)
        
        count_rules_helper(child, rules, rule_labels)
    
    if children != []:
        if tree.label in rules:
            rule_labels[tree.label] += 1
            if str(children) in  rules[tree.label]:
                rules[tree.label][str(children)] += 1
            else:
                rules[tree.label][str(children)] = 1
        else:
            rule_labels[tree.label] = 1
            rules[tree.label] = {str(children): 1}
    
    
def count_rules(trees):
    rule_labels = {}
    rules = {}
    
    for tree in trees:
        count_rules_helper(tree.root, rules, rule_labels)
    
    return (rules, rule_labels)    

# def get_most_freq(rules, top=10):
#     most_freq = {}
#     for rule in rules.keys():
#         for sub in rules[rule].keys():
#             rule_name = f"{rule} -> {sub}"
#             if len(most_freq) < top:
#                 most_freq[rule_name] = rules[rule][sub]
#             else:
#                 for key,freq in most_freq.items():
#                     if freq < rules[rule][sub]:
#                         del  most_freq[key]
#                         most_freq[rule_name] = rules[rule][sub]
#                         break
                    
#     sorted_most_freq = sorted(most_freq.items(), key=lambda item:item[1], reverse=True)
    
#     return sorted_most_freq, most_freq

def get_most_freq(rules, top=5):
    most_freq = []
    for rule in rules.keys():
        for sub in rules[rule].keys():
            rule_name = f"{rule} -> {sub}"
            if len(most_freq) < top:
                most_freq.append((rules[rule][sub], cleanup_rule_name(rule_name)))
            else:
                most_freq = sorted(most_freq, key=lambda item:item[0])
                if most_freq[0][0] < rules[rule][sub]:
                    most_freq[0] = (rules[rule][sub], cleanup_rule_name(rule_name))
                
    sorted_most_freq = sorted(most_freq, key=lambda item:item[0], reverse=True)
    
    print(f'Top {top} Frequent Rules:')
    for i in sorted_most_freq:
        print(f'\t{i[1]} # {i[0]}')
    
    return sorted_most_freq

def probability(rules, labels, rule):
    print(rule)
    return rules[rule[0]][rule[1]]/labels[rule[0]]

def cleanup_rule_name(rule_name):
    return rule_name.replace('[', '').replace(']', '').replace(',', '').replace("'", '')
     
def unique_rules(rules):
    unique = 0
    
    for rule in rules:
        unique+= len(rules[rule])
    
    return unique

def rules_probabilities(rules, labels):
    rules_prob = {}
    for rule in rules.keys():
        for sub in rules[rule].keys():
            rule_name = f"{rule} -> {sub}"
            rules_prob[rule_name] = probability(rules, labels, (rule, sub))
    
    return rules_prob

def highest_prob(rules_prob, top = 5):
    prob = []
    print(f'Top {top} Probability Rules:')
    for rule in rules_prob.keys():
        if len(prob) < top:
            prob.append((rules_prob[rule], cleanup_rule_name(rule)))
        else:
            prob = sorted(prob, key=lambda item:item[0])
            if prob[0][0] < rules_prob[rule]:
                prob[0] = (rules_prob[rule], cleanup_rule_name(rule))
    
    sorted_prob = sorted(prob, key=lambda item:item[0], reverse=True)
    for i in sorted_prob:    
        print(f'\t{i[1]} #  {i[0]:.5}')

##########
# Part 1 #
##########

train_dat_file = '../data/train.trees'
dev_dat_file = '../data/dev.trees'
#Only have to run once to save the file
# data = pre_unk(train_dat_file)
# data = pre_unk(dev_dat_file)
processed_train_dat_file = train_dat_file+'.pre.unk'
processed_dev_dat_file = dev_dat_file+'.pre.unk'

trees = read_tree(processed_train_dat_file)

rules, rule_labels = count_rules(trees)

uni_rule = unique_rules(rules)

print(f'\nUnique Rules: {uni_rule}\n')
rules_prob = rules_probabilities(rules, rule_labels)

sorted_most_frequent= get_most_freq(rules, 5)
print('\n')
sorted_highest_prob = highest_prob(rules_prob, 5)













