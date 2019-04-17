from matching.matchingdevice import MatchingDevice
import config

filenames = ["new_spanner.txt", "counter.txt", "pentagon.txt", "randomTetris.txt"]
filepaths = [config.GRAPHS_DIR + fn for fn in filenames]

mainWin = MatchingDevice(filepaths)
mainWin.begin()
