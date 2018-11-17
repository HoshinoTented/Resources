#!/usr/bin/python3
# -*- coding: utf-8 -*-

import graphviz
import os

dot = graphviz.Graph()
nilCount = 0
drawCount = 0
green = "#00FF00"


def draw():
    global drawCount, root
    root.draw(root.parent)

    file = open(str(drawCount) + ".dot", "w")
    file.write(dot.source)
    file.close()
    os.system("./tree.sh " + str(drawCount))
    dot.clear()

    drawCount = drawCount + 1


class Tree:
    def __init__(self, v, w, p, l, r, color="#FFFFFF"):
        self.v = v
        self.w = w
        self.parent = p
        self.leftChild = l
        self.rightChild = r
        self.color = color

    def name(self):
        return str(self.v)

    def left_rotate(self):
        if type(self.parent) is Tree:
            if type(self.parent.parent) is Tree:
                if self.parent.parent.leftChild == self.parent:
                    self.parent.parent.leftChild = self
                else:
                    self.parent.parent.rightChild = self

            self.parent.rightChild = self.leftChild
            if type(self.leftChild) is Tree:
                self.leftChild.parent = self.parent
            self.leftChild = self.parent

            old_parent = self.parent
            self.parent = old_parent.parent
            old_parent.parent = self

    def right_rotate(self):
        if type(self.parent) is Tree:
            if type(self.parent.parent) is Tree:
                if self.parent.parent.leftChild == self.parent:
                    self.parent.parent.leftChild = self
                else:
                    self.parent.parent.rightChild = self
            
            self.parent.leftChild = self.rightChild
            if type(self.rightChild) is Tree:
                self.rightChild.parent = self.parent
            self.rightChild = self.parent

            old_parent = self.parent
            self.parent = old_parent.parent
            old_parent.parent = self

    def search(self, v):
        if self.v == v:
            return True, self
        else:
            if v < self.v and type(self.leftChild) is Tree:
                return self.leftChild.search(v)
            elif v > self.v and type(self.rightChild) is Tree:
                return self.rightChild.search(v)
            else:
                return False, self

    def add(self, v, w, default, color="#FFFFFF"):
        result, node = self.search(v)
        if not result:
            new_node = Tree(v, w, node, default, default, color)
            if v < node.v:
                node.leftChild = new_node
            else:
                node.rightChild = new_node
            new_node.update()

    def update(self):
        global root
        draw()

        while type(self.parent) is Tree and self.parent.w > self.w:
            if self.parent == root:
                root = self
            if self.parent.leftChild == self:
                self.right_rotate()
            else:
                self.left_rotate()
            draw()

    def draw(self, parent):
        name = self.name()
        if type(parent) is Tree:
            dot.edge(parent.name(), name)
        dot.node(name, "%s(%s)" % (name, str(self.w)), shape="circle", style="filled", fillcolor=self.color)
        if self.leftChild != self.rightChild:
            self.leftChild.draw(self)
            self.rightChild.draw(self)

        return name


class Nil(Tree):
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


def resetColor(_root):
    if type(_root) is Tree:
        _root.color = "#FFFFFF"
        resetColor(_root.leftChild)
        resetColor(_root.rightChild)


nilNode = Nil()

root = Tree(10, 15, nilNode, nilNode, nilNode)
root.add(5, 16, nilNode)
root.add(15, 21, nilNode)
root.add(12, 17, nilNode, green)
resetColor(root)

root.add(11, 12, nilNode, green)
