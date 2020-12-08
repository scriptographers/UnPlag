#include <iostream>
using namespace std;

struct adjNode {
    adjNode* next;
    int val, cost;
};

// print all adjacent vertices of given vertex
void display_AdjList(adjNode* ptr, int i){
    while (ptr != nullptr) {
        cout << "(" << i << ", " << ptr->val
            << ", " << ptr->cost << ") ";
        ptr = ptr->next;
    }
    cout << endl;
}

struct graphEdge {
    int end_ver, weight, start_ver;
};

class DiaGraph{
    // insert new nodes into adjacency list from given graph
    int N;  // number of nodes in the graph
    adjNode* getAdjListNode(int value, adjNode* head, int weight,)   {
        adjNode* newNode = new adjNode;
        newNode->cost = weight;
        newNode->next = head;   // point new node to current head
        newNode->val = value;
        return newNode;
    }

    public:
    adjNode **head;                //adjacency list as array of pointers
     // Destructor
     ~DiaGraph() {
     for (int i = 0; i < N; i++)
        delete[] head[i];
        delete[] head;
     }
    // Constructor
    DiaGraph(graphEdge edges[], int n, int N)  {
        this->N = N;
        // allocate new node
        head = new adjNode*[N]();
        // initialize head pointer for all vertices
        for (int i = 0; i < N; ++i)
            head[i] = nullptr;
        // construct directed graph by adding edges to it
        for (unsigned i = 0; i < n; i++)  {
            int start_ver = edges[i].start_ver;
            int end_ver = edges[i].end_ver;
            int weight = edges[i].weight;
            // insert in the beginning
            adjNode* newNode = getAdjListNode(end_ver, weight, head[start_ver]);
            head[start_ver] = newNode;
        }
    }
};

// graph implementation
int main(){
    cout<<"Graph adjacency list "<<endl<<"(start_vertex, end_vertex, weight):"<<endl;
    // graph edges array.
    int N = 6;
    graphEdge edges[] = {
        // (x, y, w) -> edge from x to y with weight w
        {0,1,2},{0,2,4},{1,4,3},{2,3,2},{3,1,4},{4,3,3}
    };      // Number of vertices in the graph
    // calculate number of edges
    int n = sizeof(edges)/sizeof(edges[0]);
    // construct graph
    DiaGraph diagraph(edges, n, N);
    // print adjacency list representation of graph
    for (int i = 0; i < N; i++)
        // display adjacent vertices of vertex i
        display_AdjList(diagraph.head[i], i);
    return 0;
}