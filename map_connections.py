import pandas as pd
import os

from utility_functions import get_node_props

## Function to perform the search
def extract_hierarchy(mappings: pd.core.frame.DataFrame, start_nodes: list, pattern: str) -> tuple[pd.core.frame.DataFrame, dict]:
    
    """
    This function traverses a set of partially connected layers via a depth first search, tracking 
    the product of edge weights connecting the first and last node of each traversal. The search explores
    all nodes, edges and paths.

    Args:
        mappings (pandas dataframe): dataframe with two columns specifying set_id and member_id.
        start_nodes (list): list of nodes to start traversing the edge list
        pattern: whether to traverse top down or bottom up

    Returns:
        results_df: dataframe containing product of edge weights connecting first and last node on a tree_path
        hierarchy: dictionary logging current node and paths

    """
    
    if pattern not in node_types:
        raise ValueError("argument 'pattern' must have value 'top_down' or 'bottom_up'")
    
    if pattern == 'top_down':
        left_node = 'source_node'
        right_node = 'dest_node'
        start_layer = 0
    
    if pattern == 'bottom_up':
        left_node = 'dest_node'
        right_node = 'source_node'
        start_layer = max(mappings['layer']) + 1

    node_types = ['top_down', 'bottom_up']
 
    # Pandas df to store results
    results_df = pd.DataFrame()
    hierarchy = dict()
   
    for node in start_nodes:    
        
        nodes = [node]
        base_case = {'layer': start_layer,
                     'source_node': node,
                     'dest_node': node,
                     'edge_weight': 1.0,
                     'weight_product': 1.0,
                     'tree_path': node}    

        results = [base_case]

        while len(nodes) > 0:

            node = nodes.pop()
            edges = mappings[mappings[left_node]== node] 

            for i, e in edges.iterrows():

                weighting, layer, tree_path = get_node_props(e[left_node], results, kind = left_node) 

                if pattern == 'top_down':
                    result = {'layer': layer+1, 
                              'source_node': node, 
                              'dest_node': e[right_node], 
                              'edge_weight': e['edge_weight'],
                              'weight_product': e['edge_weight']*weighting,
                              'tree_path': tree_path + ' - ' + e[right_node]} 
                else:
                    result = {'layer': layer-1, 
                              'source_node': e[right_node],  
                              'dest_node': node, 
                              'edge_weight': e['edge_weight'],
                              'weight_product': e['edge_weight']*weighting,
                              'tree_path': tree_path + ' - ' + e[right_node]} 

                nodes.append(e[right_node]) 

                results.append(result)
                hierarchy[tree_path + ' - ' + e[right_node]] = tree_path 


            results_df_temp = pd.DataFrame(results)

        results_df = pd.concat([results_df, results_df_temp])

    results_df = results_df[results_df[left_node]!=results_df[right_node]]
    results_df.reset_index(inplace=True, drop=True)

    return results_df, hierarchy


## Load data
data_dir = 'data'
mappings = pd.read_csv(f'{data_dir}/edge_list.csv', dtype = {'layer': int, 
                                                             'source_node': object, 
                                                             'dest_node': object,
                                                             'edge_weight': float})

##  Extract nodes of first and last layer - these act as the seed nodes
root_nodes = list(mappings[mappings['layer']==1]['source_node'].unique())
leaf_nodes = list(mappings[mappings['layer']==max(mappings['layer'])]['dest_node'].unique())
leaf_nodes = sorted(leaf_nodes)

## Run hierarchy extraction
results_df, hierarchy = extract_hierarchy(mappings = mappings, start_nodes = root_nodes, pattern = 'top_down')
inverted_results_df, inverted_hierarchy = extract_hierarchy(mappings = mappings, start_nodes = leaf_nodes, pattern = 'bottom_up')

## Save results
results_df.to_csv(f'{data_dir}/mapped_connections.csv')
inverted_results_df.to_csv(f'{data_dir}/inverted_mapped_connections.csv')

