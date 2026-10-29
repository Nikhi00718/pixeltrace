"""Sixteenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=653, slug="two-sum-iv-input-is-a-bst", title="Two Sum IV - Input is a BST", difficulty="Easy", world="trees", tags=["hash-table", "two-pointers", "tree", "bst"],
    story=dict(title="Two Fruits That Weigh k", text="A squirrel climbs the orchard asking the lockers whether the partner weight k - val was already seen.",
               goal="Return true if two nodes sum to k."),
    spec=dict(method="findTarget", ret="bool", params=[["TreeNode*", "root"], ["int", "k"]]),
    tests=[dict(args=[[5, 3, 6, 2, 4, None, 7], 9], expected=True), dict(args=[[5, 3, 6, 2, 4, None, 7], 28], expected=False)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="set", var="seen", label="weights seen"),
    ]),
    reference="""class Solution {
public:
    set<int> seen;
    bool find(TreeNode* node, int k) {
        if (!node) return false;
        if (seen.count(k - node->val)) return true;
        seen.insert(node->val);
        return find(node->left, k) || find(node->right, k);
    }
    bool findTarget(TreeNode* root, int k) {
        return find(root, k);
    }
};""",
)

add(
    id=654, slug="maximum-binary-tree", title="Maximum Binary Tree", difficulty="Medium", world="trees", tags=["array", "divide-and-conquer", "stack", "tree", "monotonic-stack"],
    story=dict(title="The Tallest Fruit Rules", text="The heaviest fruit in the stretch becomes the root; everything left of it builds the left branch and everything right the right branch.",
               goal="Return the maximum binary tree."),
    spec=dict(method="constructMaximumBinaryTree", ret="TreeNode*", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[3, 2, 1, 6, 0, 5]], expected=[6, 3, 5, None, 2, 0, None, None, 1]), dict(args=[[3, 2, 1]], expected=[3, None, 2, None, 1])],
    scene=dict(theme="forest", layers=[dict(kind="array", var="nums", label="fruit weights", pointers=["lo", "best", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    TreeNode* build(vector<int>& nums, int lo, int hi) {
        if (lo > hi) return nullptr;
        int best = lo;
        for (int i = lo; i <= hi; i++) {
            if (nums[i] > nums[best]) best = i;
        }
        TreeNode* node = new TreeNode(nums[best]);
        node->left = build(nums, lo, best - 1);
        node->right = build(nums, best + 1, hi);
        return node;
    }
    TreeNode* constructMaximumBinaryTree(vector<int>& nums) {
        return build(nums, 0, nums.size() - 1);
    }
};""",
)

add(
    id=657, slug="robot-return-to-origin", title="Robot Return to Origin", difficulty="Easy", world="arrays", tags=["string", "simulation"],
    story=dict(title="The Wandering Robot", text="Follow the robot's moves on a grid, adjusting x and y. It's home if both are zero at the end.",
               goal="Return true if the robot ends at the origin."),
    spec=dict(method="judgeCircle", ret="bool", params=[["string", "moves"]]),
    tests=[dict(args=["UD"], expected=True), dict(args=["LL"], expected=False), dict(args=["RRDDLUUL"], expected=True)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="moves", label="moves", pointers=["i"]),
        dict(kind="values", vars=["x", "y"]),
    ]),
    reference="""class Solution {
public:
    bool judgeCircle(string moves) {
        int x = 0, y = 0;
        for (int i = 0; i < (int)moves.size(); i++) {
            char m = moves[i];
            if (m == 'U') y++;
            else if (m == 'D') y--;
            else if (m == 'L') x--;
            else x++;
        }
        return x == 0 && y == 0;
    }
};""",
)

