
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