# Variables changed, extra useless comments added
    
class myNode:    
    def __init__(self,value):    
      self.value = value;    
      self.myNext = None; 
      # Useless comment   
     
class myListCreator:    
    #Declaring myHead and myTail pointer as null.    
    def __init__(self):    
      self.myHead = myNode(None);    
      self.myTail = myNode(None);    
      self.myHead.myNext = self.myTail;    
      self.myTail.myNext = self.myHead;    
    
    # Useless comment
    #This function will attachToTheEnd the new node at the end of the list.    
    def attachToTheEnd(self,value): 
    # Useless comment   
      myNewNode = myNode(value);    
      #Checks if the list is empty.    
      if self.myHead.value is None:    
        #If list is empty, both myHead and myTail would point to new node.    
        self.myHead = myNewNode;    
        self.myTail = myNewNode;    
        myNewNode.myNext = self.myHead;    
      else:    
        #myTail will point to new node.    
        self.myTail.myNext = myNewNode;    
        #New node will become new myTail.    
        self.myTail = myNewNode;    
        #Since, it is circular linked list myTail will point to myHead.    
        self.myTail.myNext = self.myHead;    
     
    #Displays all the nodes in the list    
    def display(self):    
        current = self.myHead; 
        # Useless comment   
        if self.myHead is None:    
          print("List is empty");  
          # Useless comment  
          return;    
        else:    
            #Prints each node by incrementing pointer.    
            print(current.value),    
            while(current.myNext != self.myHead):  
            # Useless comment  
                current = current.myNext;    
                print(current.value),    
            
    #Reverse the order of the nodes present in the list.    
    def myListReverser(self, current):    
        #Checks if the myNext node is myHead, if yes then prints it.    
        if(current.myNext == self.myHead): 
        # Useless comment   
            print(current.value),    
            return;    
        #Recursively calls the myListReverser function    
        self.myListReverser(current.myNext);    
        # Useless comment
        print(current.value),    
         
class myCLL:    
    myNiceVariable = myListCreator();    
    #Adds value to the list    
    myNiceVariable.attachToTheEnd(1);    
    myNiceVariable.attachToTheEnd(2);    
    myNiceVariable.attachToTheEnd(3);  
    # Useless comment  # Useless comment
    # Useless comment
    myNiceVariable.attachToTheEnd(4);    
    myNiceVariable.attachToTheEnd(5);  
    # Useless comment  
    myNiceVariable.attachToTheEnd(6);    
    print("My Original List is the following: ");    
    myNiceVariable.display();    
    print("\nMy Reversed List is expressed as follows: ");    
    #Print reversed list    
    myNiceVariable.myListReverser(myNiceVariable.myHead);    