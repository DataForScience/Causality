### −∗− mode : python ; −∗−
# @file CausalModel.py
# @author Bruno Goncalves
######################################################

import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import re
import base64
import requests

import warnings
warnings.filterwarnings("ignore")

from tqdm import tqdm
tqdm.pandas()


plt.style.use('./d4sci.mplstyle')

class CausalModel(object):
    """Simple Causal Model Implementation
    
        Provides a way to represent causal DAGs
    """

    def __init__(self, filename=None):
        #self.daggity_coords = re.compile(r'@[0-9.]+,[0-9.]+\s*')
        self.pos = None

        if filename is not None:
            self.load_model(filename)
        else:
            self.dag = nx.DiGraph()

        self.colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


    # def _load_dagitty(self, graph_id):
    #     if graph_id[0] == 'm':
    #         graph_id = graph_id[1:]

    #     data = requests.get('http://dagitty.net/dags/load.php?id=%s' % graph_id)
    #     dag = base64.b64decode(data.text).decode('utf8')

    #     nodes, edges = dag.strip().split('\n\n')

    #     edges = edges.strip().split('\n')
    #     edges = [re.sub(self.daggity_coords, '', edge).strip() for edge in edges]

    #     self.dag = nx.parse_adjlist(edges, create_using=nx.DiGraph)
    #     self.pos = {}

    #     for node in nodes.split('\n'):
    #         node, node_type, layout = node.split()
    #         x, y = layout[1:].split(',')

    #         self.dag.add_node(node, type=node_type)
    #         self.pos[node] = (float(x), -float(y))

    def add_causation(self, source, target, label=None):
        """Add a causal link between source and target with an optional label.

        Parameters
        ----------
        source : node-like
            The source node

        target : node-like
            The target node

        label : string-like or None
            The label for the causal link

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.add_causation('X', 'Y')

        """
     
        if label is None:        
            self.dag.add_edge(source, target)
        else:
            self.dag.add_edge(source, target, label=label)        

    def load_model(self, path):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """

        G = nx.drawing.nx_pydot.read_dot(path)

        pos = {}

        for key, values in G.nodes(data=True):
            if 'x' not in values:
                pos = None
                break

            x = values['x']
            y = values['y']
            
            if x[0] == '"':
                x = x[1:-1]
            
            if y[0] == '"':
                y = y[1:-1]
                
            pos[key] = (float(x), float(y))

        self.dag = nx.DiGraph(G)
        self.pos = pos


    def save_model(self, filename):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        G = self.dag.copy()

        if self.pos is not None:
            nodes = list(G.nodes())

            for node in nodes:
                G.nodes[node]['x'] = str(self.pos[node][0])
                G.nodes[node]['y'] = str(self.pos[node][1])

        nx.drawing.nx_pydot.write_dot(G, filename)

    def layout(self):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        pos = graphviz_layout(self.dag, 'dot')

        keys = list(pos.keys())
        coords = np.array([pos[key] for key in keys])
        coords = nx.rescale_layout(coords, 1)
        pos = dict(zip(keys, coords))

        xs = []
        ys = []

        for key, value in pos.items():
            xs.append(value[0])
            ys.append(value[1])

        # All xx coordinates are the same, switch x and y
        # To make it horizontal instead of vertical
        if len(set(xs)) == 1:
            pos = {key: [-value[1], value[0]] for key, value in pos.items()}

        return pos

    def parents(self, node):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        return list(self.dag.predecessors(node))

    def ancestors(self, node):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        return list(nx.ancestors(self.dag, node))

    def children(self, node):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        return list(self.dag.successors(node))

    def descendents(self, node):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        return list(nx.descendants(self.dag, node))

    def directed_paths(self, source, target):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        return {tuple(path) for path in nx.all_simple_paths(self.dag, source, target)}

    def all_paths(self, source, target):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """
        return {tuple(path) for path in nx.all_simple_paths(self.dag.to_undirected(), source, target)}


    def all_paths_conditional(self, source, target, remove):
        """Initialize the CausalModel object by reading the information from the dot file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`

        """

        dag = self.dag.to_undirected()
        dag.remove_nodes_from(remove)

        return {tuple(path) for path in nx.all_simple_paths(dag, source, target)}




    def plot_path(self, path, ax=None):
        """Initialize the CausalModel object by reading the information from the dot
         file with the passed path.

        The file should be a `dot` file and if it contains multiple graphs, only the 
        first such graph is returned. All graphs _except_ the first are silently ignored.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        None

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.read_dot`


        """
        fig = None
        
        if ax == None:
            fig, ax = plt.subplots(1)
        
        edgelist = {(path[i], path[i+1]) for i in range(len(path)-1)}
        edges = set(self.dag.edges()) - set(edgelist)
        
        nx.draw(self.dag, self.pos, node_color=self.colors[0], ax=ax, edgelist=[])
        nx.draw_networkx_labels(self.dag, self.pos, ax=ax)
        nx.draw_networkx_edges(self.dag, self.pos,
                           edgelist=edgelist,
                           width=3, edge_color=self.colors[1], ax=ax)
        nx.draw_networkx_edges(self.dag, self.pos,
                           edgelist=edges,
                           width=1, ax=ax)
        if fig is not None:
            fig.tight_layout()


    def inputs(self):
        nodes = set()

        for node, deg in self.dag.in_degree():
            if deg == 0:
                nodes.add(node)

        return nodes

    def outputs(self):
        nodes = set()

        for node, deg in self.dag.out_degree():
            if deg == 0:
                nodes.add(node)

        return nodes

    def plot(self, output=None, pos=None, legend=False, ax=None, colors=False):
        if pos is None:
            if self.pos is None:
                self.pos = self.layout()
            
            pos = self.pos

        nodes = list(pos.keys())
        inputs = self.inputs()
        outputs = self.outputs()

        node_colors = []
        node_pos = []

        for node in nodes:
            node_pos.append(pos[node])

            if colors:
                if node in inputs:
                    node_colors.append(self.colors[2])
                elif node in outputs:
                    node_colors.append(self.colors[1])
                else:
                    node_colors.append(self.colors[0])
            else:
                node_colors.append(self.colors[0])

        node_pos = np.array(node_pos)

        if ax is None:
            ax = nx.draw(self.dag, pos, nodelist=nodes, node_color=node_colors)#, node_size=300)
        else:
            nx.draw(self.dag, pos, nodelist=nodes, node_color=node_colors, ax=ax)#, node_size=300) 


        labels = {(node_i, node_j) : label for node_i, node_j, label in self.dag.edges(data='label', default='')}

        nx.draw_networkx_labels(self.dag, pos, ax=ax)
        nx.draw_networkx_edge_labels(self.dag, pos, labels, ax=ax)

        if legend:
            node_types = ['Regular node', 'Input', 'Output']
            node_colors = [self.colors[0], self.colors[2], self.colors[1]]

            patches = [mpl.patches.Patch(color=node_colors[i], label=label) for i, label in enumerate(node_types)]

            plt.legend(handles=patches, fontsize=10)

        plt.gcf().tight_layout()

        if output is None:
            plt.show()
        else:
            plt.savefig(output, dpi=300)

        plt.close()

if __name__ == "__main__":
    names = ['m331', 'moAh6a6', 'vcFQ']

    graph_id = 'temp'#names[2]

    temp = CausalModel()#graph_id)
    temp.add_causation('X', 'Y', None)
    temp.add_causation('Y', 'Z', None)
    print("Inputs:", temp.inputs())
    print("Outputs:", temp.outputs())
    temp.plot(output=graph_id + '.png', legend=True)
