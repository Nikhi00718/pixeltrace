// Included before the user's solution. Mirrors the LeetCode C++ environment.
#pragma once
#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

namespace pt_io {

const int NUL = INT_MIN;

inline ListNode* mkList(const vector<int>& v, int pos = -1) {
    ListNode dummy;
    ListNode* tail = &dummy;
    ListNode* cyc = nullptr;
    for (size_t i = 0; i < v.size(); i++) {
        tail->next = new ListNode(v[i]);
        tail = tail->next;
        if ((int)i == pos) cyc = tail;
    }
    if (cyc) tail->next = cyc;
    return dummy.next;
}

inline TreeNode* mkTree(const vector<int>& v) {
    if (v.empty() || v[0] == NUL) return nullptr;
    TreeNode* root = new TreeNode(v[0]);
    queue<TreeNode*> q;
    q.push(root);
    size_t i = 1;
    while (!q.empty() && i < v.size()) {
        TreeNode* n = q.front(); q.pop();
        if (i < v.size() && v[i] != NUL) { n->left = new TreeNode(v[i]); q.push(n->left); }
        i++;
        if (i < v.size() && v[i] != NUL) { n->right = new TreeNode(v[i]); q.push(n->right); }
        i++;
    }
    return root;
}

inline void pj(ostream& o, int v) { o << v; }
inline void pj(ostream& o, long v) { o << v; }
inline void pj(ostream& o, long long v) { o << v; }
inline void pj(ostream& o, unsigned v) { o << v; }
inline void pj(ostream& o, unsigned long v) { o << v; }
inline void pj(ostream& o, unsigned long long v) { o << v; }
inline void pj(ostream& o, bool v) { o << (v ? "true" : "false"); }
inline void pj(ostream& o, double v) {
    if (std::isnan(v) || std::isinf(v)) { o << "null"; return; }
    o << setprecision(12) << v;
}
inline void pj(ostream& o, const string& s) {
    o << '"';
    for (char c : s) {
        if (c == '"' || c == '\\') o << '\\' << c;
        else if (c == '\n') o << "\\n";
        else if ((unsigned char)c < 0x20) o << ' ';
        else o << c;
    }
    o << '"';
}
inline void pj(ostream& o, char c) { pj(o, string(1, c)); }
inline void pj(ostream& o, const char* s) { pj(o, string(s)); }

inline void pj(ostream& o, ListNode* h) {
    o << '[';
    int n = 0;
    for (ListNode* p = h; p && n < 10000; p = p->next, n++) {
        if (n) o << ',';
        o << p->val;
    }
    o << ']';
}

inline void pj(ostream& o, TreeNode* root) {
    vector<TreeNode*> order;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty() && order.size() < 20000) {
        TreeNode* n = q.front(); q.pop();
        order.push_back(n);
        if (n) { q.push(n->left); q.push(n->right); }
    }
    while (!order.empty() && order.back() == nullptr) order.pop_back();
    o << '[';
    for (size_t i = 0; i < order.size(); i++) {
        if (i) o << ',';
        if (order[i]) o << order[i]->val; else o << "null";
    }
    o << ']';
}

template <class A, class B> void pj(ostream& o, const pair<A, B>& p);
template <class T> void pj(ostream& o, const vector<T>& v);

template <class A, class B> void pj(ostream& o, const pair<A, B>& p) {
    o << '['; pj(o, p.first); o << ','; pj(o, p.second); o << ']';
}

template <class T> void pj(ostream& o, const vector<T>& v) {
    o << '[';
    for (size_t i = 0; i < v.size(); i++) {
        if (i) o << ',';
        pj(o, (T)v[i]);
    }
    o << ']';
}

template <class T> void emit(const T& v) {
    cout << flush;
    cout << "\n@@RESULT@@";
    pj(cout, v);
    cout << "\n" << flush;
}

}  // namespace pt_io