add(
    id=658, slug="find-k-closest-elements", title="Find K Closest Elements", difficulty="Medium", world="binary-search", tags=["array", "two-pointers", "binary-search", "sorting", "sliding-window", "heap"],
    story=dict(title="The Best Window of k", text="Binary-search where a window of k starts: if x is closer to the element just past the window than to its first, the window should move right.",
               goal="Return the k closest elements to x, in ascending order."),
    spec=dict(method="findClosestElements", ret="vector<int>", params=[["vector<int>&", "arr"], ["int", "k"], ["int", "x"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], 4, 3], expected=[1, 2, 3, 4]), dict(args=[[1, 1, 2, 3, 4, 5], 4, -1], expected=[1, 1, 2, 3]), dict(args=[[1, 3, 5, 7, 9, 11], 3, 8], expected=[5, 7, 9])],
    visualTest=2,
    scene=dict(theme="cave", layers=[dict(kind="array", var="arr", label="sorted values", pointers=["lo", "mid", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int lo = 0, hi = arr.size() - k;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (x - arr[mid] > arr[mid + k] - x) lo = mid + 1;
            else hi = mid;
        }
        return vector<int>(arr.begin() + lo, arr.begin() + lo + k);
    }
};""",
)

add(
    id=662, slug="maximum-width-of-binary-tree", title="Maximum Width of Binary Tree", difficulty="Medium", world="trees", tags=["tree", "dfs", "bfs"],
    story=dict(title="The Widest Row", text="Number every slot in a row as if the tree were full: a child of slot i is 2i or 2i+1. Each row's width is the last slot minus the first, plus one.",
               goal="Return the maximum width over all levels."),
    spec=dict(method="widthOfBinaryTree", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 3, 2, 5, 3, None, 9]], expected=4), dict(args=[[1, 3, 2, 5, None, None, 9, 6, None, 7]], expected=7), dict(args=[[1, 3, 2, 5]], expected=2)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="row [node, slot]"),
        dict(kind="values", vars=["first", "last", "best"]),
    ]),
    reference="""class Solution {
public:
    int widthOfBinaryTree(TreeNode* root) {
        queue<pair<TreeNode*, unsigned long long>> q;
        q.push({root, 0});
        unsigned long long best = 0;
        while (!q.empty()) {
            int sz = q.size();
            unsigned long long first = q.front().second, last = first;
            for (int k = 0; k < sz; k++) {
                auto [node, slot] = q.front();
                q.pop();
                last = slot;
                if (node->left) q.push({node->left, 2 * (slot - first)});
                if (node->right) q.push({node->right, 2 * (slot - first) + 1});
            }
            best = max(best, last - first + 1);
        }
        return best;
    }
};""",
)

add(
    id=669, slug="trim-a-binary-search-tree", title="Trim a Binary Search Tree", difficulty="Medium", world="trees", tags=["tree", "dfs", "bst"],
    story=dict(title="Pruning to a Weight Range", text="A fruit lighter than low takes its whole left branch with it, so only its right branch survives; a fruit heavier than high keeps only its left.",
               goal="Return the tree with only values in [low, high]."),
    spec=dict(method="trimBST", ret="TreeNode*", params=[["TreeNode*", "root"], ["int", "low"], ["int", "high"]]),
    tests=[dict(args=[[1, 0, 2], 1, 2], expected=[1, None, 2]), dict(args=[[3, 0, 4, None, 2, None, None, 1], 1, 3], expected=[3, 2, None, 1])],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["root"], label="orchard"),
        dict(kind="values", vars=["low", "high"]),
    ]),
    reference="""class Solution {
public:
    TreeNode* trimBST(TreeNode* root, int low, int high) {
        if (!root) return nullptr;
        if (root->val < low) return trimBST(root->right, low, high);
        if (root->val > high) return trimBST(root->left, low, high);
        root->left = trimBST(root->left, low, high);
        root->right = trimBST(root->right, low, high);
        return root;
    }
};""",
)

add(
    id=674, slug="longest-continuous-increasing-subsequence", title="Longest Continuous Increasing Subsequence", difficulty="Easy", world="greedy", tags=["array"],
    story=dict(title="The Longest Uphill Stretch", text="Walk the trail counting the current climb; any step down or flat resets it.",
               goal="Return the length of the longest strictly increasing run."),
    spec=dict(method="findLengthOfLCIS", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 3, 5, 4, 7]], expected=3), dict(args=[[2, 2, 2, 2, 2]], expected=1)],
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="nums", label="trail", pointers=["i"]),
        dict(kind="values", vars=["run", "best"]),
    ]),
    reference="""class Solution {
public:
    int findLengthOfLCIS(vector<int>& nums) {
        int run = 1, best = 1;
        for (int i = 1; i < (int)nums.size(); i++) {
            run = nums[i] > nums[i - 1] ? run + 1 : 1;
            best = max(best, run);
        }
        return best;
    }
};""",
)

add(
    id=678, slug="valid-parenthesis-string", title="Valid Parenthesis String", difficulty="Medium", world="greedy", tags=["string", "dynamic-programming", "stack", "greedy"],
    story=dict(title="Wildcard Brackets", text="A * can be (, ) or nothing. Track the lowest and highest number of open brackets possible; if the highest ever drops below zero it's broken.",
               goal="Return true if the string can be valid."),
    spec=dict(method="checkValidString", ret="bool", params=[["string", "s"]]),
    tests=[dict(args=["()"], expected=True), dict(args=["(*)"], expected=True), dict(args=["(*))"], expected=True), dict(args=["((*)(*))((*"], expected=False)],
    visualTest=3,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="brackets", pointers=["i"]),
        dict(kind="values", vars=["lo", "hi"]),
    ]),
    reference="""class Solution {
public:
    bool checkValidString(string s) {
        int lo = 0, hi = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') {
                lo++;
                hi++;
            } else if (s[i] == ')') {
                lo--;
                hi--;
            } else {
                lo--;
                hi++;
            }
            if (hi < 0) return false;
            lo = max(lo, 0);
        }
        return lo == 0;
    }
};""",
)

add(
    id=684, slug="redundant-connection", title="Redundant Connection", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "union-find", "graph"],
    story=dict(title="The Extra Road", text="Roads are added one by one, joining kingdoms. A road whose two towns already share a kingdom closes a loop: that's the extra road.",
               goal="Return the edge that can be removed to leave a tree."),
    spec=dict(method="findRedundantConnection", ret="vector<int>", params=[["vector<vector<int>>&", "edges"]]),
    tests=[dict(args=[[[1, 2], [1, 3], [2, 3]]], expected=[2, 3]), dict(args=[[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]], expected=[1, 4])],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="edges", label="roads", style="tiles", pointers=["k"]),
        dict(kind="array", var="parent", label="kingdom leader by town", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> parent;
    int leader(int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];
        return x;
    }
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        parent.resize(edges.size() + 1);
        for (int v = 0; v < (int)parent.size(); v++) parent[v] = v;
        for (int k = 0; k < (int)edges.size(); k++) {
            int a = leader(edges[k][0]), b = leader(edges[k][1]);
            if (a == b) return edges[k];
            parent[a] = b;
        }
        return {};
    }
};""",
)

