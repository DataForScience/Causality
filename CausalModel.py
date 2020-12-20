### −∗− mode : python ; −∗−
# @file CausalModel.py
# @author Bruno Goncalves
######################################################

import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from itertools import combinations
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
        self.pos = None

        if filename is not None:
            self.load_model(filename)
        else:
            self.dag = nx.DiGraph()

        self.colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    def copy(self):
        G = CausalModel()
        G.dag = self.dag.copy()
        G.pos = dict(self.pos)
        G.colors = [color for color in self.colors]

        return G


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


    def save_model(self, path):
        """Save the causal model as a `dot` file.

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
        >>> G.add_causation('X', 'Y')
        >>> G.add_causation('Y', 'Z')
        >>> G.pos = {'X':(-1, 0), 'Y': (0, 0), 'Z': (1, 0)}
        >>> G.save_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.drawing.nx_pydot.write_dot`

        """
        G = self.dag.copy()

        if self.pos is not None:
            nodes = list(G.nodes())

            for node in nodes:
                G.nodes[node]['x'] = str(self.pos[node][0])
                G.nodes[node]['y'] = str(self.pos[node][1])

        nx.drawing.nx_pydot.write_dot(G, path)

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

    def children(self, source):
        """Obtain the children of a node.

        Children are the nodes at the other end of outgoing edges.

        Parameters
        ----------
        source : node in `G`
            The parent node

        Returns
        -------
        list()
            List of the children of `source` in `G`

        Examples
        --------
        >>> G.children('X')

        Notes
        -----
        The heavy lifting is done by `networkx.successors`

        """
        return list(self.dag.successors(source))

    def descendants(self, source):
        """Obtain the descendants of a node.

        Descendants are all the nodes reacheable through outgoing edges.

        Parameters
        ----------
        path : str or file
            Filename or file handle.

        Returns
        -------
        list()
            List of the descendants of `source` in `G`

        Examples
        --------
        >>> G = CausalModel()
        >>> G.load_model('temp.dot')

        Notes
        -----
        The heavy lifting is done by `networkx.descendants`

        """
        return list(nx.descendants(self.dag, source))

    def backdoor_paths(self, source, target):
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

        allPaths = self.all_paths(source, target)
        directed = self.directed_paths(source, target)

        return allPaths-directed


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


    def plot_path(self, path, edges=False, ax=None, conditional=False, lw=3):
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
        
        if edges:
            edgelist = path
        else:
            edgelist = {(path[i], path[i+1]) for i in range(len(path)-1)}

        edges = set(self.dag.edges()) - set(edgelist)
        
        nx.draw(self.dag, self.pos, node_color=self.colors[0], ax=ax, edgelist=[])
        nx.draw_networkx_labels(self.dag, self.pos, ax=ax)

        if conditional:
            nx.draw_networkx_edges(self.dag, self.pos,
                               edgelist=edgelist,
                               width=lw, edge_color=self.colors[1], ax=ax, style='dotted')
        else:
            nx.draw_networkx_edges(self.dag, self.pos,
                               edgelist=edgelist,
                               width=lw, edge_color=self.colors[1], ax=ax)

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
            ax = nx.draw(self.dag, pos, nodelist=nodes, node_color=node_colors)
        else:
            nx.draw(self.dag, pos, nodelist=nodes, node_color=node_colors, ax=ax)


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
        

    def v_structures(self):
        structs = set()

        degrees = dict(self.dag.in_degree())

        for node in degrees:
            if degrees[node] >= 2:
                for edge_i, edge_j in combinations(self.dag.in_edges(node), 2):
                    node_i = edge_i[0]
                    node_j = edge_j[0]
                    
                    if not (node_i, node_j) in self.dag.edges and not (node_j, node_i) in self.dag.edges:
                        structs.add(tuple(sorted([edge_i, edge_j])))

        return structs

    def equivalence_class(self):
        edges = list(self.dag.edges(data=True))

        equivalent = [[self.copy(), []]]

        structs = self.v_structures()

        for i, edge in enumerate(edges):
            new_edges = list(edges)

            new_edges[i] = (edge[1], edge[0], edge[2])

            G = CausalModel()
            G.dag.add_edges_from(new_edges)

            new_structs = CausalModel.v_structures(G)

            if new_structs == structs and len(list(nx.simple_cycles(G.dag)))==0:
                G.pos = dict(self.pos)
                G.colors = [color for color in self.colors]
                equivalent.append([G, new_edges[i][:2]])

        return equivalent


    def basis_set(self):
        nodes = set(self.dag.nodes())

        eqn = []

        for node in nodes:
            parents = set(self.parents(node))
            descendants = set(self.descendants(node))
            
            others = {n for n in nodes if n != node}
            others -= parents
            others -= descendants
            
            others = sorted(others)
            parents = sorted(parents)

            if len(others) > 0:
                if len(parents) > 0:
                    eqn.append('%s _||_ %s | %s' % (node, ", ".join(others), ', '.join(parents)))
                else:
                    eqn.append('%s _||_ %s' % (node, ", ".join(others)))

        return sorted(eqn)
            

    def intervention_graph(self, nodes, drop_nodes=False):
        G = self.copy()

        for node in nodes:
            G.dag.remove_edges_from(list(self.dag.in_edges(nodes)))

        if drop_nodes:
            degrees = dict(G.dag.degree())

            remove = []

            for node in degrees:
                if degrees[node] == 0:
                    remove.append(node)
                    del G.pos[node]

            G.dag.remove_nodes_from(remove)

        return G

    def conditional_intervention_graph(self, nodes, dependencies, drop_nodes=False):
        G = self.copy()

        for node in nodes:
            G.dag.remove_edges_from(list(self.dag.in_edges(nodes)))

        G.dag.add_edges_from(dependencies)

        if drop_nodes:
            degrees = dict(G.dag.degree())

            remove = []

            for node in degrees:
                if degrees[node] == 0:
                    remove.append(node)
                    del G.pos[node]

            G.dag.remove_nodes_from(remove)

        return G



if __name__ == "__main__":
    names = ['m331', 'moAh6a6', 'vcFQ']

    graph_id = 'temp'#names[2]

    G = CausalModel()#graph_id)
    G.load_model('dags/Primer.Fig.2.9.dot')

    Gx = G.intervention_graph('X')
    Gx2 = Gx.intervention_graph('Z3')
    print("ok")