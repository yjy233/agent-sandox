// Data-structure helpers for the exercise judge (C++17).
#pragma once
#include "json.hpp"
#include <algorithm>
#include <map>
#include <queue>
#include <set>
#include <utility>

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(v), left(l), right(r) {}
};

struct Node {
    int val;
    Node* left;
    Node* right;
    Node* next;
    Node(int v = 0, Node* l = nullptr, Node* r = nullptr, Node* n = nullptr)
        : val(v), left(l), right(r), next(n) {}
};

struct GNode {
    int val;
    std::vector<GNode*> neighbors;
    GNode(int v = 0) : val(v) {}
};

struct RNode {
    int val;
    RNode* next;
    RNode* random;
    RNode(int v = 0) : val(v), next(nullptr), random(nullptr) {}
};

inline std::vector<int> jsonToInts(const Json& j) {
    std::vector<int> out;
    for (const auto& v : j.as_array()) out.push_back((int)v.as_long());
    return out;
}
inline std::vector<std::vector<int>> jsonToIntss(const Json& j) {
    std::vector<std::vector<int>> out;
    for (const auto& v : j.as_array()) out.push_back(jsonToInts(v));
    return out;
}
inline std::vector<std::string> jsonToStrings(const Json& j) {
    std::vector<std::string> out;
    for (const auto& v : j.as_array()) out.push_back(v.as_string());
    return out;
}
inline std::vector<std::vector<std::string>> jsonToStringss(const Json& j) {
    std::vector<std::vector<std::string>> out;
    for (const auto& v : j.as_array()) out.push_back(jsonToStrings(v));
    return out;
}
inline Json intsToJson(const std::vector<int>& v) {
    std::vector<Json> out;
    for (int x : v) out.push_back(Json::mk_num(x));
    return Json::mk_arr(out);
}
inline Json intssToJson(const std::vector<std::vector<int>>& v) {
    std::vector<Json> out;
    for (const auto& x : v) out.push_back(intsToJson(x));
    return Json::mk_arr(out);
}
inline Json stringsToJson(const std::vector<std::string>& v) {
    std::vector<Json> out;
    for (const auto& x : v) out.push_back(Json::mk_str(x));
    return Json::mk_arr(out);
}
inline Json stringssToJson(const std::vector<std::vector<std::string>>& v) {
    std::vector<Json> out;
    for (const auto& x : v) out.push_back(stringsToJson(x));
    return Json::mk_arr(out);
}

inline ListNode* buildList(const std::vector<int>& vals) {
    ListNode dummy;
    ListNode* cur = &dummy;
    for (int v : vals) {
        cur->next = new ListNode(v);
        cur = cur->next;
    }
    return dummy.next;
}
inline Json listToJson(ListNode* head) {
    std::vector<Json> out;
    while (head) {
        out.push_back(Json::mk_num(head->val));
        head = head->next;
    }
    return Json::mk_arr(out);
}

inline TreeNode* buildTree(const std::vector<Json>& vals) {
    if (vals.empty() || vals[0].is_null()) return nullptr;
    TreeNode* root = new TreeNode((int)vals[0].as_long());
    std::queue<TreeNode*> q;
    q.push(root);
    size_t i = 1;
    while (!q.empty() && i < vals.size()) {
        TreeNode* n = q.front();
        q.pop();
        if (i < vals.size()) {
            const Json& v = vals[i++];
            if (!v.is_null()) {
                n->left = new TreeNode((int)v.as_long());
                q.push(n->left);
            }
        }
        if (i < vals.size()) {
            const Json& v = vals[i++];
            if (!v.is_null()) {
                n->right = new TreeNode((int)v.as_long());
                q.push(n->right);
            }
        }
    }
    return root;
}
inline Json treeToJson(TreeNode* root) {
    if (!root) return Json::mk_arr({});
    std::vector<Json> out;
    std::queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* n = q.front();
        q.pop();
        if (!n) {
            out.push_back(Json::mk_null());
            continue;
        }
        out.push_back(Json::mk_num(n->val));
        q.push(n->left);
        q.push(n->right);
    }
    while (!out.empty() && out.back().is_null()) out.pop_back();
    return Json::mk_arr(out);
}
inline Json treesToJson(const std::vector<TreeNode*>& roots) {
    std::vector<Json> out;
    for (auto r : roots) out.push_back(treeToJson(r));
    return Json::mk_arr(out);
}

inline Node* buildNextTree(const std::vector<Json>& vals) {
    if (vals.empty() || vals[0].is_null()) return nullptr;
    Node* root = new Node((int)vals[0].as_long());
    std::queue<Node*> q;
    q.push(root);
    size_t i = 1;
    while (!q.empty() && i < vals.size()) {
        Node* n = q.front();
        q.pop();
        if (i < vals.size()) {
            const Json& v = vals[i++];
            if (!v.is_null()) {
                n->left = new Node((int)v.as_long());
                q.push(n->left);
            }
        }
        if (i < vals.size()) {
            const Json& v = vals[i++];
            if (!v.is_null()) {
                n->right = new Node((int)v.as_long());
                q.push(n->right);
            }
        }
    }
    return root;
}
inline Json nextLevelsJson(Node* root) {
    if (!root) return Json::mk_arr({});
    std::vector<Json> out;
    Node* leftmost = root;
    while (leftmost) {
        std::vector<Json> level;
        for (Node* n = leftmost; n; n = n->next) level.push_back(Json::mk_num(n->val));
        out.push_back(Json::mk_arr(level));
        Node* nxt = nullptr;
        for (Node* n = leftmost; n; n = n->next) {
            if (n->left) { nxt = n->left; break; }
            if (n->right) { nxt = n->right; break; }
        }
        leftmost = nxt;
    }
    return Json::mk_arr(out);
}

