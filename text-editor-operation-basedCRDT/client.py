from uID_tree_node import uID_tree_node
from utils import get_node_with_ID, get_document

# Tree representation of each document
class client():
    def __init__(self, site_id):
        self.rootNode = uID_tree_node(None, "0")
        self.site_id = site_id
        self.element_mapping = []
        self.unshared_operations = []

    # inserts the element directly after the previous_id on the client
    def local_insert(self, element, previous_id):
        #get the previous node
        previous_node = get_node_with_ID(self.rootNode, previous_id)
        #create new element
        safe_element = element + ":" + self.site_id
        #insert the new element as the right child
        inserted_id = previous_node.setRightChild(safe_element)
        self.element_mapping.append((safe_element, inserted_id))
        self.unshared_operations.append(("insert", safe_element, inserted_id))

    # deletes the element from the node with id on the client 
    def local_delete(self, element, id):
        self.delete(element, id)        
        self.unshared_operations.append(("delete", element, id))

    # deletes the element in the given node
    def delete(self, element, id):
        node = get_node_with_ID(self.rootNode, id)
        if element in node.elements:
            node.elements.remove(element)
            self.element_mapping.remove((element, id))

    # execute received remote operations  
    def remote_operations(self, remote_operations):
        for op in remote_operations:
            (operation, element, id) = op
            if operation == "insert":
                node = get_node_with_ID(self.rootNode, id)
                if node.elements == [None]:
                    node.elements = [element]
                else:
                    node.elements.append(element)
                self.element_mapping.append((element, id))
            if operation == "delete":
                #print(get_document(self.rootNode))
                self.delete(element, id)

    # returns the elements of a given node
    def lookup(self, id):
        node = get_node_with_ID(self.rootNode, id)
        return node.elements
    
    # determines if two nodes are equivalent (same characters in same location)
    def compare(self, x):
        doc1_elements = self.element_mapping
        doc2_elements = x.element_mapping
        for element in doc1_elements:
            if element not in doc2_elements:
                print("not found in doc 2:")
                print(element)
                return False
        for element in doc2_elements:
            if element not in doc1_elements:
                print("not found in doc 1: ")
                print(element)
                return False
        return True