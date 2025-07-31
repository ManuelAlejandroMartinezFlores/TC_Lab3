import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from lab2_ejercicioc import *

class RegexNode:
    """Para realizar el árbol sintáctico"""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"RegexNode({self.value})"

def postfix_to_tree(postfix):
    """Postfix a árbol"""
    stack = deque()
    
    for char in postfix:
        if char in ('.', '|'):  # Operadores
            right = stack.pop()
            left = stack.pop()
            stack.append(RegexNode(char, left, right))
        elif char in ('*', '+', '?'):  # Operadores unitarios
            child = stack.pop()
            stack.append(RegexNode(char, child))
        else:  # Operandos
            stack.append(RegexNode(char))
    
    if len(stack) != 1:
        raise ValueError("Postfix inválido")
    
    return stack.pop()

def tree_to_networkx(tree, graph=None, parent=None, edge_label=""):
    """Árbol a NetworkX"""
    if graph is None:
        graph = nx.DiGraph()
    
    if tree is None:
        return graph
    
    node_id = id(tree)
    graph.add_node(node_id, label=tree.value)
    
    if parent is not None:
        graph.add_edge(parent, node_id, label=edge_label)
    
    if tree.left is not None:
        tree_to_networkx(tree.left, graph, node_id, "L")
    if tree.right is not None:
        tree_to_networkx(tree.right, graph, node_id, "R")
    
    return graph

def plot_regex_tree(postfix):
    """Realiza la gráfica"""
    try:
        tree = postfix_to_tree(postfix)
        
        G = tree_to_networkx(tree)
        
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        labels = nx.get_node_attributes(G, 'label')
        edge_labels = nx.get_edge_attributes(G, 'label')
        
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, 
                node_color='lightblue', font_size=12, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        plt.title(f"Árbol para: {postfix}")
        plt.show()
        
        return tree
    except Exception as e:
        print(f"Error visualizando el árbol: {e}")
        return None

def process_regex(filename):
    """Procesa la expresión regular"""
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line:  
                    try:
                        validate_regex(line)
                        postfix = shunting_yard(line)
                        print(f"Original: {line}")
                        print(f"Postfix: {postfix}")
                        plot_regex_tree(postfix)
                    except ValueError as e:
                        print(f"Expresión regular inválida: {e}")
                        return None
                    print("="*30)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

if __name__ == "__main__":
    filename = input("Nombre del archivo: ")
    process_regex(filename)