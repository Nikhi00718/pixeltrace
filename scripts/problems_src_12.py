"""Twelfth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=105, slug="construct-binary-tree-from-preorder-and-inorder-traversal", title="Construct Binary Tree from Preorder and Inorder Traversal",
    difficulty="Medium", world="trees", tags=["array", "hash-table", "divide-and-conquer", "tree"],
    story=dict(
        title="Replanting the Orchard from Two Records",
        text="One record lists fruit top-down (preorder), the other left-to-right (inorder). The next preorder fruit is "
             "always the root of the current stretch; its place in the inorder record splits the stretch into left and "
             "right branches.",
        goal="Rebuild the tree and return its root.",
    ),
    spec=dict(method="buildTree", ret="TreeNode*", params=[["vector<int>&", "preorder"], ["vector<int>&", "inorder"]]),
    tests=[dict(args=[[3, 9, 20, 15, 7], [9, 3, 15, 20, 7]], expected=[3, 9, 20, None, None, 15, 7]), dict(args=[[-1], [-1]], expected=[-1])],
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="preorder", label="top-down record", pointers=["pre"]),
        dict(kind="array", var="inorder", label="left-to-right record", pointers=["lo", "mid", "hi"], window=["lo", "hi"]),
    ]),
    reference="""class Solution {
public:
    int pre = 0;
    map<int, int> where;
    TreeNode* build(vector<int>& preorder, int lo, int hi) {
        if (lo > hi) return nullptr;
        TreeNode* node = new TreeNode(preorder[pre++]);
        int mid = where[node->val];
        node->left = build(preorder, lo, mid - 1);
        node->right = build(preorder, mid + 1, hi);
        return node;
    }
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        for (int i = 0; i < (int)inorder.size(); i++) where[inorder[i]] = i;
        return build(preorder, 0, inorder.size() - 1);
    }
};""",
)

add(
    id=108, slug="convert-sorted-array-to-binary-search-tree", title="Convert Sorted Array to Binary Search Tree", difficulty="Easy",
    world="trees", tags=["array", "divide-and-conquer", "tree", "bst"],
    story=dict(
        title="Planting a Balanced Orchard",
        text="Sorted fruit weights are planted so the tree stays balanced: the middle weight becomes the root, and each "
             "half is planted the same way as its branch.",
        goal="Return a height-balanced BST built from the sorted array.",
    ),
    spec=dict(method="sortedArrayToBST", ret="TreeNode*", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[-10, -3, 0, 5, 9]], expected=[0, -10, 5, None, -3, None, 9]), dict(args=[[1, 3]], expected=[1, None, 3])],
    scene=dict(theme="forest", layers=[dict(kind="array", var="nums", label="sorted weights", pointers=["lo", "mid", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    TreeNode* build(vector<int>& nums, int lo, int hi) {
        if (lo > hi) return nullptr;
        int mid = (lo + hi) / 2;
        TreeNode* node = new TreeNode(nums[mid]);
        node->left = build(nums, lo, mid - 1);
        node->right = build(nums, mid + 1, hi);
        return node;
    }
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        return build(nums, 0, nums.size() - 1);
    }
};""",
    hints=["Several balanced trees are valid on LeetCode; these tests expect the lower-middle root, mid = (lo + hi) / 2."],
)

