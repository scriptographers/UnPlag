# Another approach, from GeeksForGeeks
import math 

# Linked list node 
class Node: 
    def __init__(self, data): 
        self.data = data 
        self.next = None

# function to get a new node 
def getNode(data): 
    
    # allocate memory for node 
    newNode = Node(data) 

    # put in the data 
    newNode.data = data 
    newNode.next = None
    return newNode 

# Function to reverse the 
# circular linked list 
def reverse(head_ref): 
    
    # if list is empty 
    if (head_ref == None): 
        return None

    # reverse procedure same as 
    # reversing a singly linked list 
    prev = None
    current = head_ref 
    
    next = current.next
    current.next = prev 
    prev = current 
    current = next
    while (current != head_ref): 
        next = current.next
        current.next = prev 
        prev = current 
        current = next

    # adjutsing the links so as to make the 
    # last node po to the first node 
    head_ref.next = prev 
    head_ref = prev 
    return head_ref 

# Function to print circular linked list 
def prList(head): 
    if (head == None): 
        return

    temp = head 
    
    print(temp.data, end = " ") 
    temp = temp.next
    while (temp != head): 
        print(temp.data, end = " ") 
        temp = temp.next

# Driver Code 
if __name__=='__main__': 
    
    # Create a circular linked list 
    # 1.2.3.4.1 
    head = getNode(1) 
    head.next = getNode(2) 
    head.next.next = getNode(3) 
    head.next.next.next = getNode(4) 
    head.next.next.next.next = head 

    print("Given circular linked list: ", 
                                end = "") 
    prList(head) 

    head = reverse(head) 

    print("\nReversed circular linked list: ", 
                                    end = "") 
    prList(head) 