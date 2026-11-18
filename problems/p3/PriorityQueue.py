def parent(index):
    return int((index - 1) / 2)

def left(index):
    return (2 * index) + 1

def right(index):
    return (2 * index) + 2

def swap(lis, i, ii):
    swap = lis[i]
    lis[i] = lis[ii]
    lis[ii] = swap
    return lis

class PriorityQueue:
    def __init__(self, data):
        self.list = []
        self.priority_list = []
        for item in data:
            self.push(item[0], item[1])

    def push(self, element, priority):
        self.list.append(element)
        self.priority_list.append(element)
        i = len(self.list) - 1
        while (i > 0 and self.priority_list[parent(i)] > self.priority_list[i]):
            self.list = swap(self.list, i, parent(i))
            self.priority_list = swap(self.priority_list, i, parent(i))
            i = parent(i)

    def pop(self):
        if len(self.list) == 0:
            return None

        result = self.list[0]
        self.list[0] = self.list[-1]
        self.priority_list[0] = self.priority_list[-1]
        del self.list[-1]
        del self.priority_list[-1]
        
        self.max_heapify(0)
        return result

    def max_heapify(self, start_index):
        smallest = start_index
        if left(start_index) < len(self.list) and self.priority_list[left(start_index)] < self.priority_list[smallest]:
            smallest = left(start_index)
        if right(start_index) < len(self.list) and self.priority_list[right(start_index)] < self.priority_list[smallest]:
            smallest = right(start_index)

        if smallest != start_index:
            self.list = swap(self.list, smallest, start_index)
            self.priority_list = swap(self.priority_list, smallest, start_index)
            self.max_heapify(smallest)

    def __len__(self):
        return len(self.list)
