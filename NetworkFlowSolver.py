import pandas as pd
import numpy as np
from scipy.optimize import minimize
import networkx as nx
import matplotlib.pyplot as plt

class NetworkFlowSolver:
    def __init__(self, adjacency_matrix, objective_function, constraints_list):
        self.adjacency_matrix = adjacency_matrix
        self.objective_function = objective_function
        self.constraints_list = constraints_list
        self.optimized_matrix = None
        self.graph = self._create_initial_network()

    def _create_initial_network(self):
        G = nx.from_numpy_array(self.adjacency_matrix, create_using=nx.DiGraph)
        return G

    def solve(self, method = 'SLSQP', options={'maxiter':10000}):
        initial_guess = np.random.rand(self.adjacency_matrix.size)
        result = minimize(self.objective_function, initial_guess, constraints=self.constraints_list, method=method, options=options)
        if result.success:
            self.optimized_matrix = result.x.reshape(self.adjacency_matrix.shape)
            return self.optimized_matrix
        else:
            raise Exception("Optimization failed: ", result.message)

    def visualize_initial_network(self, node_options={}, edge_color='black', figsize=(8, 6)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.graph)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx(self.graph, pos, edge_color=edge_color, **node_options)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

    def visualize_solution(self, node_options={}, edge_color='black', figsize=(8, 6)):
        if self.optimized_matrix is None:
            raise Exception("You must first solve the optimization problem")
        plt.figure(figsize=figsize)
        G = nx.from_numpy_array(self.optimized_matrix, create_using=nx.DiGraph)
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx(G, pos, edge_color=edge_color, **node_options)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()
