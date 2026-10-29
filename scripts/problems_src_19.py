"""Nineteenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=989, slug="add-to-array-form-of-integer", title="Add to Array-Form of Integer", difficulty="Easy", world="arrays", tags=["array", "math"],
    story=dict(title="Adding to the Digit Wheels", text="Add k into the last wheel and let the carry ripple left, adding new wheels at the front if the carry outlives the number.",
               goal="Return the array form of num + k."),
    spec=dict(method="addToArrayForm", ret="vector<int>", params=[["vector<int>&", "num"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 0, 0], 34], expected=[1, 2, 3, 4]), dict(args=[[2, 7, 4], 181], expected=[4, 5, 5]), dict(args=[[2, 1, 5], 806], expected=[1, 0, 2, 1])],
    visualTest=2,
    scene=dict(theme="city", layers=[
        dict(kind="array", var="num", label="wheels", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["k"]),
    ]),
    reference="""class Solution {
public:
    vector<int> addToArrayForm(vector<int>& num, int k) {
        for (int i = num.size() - 1; i >= 0 && k > 0; i--) {
            k += num[i];
            num[i] = k % 10;
            k /= 10;
        }
        while (k > 0) {
            num.insert(num.begin(), k % 10);
            k /= 10;
        }
        return num;
    }
};""",
)

add(
    id=990, slug="satisfiability-of-equality-equations", title="Satisfiability of Equality Equations", difficulty="Medium", world="graphs", tags=["array", "string", "union-find", "graph"],
    story=dict(title="Who Must Be Equal?", text="First every a==b joins two letters into one family. Then each a!=b is checked: if both letters share a family, the equations contradict.",
               goal="Return true if all equations can be satisfied."),
    spec=dict(method="equationsPossible", ret="bool", params=[["vector<string>&", "equations"]]),
    tests=[dict(args=[["a==b", "b!=a"]], expected=False), dict(args=[["b==a", "a==b"]], expected=True), dict(args=[["a==b", "b==c", "a==c"]], expected=True), dict(args=[["a==b", "b!=c", "c==a"]], expected=False)],
    visualTest=3,
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="equations", label="equations", style="tiles", pointers=["k"]),
        dict(kind="array", var="parent", label="family leader by letter", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> parent;
    int leader(int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }
    bool equationsPossible(vector<string>& equations) {
        parent.resize(26);
        for (int i = 0; i < 26; i++) parent[i] = i;
        for (int k = 0; k < (int)equations.size(); k++) {
            string& e = equations[k];
            if (e[1] == '=') parent[leader(e[0] - 'a')] = leader(e[3] - 'a');
        }
        for (int k = 0; k < (int)equations.size(); k++) {
            string& e = equations[k];
            if (e[1] == '!' && leader(e[0] - 'a') == leader(e[3] - 'a')) return false;
        }
        return true;
    }
};""",
)

add(
    id=993, slug="cousins-in-binary-tree", title="Cousins in Binary Tree", difficulty="Easy", world="trees", tags=["tree", "dfs", "bfs"],
    story=dict(title="Same Row, Different Parents", text="Walk the orchard recording each fruit's depth and parent. Cousins hang at the same depth from different parents.",
               goal="Return true if x and y are cousins."),
    spec=dict(method="isCousins", ret="bool", params=[["TreeNode*", "root"], ["int", "x"], ["int", "y"]]),
    tests=[dict(args=[[1, 2, 3, 4], 4, 3], expected=False), dict(args=[[1, 2, 3, None, 4, None, 5], 5, 4], expected=True), dict(args=[[1, 2, 3, None, 4], 2, 3], expected=False)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["dx", "dy", "px", "py"]),
    ]),
    reference="""class Solution {
public:
    int dx = -1, dy = -1, px = -1, py = -1;
    void walk(TreeNode* node, int parent, int depth, int x, int y) {
        if (!node) return;
        if (node->val == x) {
            dx = depth;
            px = parent;
        }
        if (node->val == y) {
            dy = depth;
            py = parent;
        }
        walk(node->left, node->val, depth + 1, x, y);
        walk(node->right, node->val, depth + 1, x, y);
    }
    bool isCousins(TreeNode* root, int x, int y) {
        walk(root, -1, 0, x, y);
        return dx == dy && px != py;
    }
};""",
)

