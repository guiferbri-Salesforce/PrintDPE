import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
import sys, getopt

def defineNodePosition(rowposByMetadata, metadataElementsList):
    pos = {}
    for elem in metadataElementsList:
        elementList = metadata[elem]
        column = rowposByMetadata.get(elem)
        count = 1
        for item in elementList:
            label = item['name']
            pos[label] = (count, column)
            count += 1
    return pos

def defineNodeColors(colorByMetadata, metadataElementsList):
    itemsColor = {}
    for elem in metadataElementsList:
        elementList = metadata[elem]
        color = colorByMetadata.get(elem)
        count = 1
        for item in elementList:
            label = item['name']
            itemsColor[label] = color
    return itemsColor

def getNameLabelDict(metadataElements):
    global nameLabelDict
    global labelsByMetadata
    nameLabelDict = {}
    labelsByMetadata = {}
    for elem in metadataElements:
        elementList = metadata[elem]
        metadataLabels = []
        for item in elementList:
            label = item['label']
            nameLabelDict[item['name']] = label
            metadataLabels.append(label)
        labelsByMetadata[elem] = metadataLabels
    return nameLabelDict

def getFromToNodes(metadataElementsList):
    # Init dictionary
    fromToNodesDict = {
        'from' : [],
        'to' : []
    }
    fromNodes = fromToNodesDict['from']
    toNodes = fromToNodesDict['to']
    for metadataElem in metadataElementsList:
        elementList = metadata[metadataElem]
        for elem in elementList:
            if "primarySourceName" in elem:
                primarySourceName = elem['primarySourceName']
                secondarySourceName = elem['secondarySourceName']
                
                fromNodes.append(primarySourceName)
                fromNodes.append(secondarySourceName)
                toNodes.append(elem['name'])
            elif "sourceName" in elem:
                sourceName = elem['sourceName']
                fromNodes.append(sourceName)
            else:
                sourceName = elem['name']
                fromNodes.append(sourceName)
            toNodes.append(elem['name'])
    fromToNodesDict['from'] = fromNodes
    fromToNodesDict['to'] = toNodes
    return fromToNodesDict

def checkNodeElements(metadataElementsList):
    result = []
    for metadataElem in metadataElementsList:
        if metadataElem in metadata:
            result.append(metadataElem)
    return result

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print ('dpe.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('dpe.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    outputfile = inputfile.rsplit('.', 1)[0] + ' Graph.png'

    f = open(inputfile)
    data = json.load(f)
    global metadata
    metadata = data['Metadata']

    # Create dict with metadata info. Key:name, Value:label
    metadataElementsFull = ['datasources','joins','filters','writebacks','transforms','aggregates','parameters']
    metadataElements = checkNodeElements(metadataElementsFull)
    nameLabelDict = getNameLabelDict(metadataElements)

    ## Get From and To Nodes
    fromToNodesDict = getFromToNodes(metadataElements[1:-1])
    #print(fromToNodesDict)
    df = pd.DataFrame({ 'from': fromToNodesDict['from'], 'to': fromToNodesDict['to']})

    # Define Node Position
    rowposByMetadata = {
        'parameters' : 7,
        'datasources' : 6,
        'joins' : 5,
        'filters' : 4,
        'transforms' : 3,
        'aggregates' : 2,
        'writebacks' : 1
    }
    nodePosition = defineNodePosition(rowposByMetadata, metadataElements)
    #print(nodePosition)

    # Define Node Colors
    colorByMetadata = {
        'parameters' : '#F9C80E',
        'datasources' : '#F99719',
        'joins' : '#F86624',
        'filters' : '#EA3546',
        'transforms' : '#662E9B',
        'aggregates' : '#5575B4',
        'writebacks' : '#43BCCD'
    }
    nodeColor = defineNodeColors(colorByMetadata, metadataElements)
    #print(nodeColor)

    # Create Graph
    G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())
    circles = []
    colorsCircles = []
    for n in G.nodes:
        circles.append(n)
        colorsCircles.append(nodeColor[n])
    nodes = nx.draw_networkx_nodes(G, nodePosition, nodelist = circles, node_color=colorsCircles, node_size=3000, node_shape='o', edgecolors='black', alpha=0.5)

    # Define parameters nodes as hexagon
    fromToNodesDictParams = getFromToNodes(['parameters'])
    df_params = pd.DataFrame({ 'from': fromToNodesDictParams['from'], 'to': fromToNodesDictParams['to']})
    G_params=nx.from_pandas_edgelist(df_params, 'from', 'to', create_using=nx.DiGraph())
    hexagons = []
    colorsHexagon = []
    for n in G_params.nodes:
        hexagons.append(n)
        colorsHexagon.append(nodeColor[n])
    nodes = nx.draw_networkx_nodes(G_params, nodePosition, nodelist = hexagons, node_color=colorsHexagon, node_size=2500, node_shape='H', edgecolors='black', alpha=0.5)

    allLabels = {}
    for key in nameLabelDict.keys():
        label = nameLabelDict.get(key)
        allLabels[key] = label.replace(" ","\n")
    nx.draw_networkx_labels(G, nodePosition, allLabels, font_size=8)
    edges = nx.draw_networkx_edges(G, nodePosition, node_size=3000, arrowstyle='->', width=2, arrowsize=20)

    plt.tight_layout()
    plt.axis('off')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    # Show legend
    for metadataType in colorByMetadata.keys():
        color = colorByMetadata.get(metadataType)
        plt.scatter([],[], c=color, label='{}'.format(metadataType))
    plt.legend()
    # Save graph as image
    plt.savefig(outputfile, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
   main(sys.argv[1:])