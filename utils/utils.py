# -*- coding: utf-8 -*-

import json
import node
import csv

def readNodesJsonFile():
    """ read data/nodes.json file from this project """
    fileName = "data/nodes.json"
    with open(fileName, "r") as f:
        jsonString = f.read()
        return jsonString


def parseJsonString(jsonString):
    """ creates nodes list from jsonString """
    nodes = []
    terminals = []
    jsonStruct = json.loads(jsonString)
    for jsonNode in jsonStruct['network']['nodes']:
        nodes.append(node.Node(jsonNode['id'],
                               jsonNode['label'],
                               jsonNode['neighbors'],
                               jsonNode['distance'],
                               jsonNode['latlong'],
                               jsonNode['neighbors_latlong']))

    for jsonNode in jsonStruct['network']['terminals']:
        terminals.append(node.Node(jsonNode['id'],
                                   jsonNode['label'],
                                   jsonNode['neighbors'],
                                   jsonNode['distance'],
                                   jsonNode['latlong'],
                                   jsonNode['neighbors_latlong']))
    return [nodes, terminals]

def print_GTFS (generation):
    
    jsonStr = readNodesJsonFile()
    [Nodes, Terminals] = parseJsonString(jsonStr)
    allNodes = Terminals + Nodes
    print_gtfs_stops_file(generation, allNodes)
    print_gtfs_shapes_file(generation, allNodes)
       
# create a file stops.txt (save bus stops and its infos)
# must have points_ID, points_lat, points_lon at least
def print_gtfs_stops_file(generation, allNodes):
    stops = open("data/stops.txt","w")
    stops.write("stop_id,\"stop_name\",\"stop_desc\",stop_lat,stop_lon,stop_url,location_type,parent_station\n")
    for a_node in allNodes:
        id, name, latlon = a_node.getIdx(), a_node.getLabel(), a_node.getLatLong()
        prtname = "\"%s\"" % name
        string = (str(id)+","+prtname+","+","+str(latlon[0])+","+str(latlon[1])+","+","+","+"\n")
        stops.writelines(string)
    stops.close()

# create a file shapes.txt (save bus lines and its infos)
# must have points_ID, points_lat, points_lon at least
def print_gtfs_shapes_file(generation, allNodes):
    routeIndex = 0
    shapes = open('data/shapes.txt', 'w')
    shapes.write("shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled\n")
    for individual in generation:
        routeList = individual.getGenes()
        for rt in routeList:
            nodeList = rt.getNodes()
            routeIndex+=1
            nodeSeq, distAcc = 0, 0
            last_node=""
            for i, a_node in enumerate(nodeList):
                # first node doesn't need distance
                if (i != 0):
                    distAcc+= last_node.getDistanceOfNode(a_node)
                    # last node doesn't have neighbor ahead
                    if ( i < len(nodeList) ):
                        nll = last_node.getNeighborsLatLong(a_node) #neighbor_latlon_list
                        for j in range (0, len(nll), 2):
                            nodeSeq+=1
                            string=(str(routeIndex)+","+str(nll[j])+","+str(nll[j+1])+","+str(nodeSeq)+","+"\n")
                            shapes.writelines(string)
                latlon = a_node.getLatLong()
                nodeSeq+=1
                string=(str(routeIndex)+","+str(latlon[0])+","+str(latlon[1])+","+str(nodeSeq)+","+str(distAcc)+"\n")
                last_node = a_node
                shapes.writelines(string)
    shapes.close()
    

# method that reads OD info from .csv file
def parseCsvODFile():
    od_matrix = "data/matriz_od_fake.csv"
    with open(od_matrix, 'rb') as csvfile:
        filereader = csv.reader(csvfile)
        destinations = filereader.next()
        demandMatrix = []
        for row in filereader:
            origin = row[0]
            tam = len(row)
            for i in range(1, tam):
                dest = row[i]
                if dest != "" and dest != "EOT" and dest != "0":
                    demandMatrix.append([int(origin), int(destinations[i]),
                                         int(dest)])
        return demandMatrix
