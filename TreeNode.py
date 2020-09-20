# Node Class
class TreeNode:
    
    classAtrr = "yoyoma" # static field (same for all instances of a class)

    def __init__(self, value):
        self._value = value
        self._right = None
        self._left = None


    def printNode(self):
        print(f'Value: {self._value}')
        print(f'Right: {self._right}')
        print(f'Left: {self._left}')
        print()


    def setRight(self, right):
        self._right = right

    def setLeft(self, left):
        self._left = left
        