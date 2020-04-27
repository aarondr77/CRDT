#Implement query, compare
#Implement simulation

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

def get_document(rootNode):
    doc = get_document_helper(rootNode, [])
    return doc
    """
    doc = [i for i in doc if i != []] 
    temp_cleaned_doc = []
    for e in doc:
        temp_cleaned_doc.extend(e)
    cleaned_doc = []
    for e in temp_cleaned_doc:
        cleaned_doc.append(e.split(":site")[0])
    return cleaned_doc
    """

# In order traverse the tree and return the document
def get_document_helper(rootNode, document):
    if rootNode == None:
        return None
    
    get_document_helper(rootNode.leftChild, document)
    #Remove None values from list
    elements = [i for i in rootNode.elements if i] 
    #document.append(elements)
    document.append((rootNode.elements, rootNode.rootID))
    get_document_helper(rootNode.rightChild, document)
    return document

def compare(x, y):
    doc1 = get_document(x.rootNode)
    doc2 = get_document(y.rootNode)
    return doc1 == doc2

# unqique identifier tree
class client():
    def __init__(self, site_id):
        self.rootNode = uID_tree_node(None, "0")
        self.site_id = site_id
        self.element_mapping = []
        self.unshared_operations = []

    def local_insert(self, element, previous_id):
        #get the previous node
        previous_node = get_node_with_ID(self.rootNode, previous_id)
        #create new element
        safe_element = element + ":" + self.site_id
        #insert the new element as the right child
        inserted_id = previous_node.setRightChild(safe_element)
        self.element_mapping.append((safe_element, inserted_id))
        self.unshared_operations.append(("insert", safe_element, inserted_id))

    def local_delete(self, element, id):
        self.delete(element, id)        
        self.unshared_operations.append(("delete", element, id))

    def delete(self, element, id):
        node = get_node_with_ID(self.rootNode, id)
        node.elements.remove(element)
        self.element_mapping.remove((element, id))

    def remote_operations(self, remote_operations):
        for op in remote_operations:
            (operation, element, id) = op
            if operation == "insert":
                inserted_node = get_node_with_ID(self.rootNode, id[0: len(id) - 1])
                if id[len(id) - 1] == "1":
                    inserted_node.setRightChild(element)
                else:
                    inserted_node.setLeftChild(element)
                # Add id to element locations
                self.element_mapping.append((element, id))
            if operation == "delete":
                print(get_document(self.rootNode))
                self.delete(element, id)

class uID_tree_node():
    def __init__(self, element, rootID):
        self.rootID = rootID
        self.elements = [element]
        self.site_counter = 0
        self.leftChild = None
        self.rightChild = None

    def setLeftChild(self, left_child_element):
        if self.leftChild == None:
            newID = self.rootID + "0"
            self.leftChild = uID_tree_node(left_child_element, newID)
            return newID
        else: 
            self.leftChild.elements.append(left_child_element)
            return self.leftChild.rootID

    def setRightChild(self, right_child_element):
        newID = self.rootID + "1"
        if self.rightChild == None:
            self.rightChild = uID_tree_node(right_child_element, newID)
            return newID
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

    r0.unshared_operations = []
    r1.unshared_operations = []

    actions = []
    # I think the problem is deleting an element when there are other elements on the node. It deletes all
    # Lets check

    
    r0.local_insert("B", "01")
    unshared_actions = r0.unshared_operations
    print(unshared_actions)
    r1.remote_operations(unshared_actions)
    
    print(r0.element_mapping)
    print(r1.element_mapping)

    
    """
    for i in range(100):
        # choose an actor
        actor_id = random.choice([0, 1])
        actor = R[actor_id]
        # choose an action, element and location 
        action = random.uniform(0, 1)
        if action < .8:
            print("insert")
            element = random.choice(string.ascii_letters)
            if len(actor.element_mapping) == 0:
                id = "0"
            else:
                id = random.choice(actor.element_mapping)[1]
            actor.local_insert(element, id)
        else: 
            if not len(actor.element_mapping) == 0:
                (element, id) = random.choice(actor.element_mapping)
                print("delete: " + element + " @ id: " + id)
                actor.local_delete(element, id)

        actions.append((actor, action, element, id)) # mark that we are adding this
        

        # 1/20th of the time we send local ushared actions to the other actor  
        # and check that actions are included correctly 
        
        if random.choice(list(range(20))) == 0:
            other_actor = R[1 - actor_id]
            local_unshared_actions = actor.unshared_operations
            other_actor.remote_operations(local_unshared_actions)
            actor.unshared_actions = []
            print("operations are included in replica")
        
    
    # share unshared actions one last time at the end 
    # and check that the states are equal!
    print("AT THE END")
    r0_unshared_actions = r0.unshared_operations
    r1_unshared_actions = r1.unshared_operations
    r0.remote_operations(r1_unshared_actions)
    r1.remote_operations(r0_unshared_actions)
    assert get_document(r0.rootNode) == get_document(r1.rootNode)
    print("simulation complete and replica states are equivalent")

    """
    
main()




