#Implement remote_insert, query, etc. 
#Implement simulation

def add_first_node(rootNode, value):
    if rootNode.leftChild == None:
        rootNode.setLeftChild(value)
    else: add_first_node(rootNode.leftChild, value)

def getDocument(rootNode, document):
    if rootNode == None:
        return None
    
    getDocument(rootNode.leftChild, document)
    updatedDoc = document.append(rootNode.value)
    getDocument(rootNode.rightChild, document)
    return document

# unqique identifier tree
class client():
    def __init__(self, site_id):
        self.rootNode = uID_tree_node("0", "")
        self.site_id = site_id
        self.element_locations = []

    def local_insert(self, element, previous_id):
        previous_node = self.find_node_with_ID(self.rootNode, previous_id)
        previous_id.setRightChild(previous_id + "1", element + ":" + site_id)
        self.element_locations.append(previous_id + "1")

    @staticmethod
    def find_node_with_ID(rootNode, id): 
        if float(rootNode.rootID) == float(id) and rootNode.length == id.length:
            print(rootNode.rootID)
            print(rootNode.value)
            return rootNode
        elif float(root.rootID) < float(id) or float(rootNode.rootID) == float(id):
            return findNodeWithID(rootNode.leftChild, id)
        else: 
            return findNodeWithID(rootNode.rightChild, id)

class uID_tree_node():
    def __init__(self, rootID, value):
        self.rootID = rootID
        self.value = value
        self.site_counter = 0
        self.leftChild = None
        self.rightChild = None

    def setLeftChild(self, left_child_value):
        self.leftChild = uID_tree_node(self.rootID + "0", left_child_value)

    def setRightChild(self, right_child_value):
        self.rightChild = uID_tree_node(self.rootID + "1", right_child_value)

def main():
    # create truee
    r0 = client("site 1")
    r0.local_insert("A", "0")

    #tree.rootNode.setRightChild("B")
    #tree.rootNode.rightChild.setLeftChild("C")

    #add_first_node(tree.rootNode, "F")

    #print(tree.rootNode == None)

    doc = getDocument(tree.rootNode, [])
    print(doc)

main()




