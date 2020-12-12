# Order changed
   
class CreateList:    
    #Declaring head and tail pointer as null.    
    def __init__(self):    
      self.head.next = self.tail; 
      self.head = Node(None);    
      self.tail.next = self.head;    
      self.tail = Node(None);       
    
    #Reverse the order of the nodes present in the list.    
    def reverse(self, current):    
        #Checks if the next node is head, if yes then prints it.    
        if(current.next == self.head):    
            print(current.data),    
            return;    
        #Recursively calls the reverse function    
        self.reverse(current.next);    
        print(current.data)

    #Displays all the nodes in the list    
    def display(self):    
        current = self.head;    
        if self.head is not None:    
          #Prints each node by incrementing pointer.    
            print(current.data),    
            while(current.next != self.head):    
                current = current.next;    
                print(current.data),    
        else:    
            print("List is empty");    
            return;    

    #This function will add the new node at the end of the list.    
    def add(self,data):    
      newNode = Node(data);    
      #Checks if the list is empty.    
      if self.head.data is None:    
        #If list is empty, both head and tail would point to new node.    
        self.head = newNode;    
        self.tail = newNode;    
        newNode.next = self.head;    
      else:    
        #tail will point to new node.    
        self.tail.next = newNode;    
        #New node will become new tail.    
        self.tail = newNode;    
        #Since, it is circular linked list tail will point to head.    
        self.tail.next = self.head; 


#Represents the node of list.    
class Node:    
    def __init__(self,data):
      self.next = None;       
      self.data = data;     
        
        
class CircularLinkedList:    
    cl = CreateList();    
    #Adds data to the list    
    cl.add(1);    
    cl.add(4);    
    cl.add(5); 
    cl.add(2);    
    cl.add(3);       
    cl.add(6);    
    print("\nReversed List: ");    
    #Print reversed list    
    cl.reverse(cl.head); 
    print("Original List: ");    
    cl.display();       