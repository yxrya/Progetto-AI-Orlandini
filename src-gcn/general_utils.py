import networkx as nx
import numpy as np
import gensim
from node2vec import Node2Vec
from pathlib import Path

"""
Funzionamento load e getID
model = load_model("embeddings/coraEmbedding_Dimension_4_lenWalk_10_NumWalk_10_P_0.1_Q_0.1.model")
result = get_nodeID_emb(3, model)     #devo inserire id del nodo
print(result)
"""

def minMaxNormalization(X, normalizationAxis=0):
    result = (X - np.min(X, axis=normalizationAxis)) / (
                np.max(X, axis=normalizationAxis) - np.min(X, axis=normalizationAxis))


def embedding(G, name, spaceDimension=32, lenWalk=20, Pparameter=1, Qparameter=0.1, n_walk=20):
    modelName = str(name) + "_" + str(spaceDimension) + "_" + str(lenWalk) + "_" + str(n_walk) + "_P_" + str(
        Pparameter) + "_Q_" + str(Qparameter) + ".model"
    modelFile = Path(modelName)

    if modelFile.is_file():
        model = gensim.models.Word2Vec.load(modelName)
        print("---- Model loaded")
    else:
        print("---- Random walks generation----")
        # Precompute probabilities and generate walks - **ON WINDOWS ONLY WORKS WITH workers=1**
        node2vec = Node2Vec(G, dimensions=spaceDimension, walk_length=lenWalk, p=Pparameter, q=Qparameter,
                            num_walks=n_walk, workers=1)
        # Embed
        model = node2vec.fit(window=10, min_count=1,
                             batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be passed, `dimensions` and `workers` are automatically passed (from the Node2Vec constructor)
        print("Embedding completed !")
        print("---- SAVING MODEL----")
        # Save model for later use
        model.save(modelName)

    return model


def readCoraGraph(nodesPath="data/cora/cora.content", edgesPath="data/cora/cora.cites"):
    edges = open(edgesPath, "r")
    G = nx.Graph()
    nodes = open(nodesPath, "r")
    orderedNodesList = []
    for n in nodes.readlines():
        nodeID = n.split("\t")[0]
        G.add_node(nodeID)
        orderedNodesList.append(nodeID)

    # print("INITIAL NODES ARE :"+ str(len(G.nodes())))
    for line in edges.readlines():
        fields = line.split("\t")
        # print("Link between: "+fields[0]+" and "+fields[1].replace("\n",""))
        G.add_edge(fields[0].replace("\t", ""), fields[1].replace("\n", ""))
    # print("Graph has "+str(len(G.nodes))+ " nodes")
    return G, orderedNodesList



def load_model(path_filename):
    '''
    Metodo per caricare il modello salvato con w2v
    '''
    model = gensim.models.Word2Vec.load(path_filename)
    return model.wv


def get_nodeID_emb(nodeID, model_wv):
    '''
    Metodo per ottenere embedding specifico ad un nodo.
    :nodeID string o int
    :model = model from load_model
    :data = ritorna list.
            len(data) = spaceDimension
    '''

    nodeID = str(nodeID)
    data = []

    try:
        data = model_wv[nodeID]
    except:
        print("NodeId not found. Return empty list")

    return data