add(
    id=114, slug="flatten-binary-tree-to-linked-list", title="Flatten Binary Tree to Linked List", difficulty="Medium", world="trees",
    tags=["linked-list", "stack", "tree", "dfs"],
    story=dict(
        title="Training the Vine",
        text="The gardener wants every fruit on one long right-hand vine in preorder. At each fruit with a left branch, "
             "they find that branch's rightmost fruit, hang the right branch from it, and swing the left branch over.",
        goal="Flatten the tree in place into a right-only chain.",
    ),
    spec=dict(method="flatten", ret="void", params=[["TreeNode*", "root"]], output="param:0"),
    tests=[dict(args=[[1, 2, 5, 3, 4, None, 6]], expected=[1, None, 2, None, 3, None, 4, None, 5, None, 6]), dict(args=[[]], expected=[]), dict(args=[[0]], expected=[0])],
    scene=dict(theme="forest", layers=[dict(kind="tree", var="root", pointers=["cur", "tail"], label="orchard")]),
    reference="""class Solution {
public:
    void flatten(TreeNode* root) {
        TreeNode* cur = root;
        while (cur) {
            if (cur->left) {
                TreeNode* tail = cur->left;
                while (tail->right) tail = tail->right;
                tail->right = cur->right;
                cur->right = cur->left;
                cur->left = nullptr;
            }
            cur = cur->right;
        }
    }
};""",
)

add(
    id=124, slug="binary-tree-maximum-path-sum", title="Binary Tree Maximum Path Sum", difficulty="Hard", world="trees",
    tags=["dynamic-programming", "tree", "dfs"],
    story=dict(
        title="The Richest Vine",
        text="A vine may bend once at any fruit. Each fruit asks both branches for their best downward gain (ignoring "
             "negative ones); the fruit plus both gains is a candidate vine, and it reports itself plus the better gain "
             "upward.",
        goal="Return the maximum path sum.",
    ),
    spec=dict(method="maxPathSum", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3]], expected=6), dict(args=[[-10, 9, 20, None, None, 15, 7]], expected=42), dict(args=[[-3]], expected=-3)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["l", "r", "best"]),
    ]),
    reference="""class Solution {
public:
    int best = INT_MIN;
    int gain(TreeNode* node) {
        if (!node) return 0;
        int l = max(0, gain(node->left));
        int r = max(0, gain(node->right));
        best = max(best, node->val + l + r);
        return node->val + max(l, r);
    }
    int maxPathSum(TreeNode* root) {
        gain(root);
        return best;
    }
};""",
)

add(
    id=129, slug="sum-root-to-leaf-numbers", title="Sum Root to Leaf Numbers", difficulty="Medium", world="trees", tags=["tree", "dfs"],
    story=dict(
        title="Number Trails",
        text="Every fruit is a digit. Climbing down, the squirrel's number grows by one digit per fruit; each leaf adds the "
             "finished number to the total.",
        goal="Return the sum of all root-to-leaf numbers.",
    ),
    spec=dict(method="sumNumbers", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3]], expected=25), dict(args=[[4, 9, 0, 5, 1]], expected=1026)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["cur", "total"]),
    ]),
    reference="""class Solution {
public:
    int total = 0;
    void walk(TreeNode* node, int cur) {
        if (!node) return;
        cur = cur * 10 + node->val;
        if (!node->left && !node->right) total += cur;
        walk(node->left, cur);
        walk(node->right, cur);
    }
    int sumNumbers(TreeNode* root) {
        walk(root, 0);
        return total;
    }
};""",
)

add(
    id=137, slug="single-number-ii", title="Single Number II", difficulty="Medium", world="bits", tags=["array", "bit-manipulation"],
    story=dict(
        title="Counting Lamps in Threes",
        text="Every number appears three times except one. For each lamp position, count how many numbers light it; "
             "counts that aren't a multiple of three belong to the lonely number.",
        goal="Return the element that appears once.",
    ),
    spec=dict(method="singleNumber", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 2, 3, 2]], expected=3), dict(args=[[0, 1, 0, 1, 0, 1, 99]], expected=99), dict(args=[[-2, -2, 1, 1, 4, 1, 4, 4, -4, -2]], expected=-4)],
    visualTest=1,
    scene=dict(theme="space", layers=[
        dict(kind="array", var="nums", label="numbers"),
        dict(kind="values", vars=["bit", "cnt", "res"]),
    ]),
    reference="""class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int res = 0;
        for (int bit = 0; bit < 32; bit++) {
            int cnt = 0;
            for (int x : nums) cnt += (x >> bit) & 1;
            if (cnt % 3) res |= (1u << bit);
        }
        return res;
    }
};""",
)