add(
    id=1002, slug="find-common-characters", title="Find Common Characters", difficulty="Easy", world="arrays", tags=["array", "hash-table", "string"],
    story=dict(title="Letters Every Scroll Shares", text="Keep the minimum count of each letter across all scrolls; whatever survives appears in every one.",
               goal="Return every character (with repeats) that appears in all words."),
    spec=dict(method="commonChars", ret="vector<string>", params=[["vector<string>&", "words"]]),
    compare="unordered",
    tests=[dict(args=[["bella", "label", "roller"]], expected=["e", "l", "l"]), dict(args=[["cool", "lock", "cook"]], expected=["c", "o"])],
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="words", label="scrolls", style="tiles", pointers=["k"]),
        dict(kind="array", var="common", label="min count a..z", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> commonChars(vector<string>& words) {
        vector<int> common(26, INT_MAX);
        for (int k = 0; k < (int)words.size(); k++) {
            vector<int> cnt(26, 0);
            for (char c : words[k]) cnt[c - 'a']++;
            for (int i = 0; i < 26; i++) common[i] = min(common[i], cnt[i]);
        }
        vector<string> res;
        for (int i = 0; i < 26; i++)
            for (int t = 0; t < common[i]; t++) res.push_back(string(1, 'a' + i));
        return res;
    }
};""",
)

add(
    id=1005, slug="maximize-sum-of-array-after-k-negations", title="Maximize Sum Of Array After K Negations", difficulty="Easy", world="greedy", tags=["array", "greedy", "sorting"],
    story=dict(title="Flipping the Worst Debts", text="Always flip the smallest number: a pyramid keeps it on top. After k flips, add everything up.",
               goal="Return the largest possible sum after k negations."),
    spec=dict(method="largestSumAfterKNegations", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[4, 2, 3], 1], expected=5), dict(args=[[3, -1, 0, 2], 3], expected=6), dict(args=[[2, -3, -1, 5, -4], 2], expected=13)],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="heap", var="pq", label="smallest on top"),
        dict(kind="values", vars=["k"]),
    ]),
    reference="""class Solution {
public:
    int largestSumAfterKNegations(vector<int>& nums, int k) {
        priority_queue<int, vector<int>, greater<int>> pq(nums.begin(), nums.end());
        while (k-- > 0) {
            int x = pq.top();
            pq.pop();
            pq.push(-x);
        }
        int sum = 0;
        while (!pq.empty()) {
            sum += pq.top();
            pq.pop();
        }
        return sum;
    }
};""",
)

add(
    id=1007, slug="minimum-domino-rotations-for-equal-row", title="Minimum Domino Rotations For Equal Row", difficulty="Medium", world="greedy", tags=["array", "greedy"],
    story=dict(title="Making One Row Uniform", text="The winning number must be on the first domino, so try tops[0] and bottoms[0]. For each, count flips needed to bring it to the top or to the bottom.",
               goal="Return the fewest rotations to make one row all the same, or -1."),
    spec=dict(method="minDominoRotations", ret="int", params=[["vector<int>&", "tops"], ["vector<int>&", "bottoms"]]),
    tests=[dict(args=[[2, 1, 2, 4, 2, 2], [5, 2, 6, 2, 3, 2]], expected=2), dict(args=[[3, 5, 1, 2, 3], [3, 6, 3, 3, 4]], expected=-1)],
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="tops", label="tops", pointers=["i"]),
        dict(kind="array", var="bottoms", label="bottoms", pointers=["i"]),
        dict(kind="values", vars=["x", "flipTop", "flipBottom"]),
    ]),
    reference="""class Solution {
public:
    int tryValue(vector<int>& tops, vector<int>& bottoms, int x) {
        int flipTop = 0, flipBottom = 0;
        for (int i = 0; i < (int)tops.size(); i++) {
            if (tops[i] != x && bottoms[i] != x) return INT_MAX;
            if (tops[i] != x) flipTop++;
            if (bottoms[i] != x) flipBottom++;
        }
        return min(flipTop, flipBottom);
    }
    int minDominoRotations(vector<int>& tops, vector<int>& bottoms) {
        int best = min(tryValue(tops, bottoms, tops[0]), tryValue(tops, bottoms, bottoms[0]));
        return best == INT_MAX ? -1 : best;
    }
};""",
)

add(
    id=1008, slug="construct-binary-search-tree-from-preorder-traversal", title="Construct Binary Search Tree from Preorder Traversal", difficulty="Medium",
    world="trees", tags=["array", "stack", "tree", "bst", "monotonic-stack"],
    story=dict(title="Replanting from the Top-Down Record", text="Read the record in order. Each branch accepts fruit only below a ceiling; a fruit too heavy for this branch is left for an ancestor's right side.",
               goal="Return the BST with this preorder."),
    spec=dict(method="bstFromPreorder", ret="TreeNode*", params=[["vector<int>&", "preorder"]]),
    tests=[dict(args=[[8, 5, 1, 7, 10, 12]], expected=[8, 5, 10, 1, 7, None, 12]), dict(args=[[1, 3]], expected=[1, None, 3])],
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="preorder", label="top-down record", pointers=["idx"]),
        dict(kind="values", vars=["ceiling"]),
    ]),
    reference="""class Solution {
public:
    int idx = 0;
    TreeNode* build(vector<int>& preorder, int ceiling) {
        if (idx == (int)preorder.size() || preorder[idx] > ceiling) return nullptr;
        TreeNode* node = new TreeNode(preorder[idx++]);
        node->left = build(preorder, node->val);
        node->right = build(preorder, ceiling);
        return node;
    }
    TreeNode* bstFromPreorder(vector<int>& preorder) {
        return build(preorder, INT_MAX);
    }
};""",
)

add(
    id=1010, slug="pairs-of-songs-with-total-durations-divisible-by-60", title="Pairs of Songs With Total Durations Divisible by 60", difficulty="Medium",
    world="arrays", tags=["array", "hash-table", "counting"],
    story=dict(title="Songs That Finish on the Minute", text="Each song's remainder mod 60 needs a partner with remainder 60 - r (or 0 with 0). Lockers count remainders seen so far.",
               goal="Return how many pairs have a total duration divisible by 60."),
    spec=dict(method="numPairsDivisibleBy60", ret="int", params=[["vector<int>&", "time"]]),
    tests=[dict(args=[[30, 20, 150, 100, 40]], expected=3), dict(args=[[60, 60, 60]], expected=3)],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="time", label="songs (seconds)", pointers=["i"]),
        dict(kind="array", var="cnt", label="remainders seen", style="tiles"),
        dict(kind="values", vars=["r", "pairs"]),
    ]),
    reference="""class Solution {
public:
    int numPairsDivisibleBy60(vector<int>& time) {
        vector<int> cnt(60, 0);
        int pairs = 0;
        for (int i = 0; i < (int)time.size(); i++) {
            int r = time[i] % 60;
            pairs += cnt[(60 - r) % 60];
            cnt[r]++;
        }
        return pairs;
    }
};""",
)

add(
    id=1013, slug="partition-array-into-three-parts-with-equal-sum", title="Partition Array Into Three Parts With Equal Sum", difficulty="Easy",
    world="arrays", tags=["array", "greedy"],
    story=dict(title="Three Fair Shares", text="Each share must weigh a third of the total. Walk the crates; every time the running weight reaches a share, cut and start the next.",
               goal="Return true if the array splits into three non-empty parts of equal sum."),
    spec=dict(method="canThreePartsEqualSum", ret="bool", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[0, 2, 1, -6, 6, -7, 9, 1, 2, 0, 1]], expected=True), dict(args=[[0, 2, 1, -6, 6, 7, 9, -1, 2, 0, 1]], expected=False), dict(args=[[3, 3, 6, 5, -2, 2, 5, 1, -9, 4]], expected=True)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="arr", label="crates", pointers=["i"]),
        dict(kind="values", vars=["share", "run", "parts"]),
    ]),
    reference="""class Solution {
public:
    bool canThreePartsEqualSum(vector<int>& arr) {
        int total = 0;
        for (int x : arr) total += x;
        if (total % 3) return false;
        int share = total / 3, run = 0, parts = 0;
        for (int i = 0; i < (int)arr.size(); i++) {
            run += arr[i];
            if (run == share && parts < 2) {
                parts++;
                run = 0;
            }
        }
        return parts == 2 && run == share;
    }
};""",
)

add(
    id=1014, slug="best-sightseeing-pair", title="Best Sightseeing Pair", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Two Viewpoints, Not Too Far Apart", text="A pair scores values[i] + i plus values[j] - j. Walking right, remember the best values[i] + i seen so far.",
               goal="Return the maximum score of a sightseeing pair."),
    spec=dict(method="maxScoreSightseeingPair", ret="int", params=[["vector<int>&", "values"]]),
    tests=[dict(args=[[8, 1, 5, 2, 6]], expected=11), dict(args=[[1, 2]], expected=2)],
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="values", label="viewpoints", pointers=["j"]),
        dict(kind="values", vars=["bestLeft", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxScoreSightseeingPair(vector<int>& values) {
        int bestLeft = values[0], best = INT_MIN;
        for (int j = 1; j < (int)values.size(); j++) {
            best = max(best, bestLeft + values[j] - j);
            bestLeft = max(bestLeft, values[j] + j);
        }
        return best;
    }
};""",
)

