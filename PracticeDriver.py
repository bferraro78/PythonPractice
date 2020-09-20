import os
import sys
from TreeNode import TreeNode


print('Sum of list Generator with global list:')
print()

arr = list()
arr.extend([1,2,3,4,5,6])

# Generator no list pass in
def sumGenerator():
    sum = 0
    for num in arr:
        sum += num
        yield sum


for generator in sumGenerator():
    print(generator)

print()
print('Sum of list Generator with passed in list:')
print()

# Generator list pass in
def sumGeneratorWithList(sumArr):
    sum = 0
    for num in sumArr:
        sum += num
        yield sum

secSum = sumGeneratorWithList(arr)

for generator in sumGeneratorWithList(arr):
    total = generator
    print(total)


print()
print('Fibonacci Generator:')
print()

# Fibonacci
def fib(fibNum):
    start, nextNum = 0, 1
    for num in range(fibNum):
        tempNumber = start + nextNum
        start = nextNum
        nextNum = tempNumber
        yield tempNumber

for generator in fib(12):
    print(generator)



# Creating an object from another file
print()
print('Import / Use class object:')
print()

node  = TreeNode(10)

print(f'{node.__class__.classAtrr}') # print a class attr (static field)
node.printNode() # To String

node.setLeft("Left Set String")
node.setRight(TreeNode(11))
node.printNode()


print()
print('Tree Practice Functions')
print()

# Build the tree structure
root = TreeNode(1)
root._left = TreeNode(2)
root._right = TreeNode(3)
root._left._left = TreeNode(4)
root._left._right = TreeNode(5)

def preOrderTraverse(root):
    if root != None:
        print(root._value)
    if root._left != None:
        preOrderTraverse(root._left)
    if root._right != None:
        preOrderTraverse(root._right)

print(f'PreOrder Traversal of Tree: ')
preOrderTraverse(root)
print()

def heightOfTree(root):
    if root == None:
        return 0
    elif root._left != None:
        return heightOfTree(root._left) + 1
    elif root._right != None:
        return heightOfTree(root._right) + 1
    else:
        return 0

height = heightOfTree(root)
print(f'Height: {height}')