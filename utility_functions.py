## Function to extract source node properties whilst mapping connections through the graph
def get_node_props(node: str, results: list[dict], kind: str) -> tuple:
    
    """
    This function takes a destination node and a list of source node properties and extracts the 
    relevant source data

    Args:
        dest_node (str): the identifier of the current node
        results (list[dict]): list of potential source nodes through which to search
        kind (str): node type indicator, either "source_node" or "dest_node"

    Returns:
        tuple: source weight_product, layer and tree_path (extracted from source node dictionary)

    """

    node_types = ['source_node', 'dest_node']
 
    if kind not in node_types:
        raise ValueError("argument 'kind' must have value 'source_node' or 'dest_node'")
    
    node_types.remove(kind)
    
    for r in results:
        if r[node_types[0]] == node:
            return r['weight_product'], r['layer'], r['tree_path']
    
    # Return default if no value found
    return 1.0, 0, node