add(
    id=139, slug="word-break", title="Word Break", difficulty="Medium", world="dp", tags=["array", "hash-table", "string", "dynamic-programming", "trie"],
    story=dict(
        title="Cutting the Banner into Words",
        text="The ledger marks every prefix of the banner that can be cut into dictionary words. A prefix is good if some "
             "earlier good cut is followed by a dictionary word up to here.",
        goal="Return true if s can be split into dictionary words.",
    ),
    spec=dict(method="wordBreak", ret="bool", params=[["string", "s"], ["vector<string>&", "wordDict"]]),
    tests=[dict(args=["leetcode", ["leet", "code"]], expected=True), dict(args=["applepenapple", ["apple", "pen"]], expected=True),
           dict(args=["catsandog", ["cats", "dog", "sand", "and", "cat"]], expected=False)],
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="banner", pointers=["j", "i"], window=["j", "i"], windowExclusive=True),
        dict(kind="array", var="ok", label="good cut after", style="tiles", pointers=["i"]),
        dict(kind="set", var="dict", label="dictionary"),
    ]),
    reference="""class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        set<string> dict(wordDict.begin(), wordDict.end());
        int n = s.size();
        vector<bool> ok(n + 1, false);
        ok[0] = true;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (ok[j] && dict.count(s.substr(j, i - j))) {
                    ok[i] = true;
                    break;
                }
            }
        }
        return ok[n];
    }
};""",
)

add(
    id=148, slug="sort-list", title="Sort List", difficulty="Medium", world="linked-list", tags=["linked-list", "two-pointers", "divide-and-conquer", "sorting", "merge-sort"],
    story=dict(
        title="Merge-Sorting the Train",
        text="The train is cut in half at the middle, each half is sorted the same way behind its own door, and the two "
             "sorted halves are zipped back together.",
        goal="Return the list sorted in ascending order.",
    ),
    spec=dict(method="sortList", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[4, 2, 1, 3]], expected=[1, 2, 3, 4]), dict(args=[[-1, 5, 3, 4, 0]], expected=[-1, 0, 3, 4, 5]), dict(args=[[]], expected=[])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "slow", "fast", "a", "b", "tail"], heads=["head"], label="yard")]),
    reference="""class Solution {
public:
    ListNode* mergeLists(ListNode* a, ListNode* b) {
        ListNode dummy;
        ListNode* tail = &dummy;
        while (a && b) {
            if (a->val <= b->val) {
                tail->next = a;
                a = a->next;
            } else {
                tail->next = b;
                b = b->next;
            }
            tail = tail->next;
        }
        tail->next = a ? a : b;
        return dummy.next;
    }
    ListNode* sortList(ListNode* head) {
        if (!head || !head->next) return head;
        ListNode* slow = head;
        ListNode* fast = head->next;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode* right = slow->next;
        slow->next = nullptr;
        return mergeLists(sortList(head), sortList(right));
    }
};""",
)

add(
    id=165, slug="compare-version-numbers", title="Compare Version Numbers", difficulty="Medium", world="two-pointers", tags=["two-pointers", "string"],
    story=dict(
        title="Which Release Is Newer?",
        text="Two clerks read version labels part by part, each turning the digits up to the next dot into a number. The "
             "first part that differs decides; missing parts count as 0.",
        goal="Return -1, 0 or 1 comparing version1 with version2.",
    ),
    spec=dict(method="compareVersion", ret="int", params=[["string", "version1"], ["string", "version2"]]),
    tests=[dict(args=["1.2", "1.10"], expected=-1), dict(args=["1.01", "1.001"], expected=0), dict(args=["1.0", "1.0.0.0"], expected=0), dict(args=["1.0.1", "1"], expected=1)],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="version1", label="version 1", pointers=["i"]),
        dict(kind="string", var="version2", label="version 2", pointers=["j"]),
        dict(kind="values", vars=["a", "b"]),
    ]),
    reference="""class Solution {
public:
    int compareVersion(string version1, string version2) {
        int i = 0, j = 0, n = version1.size(), m = version2.size();
        while (i < n || j < m) {
            long long a = 0, b = 0;
            while (i < n && version1[i] != '.') a = a * 10 + (version1[i++] - '0');
            while (j < m && version2[j] != '.') b = b * 10 + (version2[j++] - '0');
            if (a < b) return -1;
            if (a > b) return 1;
            i++;
            j++;
        }
        return 0;
    }
};""",
)

