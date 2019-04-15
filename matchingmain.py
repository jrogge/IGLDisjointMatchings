from matchingdevice import MatchingDevice
import gutils

filename = "counter.txt"

mainWin = MatchingDevice()
max_edges = 27
mainWin.load_graph(filename, max_edges)
mainWin.begin()
