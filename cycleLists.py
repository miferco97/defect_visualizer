
class CycleIndexes():
    def __init__(self,max_index):
        self.max = max_index 
        self.internal_index = None
        self.last_function = None
    
    def lastStep(self):
        return self.last_function(self)

    def get(self):
        if self.internal_index is None:
            self.internal_index = 0
        return self.internal_index%self.max

    def next(self):
        self.last_function = CycleIndexes.next
        if self.internal_index is None:
            self.internal_index = -1
        self.internal_index += 1
        return self.internal_index%self.max

    def previous(self):
        self.last_function = CycleIndexes.previous
        if self.internal_index is None:
            self.internal_index = 1
        self.internal_index -=1
        return self.internal_index%self.max

    def setInternalIndex(self, value):
        self.internal_index = value
    
    def __len__(self):
        return self.max

    def reset(self):
        self.internal_index = None


class CycleList():
    def __init__(self,iterable):
        self.iterable = iterable
        self.len = len(iterable)
        self.internal_index = None
        self.last_function = None
    
    def lastStep(self):
        return self.last_function(self)
    
    def __getitem__(self,i):
        return self.iterable[i%self.len]

    def __len__(self):
        return self.len
        
    def get(self):
        if self.internal_index is None:
            self.internal_index = 0
        return self.__getitem__(self.internal_index)
        
    def next(self):
        self.last_function = CycleList.next
        if self.internal_index is None:
            self.internal_index = -1

        self.internal_index += 1
        return self.__getitem__(self.internal_index)
        
    def previous(self):
        self.last_function = CycleList.previous
        if self.internal_index is None:
            self.internal_index = 1
        
        self.internal_index -= 1
        return self.__getitem__(self.internal_index)
    
    def setInternalIndex(self, value):
        self.internal_index = value
    
    def reset(self):
        self.internal_index = None

if __name__ == "__main__":
    l  = CycleList(['hola','que tal','adios'])
    # for a in range(3*len(l)):
    #     print(l.next())
    
    for a in range(3*len(l)):
        print(l.previous())
        
    # l  = CycleIndexes(33)
    # for a in range(3*len(l)):
    #     print(l.previous())