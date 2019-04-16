import networkx as nx
from tkinter import *
import gutils
import states as st

class Tetris(object):
    '''Tetris graph generating tkinter window'''

    def __init__(self):

        #defaults
        self.graph = nx.Graph()
