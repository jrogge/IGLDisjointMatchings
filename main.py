from basic.graphmaker import GraphMaker
import gutils
import config

filename = "counter.txt"
filepath = config.GRAPHS_DIR + filename
savefile = "graphs/spanner.txt"

mainWin = GraphMaker()
#mainWin.load_graph(filepath)
mainWin.filename = savefile
mainWin.begin()
