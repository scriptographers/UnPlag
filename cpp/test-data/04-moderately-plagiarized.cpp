#include <iostream>
using namespace std;

struct adjNode {
    int val, cost;
    adjNode* next;
};

struct graphEdge {
    int start_ver, end_ver, weight;
};

void display(adjNode* ptr, int i){
    for (; ptr != NULL; ptr = ptr->next)
        cout << i << ", " << ptr->val << ", " << ptr->cost;
    cout << "\n";
    return;
}

struct DiaGraph{

    int N;
    adjNode **head; 

    // Constructor
    DiaGraph(graphEdge edges[], int n, int N)  {

        head = new adjNode*[N]();
        this->N = N;

        for (int i = 0; i < N; i++)
            head[i] = NULL;

        for (int i = 0; i < n; i++){
            adjNode* newNode = getAdjListNode(edges[i].end_ver, edges[i].weight, head[edges[i].start_ver]);
            head[edges[i].start_ver] = newNode;
        }
    }

    adjNode* getAdjListNode(int value, int weight, adjNode* head){
        adjNode* newNode = new adjNode;
        newNode->val = value;
        newNode->cost = weight;
        newNode->next = head;
        return newNode;
    }

    ~DiaGraph(){
        for (int i = 0; i < N; i++)
            delete[] head[i];
        delete[] head;
    }
};

int main(){
    int N; cin >> N;
    int n; cin >> n;
    graphEdge edges[n][3];
    for (int i=0 ; i<n; i++)
        cin >> edges[i][0] >> edges[i][1] >> edges[i][2];
    DiaGraph diagraph(edges, n, N);
    return 0;
}