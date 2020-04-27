import string
import random

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
            return get_node_with_ID(rootNode.rightChild, id)
        else: 
            if rootNode.leftChild == None:
                rootNode.setLeftChild(None)
            return get_node_with_ID(rootNode.leftChild, id)

# returns the document in list format
def get_document(rootNode):
    doc = get_document_helper(rootNode, [])  
    doc = [i for i in doc if i != []] 
    temp_cleaned_doc = []
    for e in doc:
        temp_cleaned_doc.extend(e)
    cleaned_doc = []
    for elements in temp_cleaned_doc:
        cleaned_doc.append(elements.split(":site"))
    return cleaned_doc

# In order traverse the tree and return the document
def get_document_helper(rootNode, document):
    if rootNode == None:
        return None
    
    get_document_helper(rootNode.leftChild, document)
    #Remove None values from list
    elements = [i for i in rootNode.elements if i] 
    document.append(elements)
    #document.append((rootNode.elements, rootNode.rootID))
    get_document_helper(rootNode.rightChild, document)
    return document

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
            
        
# universal id tree nodes
class uID_tree_node():
    def __init__(self, element, rootID):
        self.rootID = rootID
        self.elements = [element]
        self.site_counter = 0
        self.leftChild = None
        self.rightChild = None

    # add the left_child_element to the left child of the node
    def setLeftChild(self, left_child_element):
        if self.leftChild == None:
            newID = self.rootID + "0"
            self.leftChild = uID_tree_node(left_child_element, newID)
            return newID
        else: 
            if self.leftChild.elements == [None]:
                self.leftChild.elements = [left_child_element]
            else:
                self.leftChild.elements.append(left_child_element)
            return self.leftChild.rootID

    # add the right_child_element to the right child of the node
    def setRightChild(self, right_child_element):
        if self.rightChild == None:
            newID = self.rootID + "1"
            self.rightChild = uID_tree_node(right_child_element, newID)
            return newID
        else: 
            if self.rightChild.elements == [None]:
                self.rightChild.elements = [right_child_element]
            else: 
                self.rightChild.elements.append(right_child_element)
            return self.rightChild.rootID

def main():
    
    # replicas r0, r1 which receive local state manipulations
    r0 = client("site 0")
    r1 = client("site 1")
    
    # Distributed system R comprised of r0, r1
    R = [r0, r1]

    #Start each client on the same document
    r0.local_insert("A", "0")
    r1.local_insert("A", "0")

    actions = []

    for i in range(100):
        # choose an actor
        actor_id = random.choice([0, 1])
        actor = R[actor_id]
        # choose an action, element and location 
        action = random.uniform(0, 1)
        if action < .8:
            # insert action
            element = random.choice(string.ascii_letters)
            # choose the id of the node to insert after
            if len(actor.element_mapping) == 0:
                id = "0"
            else:
                id = random.choice(actor.element_mapping)[1]
            # insert locally
            actor.local_insert(element, id)
        else: 
            # delete action
            if not len(actor.element_mapping) == 0:
                (element, id) = random.choice(actor.element_mapping)
                actor.local_delete(element, id)

        actions.append((actor.site_id, action, element, id)) # mark that we are adding this
        

        # 1/20th of the time we send local ushared actions to the other actor  
        # and check that actions are included correctly 
        if random.choice(list(range(20))) == 0:
            other_actor = R[1 - actor_id]
            local_unshared_actions = actor.unshared_operations
            other_actor.remote_operations(local_unshared_actions)
            actor.unshared_operations = []
            print("merged the actions of: " + actor.site_id + " into: " + other_actor.site_id)
        
    
    # share unshared actions one last time at the end 
    # and check that the states are equal!
    r0_unshared_actions = r0.unshared_operations
    r1_unshared_actions = r1.unshared_operations
    r0.remote_operations(r1_unshared_actions)
    r1.remote_operations(r0_unshared_actions)

    assert r0.compare(r1)
    print("simulation complete and replica states are equivalent")

main()




