#Implement remote_insert, query, etc. 
#Implement simulation

# Find a node with a given ID
def find_node_with_ID(rootNode, id):
    if float(rootNode.rootID) == float(id) and len(rootNode.rootID) == len(id):
        return rootNode
    elif float(rootNode.rootID) < float(id) or float(rootNode.rootID) == float(id):
        #print(rootNode.rightChild.value)
        return find_node_with_ID(rootNode.rightChild, id)
    else: 
        #print(rootNode.leftChild.value)
        return find_node_with_ID(rootNode.leftChild, id)

# Insert a value at the given ID
def insert_at_ID(rootNode, id, value):
    if float(rootNode.rootID) == float(id) and len(rootNode.rootID) == len(id):
        rootNode.value.append(value)
        return rootNode
    else:
        #compare the next path item in the string
        root_id_len = len(rootNode.rootID)
        next_path_director = id[root_id_len]
        if next_path_director == "1":
            if rootNode.rightChild == None:
                rootNode.setRightChild(None)
            print(rootNode.rightChild.rootID)
            return insert_at_ID(rootNode.rightChild, id, value)
        else: 
            if rootNode.leftChild == None:
                rootNode.setLeftChild(None)
            return insert_at_ID(rootNode.leftChild, id, value)

# In order traverse the tree and return the document
def get_document(rootNode, document):
    if rootNode == None:
        return None
    
    get_document(rootNode.leftChild, document)
    document.append((rootNode.rootID, rootNode.value))
    get_document(rootNode.rightChild, document)
    return document

# unqique identifier tree
class client():
    def __init__(self, site_id):
        self.rootNode = uID_tree_node("0", None)
        self.site_id = site_id
        self.element_locations = []
        self.unshared_operations = []

    def local_insert(self, element, previous_id):
        #get the previous node
        previous_node = find_node_with_ID(self.rootNode, previous_id)
        #print(previous_node.value)
        #create new element
        safe_element = element + ":" + self.site_id
        #insert the new element as the right child
        inserted_id = previous_node.setRightChild(safe_element)
        self.element_locations.append(inserted_id)
        self.unshared_operations.append(("insert", inserted_id, safe_element))

    def remote_insert(self, remote_operations):
        for op in remote_operations:
            if op[0] == "insert":
                print(op[1])
                #print(self.rootNode.rootID)
                insert_at_ID(self.rootNode, op[1], op[2])

    @staticmethod
    def add_first_node(rootNode, value):
        if rootNode.leftChild == None:
            rootNode.setLeftChild(value)
        else: add_first_node(rootNode.leftChild, value)

class uID_tree_node():
    def __init__(self, rootID, value):
        self.rootID = rootID
        self.value = [value]
        self.site_counter = 0
        self.leftChild = None
        self.rightChild = None

    def setLeftChild(self, left_child_value):
        newID = self.rootID + "0"
        self.leftChild = uID_tree_node(newID, left_child_value)
        return newID

    def setRightChild(self, right_child_value):
        newID = self.rootID + "1"
        self.rightChild = uID_tree_node(newID, right_child_value)
        return newID

def main():
    # create truee
    r0 = client("site 1")
    r0.local_insert("A", "0")
    r0.local_insert("B", "01")

    print(r0.unshared_operations)
    #r0.local_insert("B", "011")

    r0.remote_insert([("insert", "0", "X")])

    #tree.rootNode.setRightChild("B")
    #tree.rootNode.rightChild.setLeftChild("C")

    #add_first_node(tree.rootNode, "F")

    #print(tree.rootNode == None)

    doc = get_document(r0.rootNode, [])
    print(doc)

main()




