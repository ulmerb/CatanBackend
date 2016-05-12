from Location import *
from Board import *
import Player
import random

def test1():
  b = board()
  verts = []
  edges = []
  hexes = []
  for row in b.tiles:
    for hex in row:
      if hex is not None:
        vs = b.getTileToVertices(hex)
        es = b.getTileToEdges(hex)
        verts += vs
        edges += es
        hexes.append(hex)
  edges = set(edges)
  verts = set(verts)
  for row in b.vertices:
    arr = [str(v.x) + ',' + str(v.y) if v in verts else 'None' for v in row]
    print ' '.join(arr)
  print "----------------------------------------"
  for row in b.edges:
    arr = [str(v.x) + ',' + str(v.y) if v in edges else 'None' for v in row]
    print ' '.join(arr)
  print "----------------------------------------"
  for t in b.tiles:
    for tile in t:
      if tile is not None:
        arr = [str(v.x) + "," + str(v.y) for v in b.getTileToVertices(tile)]
        print tile.x, tile.y, "vertices: ", ' '.join(arr) 
  print "----------------------------------------"
  for t in b.tiles:
    for tile in t:
      if tile is not None:
        arr = [str(v.x) + "," + str(v.y) for v in b.getTileToTiles(tile)]
        print tile.x, tile.y, "tiles: ", ' '.join(arr)



def test2():
  b = board()
# test1()
test2()