add(
    id=1019, slug="next-greater-node-in-linked-list", title="Next Greater Node In Linked List", difficulty="Medium", world="linked-list", tags=["array", "linked-list", "stack", "monotonic-stack"],
    story=dict(title="The Next Heavier Car", text="Walk the train numbering cars. Cars still waiting for a heavier car behind them wait on a tower; each new heavier car answers them.",
               goal="Return, for each node, the value of the next greater node (or 0)."),
    spec=dict(method="nextLargerNodes", ret="vector<int>", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[2, 1, 5]], expected=[5, 5, 0]), dict(args=[[2, 7, 4, 3, 5]], expected=[7, 0, 5, 5, 0])],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "cur"], heads=["head"], label="train"),
        dict(kind="stack", var="st", label="waiting (position)"),
        dict(kind="array", var="res", label="answers", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> nextLargerNodes(ListNode* head) {
        vector<int> vals, res;
        stack<int> st;
        int i = 0;
        for (ListNode* cur = head; cur; cur = cur->next, i++) {
            vals.push_back(cur->val);
            res.push_back(0);
            while (!st.empty() && vals[st.top()] < cur->val) {
                res[st.top()] = cur->val;
                st.pop();
            }
            st.push(i);
        }
        return res;
    }
};""",
)

add(
    id=1026, slug="maximum-difference-between-node-and-ancestor", title="Maximum Difference Between Node and Ancestor", difficulty="Medium",
    world="trees", tags=["tree", "dfs"],
    story=dict(title="The Biggest Drop Down a Branch", text="Climbing down, carry the lightest and heaviest fruit seen on this path. At each fruit, the gap to either is a candidate.",
               goal="Return the maximum |ancestor - node|."),
    spec=dict(method="maxAncestorDiff", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13]], expected=7), dict(args=[[1, None, 2, None, 0, 3]], expected=3)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["lo", "hi", "best"]),
    ]),
    reference="""class Solution {
public:
    int best = 0;
    void walk(TreeNode* node, int lo, int hi) {
        if (!node) return;
        best = max({best, abs(node->val - lo), abs(node->val - hi)});
        lo = min(lo, node->val);
        hi = max(hi, node->val);
        walk(node->left, lo, hi);
        walk(node->right, lo, hi);
    }
    int maxAncestorDiff(TreeNode* root) {
        walk(root, root->val, root->val);
        return best;
    }
};""",
)

add(
    id=1035, slug="uncrossed-lines", title="Uncrossed Lines", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Strings Between Two Rows", text="Matching numbers can be joined by a string, but strings can't cross. That's a longest common subsequence: each cell keeps the best for two prefixes.",
               goal="Return the maximum number of non-crossing connecting lines."),
    spec=dict(method="maxUncrossedLines", ret="int", params=[["vector<int>&", "nums1"], ["vector<int>&", "nums2"]]),
    tests=[dict(args=[[1, 4, 2], [1, 2, 4]], expected=2), dict(args=[[2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2]], expected=3)],
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[dict(kind="array", var="nums1", label="top row"), dict(kind="array", var="nums2", label="bottom row")]),
        dict(kind="grid", var="dp", palette="dp", label="best lines", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    int maxUncrossedLines(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size(), m = nums2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                dp[i][j] = nums1[i - 1] == nums2[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
        return dp[n][m];
    }
};""",
)

