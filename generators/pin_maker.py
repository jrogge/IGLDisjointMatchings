import networkx as nx
import gutils

grid = nx.Graph()
margin = 100
tile_size = 50
num_blocks = 8

def get_index(x, y, size=(num_blocks + 1)):
    return x + y * size

for col in range(num_blocks + 1):
    for row in range(num_blocks + 1):
        print()
        idx = get_index(row, col)
        coord = [margin + row * tile_size, margin + col * tile_size]
        grid.add_node(idx, coord=coord)
        #print("adding node at pos (", row, ",", col, ")")
        #print("index:", idx)

for col in range(num_blocks+1):
    for row in range(num_blocks+1):
        idx = get_index(row, col)
        if (row > 0):
            idx_row_before = get_index(row - 1, col)
            print("adding left edge, indices:", idx, idx_row_before)
            grid.add_edge(idx, idx_row_before)
        if (row < num_blocks):
            idx_row_after = get_index(row + 1, col)
            print("adding right edge, indices:", idx, idx_row_after)
            grid.add_edge(idx, idx_row_after)
        if (col > 0):
            idx_col_before = get_index(row, col - 1)
            print("adding top edge, index:", idx, idx_col_before)
            grid.add_edge(idx, idx_col_before)
        if (col < num_blocks):
            idx_col_after = get_index(row, col + 1)
            print("adding bot edge, index:", idx, idx_col_after)
            grid.add_edge(idx, idx_col_after)

gutils.save_graph(grid, "pin8.ten")
