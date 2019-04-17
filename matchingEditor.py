from matching.matchingdevice import MatchingDevice
import config

filenames = ["spanner.txt", "pentagon.txt", "hexagon.txt", "counter.txt"]
filepaths = [config.GRAPHS_DIR + fn for fn in filenames]

mainWin = MatchingDevice(filepaths)
mainWin.begin()