add(
    id=1039, slug="minimum-score-triangulation-of-polygon", title="Minimum Score Triangulation of Polygon", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Cutting the Polygon Rug", text="For every stretch of corners i..j, try each corner k between them as the third corner of the triangle on edge (i, j), plus the best cuts on each side.",
               goal="Return the minimum total score of a triangulation."),
    spec=dict(method="minScoreTriangulation", ret="int", params=[["vector<int>&", "values"]]),
    tests=[dict(args=[[1, 2, 3]], expected=6), dict(args=[[3, 7, 4, 5]], expected=144), dict(args=[[1, 3, 1, 4, 1, 5]], expected=13)],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="values", label="corners", pointers=["i", "k", "j"]),
        dict(kind="grid", var="dp", palette="dp", label="best for corners i..j", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    int minScoreTriangulation(vector<int>& values) {
        int n = values.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int len = 3; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                dp[i][j] = INT_MAX;
                for (int k = i + 1; k < j; k++) dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + values[i] * values[k] * values[j]);
            }
        }
        return dp[0][n - 1];
    }
};""",
)

add(
    id=1041, slug="robot-bounded-in-circle", title="Robot Bounded In Circle", difficulty="Medium", world="greedy", tags=["math", "string", "simulation"],
    story=dict(title="The Looping Robot", text="Run the instructions once. If the robot is back home, or facing a new direction, repeating them keeps it within a circle.",
               goal="Return true if the robot stays in a bounded circle."),
    spec=dict(method="isRobotBounded", ret="bool", params=[["string", "instructions"]]),
    tests=[dict(args=["GGLLGG"], expected=True), dict(args=["GG"], expected=False), dict(args=["GL"], expected=True)],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="instructions", label="instructions", pointers=["i"]),
        dict(kind="values", vars=["x", "y", "dir"]),
    ]),
    reference="""class Solution {
public:
    bool isRobotBounded(string instructions) {
        int x = 0, y = 0, dir = 0;
        int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};
        for (int i = 0; i < (int)instructions.size(); i++) {
            char c = instructions[i];
            if (c == 'G') {
                x += dx[dir];
                y += dy[dir];
            } else if (c == 'L') {
                dir = (dir + 3) % 4;
            } else {
                dir = (dir + 1) % 4;
            }
        }
        return (x == 0 && y == 0) || dir != 0;
    }
};""",
)

add(
    id=1043, slug="partition-array-for-maximum-sum", title="Partition Array for Maximum Sum", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Levelling Up Short Stretches", text="Cut the row into pieces of at most k; every crate in a piece becomes the piece's heaviest. The ledger tries every last-piece length.",
               goal="Return the largest sum after partitioning."),
    spec=dict(method="maxSumAfterPartitioning", ret="int", params=[["vector<int>&", "arr"], ["int", "k"]]),
    tests=[dict(args=[[1, 15, 7, 9, 2, 5, 10], 3], expected=84), dict(args=[[1, 4, 1, 5, 7, 3, 6, 1, 9, 9, 3], 4], expected=83), dict(args=[[1], 1], expected=1)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="arr", label="crates", pointers=["i"]),
        dict(kind="array", var="dp", label="best sum for prefix", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["len", "top"]),
    ]),
    reference="""class Solution {
public:
    int maxSumAfterPartitioning(vector<int>& arr, int k) {
        int n = arr.size();
        vector<int> dp(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            int top = 0;
            for (int len = 1; len <= k && len <= i; len++) {
                top = max(top, arr[i - len]);
                dp[i] = max(dp[i], dp[i - len] + top * len);
            }
        }
        return dp[n];
    }
};""",
)

add(
    id=1048, slug="longest-string-chain", title="Longest String Chain", difficulty="Medium", world="dp", tags=["array", "hash-table", "two-pointers", "string", "dynamic-programming", "sorting"],
    story=dict(title="Growing Words One Letter at a Time", text="Words are sorted by length. Each word tries removing one letter at a time; if the shorter word is in the lockers, its chain extends by one.",
               goal="Return the length of the longest word chain."),
    spec=dict(method="longestStrChain", ret="int", params=[["vector<string>&", "words"]]),
    tests=[dict(args=[["a", "b", "ba", "bca", "bda", "bdca"]], expected=4), dict(args=[["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]], expected=5), dict(args=[["abcd", "dbqca"]], expected=1)],
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="words", label="words (by length)", style="tiles", pointers=["k"]),
        dict(kind="map", var="chain", label="longest chain ending in"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int longestStrChain(vector<string>& words) {
        sort(words.begin(), words.end(), [](const string& a, const string& b) { return a.size() < b.size(); });
        map<string, int> chain;
        int best = 0;
        for (int k = 0; k < (int)words.size(); k++) {
            string& w = words[k];
            int cur = 1;
            for (int i = 0; i < (int)w.size(); i++) {
                string shorter = w.substr(0, i) + w.substr(i + 1);
                if (chain.count(shorter)) cur = max(cur, chain[shorter] + 1);
            }
            chain[w] = cur;
            best = max(best, cur);
        }
        return best;
    }
};""",
)

