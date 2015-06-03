# -*- coding: utf-8 -*-
"""
Модуль для эффиктивного кодирования символом методом Хаффмана
"""


class Node(object):
    """
    Класс, описывающий вершину дерева Хаффмана
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
        Назначение кода Хаффмана каждой вершине
        в соответствии с текущим деревомм
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
        Метод получения кода для всех листьев всех потомков вершины (кода символа)
        Формируется словарь: символ - код
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
    Функция получения кодов Хаффмана для всех символов,
    встречающихся в исходной строке. Возвращает словарь кодов символов
    и построенное дерево Хаффмана(корень)
    """
    # Создание первичного списка вершин и определение алфавита
    listNode = []
    alphabet = list(set(inputStr))
    if alphabet:
        # Формирование словаря: 
        # символ - кол-во вхождений символа в исходной строке
        dicWeight = {tmp: 0 for tmp in alphabet}
        for tmp in inputStr:
            dicWeight[tmp] += 1
        # Заполнение списка вершин элементами словаря
        for key, value in dicWeight.items():
            listNode.append(Node(key, value))
        # Построение дерева по определенным вершинам. Построение от листьев
        # к вершине. На каждой итерации выбираются два элемента с наименьшим
        # "весом", удаляются из словаря и добавляются в дерево. Создаается
        # новый элемент - слияние удаленных и записывается в список
        while len(listNode) > 1:
            # Список сортируется по "весу элементов"
            listNode.sort(key=lambda element: element.getWeight(), reverse=True)
            rch = listNode.pop()
            lch = listNode.pop()
            newNode = Node(lch.getKey() + rch.getKey(), lch.getWeight() + rch.getWeight(), lch, rch)
            listNode.append(newNode)
        # Последний элемент - корень дерева (содержит весь алфавит)
        root = listNode.pop()
        # Построение дерева закончено. Формирование кодов
        root.setCode()
    # Если строка не содержит символов - пустое дерево
    else:
        root = Node("", 0)
    dicCode = root.getDictLeafCode()
    return dicCode, root


def HuffStr(inputStr):
    """Кодирование исходной строки кодами Хаффмана"""
    tmpCode, tmpHuffTree = HuffCode(inputStr)
    return ''.join([tmpCode[x] for x in inputStr])


if __name__ == '__main__':
    # Консольный тест модуля
    inputStr = str(input('please enter test:'))
    Code, HuffTree = HuffCode(inputStr)
    print(HuffTree.show())
    print("{:|^19}".format(''))
    for key, value in Code.items():
        print("||{:<2} : {:<10}||".format(key, value))
    print("{:|^19}".format(''))
    print(HuffStr(inputStr))
