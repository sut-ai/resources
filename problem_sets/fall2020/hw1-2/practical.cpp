// credits go to Mr. Masih Eskandar (masih.eskandar@gmail.com)
using namespace std;

#include <iostream>
#include <vector>
#include <cmath>
#include <limits>

class Node {
public:
    int n;
    int **state;
    double h;

    Node(int n) {
        this->n = n;
        state = new int *[n];
        for (int i = 0; i < n; ++i) {
            state[i] = new int[n];
        }
    }

    void set_h(double h) {
        this->h = h;
    }

    void set_element(int i, int j, int e) {
        state[i][j] = e;
    }
};


int compute_d(int i, int j, int n, int e, Node *node) {
    node->state[i][j] = e;
    int x_d, y_d;
    int ind = (e - 1) % n;
    int ind_y = (e - 1) / n;
    x_d = min((int) (abs(ind - j)), min(j + n - ind, n - j + ind));
    y_d = min((int) (abs(ind_y - i)), min(i + n - ind_y, n - i + ind_y));
    return x_d + y_d;
}

int compute_d_p(int i, int j, int n, int e) {
    int x_d, y_d;
    int ind = (e - 1) % n;
    int ind_y = (e - 1) / n;
    x_d = min((int) (abs(ind - j)), min(j + n - ind, n - j + ind));
    y_d = min((int) (abs(ind_y - i)), min(i + n - ind_y, n - i + ind_y));
    return x_d + y_d;
}


long long int g = 0;
double f;

double search(double bound, vector<Node *> *path);


bool is_same_node(Node *n1, Node *n2) {

    for (int i = 0; i < n1->n; ++i) {
        for (int j = 0; j < n1->n; ++j) {
            if (n1->state[i][j] != n2->state[i][j]) return false;
        }
    }
    return true;
}

void print_node(Node *node) {
    for (int i = 0; i < node->n; ++i) {
        for (int j = 0; j < node->n; ++j) {
            cout << node->state[i][j] << " ";
        }
        cout << endl;
    }
    cout << " h: " << node->h << endl;
}

void shift_up(int **state, int n, int k) {
    int temp = state[0][k];
    for (int i = 0; i < n - 1; ++i) 
        state[i][k] = state[i + 1][k];
    state[n - 1][k] = temp;
}

void shift_left(int **state, int n, int k) {
    int temp = state[k][0];
    for (int i = 0; i < n - 1; ++i) 
        state[k][i] = state[k][i + 1];
    state[k][n - 1] = temp;
}

void shift_right(int **state, int n, int k) {
    int temp = state[k][n - 1];
    for (int i = n - 1; i > 0; --i) 
        state[k][i] = state[k][i - 1];
    state[k][0] = temp;
}

void shift_down(int **state, int n, int k) {
    int temp = state[n - 1][k];
    for (int i = n - 1; i > 0; --i) 
        state[i][k] = state[i - 1][k];
    state[0][k] = temp;
}

double search_p(double bound, int **state, int n) {
    int sum = 0;
    //cout << "Entering state: " << endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            sum += compute_d_p(i, j, n, state[i][j]);
            //cout << state[i][j] << " ";
        }
        //cout << endl;
    }
    double h = (double) sum / (double) n;
    if (h <= 0.0001) {
        return -1;
    }
    double f = (double) g + h;
    if (f > bound) {
        return f;
    }
    double minim = numeric_limits<double>::max();
    for (int k = 0; k < n; ++k) {
        double t;
        //up
        shift_up(state, n, k);
        g += 1;
        t = search_p(bound, state, n);
        if (t == -1) return -1;
        g -= 1;
        if (t < minim) minim = t;
        shift_down(state, n, k);

        //down
        shift_down(state, n, k);
        g += 1;
        t = search_p(bound, state, n);
        if (t == -1) return -1;
        g -= 1;
        if (t < minim) minim = t;
        shift_up(state, n, k);

        //left
        shift_left(state, n, k);
        g += 1;
        t = search_p(bound, state, n);
        if (t == -1) return -1;
        g -= 1;
        if (t < minim) minim = t;
        shift_right(state, n, k);

        //right
        shift_right(state, n, k);
        g += 1;
        t = search_p(bound, state, n);
        if (t == -1) return -1;
        g -= 1;
        if (t < minim) minim = t;
        shift_left(state, n, k);

    }
    return minim;
}

void ida_star(Node root) {
    vector < Node * > path;
    double bound = root.h;
    while ((int) bound != -1) 
        bound = search_p(bound, root.state, root.n);
    cout << g;
}


double search(double bound, vector<Node *> *pathp) {
    Node *curr = pathp->back();
    f = g + curr->h;
    if (curr->h <= 0.0001) 
        return -1;
    

    if (f > bound) 
        return f;
    
    int num = curr->n;
    double minim = numeric_limits<double>::max();
    for (int i = 0; i < num; ++i) {
        Node up(num);
        Node down(num);
        Node left(num);
        Node right(num);
        int diff_up = 0;
        int diff_down = 0;
        int diff_left = 0;
        int diff_right = 0;
        for (int j = 0; j < num; ++j) {
            int **state = curr->state;
            diff_down += compute_d((j + 1) == num ? 0 : j + 1, i,
                                   num, state[j][i], &up);
            diff_up += compute_d((j - 1) == -1 ? num - 1 : j - 1,
                                 i, num, state[j][i], &down);
            diff_right += compute_d(i, (j + 1) == num ? 0 : j + 1,
                                    num, state[i][j], &right);
            diff_left += compute_d(i, (j - 1) == -1 ? num - 1 : j - 1,
                                   num, state[i][j], &left);
        }
        for (int k = 0; k < num; ++k) {
            if (k == i) continue;
            for (int j = 0; j < num; ++j) {
                diff_up += compute_d(j, k, num, curr->state[j][k], &up);
                diff_down += compute_d(j, k, num, curr->state[j][k], &down);
                diff_left += compute_d(k, j, num, curr->state[k][j], &left);
                diff_right += compute_d(k, j, num, curr->state[k][j], &right);
            }
        }
        up.set_h(((double) diff_up / (double) num));

        bool flag = true;

        if (flag) {
            pathp->push_back(&up);
            g += 1;
            double t = search(bound, pathp);
            if (t == -1) return -1;
            g -= 1;
            if (t < minim) minim = t;
            pathp->pop_back();
        }

        down.set_h(((double) diff_down / (double) num));
        if (flag) {
            pathp->push_back(&down);
            g += 1;
            double t = search(bound, pathp);
            if (t == -1) return -1;
            g -= 1;
            if (t < minim) minim = t;
            pathp->pop_back();
        }

        left.set_h(((double) diff_left / (double) num));
        if (flag) {
            pathp->push_back(&left);
            g += 1;
            double t = search(bound, pathp);
            if (t == -1) return -1;
            g -= 1;
            if (t < minim) minim = t;
            pathp->pop_back();
        }

        right.set_h(((double) diff_right / (double) num));
        if (flag) {
            pathp->push_back(&right);
            g += 1;
            double t = search(bound, pathp);
            if (t == -1) return -1;
            g -= 1;
            if (t < minim) minim = t;
            pathp->pop_back();
        }

    }
    return minim;

}

int main() {
    int n;
    cin >> n;
    int mat;
    Node root(n);
    int sum = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> mat;
            root.set_element(i, j, mat);
            sum += compute_d(i, j, n, mat, &root);
        }
    }
    root.set_h(((double) sum / (double) n));
    ida_star(root);
    return 0;
}