add(
    id=1049, slug="last-stone-weight-ii", title="Last Stone Weight II", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Two Piles of Stones", text="Smashing stones really splits them into two piles and subtracts. Find the pile weight closest to half the total that is reachable.",
               goal="Return the smallest possible weight of the last stone."),
    spec=dict(method="lastStoneWeightII", ret="int", params=[["vector<int>&", "stones"]]),
    tests=[dict(args=[[2, 7, 4, 1, 8, 1]], expected=1), dict(args=[[31, 26, 33, 21, 40]], expected=5)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="stones", label="stones", pointers=["k"]),
        dict(kind="array", var="can", label="reachable pile weights", style="tiles", pointers=["s"]),
    ]),
    reference="""class Solution {
public:
    int lastStoneWeightII(vector<int>& stones) {
        int total = 0;
        for (int x : stones) total += x;
        int half = total / 2;
        vector<bool> can(half + 1, false);
        can[0] = true;
        for (int k = 0; k < (int)stones.size(); k++)
            for (int s = half; s >= stones[k]; s--)
                if (can[s - stones[k]]) can[s] = true;
        for (int s = half; s >= 0; s--)
            if (can[s]) return total - 2 * s;
        return total;
    }
};""",
)

add(
    id=1051, slug="height-checker", title="Height Checker", difficulty="Easy", world="arrays", tags=["array", "sorting", "counting-sort"],
    story=dict(title="Who's Out of Line?", text="Sort a copy of the line by height, then count the students not standing where the sorted line says.",
               goal="Return how many students are out of place."),
    spec=dict(method="heightChecker", ret="int", params=[["vector<int>&", "heights"]]),
    tests=[dict(args=[[1, 1, 4, 2, 1, 3]], expected=3), dict(args=[[5, 1, 2, 3, 4]], expected=5), dict(args=[[1, 2, 3, 4, 5]], expected=0)],
    scene=dict(theme="castle", layers=[
        dict(kind="bars", var="heights", label="line now", pointers=["i"]),
        dict(kind="bars", var="sorted", label="line sorted", pointers=["i"]),
        dict(kind="values", vars=["wrong"]),
    ]),
    reference="""class Solution {
public:
    int heightChecker(vector<int>& heights) {
        vector<int> sorted = heights;
        sort(sorted.begin(), sorted.end());
        int wrong = 0;
        for (int i = 0; i < (int)heights.size(); i++) wrong += heights[i] != sorted[i];
        return wrong;
    }
};""",
)