add(
    id=687, slug="longest-univalue-path", title="Longest Univalue Path", difficulty="Medium", world="trees", tags=["tree", "dfs"],
    story=dict(title="Vines of Matching Fruit", text="Each fruit asks its branches how long a same-valued arm reaches down. Arms only count when the child matches; both arms together form a vine through the fruit.",
               goal="Return the number of edges on the longest path of equal values."),
    spec=dict(method="longestUnivaluePath", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[5, 4, 5, 1, 1, None, 5]], expected=2), dict(args=[[1, 4, 5, 4, 4, None, 5]], expected=2)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["l", "r", "best"]),
    ]),
    reference="""class Solution {
public:
    int best = 0;
    int arm(TreeNode* node) {
        if (!node) return 0;
        int l = arm(node->left);
        int r = arm(node->right);
        l = (node->left && node->left->val == node->val) ? l + 1 : 0;
        r = (node->right && node->right->val == node->val) ? r + 1 : 0;
        best = max(best, l + r);
        return max(l, r);
    }
    int longestUnivaluePath(TreeNode* root) {
        arm(root);
        return best;
    }
};""",
)

add(
    id=692, slug="top-k-frequent-words", title="Top K Frequent Words", difficulty="Medium", world="heap", tags=["hash-table", "string", "trie", "sorting", "heap", "bucket-sort", "counting"],
    story=dict(title="The Most Spoken Words", text="Count every word, then sort by count (high first), breaking ties alphabetically, and read off the first k.",
               goal="Return the k most frequent words in that order."),
    spec=dict(method="topKFrequent", ret="vector<string>", params=[["vector<string>&", "words"], ["int", "k"]]),
    tests=[dict(args=[["i", "love", "leetcode", "i", "love", "coding"], 2], expected=["i", "love"]),
           dict(args=[["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4], expected=["the", "is", "sunny", "day"])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="map", var="cnt", label="word counts"),
        dict(kind="array", var="order", label="ranked", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> topKFrequent(vector<string>& words, int k) {
        map<string, int> cnt;
        for (auto& w : words) cnt[w]++;
        vector<string> order;
        for (auto& [w, c] : cnt) order.push_back(w);
        sort(order.begin(), order.end(), [&](const string& a, const string& b) {
            return cnt[a] != cnt[b] ? cnt[a] > cnt[b] : a < b;
        });
        order.resize(k);
        return order;
    }
};""",
)

add(
    id=696, slug="count-binary-substrings", title="Count Binary Substrings", difficulty="Easy", world="two-pointers", tags=["two-pointers", "string"],
    story=dict(title="Balanced Lamp Blocks", text="Group the lamps into runs. Two neighbouring runs of lengths a and b give min(a, b) balanced substrings.",
               goal="Return the number of substrings with equal grouped 0s and 1s."),
    spec=dict(method="countBinarySubstrings", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["00110011"], expected=6), dict(args=["10101"], expected=4)],
    scene=dict(theme="space", layers=[
        dict(kind="string", var="s", label="lamps", pointers=["i"]),
        dict(kind="values", vars=["prev", "cur", "total"]),
    ]),
    reference="""class Solution {
public:
    int countBinarySubstrings(string s) {
        int prev = 0, cur = 1, total = 0;
        for (int i = 1; i < (int)s.size(); i++) {
            if (s[i] == s[i - 1]) {
                cur++;
            } else {
                total += min(prev, cur);
                prev = cur;
                cur = 1;
            }
        }
        return total + min(prev, cur);
    }
};""",
)

add(
    id=697, slug="degree-of-an-array", title="Degree of an Array", difficulty="Easy", world="arrays", tags=["array", "hash-table"],
    story=dict(title="The Shortest Stretch with the Busiest Value", text="Lockers remember each value's count and first position. The busiest values' first-to-last spans are candidates; keep the shortest.",
               goal="Return the length of the shortest subarray with the same degree as the whole array."),
    spec=dict(method="findShortestSubArray", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 2, 3, 1]], expected=2), dict(args=[[1, 2, 2, 3, 1, 4, 2]], expected=6)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="values", pointers=["i"]),
        dict(kind="row", children=[dict(kind="map", var="cnt", label="counts"), dict(kind="map", var="first", label="first seen at")]),
        dict(kind="values", vars=["degree", "best"]),
    ]),
    reference="""class Solution {
public:
    int findShortestSubArray(vector<int>& nums) {
        map<int, int> cnt, first;
        int degree = 0, best = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            int x = nums[i];
            if (!first.count(x)) first[x] = i;
            int c = ++cnt[x];
            int span = i - first[x] + 1;
            if (c > degree) {
                degree = c;
                best = span;
            } else if (c == degree) {
                best = min(best, span);
            }
        }
        return best;
    }
};""",
)

add(
    id=713, slug="subarray-product-less-than-k", title="Subarray Product Less Than K", difficulty="Medium", world="sliding-window", tags=["array", "binary-search", "sliding-window", "prefix-sum"],
    story=dict(title="The Multiplying Net", text="The net stretches right multiplying crate weights. While the product reaches k, it shrinks from the left; every crate in the net ending at r starts a valid stretch.",
               goal="Return how many contiguous subarrays have product less than k."),
    spec=dict(method="numSubarrayProductLessThanK", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[10, 5, 2, 6], 100], expected=8), dict(args=[[1, 2, 3], 0], expected=0)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["prod", "count"]),
    ]),
    reference="""class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        if (k <= 1) return 0;
        long long prod = 1;
        int l = 0, count = 0;
        for (int r = 0; r < (int)nums.size(); r++) {
            prod *= nums[r];
            while (prod >= k) {
                prod /= nums[l];
                l++;
            }
            count += r - l + 1;
        }
        return count;
    }
};""",
)

add(
    id=717, slug="1-bit-and-2-bit-characters", title="1-bit and 2-bit Characters", difficulty="Easy", world="bits", tags=["array"],
    story=dict(title="Reading the Lamp Code", text="A 1 starts a two-lamp character; a 0 alone is a one-lamp character. Hop through the code; is the last character a single 0?",
               goal="Return true if the last character must be a one-bit character."),
    spec=dict(method="isOneBitCharacter", ret="bool", params=[["vector<int>&", "bits"]]),
    tests=[dict(args=[[1, 0, 0]], expected=True), dict(args=[[1, 1, 1, 0]], expected=False)],
    scene=dict(theme="space", layers=[dict(kind="array", var="bits", label="lamps", pointers=["i"])]),
    reference="""class Solution {
public:
    bool isOneBitCharacter(vector<int>& bits) {
        int i = 0, n = bits.size();
        while (i < n - 1) i += bits[i] + 1;
        return i == n - 1;
    }
};""",
)

add(
    id=718, slug="maximum-length-of-repeated-subarray", title="Maximum Length of Repeated Subarray", difficulty="Medium", world="dp", tags=["array", "binary-search", "dynamic-programming", "sliding-window", "rolling-hash", "hash-function"],
    story=dict(title="The Longest Shared Strip", text="Each grid cell records how long a matching strip ends at both positions: one more than the diagonal if the two crates match, else zero.",
               goal="Return the length of the longest common subarray."),
    spec=dict(method="findLength", ret="int", params=[["vector<int>&", "nums1"], ["vector<int>&", "nums2"]]),
    tests=[dict(args=[[1, 2, 3, 2, 1], [3, 2, 1, 4, 7]], expected=3), dict(args=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], expected=5)],
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[dict(kind="array", var="nums1", label="strip 1"), dict(kind="array", var="nums2", label="strip 2")]),
        dict(kind="grid", var="dp", palette="dp", label="matching run", pointers=[["i", "j"]]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int findLength(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size(), m = nums2.size(), best = 0;
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                if (nums1[i - 1] == nums2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                    best = max(best, dp[i][j]);
                }
        return best;
    }
};""",
)

add(
    id=728, slug="self-dividing-numbers", title="Self Dividing Numbers", difficulty="Easy", world="bits", tags=["math"],
    story=dict(title="Numbers Divisible by Their Own Digits", text="Peel off each digit and check it divides the number (and isn't zero).",
               goal="Return every self-dividing number in [left, right]."),
    spec=dict(method="selfDividingNumbers", ret="vector<int>", params=[["int", "left"], ["int", "right"]]),
    tests=[dict(args=[1, 22], expected=[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]), dict(args=[47, 85], expected=[48, 55, 66, 77])],
    visualTest=1,
    scene=dict(theme="space", layers=[
        dict(kind="array", var="res", label="self-dividing", style="tiles"),
        dict(kind="values", vars=["v", "x", "d"]),
    ]),
    reference="""class Solution {
public:
    vector<int> selfDividingNumbers(int left, int right) {
        vector<int> res;
        for (int v = left; v <= right; v++) {
            int x = v;
            bool ok = true;
            while (x > 0 && ok) {
                int d = x % 10;
                if (d == 0 || v % d != 0) ok = false;
                x /= 10;
            }
            if (ok) res.push_back(v);
        }
        return res;
    }
};""",
)

add(
    id=740, slug="delete-and-earn", title="Delete and Earn", difficulty="Medium", world="dp", tags=["array", "hash-table", "dynamic-programming"],
    story=dict(title="The Fox and the Numbered Henhouses", text="Earning v burns every v-1 and v+1. Pile the points by value, then it's House Robber over the values.",
               goal="Return the maximum points."),
    spec=dict(method="deleteAndEarn", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[3, 4, 2]], expected=6), dict(args=[[2, 2, 3, 3, 3, 4]], expected=9)],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="points", label="points by value", style="tiles", pointers=["v"]),
        dict(kind="values", vars=["take", "skip"]),
    ]),
    reference="""class Solution {
public:
    int deleteAndEarn(vector<int>& nums) {
        int top = *max_element(nums.begin(), nums.end());
        vector<int> points(top + 1, 0);
        for (int x : nums) points[x] += x;
        int take = 0, skip = 0;
        for (int v = 0; v <= top; v++) {
            int nt = skip + points[v];
            skip = max(skip, take);
            take = nt;
        }
        return max(take, skip);
    }
};""",
)

