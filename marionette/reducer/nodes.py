



class Node:
    
def username_from_id(id):
    pass

class User(Node):

    def __init__(self, **, id=None, username=None, data=None):
        self.data = data
        self._id = id
        self._username = username
                
     def username(self):
         if self._username:
             return self_username
         elif self._id:
             return username_from_id(self._id)
         elif self.data:
             return self.data['user']['username']  


class Media(