add(
    id=168, slug="excel-sheet-column-title", title="Excel Sheet Column Title", difficulty="Easy", world="bits", tags=["math", "string"],
    story=dict(
        title="Labelling the Ledger Columns",
        text="Column letters count in base 26 with no zero: A is 1 and Z is 26. Shift down by one, peel off the last "
             "letter, and divide, until nothing is left.",
        goal="Return the column title for a column number.",
    ),
    spec=dict(method="convertToTitle", ret="string", params=[["int", "columnNumber"]]),
    tests=[dict(args=[1], expected="A"), dict(args=[28], expected="AB"), dict(args=[701], expected="ZY")],
    visualTest=2,
    scene=dict(theme="lab", layers=[dict(kind="values", vars=["columnNumber", "res"])]),
    reference="""class Solution {
public:
    string convertToTitle(int columnNumber) {
        string res;
        while (columnNumber > 0) {
            columnNumber--;
            res.push_back('A' + columnNumber % 26);
            columnNumber /= 26;
        }
        reverse(res.begin(), res.end());
        return res;
    }
};""",
)

add(
    id=171, slug="excel-sheet-column-number", title="Excel Sheet Column Number", difficulty="Easy", world="bits", tags=["math", "string"],
    story=dict(
        title="Reading the Column Label",
        text="Read the label left to right: multiply the running number by 26 and add the letter's position.",
        goal="Return the column number for a title.",
    ),
    spec=dict(method="titleToNumber", ret="int", params=[["string", "columnTitle"]]),
    tests=[dict(args=["A"], expected=1), dict(args=["AB"], expected=28), dict(args=["ZY"], expected=701)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="columnTitle", label="label", pointers=["i"]),
        dict(kind="values", vars=["num"]),
    ]),
    reference="""class Solution {
public:
    int titleToNumber(string columnTitle) {
        long long num = 0;
        for (int i = 0; i < (int)columnTitle.size(); i++) num = num * 26 + (columnTitle[i] - 'A' + 1);
        return num;
    }
};""",
)

add(
    id=172, slug="factorial-trailing-zeroes", title="Factorial Trailing Zeroes", difficulty="Medium", world="bits", tags=["math"],
    story=dict(
        title="Counting the Fives",
        text="Every trailing zero needs a pair of 2 and 5, and fives are rarer. Count the multiples of 5, then of 25, then "
             "125, and so on.",
        goal="Return the number of trailing zeroes in n!.",
    ),
    spec=dict(method="trailingZeroes", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[3], expected=0), dict(args=[5], expected=1), dict(args=[130], expected=32)],
    visualTest=2,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n", "zeros"])]),
    reference="""class Solution {
public:
    int trailingZeroes(int n) {
        int zeros = 0;
        while (n > 0) {
            n /= 5;
            zeros += n;
        }
        return zeros;
    }
};""",
)

