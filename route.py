# -*- coding: utf-8 -*-

import node
import random
import utils.utils as utils


class Route:
    """ Class that represents the route data and its methods """

    def __init__(self, label="", nodes=None, deniedNodes=None):
        self.label = label
        # array of route nodes
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes
        # array of nodes that results on non terminal ending route 
        if deniedNodes is None:
            self.invalid = []
        else:
            self.invalid = deniedNodes
        # route length: used to rank routes
        self.length = self.evalRouteDistance()

    def __str__(self):
        return "Route object"

    def __repr__(self):
        return "<Route " + self.label + " >"

    # simply append a node to nodes list
    def addNode(self, newNode):
        if isinstance(newNode, node.Node):
            self.nodes.append(newNode)
        else:
            raise TypeError("The object " + str(type(newNode)) +
                            " is not of type " + str(type(node.Node())))

    # returns the route's last node
    def getLastNode(self):
        if len(self.nodes) != 0:
            return self.nodes[-1]

    # finds a node at this route's nodes list
    def getNodeByLabel(self, nodeLabel):
        for aNode in self.nodes:
            if nodeLabel == aNode.getLabel():
                return aNode

    # returns the lengh of nodes list
    def getNumberOfNodes(self):
        return len(self.nodes)

    def getLabel(self):
        return self.label

    def evalRouteDistance(self):
        cDistance = 0
        if len(self.nodes) != 0:
            lastNode = self.nodes[0]
            for aNode in self.nodes[1:]:
                cDistance += aNode.getDistanceOfNode(lastNode)
        return cDistance

    # remove the last node and returns it
    def removeLastNode(self):
        if len(self.nodes) != 0:
            return self.nodes.pop()

    # adds a node to invalid list
    def denyInvalidNode(self, invalidNode):
        self.invalid.append(invalidNode)

    # removes and invalidates last node
    def denyLastNode(self):
        invalidNode = self.removeLastNode()
        invalidNodeLabel = invalidNode.getLabel()
        self.denyInvalidNode(invalidNodeLabel)
        print ("Node " + invalidNode.getLabel() + " in invalid for route " + self.getLabel())

    # returns true if route is terminal ended
    def isTerminalEnded(self):
        lastNode = self.getLastNode()
        if lastNode in RouteGenerator.Terminals:
            return True
        return False

    def printRouteNodes(self):
        print ("Print route  " + self.label)
        for aNode in self.nodes:
            print (aNode.getLabel()),
        print ("")

    # returns a list of available nodes of last neighbor
    def getValidNeighbors(self):
        validNodes = []
        lastNode = self.getLastNode()
        neighborhood = lastNode.getNeighbors()
        for neighbor in neighborhood:
            neighborNode = self.getNodeByLabel(neighbor)
            # denys existing inner nodes and invalid ones, but adds a terminal neighbor
            if (((neighborNode is None) or (neighborNode in RouteGenerator.Terminals)) and (neighbor not in self.invalid)):
                validNodes.append(neighbor)
        return validNodes

class RouteGenerator:
    """ Static class used to create Route objects """

    MAX_NUMBER_OF_NODES = 15
    ONLY_TERMINAL_ENDING = True

    jsonString = utils.readNodesJsonFile()
    [Nodes, Terminals] = utils.parseJsonString(jsonString)
    del(jsonString)

    # static method that finds a node at data bank
    def findNodeByLabel(nodeLabel):
        allNodes = RouteGenerator.Nodes + RouteGenerator.Terminals # concatenates the 2 lists
        for aNode in allNodes:
            if aNode.getLabel() == nodeLabel:
                return aNode

    # adds a random neighbor to a given route. returns true if
    # succeeds and false otherwise
    def addRandomNeighborNode(aRoute):
        neighborList = aRoute.getValidNeighbors()
        if len(neighborList) != 0:
            # picks a random neighbor label from last node
            key = random.choice(neighborList)
            # finds node from database
            node = RouteGenerator.findNodeByLabel(key)
            aRoute.addNode(node)
            print ("Node " + node.getLabel() + " added to route " + aRoute.getLabel())
            return True
        else:
            # len(neighborList) == 0, no more valid neighbors
            print ("No valid neighbors.")
            return False

    # receives a route and returns true if a valid route is created
    def startRandomRouteFromTerminal(newRoute):
        numberOfNodes = newRoute.getNumberOfNodes()
        if (numberOfNodes == 0):
            # Inits route with random terminal
            randomTerminal = random.choice(RouteGenerator.Terminals)
            newRoute.addNode(randomTerminal)
            print ("Terminal " + randomTerminal.getLabel() + " added to route " + newRoute.getLabel())
        elif (numberOfNodes == RouteGenerator.MAX_NUMBER_OF_NODES):
            print ("Route " + newRoute.getLabel() + " ended max nodes")
            return False
        wasNodeAdded = RouteGenerator.addRandomNeighborNode(newRoute)
        if wasNodeAdded:
            if newRoute.isTerminalEnded():
                print ("Route " + newRoute.getLabel() + " ended with terminal " + newRoute.getLastNode().getLabel())
                return True
        else:
            if not RouteGenerator.ONLY_TERMINAL_ENDING:
                # allows inner node ending
                return True
            else:
                print ("Route " + newRoute.getLabel() + " has no valid end. Deleting " + newRoute.getLastNode().getLabel())
                newRoute.denyLastNode()
        return RouteGenerator.startRandomRouteFromTerminal(newRoute)

    # method that returns a valid route
    def getNewRoute(label=""):
        if (label == ""):
            label = "sample route"
        routeDone = False
        newRoute = None
        while not routeDone:
            if newRoute != None:
                print("An invalid route was created and abbandoned.")
                del(newRoute)
            newRoute = Route(label)
            routeDone = RouteGenerator.startRandomRouteFromTerminal(newRoute)
        print ("Route " + label + " is VALID.")
        return newRoute
