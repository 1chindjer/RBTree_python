from enum import Enum


class Color(Enum):
    RED = 1
    BLACK = 2

# класс Нода
class Node:
    def __init__ (self, data):
        self.data = data
        self.left = self.right = self.parent = None
        self.color = Color.RED

# Сущность дерева
class Tree:
    def __init__ (self):
        self.root = None
    
    def __find(self, node, parent, value):
        if node is None:
            return None, parent, False
        
        if value == node.data:
            return node, parent, True
        if value < node.data:
            if node.left:
                return self.__find(node.left, node, value)
        if value > node.data:
            if node.right:
                return self.__find(node.right, node, value)
            
        return node, parent, False


    def append(self, value):
        new_node = Node(value)
        self.root = self._append(self.root, new_node)
        self.insert_fixup(new_node)
        self.root.color = Color.BLACK


    def _append(self, node, new_node):
        if node is None:
            return new_node

        if new_node.data < node.data:
            node.left = self._append(node.left, new_node)
            node.left.parent = node  
        elif new_node.data > node.data:
            node.right = self._append(node.right, new_node)
            node.right.parent = node  

        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotate_left(node)

        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)

        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        return node
    
    def is_red(self, node):
        if node is None:
            return False
        return node.color == Color.RED


    def show_tree(self, node):
        if node is None:
            return
        
        self.show_tree(node.left)
        print(node.data)
        self.show_tree(node.right)
# Удаляем лист
    def __del_leaf(self, s, p):
        if p.left ==s:
            p.left = None
        elif p.right ==s:
            p.right = None


    def __del_one_child(self, s, p):
        if p.left == s:
            if s.left is None:
                p.left = s.right
            elif s.right is None:
                p.left = s.left
        elif p.right == s:
            if s.left is None:
                p.right = s.right
            elif s.right is None:
                p.right = s.left

    def __find_min(self, node, parent):
        if node.left:
            return self.__find_min(node.left, node) 
        return node, parent
    
# удаление нода
    def del_node(self, key):
        s, p, fl_find = self.__find(self.root, None, key)
        if not fl_find:
            return None
        
        if s.left is None and s.right is None:
            self.__del_leaf( s, p )

        elif s.left is None or s.right is None:
            self.__del_one_child(s, p)
        else:
            sr, pr = self.__find_min(s.right, s)
            s.data = sr.data
            self.__del_one_child(sr, pr)

# Врещение и смена цвета
    def rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        right.color = node.color
        node.color = Color.RED
        return right

    def rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        left.color = node.color
        node.color = Color.RED
        return left

    def flip_colors(self, node):
        node.color = Color.RED
        node.left.color = Color.BLACK
        node.right.color = Color.BLACK

# Печатаем визуализацию в консоль
    def print_vertical_tree(self, node, indent=0, prefix=''):
        if node is not None:
            color_char = 'r' if node.color == Color.RED else 'b'
            if node.right:
                self.print_vertical_tree(node.right, indent + 1, '/ - - ')
            print('      ' * indent + prefix + str(node.data) + '(' + color_char + ')')
            if node.left:
                self.print_vertical_tree(node.left, indent + 1, '\\ - - ')


    def get_uncle(self, node):
        if node.parent is None or node.parent.parent is None:
            return None
        if node.parent == node.parent.parent.left:
            return node.parent.parent.right
        else:
            return node.parent.parent.left

    def insert_fixup(self, node):
        while node != self.root and node.parent is not None and node.parent.color == Color.RED:
            if node.parent.parent is None:  # если корень
                break
            if node.parent == node.parent.parent.left:  # если левый наследователь
                uncle = self.get_uncle(node)
                
                # Case 1: Красный
                if uncle and uncle.color == Color.RED:
                    node.parent.color = Color.BLACK  # Цвет родителя черный
                    uncle.color = Color.BLACK  
                    node.parent.parent.color = Color.RED  
                    node = node.parent.parent  
                    
                else: 
                    
                    # Case 2: 
                    if node == node.parent.right:
                        node = node.parent  # переход на родителя
                        self.rotate_left(node)
                        
                    # Case 3: Нод левый
                    node.parent.color = Color.BLACK  # цвет родителя черный
                    node.parent.parent.color = Color.RED 
                    self.rotate_right(node.parent.parent)
                    
            else:  
                uncle = self.get_uncle(node)
                
              
                if uncle and uncle.color == Color.RED:
                    node.parent.color = Color.BLACK  
                    uncle.color = Color.BLACK  
                    node.parent.parent.color = Color.RED  
                    node = node.parent.parent  
                    
                else: 
                    
                    # Case 2:
                    if node == node.parent.left:
                        node = node.parent  
                        self.rotate_right(node)
                        
                    # Case 3:
                    node.parent.color = Color.BLACK  
                    node.parent.parent.color = Color.RED  
                    self.rotate_left(node.parent.parent)

        self.root.color = Color.BLACK  # корень всегда черный





# задаем элементы
v = [5,3,7,6,1]

t = Tree()
for x in v:
    t.append(x)



# Выводим до удаления
t.print_vertical_tree(t.root)
print(' ')
# Удаляем элемент 5
t.del_node(5)
print(' ')
t.append(6)
# Выводим после удаления
t.print_vertical_tree(t.root)

