from collections import OrderedDict

class Node(OrderedDict):
    def __bool__(self):
        return True
    def get_data(self, bot):
        return {}