add(
    id=743, slug="network-delay-time", title="Network Delay Time", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "graph", "heap", "shortest-path"],
    story=dict(title="How Long Until Everyone Hears?", text="A signal leaves town k. The pyramid always picks the nearest unsettled town (Dijkstra); its time is final, and its roads offer shorter times to neighbours.",
               goal="Return the time for all nodes to receive the signal, or -1."),
    spec=dict(method="networkDelayTime", ret="int", params=[["vector<vector<int>>&", "times"], ["int", "n"], ["int", "k"]]),
    tests=[dict(args=[[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], expected=2), dict(args=[[[1, 2, 1]], 2, 1], expected=1), dict(args=[[[1, 2, 1]], 2, 2], expected=-1)],
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="dist", label="arrival time by town", style="tiles", pointers=["u"]),
        dict(kind="heap", var="pq", label="pyramid [time, town]"),
    ]),
    reference="""class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int, int>>> adj(n + 1);
        for (auto& t : times) adj[t[0]].push_back({t[1], t[2]});
        vector<int> dist(n + 1, INT_MAX);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        dist[k] = 0;
        pq.push({0, k});
        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            if (d > dist[u]) continue;
            for (auto& [v, w] : adj[u]) {
                if (d + w < dist[v]) {
                    dist[v] = d + w;
                    pq.push({dist[v], v});
                }
            }
        }
        int worst = 0;
        for (int v = 1; v <= n; v++) {
            if (dist[v] == INT_MAX) return -1;
            worst = max(worst, dist[v]);
        }
        return worst;
    }
};""",
)