add(
    id=179, slug="largest-number", title="Largest Number", difficulty="Medium", world="greedy", tags=["array", "string", "greedy", "sorting"],
    story=dict(
        title="Lining Up Number Cards",
        text="Number cards are arranged to spell the biggest number. Card a goes before card b whenever a followed by b "
             "reads bigger than b followed by a.",
        goal="Return the largest number as a string.",
    ),
    spec=dict(method="largestNumber", ret="string", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[10, 2]], expected="210"), dict(args=[[3, 30, 34, 5, 9]], expected="9534330"), dict(args=[[0, 0]], expected="0")],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="cards", label="cards (sorted)", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["res"]),
    ]),
    reference="""class Solution {
public:
    string largestNumber(vector<int>& nums) {
        vector<string> cards;
        for (int x : nums) cards.push_back(to_string(x));
        sort(cards.begin(), cards.end(), [](const string& a, const string& b) { return a + b > b + a; });
        if (cards[0] == "0") return "0";
        string res;
        for (int i = 0; i < (int)cards.size(); i++) res += cards[i];
        return res;
    }
};""",
)

add(
    id=187, slug="repeated-dna-sequences", title="Repeated DNA Sequences", difficulty="Medium", world="sliding-window",
    tags=["hash-table", "string", "bit-manipulation", "sliding-window", "rolling-hash"],
    story=dict(
        title="Spotting Repeated Gene Strips",
        text="A ten-letter window slides along the DNA strand. Every strip it sees goes into the lockers; a strip seen a "
             "second time is written down once.",
        goal="Return every 10-letter sequence that occurs more than once (any order).",
    ),
    spec=dict(method="findRepeatedDnaSequences", ret="vector<string>", params=[["string", "s"]]),
    compare="unordered",
    tests=[dict(args=["AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"], expected=["AAAAACCCCC", "CCCCCAAAAA"]), dict(args=["AAAAAAAAAAAAA"], expected=["AAAAAAAAAA"])],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="strand", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="map", var="seen", label="strips seen"),
    ]),
    reference="""class Solution {
public:
    vector<string> findRepeatedDnaSequences(string s) {
        map<string, int> seen;
        vector<string> res;
        for (int r = 9; r < (int)s.size(); r++) {
            int l = r - 9;
            string strip = s.substr(l, 10);
            if (++seen[strip] == 2) res.push_back(strip);
        }
        return res;
    }
};""",
)

add(
    id=190, slug="reverse-bits", title="Reverse Bits", difficulty="Easy", world="bits", tags=["divide-and-conquer", "bit-manipulation"],
    story=dict(
        title="Mirroring the Lamp Row",
        text="Take the lamps off the right end of the row one at a time and put each onto the right end of a new row, so "
             "the new row is the mirror image.",
        goal="Reverse the 32 bits of n.",
    ),
    spec=dict(method="reverseBits", ret="uint32_t", params=[["uint32_t", "n"]]),
    tests=[dict(args=[43261596], expected=964176192), dict(args=[4294967293], expected=3221225471)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n", "res", "k"])]),
    reference="""class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t res = 0;
        for (int k = 0; k < 32; k++) {
            res = (res << 1) | (n & 1);
            n >>= 1;
        }
        return res;
    }
};""",
)

add(
    id=201, slug="bitwise-and-of-numbers-range", title="Bitwise AND of Numbers Range", difficulty="Medium", world="bits", tags=["bit-manipulation"],
    story=dict(
        title="The Shared Lamp Prefix",
        text="ANDing every number from left to right keeps only the lamps they all share: the common prefix. Shift both "
             "ends right until they agree, then shift back.",
        goal="Return the AND of all numbers in [left, right].",
    ),
    spec=dict(method="rangeBitwiseAnd", ret="int", params=[["int", "left"], ["int", "right"]]),
    tests=[dict(args=[5, 7], expected=4), dict(args=[0, 0], expected=0), dict(args=[1, 2147483647], expected=0)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["left", "right", "shift"])]),
    reference="""class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        int shift = 0;
        while (left < right) {
            left >>= 1;
            right >>= 1;
            shift++;
        }
        return left << shift;
    }
};""",
)

