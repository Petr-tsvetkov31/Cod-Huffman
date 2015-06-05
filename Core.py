# -*- coding: utf-8 -*-
"""
Module for efficient coding Huffman method
"""

class Node(object):
    """
    Class that describes a tip of Huffman tree
    """

    def __init__(self, key, weight, leftChild=None, rightChild=None):
        self.key = key
        self.weight = weight
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.code = ''

    def __str__(self):
        if self.isLeaf():
            return '|({}:{})code: {} (leaf)|'.format(self.key, self.weight, self.code)
        else:
            return '|({}:{})code: {}|'.format(self.key, self.weight, self.code)

    def getKey(self):
        return self.key

    def getWeight(self):
        return self.weight

    def isLeaf(self):
        if self.leftChild == None and self.rightChild == None:
            return True
        return False

    def setCode(self, code=''):
        """
        Appointment Huffman code for each top
        according to the current tree
        """
        self.code = code
        if self.rightChild != None: self.rightChild.setCode(code + '0')
        if self.leftChild != None: self.leftChild.setCode(code + '1')
        if self.isLeaf() and self.code == '': self.code = '0'

    def show(self):
        if self.isLeaf():
            return str(self)
        else:
            return str(self) + self.leftChild.show() + '\n' + self.rightChild.show()

    def getDictLeafCode(self):
        """
        The method of obtaining the code for all the leaves of all the descendants of the top
        Formed the dictionary: symbol - code
        """

        def addDictLeafCode(self, tmpDict):
            if self.isLeaf():
                tmpDict[self.key] = self.code
            if self.rightChild != None: addDictLeafCode(self.rightChild, tmpDict)
            if self.leftChild != None: addDictLeafCode(self.leftChild, tmpDict)

        tmpDict = {}
        addDictLeafCode(self, tmpDict)
        return tmpDict


def HuffCode(inputStr):
    """
    Function receiving Huffman codes for all symbols ,
    found in the source string. Returns a dictionary of character codes
    and built Huffman tree(root)
    """
    # Creation first list of tops and determination of the alphabet
    listNode = []
    alphabet = list(set(inputStr))
    if alphabet:
        # Formation the dictionary:
        # symbol - number of occurrences symbol in source string
        dicWeight = {tmp: 0 for tmp in alphabet}
        for tmp in inputStr:
            dicWeight[tmp] += 1
        # Completing the list of tops the elements of the dictionary
        for key, value in dicWeight.items():
            listNode.append(Node(key, value))
        # Construction of tree on certain tops. Building from the leaves
        # to the top. At each iteration, selects two smallest element by
        # "weight" and removed from the dictionary and added to the tree. Сreates
        # A new element - the merger of remote and recorded in the list
        while len(listNode) > 1:
            # List sorted by "the weight of the elements"
            listNode.sort(key=lambda element: element.getWeight(), reverse=True)
            rch = listNode.pop()
            lch = listNode.pop()
            newNode = Node(lch.getKey() + rch.getKey(), lch.getWeight() + rch.getWeight(), lch, rch)
            listNode.append(newNode)
        # The final element - the root of the tree (containing the entire alphabet)
        root = listNode.pop()
        # Construction of a tree is over. Formation codes
        root.setCode()
    # If the string contains no characters - empty tree
    else:
        root = Node("", 0)
    dicCode = root.getDictLeafCode()
    return dicCode, root


def HuffStr(inputStr):
    """
    Encoding source string by Huffman code
    """
    tmpCode, tmpHuffTree = HuffCode(inputStr)
    return ''.join([tmpCode[x] for x in inputStr])


if __name__ == '__main__':
    # For test in console mode
    inputStr = str(input('please enter test:'))
    Code, HuffTree = HuffCode(inputStr)
    # print(HuffTree.show())
    print("{:|^19}".format(''))
    for key, value in Code.items():
        print("||{:<2} : {:<10}||".format(key, value))
    print("{:|^19}".format(''))
    print(HuffStr(inputStr))
