from collections import defaultdict
from grid import rc2cell

""" Creates a graph representation of the board
Adapted from https://www.geeksforgeeks.org/graph-and-its-representations/ """
 
# A class to represent a graph. A graph is the list of the adjacency lists.
# Size of the array will be the no. of the vertices "V"
class Graph:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.V = self.grid_size ** 2
        #self.graph = [None] * self.V
        self.adj = [[] for i in range(self.V)]
 
    
    def DFSUtil(self, temp, v, visited):

        # Mark the current vertex as visited
        visited[v] = True

        # Store the vertex to the list
        temp.append(v)

        # Repeat for all vertices adjacent to this vertex
        for i in self.adj[v]:
            if visited[i] == False:
                temp = self.DFSUtil(temp, i, visited)

        return temp


    def connectedComponents(self):
        visited = [False for _ in range(self.V)]
        cc = []

        for v in range(self.V):
            if visited[v] == False:
                temp = []
                cc.append(self.DFSUtil(temp, v, visited))

        return cc



    def is_adjacent_(self, src, dst):
        """ Returns a boolean indicating whether src and dst are adjacent on the Sudoku board """
        
        cols = self.grid_size

        return (dst == src+1) or (dst == src-1) or (dst == src+cols) or (dst == src-cols)

    def add_component(self, nodes, sum_constraint):
        """ Specific to Killer Sudoku
        Function to create a connected component, with the sum constraint """

        if not isinstance(nodes, list):
            raise TypeError('Error - nodes should be defined as a list of grid cells')
        
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                src = nodes[i]
                dst = nodes[j]
                if self.is_adjacent_(src, dst):
                    self.add_edge(src, dst)

        pass


    # Function to add an edge in an undirected graph
    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)
 
    # Function to print the graph
    def print_graph(self):
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")


def get_graph(board, board_constraints):

    g = Graph(len(board))
    g_map = defaultdict(list)

    # Create a mapping of connected components based on the text input
    for row in range(len(board)):
        for col in range(len(board[row])):
            component = board[row][col]
            g_map[component].append(rc2cell(row,col))

    # Create the graph components
    for k,v in g_map.items():
        g.add_component(v, board_constraints[k])

    g.cc = g.connectedComponents()

    # Create the board constraints for each component in the same indexing as g.cc
    constraints = [0 for _ in range(len(g.cc))]
    for i in range(len(g.cc)):
        node = g.cc[i][0] # get any node for comparison
        for k,v in g_map.items():
            if node in v:
                constraints[i] = board_constraints[k]
                break

    g.constraints = constraints
    g.g_map = g_map
    return g

