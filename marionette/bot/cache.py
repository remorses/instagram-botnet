
class Cache(dict):
    
    def merge(self, data):
        for key, value in data.items():
            if not self[key]:
                self[key] = value
            elif is_list(self.key, value):
                self.key = [*value, *self.key]
            elif is_dict(self.key, value):
                self.key = {**value, **self.key}                
    
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)
    
    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
  
def is_list(*args):
    return all([isinstance(x, list) for x in args])

def is_dict(*args):
    return all([isinstance(x, dict) for x in args])
