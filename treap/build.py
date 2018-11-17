#!/usr/bin/python3
# -*- coding: utf-8 -*-

import graphviz
import os

dot = graphviz.Graph()
nilCount = 0
green = "#00FF00"

def drawTo(name):
    file = open(name + ".dot", "w")
    file.write(dot.source)
    file.close()
    os.system("./tree.sh " + name)
    dot.clear()

class tree:
    def __init__(self, v, w, l, r, color = "#FFFFFF"):
        self.v = v
        self.w = w
        self.l = l
        self.r = r
        self.color = color

    def name(self):
        return str(self.v)

    def draw(self, parent):
        name = self.name()
        if type(parent) is tree:
            dot.edge(parent.name(), name)
        dot.node(name, "%s(%s)" % (name, str(self.w)), shape="circle", style="filled", fillcolor=self.color)
        lName = self.l.draw(self)
        rName = self.r.draw(self)

        return name
        
class nil(tree):
    def __init__(self):
        pass

    def name(self):
        return "NIL" + str(nilCount)
    
    def draw(self, parent):
        name = self.name()
        dot.edge(parent.name(), name, style="invis")
        dot.node(name, style="invis")
        global nilCount
        nilCount = nilCount + 1
        return name

nilNode = nil()

rl = tree(5, 12, nilNode, nilNode)
rr = tree(15, 21, nilNode, nilNode)
root = tree(10, 15, rl, rr)

root.draw(nilNode)
drawTo("0")

rr.l = tree(12, 17, nilNode, nilNode, green)
root.draw(nilNode)
drawTo("1")

root.r = rr.l
rr.l.r = rr
rr.l = nilNode
root.draw(nilNode)
drawTo("2")