#Implement remote_insert, query, etc. 
#Implement simulation

def find_node_with_ID(rootNode, id):
    print("here") 
    if float(rootNode.rootID) == float(id) and len(rootNode.rootID) == len(id):
        return rootNode
    elif float(rootNode.rootID) < float(id) or float(rootNode.rootID) == float(id):
        print(rootNode.rightChild.value)
        return find_node_with_ID(rootNode.rightChild, id)
    else: 
        print(rootNode.leftChild.value)
        return find_node_with_ID(rootNode.leftChild, id)

def find_max_id_in_subtree(rootNode):
    if rootNode.rightChild == None:
        return rootNode
    else: 
        return find_max_id_in_subtree(rootNode.rightChild)

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
        print(previous_node.value)
        #create new element
        safe_element = element + ":" + self.site_id
        #insert the new element as the right child
        inserted_id = previous_node.setRightChild(safe_element)
        self.element_locations.append(inserted_id)
        self.unshared_operations.append(("insert", inserted_id, safe_element))

    def remote_insert(self, remote_operations):
        for op in remote_operations:
            if op[0] == "insert":
                self.insert_at_ID(self.rootNode, op[1], op[2])


    # Implement insert_at_ID for use in remote insert. 
    # The id added might already have a value in which case it should double up 
    # The id added might also be null, in which case we need to identify it and then apply it
    # if the operations are received out of order, then we need to recursivly make the nodes 
    # because we might need a node that is far down in the unbuilt territory
    @staticmethod 
    def insert_at_ID(rootNode, id, value):
        if float(rootNode.rootID) == float(id) and len(rootNode.rootID) == len(id):
            rootNode.value.append(value)
            return rootNode
        elif float(rootNode.rootID) < float(id) or float(rootNode.rootID) == float(id):
            if rootNode.leftChild == None:
                rootNode.setLeftChild(None)
            return insert_at_ID(rootNode.leftChild, id, value)
        else: 
            if rootNode.rightChild == None:
                rootNode.setRightChild(None)
            return insert_at_ID(rootNode.rightChild, id, value)

    @staticmethod
    def add_first_node(rootNode, value):
        if rootNode.leftChild == None:
            rootNode.setLeftChild(value)
        else: add_first_node(rootNode.leftChild, value)

def get_document(rootNode, document):
    if rootNode == None:
        return None
    
    get_document(rootNode.leftChild, document)
    document.append((rootNode.rootID, rootNode.value))
    get_document(rootNode.rightChild, document)
    return document

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

    #print(r0.unshared_operations)
    #r0.local_insert("B", "011")

    #r0.remote_insert([("insert", "100", "X"), ("insert", "101", "Y"), ("insert", "100000000", "Z")])

    #tree.rootNode.setRightChild("B")
    #tree.rootNode.rightChild.setLeftChild("C")

    #add_first_node(tree.rootNode, "F")

    #print(tree.rootNode == None)

    doc = get_document(r0.rootNode, [])
    print(doc)

main()




