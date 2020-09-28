#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:33:48 2020

@author: kitchlm1
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from brian2 import * # fix this 
import os


class Network:
    def __init__(self, **kwargs):
        '''
        Create a new brain graph. This will create an empty graph unless
        a nx graph is passed in as a kwarg
        
        net = Network()
        
        or 
        
        net = Network(graph = nx.read_graphml('c_elegans_control.graphml'))
        
        Parameters
        ----------
        **kwargs : 
            graph:  networkx graph
            

        '''
        if 'graph' in kwargs:
            self.graph = kwargs['graph']
            
        else:
            self.graph = nx.DiGraph()
        self.original_graph = self.graph.copy()
        
    def add_nodes(self, node_list):
        """
        Add one or more new neurons to the network.
        
        Arguments:
            node_list (list of str): list of nodes to add.
        """
       
        self.graph.add_nodes_from(node_list)         
    
    def add_edges(self, edge_list):
        """
        Add one or more new edges to the network.
        Arguments:
            edge_list: list of tuples (presynaptic (str), postsynaptic (str))
        """
        
        self.graph.add_edges_from(edge_list)
        
    def add_weighted_edges(self, edge_list):
        """
        Add one of more new synapses to the network.
        Arguments:
            edge_list: list of tuples (presynaptic (str), postsynaptic (str), weight)
        """
        
        self.graph.add_weighted_edges_from(edge_list)

    def ablate(self, ablate_list):
        '''
        ablates one or more neurons from the brain graph

        Parameters
        ----------
        ablate_list : list of nodes (str) to remove from the graph

        Returns
        -------
        None.

        '''
        self.graph.remove_nodes_from(ablate_list)
        
    def reset(self):
        '''
        undo the ablations

        Returns
        -------
        None.

        '''
        
        self.graph = self.original_graph.copy()
        

########## util functions #############


def get_nodes_by_attribute(brain, attribute, attribute_value):
    '''
    Returns a list of nodes that have a specific value for a specific attribute

    Parameters
    ----------
    brain : Brain class
    attribute (str): attribute name
    attribute_value (str) : attribute value

    Returns
    -------
    attr_nodes : list of nodes that have the specific value for a specific attribute

    '''
    
    attr_nodes = []
    for neuron, all_attr in brain.graph.nodes(data = True):
        if attribute in all_attr:
            if all_attr[attribute] == attribute_value:
                    attr_nodes.append(neuron)
    return attr_nodes

def get_possible_attributes(brain):
    '''
    Returns the list of all possible attributes in the graph

    Parameters
    ----------
    brain : Brain class
    

    Returns
    -------
    att_type : list of attributes in the graph

    '''
    
    # get list of possible attributes
    att_type = []
    for node, all_attr in brain.graph.nodes(data = True):
        for spec_att in all_attr:
            if spec_att not in att_type:
                att_type.append(spec_att)
    return att_type

def get_attribute_values(brain, attribute):
    '''
    Returns the list of all possible values of a specific attribute in the graph

    Parameters
    ----------
    brain : Brain class
    attribute (str): attribute name 

    Returns
    -------
    att_values : list of all possible values of a specific attribute in the graph

    '''
    att_values = []
    for node, all_attr in brain.graph.nodes(data = True):
        if attribute in all_attr:
            if all_attr[attribute] not in att_values:
                att_values.append(all_attr[attribute])
    return att_values

###############Visualization functions############   
        
def view_brain_graph(brain):
    
    pos = nx.spring_layout(brain.graph,k=1.5)        # k controls the distance between the nodes and varies between 0 and 1
        # iterations is the number of times simulated annealing is run
        # default k =0.1 and iterations=50
    #bipartite, circular,planar,rescale,spring,spiral,spectrum
    plt.figure(figsize=(50,50)) 
    nx.draw(brain.graph, pos,font_size=12, width = 2.0)

def view_brain_graph_circular(brain):
    
    plt.figure(figsize=(50,50)) 
    nx.draw_circular(brain.graph, font_size=12, width = 2.0)

     
def view_ablated_brain_graph(brain):
    #VISUALIZING NODE ABLATION
    #Node color map that adds blue if node exists in control 
    #and perturbed connectome, and red if node exists 
    #in control but NOT perturbed
    node_color_map = []
    for nodes in list(brain.original_graph.nodes()):
        if nodes in brain.graph.nodes():
            node_color_map.append('blue')
        else:
            node_color_map.append('red')

    #Edge color map that adds blue if edge exists in control/perturbed connectome, and red if edge exists in control but NOT perturbed
    edge_color_map = []
    for edges in list(brain.original_graph.edges()):
        if edges in brain.graph.edges:
            edge_color_map.append('gray')
        else:
            edge_color_map.append('red')

    pos = nx.spring_layout(brain.original_graph,k=1.5)        # k controls the distance between the nodes and varies between 0 and 1
        # iterations is the number of times simulated annealing is run
        # default k =0.1 and iterations=50
    #bipartite, circular,planar,rescale,spring,spiral,spectrum
    plt.figure(figsize=(50,50)) 
    nx.draw(brain.original_graph, pos,font_size=12, edge_color = edge_color_map,with_labels=True, node_color = node_color_map, width = 2.0)

def view_ablated_brain_graph_circular(brain):
    #VISUALIZING NODE ABLATION
    #Node color map that adds blue if node exists in control 
    #and perturbed connectome, and red if node exists 
    #in control but NOT perturbed
    node_color_map = []
    for nodes in list(brain.original_graph.nodes()):
        if nodes in brain.graph.nodes():
            node_color_map.append('blue')
        else:
            node_color_map.append('red')

    #Edge color map that adds blue if edge exists in control/perturbed connectome, and red if edge exists in control but NOT perturbed
    edge_color_map = []
    for edges in list(brain.original_graph.edges()):
        if edges in brain.graph.edges:
            edge_color_map.append('gray')
        else:
            edge_color_map.append('red')

    plt.figure(figsize=(50,50)) 
    nx.draw_circular(brain.original_graph, font_size=12, edge_color = edge_color_map,with_labels=True, node_color = node_color_map, width = 2.0)

