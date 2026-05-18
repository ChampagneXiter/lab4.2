# ============================================================
# Python модуль: Циклический односвязный список
# ============================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CyclicList:
    def __init__(self):
        self.tail = None
        self.size = 0

    def add_to_head(self, value):
        """Добавление в начало"""
        new_node = Node(value)
        if self.tail is None:
            self.tail = new_node
            new_node.next = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
        self.size += 1
        return f"Added {value} to head"

    def add_to_tail(self, value):
        """Добавление в конец"""
        new_node = Node(value)
        if self.tail is None:
            self.tail = new_node
            new_node.next = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        return f"Added {value} to tail"

    def delete_head(self):
        """Удаление первого элемента"""
        if self.tail is None:
            raise ValueError("List is empty!")
        if self.size == 1:
            val = self.tail.data
            self.tail = None
        else:
            head = self.tail.next
            val = head.data
            self.tail.next = head.next
        self.size -= 1
        return f"Deleted head: {val}"

    def delete_by_value(self, value):
        """Удаление по значению"""
        if self.tail is None:
            raise ValueError("List is empty!")
        curr = self.tail.next
        prev = self.tail
        for _ in range(self.size):
            if curr.data == value:
                if self.size == 1:
                    self.tail = None
                elif curr == self.tail:
                    prev.next = curr.next
                    self.tail = prev
                else:
                    prev.next = curr.next
                self.size -= 1
                return f"Deleted: {value}"
            prev = curr
            curr = curr.next
        raise ValueError(f"Element {value} not found!")

    def search(self, value):
        """Поиск элемента"""
        if self.tail is None:
            raise ValueError("List is empty!")
        curr = self.tail.next
        for i in range(self.size):
            if curr.data == value:
                return f"Found {value} at position {i}"
            curr = curr.next
        raise ValueError(f"Element {value} not found!")

    def get_elements(self):
        """Получить все элементы списка"""
        if self.tail is None:
            return []
        elements = []
        curr = self.tail.next
        for _ in range(self.size):
            elements.append(curr.data)
            curr = curr.next
        return elements

    def clear(self):
        """Очистка списка"""
        self.tail = None
        self.size = 0
        return "List cleared"