add(
    id=202, slug="happy-number", title="Happy Number", difficulty="Easy", world="arrays", tags=["hash-table", "math", "two-pointers"],
    story=dict(
        title="The Digit-Square Walk",
        text="Replace a number by the sum of the squares of its digits, again and again. Every number visited goes into "
             "the lockers; reaching 1 is happy, revisiting a locker means an endless loop.",
        goal="Return true if n is a happy number.",
    ),
    spec=dict(method="isHappy", ret="bool", params=[["int", "n"]]),
    tests=[dict(args=[19], expected=True), dict(args=[2], expected=False), dict(args=[7], expected=True)],
    scene=dict(theme="market", layers=[
        dict(kind="set", var="seen", label="numbers visited", lookup=["n"]),
        dict(kind="values", vars=["n", "next"]),
    ]),
    reference="""class Solution {
public:
    bool isHappy(int n) {
        set<int> seen;
        while (n != 1 && !seen.count(n)) {
            seen.insert(n);
            int next = 0;
            while (n > 0) {
                next += (n % 10) * (n % 10);
                n /= 10;
            }
            n = next;
        }
        return n == 1;
    }
};""",
)

add(
    id=204, slug="count-primes", title="Count Primes", difficulty="Medium", world="arrays", tags=["array", "math", "enumeration", "number-theory"],
    story=dict(
        title="The Sieve Field",
        text="Every plot below n starts marked prime. Walking up, each prime still standing crosses out all its multiples "
             "from its own square onward.",
        goal="Return the number of primes less than n.",
    ),
    spec=dict(method="countPrimes", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[10], expected=4), dict(args=[0], expected=0), dict(args=[30], expected=10)],
    visualTest=2,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="prime", label="still prime?", style="tiles", pointers=["p", "m"]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int countPrimes(int n) {
        if (n < 3) return 0;
        vector<bool> prime(n, true);
        prime[0] = prime[1] = false;
        for (int p = 2; p * p < n; p++) {
            if (!prime[p]) continue;
            for (int m = p * p; m < n; m += p) prime[m] = false;
        }
        int count = 0;
        for (bool b : prime) count += b;
        return count;
    }
};""",
)

add(
    id=210, slug="course-schedule-ii", title="Course Schedule II", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "graph", "topological-sort"],
    story=dict(
        title="Ordering the Quests",
        text="Every quest records how many prerequisites remain. Quests with none queue at the gate; finishing one "
             "unlocks the quests waiting on it. If some never unlock, there's a cycle.",
        goal="Return an order to finish all courses, or an empty list.",
    ),
    spec=dict(method="findOrder", ret="vector<int>", params=[["int", "numCourses"], ["vector<vector<int>>&", "prerequisites"]]),
    tests=[dict(args=[2, [[1, 0]]], expected=[0, 1]), dict(args=[4, [[1, 0], [2, 1], [3, 2]]], expected=[0, 1, 2, 3]), dict(args=[2, [[1, 0], [0, 1]]], expected=[])],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="graph", edges="prerequisites", n="numCourses", reverse=True, directed=True, state="indeg", pointers=["u"], label="quest towns"),
        dict(kind="queue", var="q", label="ready to start"),
        dict(kind="array", var="order", label="order", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> indeg(numCourses, 0);
        for (auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            indeg[p[0]]++;
        }
        queue<int> q;
        for (int v = 0; v < numCourses; v++) {
            if (indeg[v] == 0) q.push(v);
        }
        vector<int> order;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            order.push_back(u);
            for (int v : adj[u]) {
                if (--indeg[v] == 0) q.push(v);
            }
        }
        if ((int)order.size() != numCourses) return {};
        return order;
    }
};""",
    hints=["LeetCode accepts any valid order; these tests have exactly one."],
)

