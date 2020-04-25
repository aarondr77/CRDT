#Implement remote_insert, query, etc. 
#Implement simulation

# Return the node with the given ID
def get_node_with_ID(rootNode, id):
    if float(rootNode.rootID) == float(id) and len(rootNode.rootID) == len(id):
        return rootNode
    else:
        #compare the next path item in the string
        root_id_len = len(rootNode.rootID)
        next_path_director = id[root_id_len]
        if next_path_director == "1":
            if rootNode.rightChild == None:
                rootNode.setRightChild(None)
            print(rootNode.rightChild.rootID)
            return get_node_with_ID(rootNode.rightChild, id)
        else: 
            if rootNode.leftChild == None:
                rootNode.setLeftChild(None)
            return get_node_with_ID(rootNode.leftChild, id)

# In order traverse the tree and return the document
def get_document(rootNode, document):
    if rootNode == None:
        return None
    
    get_document(rootNode.leftChild, document)
    #Remove None values from list
    elements = [i for i in rootNode.value if i] 
    document.append(elements)
    #document.append((rootNode.rootID, rootNode.value))
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
        previous_node = get_node_with_ID(self.rootNode, previous_id)
        #create new element
        safe_element = element + ":" + self.site_id
        #insert the new element as the right child
        inserted_id = previous_node.setRightChild(safe_element)
        self.element_locations.append(inserted_id)
        self.unshared_operations.append(("insert", inserted_id, safe_element))

    def local_delete(self, element, id):
        node = get_node_with_ID(self.rootNode, id)
        print(node.value)
        node.value.remove(element)

    def remote_operations(self, remote_operations):
        for op in remote_operations:
            print(op)
            (operation, id, val) = op
            if operation == "insert":
                inserted_node = get_node_with_ID(self.rootNode, id)
                if id[len(id) - 1] == "1":
                    inserted_node.setRightChild(val)
                else:
                    inserted_node.setLeftChild(val)
                # Add id to element locations
                self.element_locations.append(id)
            if operation == "delete":
                self.local_delete(val, id)

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
        if self.leftChild == None:
            self.leftChild = uID_tree_node(newID, left_child_value)
        else: 
            self.leftChild.value.append(left_child_value)
        return newID

    def setRightChild(self, right_child_value):
        newID = self.rootID + "1"
        if self.rightChild == None:
            self.rightChild = uID_tree_node(newID, right_child_value)
        else: 
            self.rightChild.value.append(right_child_value)
        return newID

def main():
    # create truee
    r0 = client("site 1")
    r0.local_insert("A", "0")
    r0.local_insert("B", "0")

    #print(r0.unshared_operations)
    #r0.local_insert("B", "011")

    r0.remote_operations([("insert", "0", "X"), ("insert", "01111", "Y"), ("delete", "01", "A:site 1")])

    #tree.rootNode.setRightChild("B")
    #tree.rootNode.rightChild.setLeftChild("C")

    #add_first_node(tree.rootNode, "F")

    #print(tree.rootNode == None)

    doc = get_document(r0.rootNode, [])
    print(doc)

    #r0.local_delete("A:site 1", "01")
    #r0.remote_insert([("delete", "01", "A:site 1")])

    doc = get_document(r0.rootNode, [])
    print(doc)

main()




