from matching.matchingdevice import MatchingDevice
import config

filename = "counter.txt"
filepath = config.GRAPHS_DIR + filename
max_edges = 27

mainWin = MatchingDevice(filepath, max_edges)
mainWin.begin()
