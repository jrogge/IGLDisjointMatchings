# IGLDisjointMatchings

Software built for the Spring 2019 IGL project *Pairs of Disjoint Matchings* under professor Anush Tserunyan at the University of Illinois at Urbana-Champaign

### Requires
 - Python 3.x (developed with version 3.6.5)
 - Networkx (developed with version 2.1)
 - Tkinter (comes with python but you may need to install XServer)

## Basic Editor
```
python main.py
```

Or, if you have both Python 2.x and Python 3.x installed:
```
python3 main.py
```

## Matchings Editor
Store graph files in the graphs directory, specify the ones to be loaded in the "filenames" list in `matchingEditor.py`. e.x.
```
filenames = ["spanner.txt", "pentagon.txt", "hexagon.txt", "counter.txt"]
```
Then run with
```
python matchingEditor.py
```
Once the editor has started, pink edges represent edges that can be added to the red matching. Selected edges are red. Once there are no more available edges (i.e. once the red matching is maximal) the program will switch over to the blue matching. Available edges are similarly light blue.

Press 'n' at any point while selecting the red matching to begin selecting the blue matching.

Press 'r' to reset the matchings.

Press 1 to load the 1st graph in "filenames", similarly for the other digits. At this time the program supports only 9 graphs
accessible via the keys 1..9

#### Coming Soon
 - tetris graphs(??)
