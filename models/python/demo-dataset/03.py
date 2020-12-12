# Small changes in logic
   
class Node:    
    def __init__(self,data):
      self.next = None    
      self.data = data  

    def __str__(self):
      return self.data      
     
class CreateList:       
    def __init__(self):    
      self.head = Node(None)    
      self.tail = Node(None)    
      self.head.next = self.tail    
      self.tail.next = self.head    
            
    def add(self, data):    
      newNode = Node(data)    
      if not self.head.data:   
        self.tail = newNode     
        self.head = newNode       
        newNode.next = self.head    
      else:       
        self.tail.next = newNode       
        self.tail = newNode     
        self.tail.next = self.head    
   
    def display(self):    
        current = self.head    
        if self.head:       
            while(True):
                print(current.data)    
                current = current.next    
                if current.next == self.head:
                  break  
            
    def reverse(self, current):        
        if(current.next == self.head):    
            print(current.data),    
            return     
        self.reverse(current.next)    
        print(current.data)  

    def __str__(self):
      self.display()  
        
        
class CircularLinkedList:  

    # Create list:  
    cl = CreateList()   

    # Accept list:
    n = int(input("Enter n"))
    for _ in range(n):
      i = int(input("Enter element:"))
      cl.add(i)

    cl.display()       
    cl.reverse(cl.head)    