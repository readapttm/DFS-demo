import pandas as pd
import random
import os

## Build an edge list defined by
# Start_Node, End_Node, Edge_Weight

# Should embody graph structure with each root node having up to 5 generations (but could be fewer)
# Each node can inherit from multiple nodes

# Create 5 sets of N root nodes
# Assign a random subset of nodes in the next layer a random edgeweight
# Assemble data into a dataframe

set.seed(1)

# Set parameters
nodes_per_layer = 10
number_of_layers = 5
min_weight = 0
max_weight = 10

## Create node sets
node_sets = {(j+1): list(range(j*nodes_per_layer, (j+1)*nodes_per_layer)) for j in range(number_of_layers)}

## Function reate edge list
def generate_edge_list(nodes_per_layer: int, number_of_layers: int, min_weight: float, max_weight: float) -> pd.core.frame.DataFrame:

    """
        This function builds a network of connected layers, with a random set of connections and edge weights.
        Edge weights are defined by a uniform distribution between upper and lower limits (supplied as arguments).

    Args:
        nodes_per_layer (int): number of nodes per layer
        number_of_layers (int): number of layers
        min_weight (float): minimum edge weight
        max_weight (float): maximum edge weight

    Returns:
        pd.core.frame.DataFrame: contains all edges defined by layer, source, destination and edge weight
    
    """


    edge_list_df = pd.DataFrame()

    #j, i = 1, 5

    for j in range(1, number_of_layers):
        for i in range(nodes_per_layer):
            node = node_sets[j][i]
            
            possible_children = node_sets[j+1]
            k = random.randint(1, nodes_per_layer)
            edge_list = random.sample(possible_children, k)
            weights = [random.uniform(min_weight, max_weight) for i in range(k)]


            edge_list_df_temp = pd.DataFrame({'layer': j,
                                              'source_node': [node] * k,
                                              'dest_node': edge_list,
                                              'edge_weight': weights})
            

            edge_list_df = pd.concat([edge_list_df, edge_list_df_temp])
    
    edge_list_df.reset_index(inplace=True, drop=True)
    
    return edge_list_df


## Generate edge list
edge_list_df = generate_edge_list(nodes_per_layer, number_of_layers, min_weight, max_weight)

# Create saving directory if it doesn't exist already
output_dir = 'data'

if output_dir not in os.listdir():
    os.mkdir(output_dir)

## Save edge list
edge_list_df.to_csv(f'{output_dir}/edge_list.csv', index=False)