add(
    id=219, slug="contains-duplicate-ii", title="Contains Duplicate II", difficulty="Easy", world="sliding-window", tags=["array", "hash-table", "sliding-window"],
    story=dict(
        title="Twins Close Together",
        text="A coat-check window only remembers the last k tickets. A ticket that is already in the window means two "
             "equal tickets within k of each other.",
        goal="Return true if two equal values are at most k apart.",
    ),
    spec=dict(method="containsNearbyDuplicate", ret="bool", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 3, 1], 3], expected=True), dict(args=[[1, 0, 1, 1], 1], expected=True), dict(args=[[1, 2, 3, 1, 2, 3], 2], expected=False)],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="tickets", pointers=["i"]),
        dict(kind="set", var="window", label="last k tickets"),
    ]),
    reference="""class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        set<int> window;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (window.count(nums[i])) return true;
            window.insert(nums[i]);
            if ((int)window.size() > k) window.erase(nums[i - k]);
        }
        return false;
    }
};""",
)

add(
    id=221, slug="maximal-square", title="Maximal Square", difficulty="Medium", world="dp", tags=["array", "dynamic-programming", "matrix"],
    story=dict(
        title="The Biggest Square Field",
        text="Each plot of land (1) records the side of the biggest all-land square ending there: one more than the "
             "smallest of its top, left and top-left neighbours.",
        goal="Return the area of the largest all-1 square.",
    ),
    spec=dict(method="maximalSquare", ret="int", params=[["vector<vector<char>>&", "matrix"]]),
    tests=[dict(args=[[["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]], expected=4),
           dict(args=[[["0", "1"], ["1", "0"]]], expected=1), dict(args=[[["0"]]], expected=0)],
    scene=dict(theme="farm", layers=[
        dict(kind="row", children=[
            dict(kind="grid", var="matrix", palette="islands", label="field"),
            dict(kind="grid", var="dp", palette="dp", label="square side", pointers=[["i", "j"]]),
        ]),
        dict(kind="values", vars=["side"]),
    ]),
    reference="""class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size(), side = 0;
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (matrix[i - 1][j - 1] == '1') {
                    dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
                    side = max(side, dp[i][j]);
                }
            }
        }
        return side * side;
    }
};""",
)

add(
    id=227, slug="basic-calculator-ii", title="Basic Calculator II", difficulty="Medium", world="stack", tags=["math", "string", "stack"],
    story=dict(
        title="The Calculator Tower (with Precedence)",
        text="Numbers are read with the operator before them. + and - stack the number (negated for -); * and / combine "
             "it with the top of the tower right away. The tower's sum is the answer.",
        goal="Evaluate the expression with + - * / and no parentheses.",
    ),
    spec=dict(method="calculate", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["3+2*2"], expected=7), dict(args=[" 3/2 "], expected=1), dict(args=[" 3+5 / 2 "], expected=5), dict(args=["14-3*2+8/4"], expected=10)],
    visualTest=3,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="expression", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="st", label="tower"), dict(kind="values", vars=["num", "op"])]),
    ]),
    reference="""class Solution {
public:
    int calculate(string s) {
        vector<int> st;
        long long num = 0;
        char op = '+';
        for (int i = 0; i < (int)s.size(); i++) {
            char c = s[i];
            if (isdigit(c)) num = num * 10 + (c - '0');
            if ((!isdigit(c) && c != ' ') || i == (int)s.size() - 1) {
                if (op == '+') st.push_back(num);
                else if (op == '-') st.push_back(-num);
                else if (op == '*') st.back() *= num;
                else st.back() /= num;
                op = c;
                num = 0;
            }
        }
        int total = 0;
        for (int x : st) total += x;
        return total;
    }
};""",
)

