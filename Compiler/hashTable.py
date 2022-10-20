class Node:
    def __init__(self, value: tuple):
        self.data = value
        self.next = None

    def __str__(self):
        return str(self.data)

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, value: Node):
        if self.head is None:
            self.head = value
            self.tail = value

        else:
            self.tail.next = value
            self.tail = value

    def search(self, value):
        current = self.head

        while current is not None:
            if current.data[0] == value:
                return current

            current = current.next

        return None

    def __str__(self):
        if self.head is None:
            return ''

        res = ''

        current = self.head
        while current is not None:
            res += str(current) + ', '
            current = current.next

        return res[:-2]

class HashTable:
    def __init__(self, size=150):
        self.size = size
        self.current_index = 0
        self.data = [LinkedList() for _ in range(self.size)]

    def _hash(self, key):
        return sum(ord(c) for c in str(key)) % self.size

    def add(self, item):
        if item in self:
            # print(f'Item {item} is already here!')
            return

        index = self._hash(item)
        self.data[index].add(Node((item, self.current_index)))
        self.current_index += 1

    def __getitem__(self, key):
        index = self._hash(key)
        return self.data[index].search(key)

    def __contains__(self, key):
        index = self._hash(key)
        return True if self.data[index].search(key) is not None else False

    def __len__(self):
        return self.size

    def __str__(self):
        res = ''
        for item in self.data:
            linked_list_str = str(item)
            if len(linked_list_str) > 0:
                res += str(item) + ', '

        return res[:-2]


if __name__ == '__main__':
    ht = HashTable()
    ht.add('a')
    ht.add('lalal')
    ht.add(5)

    print(ht['a'])
    print(ht['lalal'])
    print(ht[5])

    print()

    print(5 in ht)
    print(27 in ht)
    print('lalal' in ht)

    print()

    ht.add(5)

    print()

    print(ht)