inline std::vector<ListNode*> buildLists(const std::vector<std::vector<int>>& arrs) {
    std::vector<ListNode*> out;
    for (const auto& a : arrs) out.push_back(buildList(a));
    return out;
}

inline ListNode* buildCycleList(const std::vector<int>& vals, int pos, std::vector<ListNode*>& nodes) {
    for (int v : vals) nodes.push_back(new ListNode(v));
    for (size_t i = 0; i + 1 < nodes.size(); i++) nodes[i]->next = nodes[i + 1];
    if (!nodes.empty() && pos >= 0 && pos < (int)nodes.size()) nodes.back()->next = nodes[pos];
    return nodes.empty() ? nullptr : nodes[0];
}
inline int cycleIndex(ListNode* ret, const std::vector<ListNode*>& nodes) {
    for (size_t i = 0; i < nodes.size(); i++)
        if (nodes[i] == ret) return (int)i;
    return -1;
}

inline std::pair<ListNode*, ListNode*> buildIntersect(const std::vector<int>& a,
                                                      const std::vector<int>& b,
                                                      int skipA, int skipB) {
    if (skipA >= (int)a.size() || skipB >= (int)b.size())
        return {buildList(a), buildList(b)};
    ListNode* common = buildList(std::vector<int>(a.begin() + skipA, a.end()));
    ListNode* ha = buildList(std::vector<int>(a.begin(), a.begin() + skipA));
    ListNode* hb = buildList(std::vector<int>(b.begin(), b.begin() + skipB));
    if (!ha) ha = common;
    else {
        ListNode* t = ha;
        while (t->next) t = t->next;
        t->next = common;
    }
    if (!hb) hb = common;
    else {
        ListNode* t = hb;
        while (t->next) t = t->next;
        t->next = common;
    }
    return {ha, hb};
}
inline Json valOrNullJson(ListNode* n) {
    return n ? Json::mk_num(n->val) : Json::mk_null();
}

inline RNode* buildRandomList(const std::vector<std::vector<int>>& rows) {
    if (rows.empty()) return nullptr;
    std::vector<RNode*> nodes;
    for (const auto& r : rows) nodes.push_back(new RNode(r[0]));
    for (size_t i = 0; i < rows.size(); i++) {
        if (rows[i][1] >= 0) nodes[i]->next = nodes[rows[i][1]];
        if (rows[i][2] >= 0) nodes[i]->random = nodes[rows[i][2]];
    }
    return nodes[0];
}
inline Json dumpRandomListJson(RNode* head) {
    std::vector<RNode*> nodes;
    for (RNode* n = head; n; n = n->next) nodes.push_back(n);
    std::map<RNode*, int> idx;
    for (size_t i = 0; i < nodes.size(); i++) idx[nodes[i]] = (int)i;
    std::vector<Json> out;
    for (auto n : nodes) {
        int ni = n->next ? idx[n->next] : -1;
        int ri = n->random ? idx[n->random] : -1;
        out.push_back(intsToJson({n->val, ni, ri}));
    }
    return Json::mk_arr(out);
}

inline GNode* buildGraph(const std::vector<std::vector<int>>& adj) {
    if (adj.empty()) return nullptr;
    std::vector<GNode*> nodes;
    for (size_t i = 0; i < adj.size(); i++) nodes.push_back(new GNode((int)i + 1));
    for (size_t i = 0; i < adj.size(); i++)
        for (int j : adj[i]) nodes[i]->neighbors.push_back(nodes[j - 1]);
    return nodes[0];
}
inline Json dumpGraphJson(GNode* node) {
    if (!node) return Json::mk_arr({});
    std::map<int, GNode*> seen;
    std::queue<GNode*> q;
    q.push(node);
    while (!q.empty()) {
        GNode* n = q.front();
        q.pop();
        if (seen.count(n->val)) continue;
        seen[n->val] = n;
        for (auto x : n->neighbors) q.push(x);
    }
    std::vector<Json> out;
    for (const auto& kv : seen) {
        std::vector<int> nb;
        for (auto x : kv.second->neighbors) nb.push_back(x->val);
        std::sort(nb.begin(), nb.end());
        out.push_back(intsToJson(nb));
    }
    return Json::mk_arr(out);
}

class SolutionBase {
protected:
    std::string data_;
    size_t pos_ = 0;
public:
    SolutionBase(std::string data) : data_(std::move(data)) {}
    int read4(char* buf) {
        int cnt = 0;
        while (cnt < 4 && pos_ < data_.size()) buf[cnt++] = data_[pos_++];
        return cnt;
    }
};