add(
    id=229, slug="majority-element-ii", title="Majority Element II", difficulty="Medium", world="arrays", tags=["array", "hash-table", "sorting", "counting"],
    story=dict(
        title="The Two-Candidate Vote",
        text="At most two values can each hold more than a third of the votes. Two candidates keep tallies; a vote for "
             "neither knocks one off both. A final count confirms the survivors.",
        goal="Return every value appearing more than n/3 times (any order).",
    ),
    spec=dict(method="majorityElement", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    compare="unordered",
    tests=[dict(args=[[3, 2, 3]], expected=[3]), dict(args=[[1]], expected=[1]), dict(args=[[1, 2]], expected=[1, 2]), dict(args=[[2, 1, 1, 3, 1, 4, 5, 6]], expected=[1])],
    visualTest=3,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="votes", pointers=["i"]),
        dict(kind="values", vars=["a", "ca", "b", "cb"]),
    ]),
    reference="""class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        int a = 0, b = 1, ca = 0, cb = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            int x = nums[i];
            if (x == a) ca++;
            else if (x == b) cb++;
            else if (ca == 0) {
                a = x;
                ca = 1;
            } else if (cb == 0) {
                b = x;
                cb = 1;
            } else {
                ca--;
                cb--;
            }
        }
        ca = cb = 0;
        for (int x : nums) {
            if (x == a) ca++;
            else if (x == b) cb++;
        }
        vector<int> res;
        if (ca > (int)nums.size() / 3) res.push_back(a);
        if (cb > (int)nums.size() / 3) res.push_back(b);
        return res;
    }
};""",
)

add(
    id=236, slug="lowest-common-ancestor-of-a-binary-tree", title="Lowest Common Ancestor of a Binary Tree", difficulty="Medium",
    world="trees", tags=["tree", "dfs"],
    story=dict(
        title="Where Two Searches Meet",
        text="Two birds search an unsorted orchard. Every fruit asks both branches whether they found a bird; the lowest "
             "fruit hearing \"yes\" from both sides (or being a bird itself with one yes) is where they meet.",
        goal="Return the value of the lowest common ancestor of p and q.",
    ),
    spec=dict(method="lowestCommonAncestor", ret="int", params=[["TreeNode*", "root"], ["int", "p"], ["int", "q"]]),
    tests=[dict(args=[[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1], expected=3), dict(args=[[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4], expected=5),
           dict(args=[[1, 2], 1, 2], expected=1)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["p", "q"]),
    ]),
    reference="""class Solution {
public:
    TreeNode* find(TreeNode* node, int p, int q) {
        if (!node || node->val == p || node->val == q) return node;
        TreeNode* l = find(node->left, p, q);
        TreeNode* r = find(node->right, p, q);
        if (l && r) return node;
        return l ? l : r;
    }
    int lowestCommonAncestor(TreeNode* root, int p, int q) {
        return find(root, p, q)->val;
    }
};""",
    hints=["LeetCode passes TreeNode* p and q; here they are values, which is all the search needs."],
)

add(
    id=240, slug="search-a-2d-matrix-ii", title="Search a 2D Matrix II", difficulty="Medium", world="binary-search",
    tags=["array", "binary-search", "divide-and-conquer", "matrix"],
    story=dict(
        title="The Staircase Search",
        text="Rows and columns both increase. Start at the top-right drawer: too big means the whole column is too big, "
             "so step left; too small means the whole row is too small, so step down.",
        goal="Return true if target is in the matrix.",
    ),
    spec=dict(method="searchMatrix", ret="bool", params=[["vector<vector<int>>&", "matrix"], ["int", "target"]]),
    tests=[dict(args=[[[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], 5], expected=True),
           dict(args=[[[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], 20], expected=False)],
    scene=dict(theme="cave", layers=[
        dict(kind="grid", var="matrix", palette="dp", label="vault", pointers=[["r", "c"]]),
        dict(kind="values", vars=["target"]),
    ]),
    reference="""class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int r = 0, c = matrix[0].size() - 1;
        while (r < (int)matrix.size() && c >= 0) {
            if (matrix[r][c] == target) return true;
            if (matrix[r][c] > target) c--;
            else r++;
        }
        return false;
    }
};""",
)