add(
    id=747, slug="largest-number-at-least-twice-of-others", title="Largest Number At Least Twice of Others", difficulty="Easy", world="arrays", tags=["array", "sorting"],
    story=dict(title="The Dominant Tower", text="Track the tallest and second-tallest tower; the tallest dominates if it's at least twice the runner-up.",
               goal="Return the index of the dominant element, or -1."),
    spec=dict(method="dominantIndex", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[3, 6, 1, 0]], expected=1), dict(args=[[1, 2, 3, 4]], expected=-1)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="nums", label="towers", pointers=["i", "best"]),
        dict(kind="values", vars=["second"]),
    ]),
    reference="""class Solution {
public:
    int dominantIndex(vector<int>& nums) {
        int best = 0, second = -1;
        for (int i = 1; i < (int)nums.size(); i++) {
            if (nums[i] > nums[best]) {
                second = nums[best];
                best = i;
            } else {
                second = max(second, nums[i]);
            }
        }
        return nums[best] >= 2 * second ? best : -1;
    }
};""",
)

add(
    id=752, slug="open-the-lock", title="Open the Lock", difficulty="Medium", world="graphs", tags=["array", "hash-table", "string", "bfs"],
    story=dict(title="Turning the Combination Wheels", text="From 0000, every wheel can turn up or down. Explore settings in rings of one turn each, avoiding dead ends, until the target appears.",
               goal="Return the fewest turns to reach target, or -1."),
    spec=dict(method="openLock", ret="int", params=[["vector<string>&", "deadends"], ["string", "target"]]),
    tests=[dict(args=[["0201", "0101", "0102", "1212", "2002"], "0202"], expected=6), dict(args=[["8888"], "0009"], expected=1),
           dict(args=[["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888"], expected=-1)],
    visualTest=1,
    scene=dict(theme="cave", layers=[
        dict(kind="queue", var="q", label="settings to try"),
        dict(kind="values", vars=["cur", "turns"]),
    ]),
    reference="""class Solution {
public:
    int openLock(vector<string>& deadends, string target) {
        set<string> seen(deadends.begin(), deadends.end());
        if (seen.count("0000")) return -1;
        queue<string> q;
        q.push("0000");
        seen.insert("0000");
        int turns = 0;
        while (!q.empty()) {
            int sz = q.size();
            for (int k = 0; k < sz; k++) {
                string cur = q.front();
                q.pop();
                if (cur == target) return turns;
                for (int w = 0; w < 4; w++) {
                    for (int d : {1, 9}) {
                        string next = cur;
                        next[w] = '0' + (next[w] - '0' + d) % 10;
                        if (!seen.count(next)) {
                            seen.insert(next);
                            q.push(next);
                        }
                    }
                }
            }
            turns++;
        }
        return -1;
    }
};""",
)

add(
    id=771, slug="jewels-and-stones", title="Jewels and Stones", difficulty="Easy", world="arrays", tags=["hash-table", "string"],
    story=dict(title="Sorting the Treasure Bag", text="The kinds of jewels go into lockers; then each stone in the bag is checked against them.",
               goal="Return how many stones are jewels."),
    spec=dict(method="numJewelsInStones", ret="int", params=[["string", "jewels"], ["string", "stones"]]),
    tests=[dict(args=["aA", "aAAbbbb"], expected=3), dict(args=["z", "ZZ"], expected=0)],
    scene=dict(theme="cave", layers=[
        dict(kind="string", var="stones", label="bag", pointers=["i"]),
        dict(kind="set", var="kinds", label="jewel kinds"),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int numJewelsInStones(string jewels, string stones) {
        set<char> kinds(jewels.begin(), jewels.end());
        int count = 0;
        for (int i = 0; i < (int)stones.size(); i++) count += kinds.count(stones[i]);
        return count;
    }
};""",
)

add(
    id=784, slug="letter-case-permutation", title="Letter Case Permutation", difficulty="Medium", world="backtracking", tags=["string", "backtracking", "bit-manipulation"],
    story=dict(title="Every Way to Capitalise", text="At each letter, the doors split: keep its case, or flip it. Digits pass straight through. Every finished word is written down.",
               goal="Return every case permutation (any order)."),
    spec=dict(method="letterCasePermutation", ret="vector<string>", params=[["string", "s"]]),
    compare="unordered",
    tests=[dict(args=["a1b2"], expected=["a1b2", "a1B2", "A1b2", "A1B2"]), dict(args=["3z4"], expected=["3z4", "3Z4"])],
    scene=dict(theme="cave", layers=[
        dict(kind="string", var="cur", label="word", pointers=["i"]),
        dict(kind="array", var="res", label="written", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> res;
    void go(string& cur, int i) {
        if (i == (int)cur.size()) {
            res.push_back(cur);
            return;
        }
        go(cur, i + 1);
        if (isalpha(cur[i])) {
            cur[i] ^= 32;
            go(cur, i + 1);
            cur[i] ^= 32;
        }
    }
    vector<string> letterCasePermutation(string s) {
        string cur = s;
        go(cur, 0);
        return res;
    }
};""",
)

add(
    id=785, slug="is-graph-bipartite", title="Is Graph Bipartite?", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "union-find", "graph"],
    story=dict(title="Two Rival Kingdoms", text="Paint towns in two colours so every road joins different colours. A painter floods each region alternating colours; a road between same colours breaks it.",
               goal="Return true if the graph is bipartite."),
    spec=dict(method="isBipartite", ret="bool", params=[["vector<vector<int>>&", "graph"]]),
    tests=[dict(args=[[[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]], expected=False), dict(args=[[[1, 3], [0, 2], [1, 3], [0, 2]]], expected=True)],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="graph", adj="graph", state="color", pointers=["u"], label="towns"),
        dict(kind="queue", var="q", label="to paint"),
    ]),
    reference="""class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> color(n, 0);
        for (int s = 0; s < n; s++) {
            if (color[s]) continue;
            queue<int> q;
            q.push(s);
            color[s] = 1;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                for (int v : graph[u]) {
                    if (color[v] == color[u]) return false;
                    if (!color[v]) {
                        color[v] = 3 - color[u];
                        q.push(v);
                    }
                }
            }
        }
        return true;
    }
};""",
)