add(
    id=1052, slug="grumpy-bookstore-owner", title="Grumpy Bookstore Owner", difficulty="Medium", world="sliding-window", tags=["array", "sliding-window"],
    story=dict(title="The Owner's Calm Minutes", text="Happy customers in non-grumpy minutes always count. A window of `minutes` slides along adding the grumpy-minute customers it would rescue.",
               goal="Return the maximum number of satisfied customers."),
    spec=dict(method="maxSatisfied", ret="int", params=[["vector<int>&", "customers"], ["vector<int>&", "grumpy"], ["int", "minutes"]]),
    tests=[dict(args=[[1, 0, 1, 2, 1, 1, 7, 5], [0, 1, 0, 1, 0, 1, 0, 1], 3], expected=16), dict(args=[[1], [0], 1], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="customers", label="customers per minute", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="array", var="grumpy", label="grumpy?", style="tiles"),
        dict(kind="values", vars=["base", "extra", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxSatisfied(vector<int>& customers, vector<int>& grumpy, int minutes) {
        int base = 0, extra = 0, best = 0;
        for (int r = 0; r < (int)customers.size(); r++) {
            if (!grumpy[r]) base += customers[r];
            else extra += customers[r];
            int l = r - minutes + 1;
            if (l > 0 && grumpy[l - 1]) extra -= customers[l - 1];
            best = max(best, extra);
        }
        return base + best;
    }
};""",
)

add(
    id=1071, slug="greatest-common-divisor-of-strings", title="Greatest Common Divisor of Strings", difficulty="Easy", world="arrays", tags=["math", "string"],
    story=dict(title="The Largest Shared Tile", text="Two walls are built from the same tile only if a+b equals b+a. Then the tile is as long as the gcd of their lengths.",
               goal="Return the largest string dividing both, or \"\"."),
    spec=dict(method="gcdOfStrings", ret="string", params=[["string", "str1"], ["string", "str2"]]),
    tests=[dict(args=["ABCABC", "ABC"], expected="ABC"), dict(args=["ABABAB", "ABAB"], expected="AB"), dict(args=["LEET", "CODE"], expected="")],
    visualTest=1,
    scene=dict(theme="lab", layers=[dict(kind="values", vars=["a", "b", "g"])]),
    reference="""class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        if (str1 + str2 != str2 + str1) return "";
        int a = str1.size(), b = str2.size();
        while (b) {
            int t = a % b;
            a = b;
            b = t;
        }
        int g = a;
        return str1.substr(0, g);
    }
};""",
)

add(
    id=1079, slug="letter-tile-possibilities", title="Letter Tile Possibilities", difficulty="Medium", world="backtracking", tags=["hash-table", "string", "backtracking", "counting"],
    story=dict(title="Every Word from the Tile Bag", text="At each door, take any letter still in the bag: that's one more word, then go deeper and put the tile back.",
               goal="Return the number of non-empty sequences you can make."),
    spec=dict(method="numTilePossibilities", ret="int", params=[["string", "tiles"]]),
    tests=[dict(args=["AAB"], expected=8), dict(args=["AAABBC"], expected=188), dict(args=["V"], expected=1)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="cnt", label="tiles left A..Z", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int go(vector<int>& cnt) {
        int total = 0;
        for (int i = 0; i < 26; i++) {
            if (cnt[i] == 0) continue;
            total++;
            cnt[i]--;
            total += go(cnt);
            cnt[i]++;
        }
        return total;
    }
    int numTilePossibilities(string tiles) {
        vector<int> cnt(26, 0);
        for (char c : tiles) cnt[c - 'A']++;
        return go(cnt);
    }
};""",
)

