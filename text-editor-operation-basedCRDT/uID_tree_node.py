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