add(
    id=787, slug="cheapest-flights-within-k-stops", title="Cheapest Flights Within K Stops", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "graph", "dynamic-programming", "heap", "shortest-path"],
    story=dict(title="Budget Airline Hopping", text="Each round allows one more flight. Every round, prices are relaxed from the previous round's prices only, so no route sneaks in an extra stop.",
               goal="Return the cheapest price from src to dst with at most k stops, or -1."),
    spec=dict(method="findCheapestPrice", ret="int", params=[["int", "n"], ["vector<vector<int>>&", "flights"], ["int", "src"], ["int", "dst"], ["int", "k"]]),
    tests=[dict(args=[4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1], expected=700),
           dict(args=[3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1], expected=200), dict(args=[3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], expected=500)],
    scene=dict(theme="space", layers=[
        dict(kind="array", var="cost", label="best price by city", style="tiles"),
        dict(kind="values", vars=["round"]),
    ]),
    reference="""class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        const int INF = 1e9;
        vector<int> cost(n, INF);
        cost[src] = 0;
        for (int round = 0; round <= k; round++) {
            vector<int> next = cost;
            for (auto& f : flights) {
                if (cost[f[0]] != INF && cost[f[0]] + f[2] < next[f[1]]) next[f[1]] = cost[f[0]] + f[2];
            }
            cost = next;
        }
        return cost[dst] == INF ? -1 : cost[dst];
    }
};""",
)