add(
    id=1089, slug="duplicate-zeros", title="Duplicate Zeros", difficulty="Easy", world="two-pointers", tags=["array", "two-pointers"],
    story=dict(title="Stretching the Shelf", text="Every empty crate (0) is doubled, pushing the rest right off the end. Count where things will land, then fill from the back so nothing is overwritten early.",
               goal="Duplicate each zero in place, shifting the rest right."),
    spec=dict(method="duplicateZeros", ret="void", params=[["vector<int>&", "arr"]], output="param:0"),
    tests=[dict(args=[[1, 0, 2, 3, 0, 4, 5, 0]], expected=[1, 0, 0, 2, 3, 0, 0, 4]), dict(args=[[1, 2, 3]], expected=[1, 2, 3])],
    scene=dict(theme="dock", layers=[dict(kind="array", var="arr", label="shelf", pointers=["i", "w"])]),
    reference="""class Solution {
public:
    void duplicateZeros(vector<int>& arr) {
        int n = arr.size(), zeros = 0;
        for (int x : arr) zeros += x == 0;
        for (int i = n - 1, w = n + zeros - 1; i >= 0; i--, w--) {
            if (w < n) arr[w] = arr[i];
            if (arr[i] == 0) {
                w--;
                if (w < n) arr[w] = 0;
            }
        }
    }
};""",
)

