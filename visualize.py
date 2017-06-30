import nest
import types
import pydot
from functools import reduce

def plot_network(nodes, colors, filename, ext_conns=False,
                 plot_modelnames=False):
    """Plot the given nodes and the connections that originate from
    them.
    This function depends on the availability of the pydot module.
    Parameters
    ----------
    nodes : list
        Global ids of nodes to plot
    filename : str
        Filename to save the plot to. Can end either in .pdf or .png to
        determine the type of the output.
    ext_conns : bool, optional
        Draw connections to targets that are not in nodes. If it is True,
        these are drawn to a node named 'ext'.
    plot_modelnames : bool, optional
        Description
    Raises
    ------
    nest.NESTError
    """

    if len(nodes) == 0:
        nest.NESTError("nodes must at least contain one node")

    nodes_types = map(lambda x: type(x), nodes)
    nodes_types = list(nodes_types)
    homogeneous = reduce(
        lambda x, y: x == y and x or None, nodes_types) == nodes_types[0]

    if not homogeneous:
        raise nest.NESTError("nodes must either contain only integers \
            or only list of integers")

    def get_name(node):
        if plot_modelnames:
            return "%i\\n%s" % (node, nest.GetStatus([node], "model")[0])
        else:
            return "%i" % node

    graph = pydot.Dot(rankdir='LR', ranksep='5')

    def add_nodes(node_list, name, color):
        """
        We draw one Subgraph for each list we get. This allows us to
        influence the layout of the graph to a certain extent.
        """
        subgraph = pydot.Subgraph(name)
        for node in node_list:
            subgraph.add_node(pydot.Node(name=get_name(node), fillcolor=color, style="filled"))
        graph.add_subgraph(subgraph)

    if nodes_types[0] not in (tuple, list):
        nodes = [nodes]
        
    for i, node_list in enumerate(nodes):
        add_nodes(node_list, str(i), colors[i])

    # Flatten nodes
    nodes = [node for node_list in nodes for node in node_list]
    adjlist = [
        [j, nest.GetStatus(nest.GetConnections([j]), 'target')]
        for j in nodes
    ]

    for cl in adjlist:
        if not ext_conns:
            cl[1] = [i for i in cl[1] if i in nodes]
        else:
            tmp = []
            for i in cl[1]:
                if i in nodes:
                    tmp.append(i)
                else:
                    tmp.append("external")
            cl[1] = tmp
        for t in cl[1]:
            graph.add_edge(pydot.Edge(str(cl[0]), str(t)))

    filetype = filename.rsplit(".", 1)[1]

    if filetype == "pdf":
        graph.write_pdf(filename)
    elif filetype == "png":
        graph.write_png(filename)
    else:
        raise nest.NESTError("Filename must end in '.png' or '.pdf'.")