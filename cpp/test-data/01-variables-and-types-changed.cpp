#include <iostream>
#include <vector> // Additional package included 
using namespace std;
/*
    Useless comment
    Useless comment
    Useless comment
    Useless comment
*/
// stores adjacency list items
struct myNode {
    long long int v, c;
    myNode* numberOfEdges;
};
// structure to store edges_array
struct myEdge {
    long long int startingVertex, endingVertex, w;
};
class MyGraph{
    // insert new nodes into adjacency list from given graph
    myNode* getMyNode(long long int v, long long int w, myNode* myH)   {
        myNode* myNewNode = new myNode;
        myNewNode->v = v;
        myNewNode->c = w;      
        myNewNode->numberOfEdges = myH;   // point new node to current myH
        return myNewNode;
    }
    long long int numberOfNodes;  // number of nodes in the graph
public:
    myNode **myH;                //adjacency list as array of pointers
    // Constructor
    MyGraph(myEdge edges_array[], long long int numberOfEdges, long long int numberOfNodes)  {
        // allocate new node
        myH = new myNode*[numberOfNodes]();
        this->numberOfNodes = numberOfNodes;
        // initialize myH pointer for all vertices
        for (long long int myI = 0; myI < numberOfNodes; ++myI)
            myH[myI] = nullptr;
        // construct directed graph by adding edges_array to it
        for (unsigned myI = 0; myI < numberOfEdges; myI++)  {
            long long int startingVertex = edges_array[myI].startingVertex;
            long long int endingVertex = edges_array[myI].endingVertex;
            long long int w = edges_array[myI].w;
            // insert in the beginning
            myNode* myNewNode = getMyNode(endingVertex, w, myH[startingVertex]);
             
                        // point myH pointer to new node
            myH[startingVertex] = myNewNode;
             }
    }
      // Destructor
     ~MyGraph() {
    for (long long int myI = 0; myI < numberOfNodes; myI++)
        delete[] myH[myI];
        delete[] myH;
     }
};
// print all adjacent vertices of given vertex
void tempFunc(myNode* ptr, long long int myI)
{
    while (ptr != nullptr) {
        cout << "(" << myI << ", " << ptr->v
            << ", " << ptr->c << ") ";
        ptr = ptr->numberOfEdges;
    }
    cout << endl;
}
// graph implementation
long long int main()
{
    // My Extra comment
    // graph edges_array array.
    myEdge edges_array[] = {
        // (x, y, w) -> edge from x to y with w w
        {3,2,2},{1,3,5},{0,2,3},{3,2,1},{2,4,4},{5,5,1}
    };
    long long int numberOfNodes = 7;      // Number of vertices in the graph
    // calculate number of edges_array
    long long int numberOfEdges = sizeof(edges_array)/sizeof(edges_array[0]);
    // construct graph
    MyGraph MyGraph(edges_array, numberOfEdges, numberOfNodes);
    // print adjacency list representation of graph
    cout << "This is my graph adjacency list" << endl << "(start, end, w):" << endl;
    for (long long int myI = 0; myI < numberOfNodes; myI++)
    {
        // display adjacent vertices of vertex myI
        tempFunc(MyGraph.myH[myI], myI);
    }
    return 0;
}