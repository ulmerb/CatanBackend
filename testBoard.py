from Location import *
from Board import *
import Player
import random

def specPrint(listOfEdges):
  l = []
  for edge in listOfEdges:
    l.append(str(edge.x) + str(edge.y))
  return l

def test():
  b = board()
  verts = []
  edges = []
  hexes = []
  for row in b.tiles:
    for hex in row:
      if hex is not None:
        vs = b.getTileToVertices(hex)
        es = b.getTileToEdges(hex)
        es = specPrint(es)
        verts += vs
        edges += es
        hexes.append(hex)
  print len(set(edges))
  print len(set(verts))
test()