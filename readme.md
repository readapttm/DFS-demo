# Application of depth first search to partially connected layers

This repo provides a script to track the product of edge weights through a graph via depth first search.

To simplify matters, sample data is generated in the form of a series of layers containing a specified number of nodes. Each layer is partially connected to the next by means of a random subsample. 

This calculation may be useful when investigating the connectivity between layers that are not nearest neighbours but interact via intermediate connecting nodes.

# Scripts Provided

- generate_data.py - takes a set of parameters and uses these to generate an example network:
    nodes_per_layer: number of nodes in a layer (default value 10)
    number_of_layers: number of layers (default value 5)
    min_weight: minimum edge weight (default 0)
    max_weight maximum edge weight (default 10)

    Edge weights are sampled randomly from a uniform distribution between min_weight and max_weight

    The generated edge list is saved as a dataframe.

- map_connections.py

    Takes the edge list generated above and traverses it, tracking the product of edge weights connecting the first and last node of each traversal. Saves the result in a data frame.
    The graph can be traversed either from the first layer (top down) or last layer (bottom up)

NB. All code in this repository is provided for educational purposes only, with absolutely no warranty explicit, implied, or otherwise.
