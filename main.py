from graphmaker import GraphMaker
import gutils

filename = "counter.txt"
savefile = "badCounter.txt"

mainWin = GraphMaker()
mainWin.load_graph(filename)
mainWin.filename = savefile
mainWin.begin()
