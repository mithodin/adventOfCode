#!/usr/bin/env python3
import networkx as nx
import re

rule_pattern = re.compile(r'([a-z]+ [a-z]+) bags contain (([0-9]+ [a-z]+ [a-z]+ bags?,? ?)+|(no other bags))')
contains_pattern = re.compile(r'([0-9]+) ([a-z]+ [a-z]+) bags?')
def parse_rules(filename):
    res = []
    with open(filename, 'r') as rules:
        for rule in rules:
            match = rule_pattern.match(rule).groups()
            bag_color = match[0]
            contains = []
            if match[3] is None:
                contains = contains_pattern.findall(match[1])
            res.append((bag_color, contains))
    return res


def build_network(rules):
    graph = nx.DiGraph()
    for rule in rules:
        graph.add_node(rule[0])
    for rule in rules:
        parent = rule[0]
        for child in rule[1]:
            name = child[1]
            number = int(child[0])
            graph.add_edge(parent, name, weight=number)
    return nx.freeze(graph)


def get_all_predecessors(graph, root_node):
    pred = set()
    process = {root_node}
    while len(process) > 0:
        node = process.pop()
        direct_predecessors = {n for n in graph.predecessors(node)}
        process |= direct_predecessors - (pred | {root_node})
        pred |= direct_predecessors
    return pred


def num_predecessors(graph, node):
    return len(get_all_predecessors(graph, node))


def sum_all_successors(graph, root_node):
    sum_succ = 0
    for node in graph.successors(root_node):
        weight = graph.get_edge_data(root_node, node)['weight']
        sum_succ += weight * ( sum_all_successors(graph, node) + 1 )
    return sum_succ


def test_all_predecessors():
    rules = parse_rules('example.dat')
    graph = build_network(rules)
    assert get_all_predecessors(graph, 'shiny gold').issuperset({'bright white', 'muted yellow', 'dark orange', 'light red'})


def test_sum_all_successors():
    rules = parse_rules('example.dat')
    graph = build_network(rules)
    assert sum_all_successors(graph, 'shiny gold') == 32

    rules = parse_rules('example2.dat')
    graph = build_network(rules)
    assert sum_all_successors(graph, 'shiny gold') == 126


rules = parse_rules('input.dat')
graph = build_network(rules)
print(num_predecessors(graph, 'shiny gold'))
print(sum_all_successors(graph, 'shiny gold'))