add(
    id=1103, slug="distribute-candies-to-people", title="Distribute Candies to People", difficulty="Easy", world="arrays", tags=["math", "simulation"],
    story=dict(title="Handing Out Ever More Candy", text="Going round the circle, each turn hands out one more candy than the last, until the bag runs out; the last person gets whatever is left.",
               goal="Return how many candies each person ends up with."),
    spec=dict(method="distributeCandies", ret="vector<int>", params=[["int", "candies"], ["int", "num_people"]]),
    tests=[dict(args=[7, 4], expected=[1, 2, 3, 1]), dict(args=[10, 3], expected=[5, 2, 3])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="res", label="candies per person", style="tiles", pointers=["p"]),
        dict(kind="values", vars=["give", "candies"]),
    ]),
    reference="""class Solution {
public:
    vector<int> distributeCandies(int candies, int num_people) {
        vector<int> res(num_people, 0);
        int give = 1, p = 0;
        while (candies > 0) {
            int g = min(give, candies);
            res[p] += g;
            candies -= g;
            give++;
            p = (p + 1) % num_people;
        }
        return res;
    }
};""",
)

add(
    id=1110, slug="delete-nodes-and-return-forest", title="Delete Nodes And Return Forest", difficulty="Medium", world="trees", tags=["array", "hash-table", "tree", "dfs"],
    story=dict(title="Felling Trees in the Orchard", text="Each marked fruit is cut out. Its surviving branches become new trees in the forest; a fruit whose parent was cut becomes a root.",
               goal="Return the roots of the remaining forest (any order)."),
    spec=dict(method="delNodes", ret="vector<TreeNode*>", params=[["TreeNode*", "root"], ["vector<int>&", "to_delete"]]),
    compare="unordered",
    tests=[dict(args=[[1, 2, 3, 4, 5, 6, 7], [3, 5]], expected=[[1, 2, None, 4], [6], [7]]), dict(args=[[1, 2, 4, None, 3], [3]], expected=[[1, 2, 4]])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="set", var="cut", label="to cut"),
        dict(kind="values", vars=["isRoot"]),
    ]),
    reference="""class Solution {
public:
    set<int> cut;
    vector<TreeNode*> forest;
    TreeNode* walk(TreeNode* node, bool isRoot) {
        if (!node) return nullptr;
        bool gone = cut.count(node->val);
        if (isRoot && !gone) forest.push_back(node);
        node->left = walk(node->left, gone);
        node->right = walk(node->right, gone);
        return gone ? nullptr : node;
    }
    vector<TreeNode*> delNodes(TreeNode* root, vector<int>& to_delete) {
        cut = set<int>(to_delete.begin(), to_delete.end());
        walk(root, true);
        return forest;
    }
};""",
)
