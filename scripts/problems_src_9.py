"""Ninth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=58, slug="length-of-last-word", title="Length of Last Word", difficulty="Easy", world="arrays", tags=["string"],
    story=dict(
        title="The Last Word on the Sign",
        text="A painter reads the sign from the right, first skipping the trailing spaces, then counting letters until "
             "the next space.",
        goal="Return the length of the last word.",
    ),
    spec=dict(method="lengthOfLastWord", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["Hello World"], expected=5), dict(args=["   fly me   to   the moon  "], expected=4), dict(args=["luffy is still joyboy"], expected=6)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="sign", pointers=["i"]),
        dict(kind="values", vars=["len"]),
    ]),
    reference="""class Solution {
public:
    int lengthOfLastWord(string s) {
        int i = s.size() - 1, len = 0;
        while (i >= 0 && s[i] == ' ') i--;
        while (i >= 0 && s[i] != ' ') {
            len++;
            i--;
        }
        return len;
    }
};""",
)

add(
    id=28, slug="find-the-index-of-the-first-occurrence-in-a-string", title="Find the Index of the First Occurrence in a String",
    difficulty="Easy", world="two-pointers", tags=["two-pointers", "string", "string-matching"],
    story=dict(
        title="Spotting the Stamp",
        text="A clerk slides a stamp along a long ribbon of letters. At each position they compare letter by letter, "
             "giving up at the first mismatch and sliding one step on.",
        goal="Return the first index where needle appears in haystack, or -1.",
    ),
    spec=dict(method="strStr", ret="int", params=[["string", "haystack"], ["string", "needle"]]),
    tests=[dict(args=["sadbutsad", "sad"], expected=0), dict(args=["leetcode", "leeto"], expected=-1), dict(args=["mississippi", "issip"], expected=4)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="haystack", label="ribbon", pointers=["i"]),
        dict(kind="string", var="needle", label="stamp", pointers=["j"]),
    ]),
    reference="""class Solution {
public:
    int strStr(string haystack, string needle) {
        int n = haystack.size(), m = needle.size();
        for (int i = 0; i + m <= n; i++) {
            int j = 0;
            while (j < m && haystack[i + j] == needle[j]) j++;
            if (j == m) return i;
        }
        return -1;
    }
};""",
)

add(
    id=2000, slug="reverse-prefix-of-word", title="Reverse Prefix of Word", difficulty="Easy", world="two-pointers",
    tags=["two-pointers", "string", "stack"],
    story=dict(
        title="Flipping the Front of the Banner",
        text="Find the first copy of letter ch on the banner, then two painters flip everything from the start up to "
             "that letter, swapping from both ends.",
        goal="Reverse the prefix ending at the first ch (if any).",
    ),
    spec=dict(method="reversePrefix", ret="string", params=[["string", "word"], ["char", "ch"]]),
    tests=[dict(args=["abcdefd", "d"], expected="dcbaefd"), dict(args=["xyxzxe", "z"], expected="zxyxxe"), dict(args=["abcd", "z"], expected="abcd")],
    scene=dict(theme="market", layers=[dict(kind="string", var="word", label="banner", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    string reversePrefix(string word, char ch) {
        int r = word.find(ch);
        if (r == (int)string::npos) return word;
        int l = 0;
        while (l < r) {
            swap(word[l], word[r]);
            l++;
            r--;
        }
        return word;
    }
};""",
)

add(
    id=1047, slug="remove-all-adjacent-duplicates-in-string", title="Remove All Adjacent Duplicates In String", difficulty="Easy",
    world="stack", tags=["string", "stack"],
    story=dict(
        title="Popping Twin Blocks",
        text="Letter blocks drop onto a tower one by one. When a block lands on its twin, both vanish, which may expose "
             "another twin pair underneath.",
        goal="Return what remains after removing all adjacent duplicate pairs.",
    ),
    spec=dict(method="removeDuplicates", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["abbaca"], expected="ca"), dict(args=["azxxzy"], expected="ay")],
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="blocks arriving", pointers=["i"]),
        dict(kind="stack", var="st", label="tower"),
    ]),
    reference="""class Solution {
public:
    string removeDuplicates(string s) {
        string st;
        for (int i = 0; i < (int)s.size(); i++) {
            if (!st.empty() && st.back() == s[i]) st.pop_back();
            else st.push_back(s[i]);
        }
        return st;
    }
};""",
)

add(
    id=1021, slug="remove-outermost-parentheses", title="Remove Outermost Parentheses", difficulty="Easy", world="stack",
    tags=["string", "stack"],
    story=dict(
        title="Peeling the Outer Shells",
        text="A row of nested shells is made of balanced groups. A counter tracks the depth; only brackets that are not "
             "the outermost of their group are kept.",
        goal="Remove the outer brackets of every primitive group.",
    ),
    spec=dict(method="removeOuterParentheses", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["(()())(())"], expected="()()()"), dict(args=["(()())(())(()(()))"], expected="()()()()(())"), dict(args=["()()"], expected="")],
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="shells", pointers=["i"]),
        dict(kind="values", vars=["depth", "res"]),
    ]),
    reference="""class Solution {
public:
    string removeOuterParentheses(string s) {
        string res;
        int depth = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') {
                if (depth > 0) res.push_back('(');
                depth++;
            } else {
                depth--;
                if (depth > 0) res.push_back(')');
            }
        }
        return res;
    }
};""",
)

add(
    id=1614, slug="maximum-nesting-depth-of-the-parentheses", title="Maximum Nesting Depth of the Parentheses", difficulty="Easy",
    world="stack", tags=["string", "stack"],
    story=dict(
        title="How Deep Is the Cave?",
        text="Every ( is a step down into a cave and every ) a step back up. A miner walks the expression counting how "
             "far down they are and remembers the deepest point.",
        goal="Return the maximum nesting depth.",
    ),
    spec=dict(method="maxDepth", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["(1+(2*3)+((8)/4))+1"], expected=3), dict(args=["(1)+((2))+(((3)))"], expected=3), dict(args=["()(())((()()))"], expected=3)],
    scene=dict(theme="cave", layers=[
        dict(kind="string", var="s", label="expression", pointers=["i"]),
        dict(kind="values", vars=["depth", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxDepth(string s) {
        int depth = 0, best = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') best = max(best, ++depth);
            else if (s[i] == ')') depth--;
        }
        return best;
    }
};""",
)

add(
    id=744, slug="find-smallest-letter-greater-than-target", title="Find Smallest Letter Greater Than Target", difficulty="Easy",
    world="binary-search", tags=["array", "binary-search"],
    story=dict(
        title="The Next Letter Box",
        text="Letter boxes are sorted. The guard halves the shelf looking for the first box strictly after the target; if "
             "none is, the shelf wraps around to the first box.",
        goal="Return the smallest letter greater than target (wrapping around).",
    ),
    spec=dict(method="nextGreatestLetter", ret="char", params=[["vector<char>&", "letters"], ["char", "target"]]),
    tests=[dict(args=[["c", "f", "j"], "a"], expected="c"), dict(args=[["c", "f", "j"], "c"], expected="f"), dict(args=[["x", "x", "y", "y"], "z"], expected="x")],
    visualTest=1,
    scene=dict(theme="cave", layers=[dict(kind="array", var="letters", label="boxes", style="letters", pointers=["lo", "mid", "hi"], window=["lo", "hi"], windowExclusive=True)]),
    reference="""class Solution {
public:
    char nextGreatestLetter(vector<char>& letters, char target) {
        int lo = 0, hi = letters.size();
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (letters[mid] <= target) lo = mid + 1;
            else hi = mid;
        }
        return letters[lo % letters.size()];
    }
};""",
)

add(
    id=1539, slug="kth-missing-positive-number", title="Kth Missing Positive Number", difficulty="Easy", world="binary-search",
    tags=["array", "binary-search"],
    story=dict(
        title="Missing House Numbers",
        text="Before the house at position i, exactly arr[i] - i - 1 numbers are missing. The guard binary-searches for the "
             "first house with at least k missing numbers before it.",
        goal="Return the k-th missing positive integer.",
    ),
    spec=dict(method="findKthPositive", ret="int", params=[["vector<int>&", "arr"], ["int", "k"]]),
    tests=[dict(args=[[2, 3, 4, 7, 11], 5], expected=9), dict(args=[[1, 2, 3, 4], 2], expected=6)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="arr", label="houses", pointers=["lo", "mid", "hi"], window=["lo", "hi"], windowExclusive=True),
        dict(kind="values", vars=["k", "missing"]),
    ]),
    reference="""class Solution {
public:
    int findKthPositive(vector<int>& arr, int k) {
        int lo = 0, hi = arr.size();
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            int missing = arr[mid] - mid - 1;
            if (missing < k) lo = mid + 1;
            else hi = mid;
        }
        return lo + k;
    }
};""",
)

add(
    id=1669, slug="merge-in-between-linked-lists", title="Merge In Between Linked Lists", difficulty="Medium", world="linked-list",
    tags=["linked-list"],
    story=dict(
        title="Swapping Out a Section of Train",
        text="Cars a through b of the first train are replaced by a whole second train. One worker parks just before car "
             "a, another just after car b, and the second train is coupled in between.",
        goal="Return the first train with the section replaced.",
    ),
    spec=dict(method="mergeInBetween", ret="ListNode*", params=[["ListNode*", "list1"], ["int", "a"], ["int", "b"], ["ListNode*", "list2"]]),
    tests=[dict(args=[[10, 1, 13, 6, 9, 5], 3, 4, [1000000, 1000001, 1000002]], expected=[10, 1, 13, 1000000, 1000001, 1000002, 5]),
           dict(args=[[0, 1, 2, 3, 4, 5, 6], 2, 5, [7, 8, 9]], expected=[0, 1, 7, 8, 9, 6])],
    visualTest=1,
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["list1", "list2", "before", "after", "tail"], heads=["list1", "list2"], label="trains")]),
    reference="""class Solution {
public:
    ListNode* mergeInBetween(ListNode* list1, int a, int b, ListNode* list2) {
        ListNode* before = list1;
        for (int s = 1; s < a; s++) before = before->next;
        ListNode* after = before;
        for (int s = a; s <= b + 1; s++) after = after->next;
        before->next = list2;
        ListNode* tail = list2;
        while (tail->next) tail = tail->next;
        tail->next = after;
        return list1;
    }
};""",
)

add(
    id=147, slug="insertion-sort-list", title="Insertion Sort List", difficulty="Medium", world="linked-list", tags=["linked-list", "sorting"],
    story=dict(
        title="Re-coupling in Order",
        text="Cars are taken off the old train one at a time and slid into the right place on a new, sorted train that "
             "starts behind a dummy engine.",
        goal="Return the train sorted by insertion sort.",
    ),
    spec=dict(method="insertionSortList", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[4, 2, 1, 3]], expected=[1, 2, 3, 4]), dict(args=[[-1, 5, 3, 4, 0]], expected=[-1, 0, 3, 4, 5])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "cur", "prev", "nxt"], heads=["head"], label="yard")]),
    reference="""class Solution {
public:
    ListNode* insertionSortList(ListNode* head) {
        ListNode* dummy = new ListNode(0);
        ListNode* cur = head;
        while (cur) {
            ListNode* nxt = cur->next;
            ListNode* prev = dummy;
            while (prev->next && prev->next->val < cur->val) prev = prev->next;
            cur->next = prev->next;
            prev->next = cur;
            cur = nxt;
        }
        return dummy->next;
    }
};""",
)

add(
    id=257, slug="binary-tree-paths", title="Binary Tree Paths", difficulty="Easy", world="trees", tags=["string", "backtracking", "tree", "dfs"],
    story=dict(
        title="Writing Down Every Trail",
        text="A squirrel climbs every route from the top to a leaf, writing the route as it goes. At each leaf the "
             "written route goes into the logbook.",
        goal="Return every root-to-leaf path as \"a->b->c\" (any order).",
    ),
    spec=dict(method="binaryTreePaths", ret="vector<string>", params=[["TreeNode*", "root"]]),
    compare="unordered",
    tests=[dict(args=[[1, 2, 3, None, 5]], expected=["1->2->5", "1->3"]), dict(args=[[1]], expected=["1"])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["path"]),
        dict(kind="array", var="res", label="logbook", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> res;
    void walk(TreeNode* node, string path) {
        if (!node) return;
        path += to_string(node->val);
        if (!node->left && !node->right) {
            res.push_back(path);
            return;
        }
        walk(node->left, path + "->");
        walk(node->right, path + "->");
    }
    vector<string> binaryTreePaths(TreeNode* root) {
        walk(root, "");
        return res;
    }
};""",
)

add(
    id=404, slug="sum-of-left-leaves", title="Sum of Left Leaves", difficulty="Easy", world="trees", tags=["tree", "dfs", "bfs"],
    story=dict(
        title="Only the Left-Hanging Fruit",
        text="A squirrel only collects fruit that hang at the very end of a left branch. Each branch is told whether it "
             "is a left child.",
        goal="Return the sum of all left leaves.",
    ),
    spec=dict(method="sumOfLeftLeaves", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 9, 20, None, None, 15, 7]], expected=24), dict(args=[[1]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["isLeft", "sum"]),
    ]),
    reference="""class Solution {
public:
    int sum = 0;
    void walk(TreeNode* node, bool isLeft) {
        if (!node) return;
        if (!node->left && !node->right && isLeft) sum += node->val;
        walk(node->left, true);
        walk(node->right, false);
    }
    int sumOfLeftLeaves(TreeNode* root) {
        walk(root, false);
        return sum;
    }
};""",
)

add(
    id=513, slug="find-bottom-left-tree-value", title="Find Bottom Left Tree Value", difficulty="Medium", world="trees",
    tags=["tree", "dfs", "bfs"],
    story=dict(
        title="The Lowest Leftmost Fruit",
        text="Pickers sweep each row from right to left. The very last fruit picked in the whole orchard is the lowest, "
             "leftmost one.",
        goal="Return the leftmost value in the last row.",
    ),
    spec=dict(method="findBottomLeftValue", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[2, 1, 3]], expected=1), dict(args=[[1, 2, 3, 4, None, 5, 6, None, None, 7]], expected=7)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="pickers (right to left)"),
    ]),
    reference="""class Solution {
public:
    int findBottomLeftValue(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);
        TreeNode* node = root;
        while (!q.empty()) {
            node = q.front();
            q.pop();
            if (node->right) q.push(node->right);
            if (node->left) q.push(node->left);
        }
        return node->val;
    }
};""",
)

add(
    id=700, slug="search-in-a-binary-search-tree", title="Search in a Binary Search Tree", difficulty="Easy", world="trees",
    tags=["tree", "bst"],
    story=dict(
        title="Finding the Labelled Fruit",
        text="In a sorted orchard a picker goes left for smaller labels and right for bigger ones until they find the "
             "fruit, or run out of branches.",
        goal="Return the subtree rooted at val, or an empty tree.",
    ),
    spec=dict(method="searchBST", ret="TreeNode*", params=[["TreeNode*", "root"], ["int", "val"]]),
    tests=[dict(args=[[4, 2, 7, 1, 3], 2], expected=[2, 1, 3]), dict(args=[[4, 2, 7, 1, 3], 5], expected=[])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["cur"], label="orchard"),
        dict(kind="values", vars=["val"]),
    ]),
    reference="""class Solution {
public:
    TreeNode* searchBST(TreeNode* root, int val) {
        TreeNode* cur = root;
        while (cur && cur->val != val) cur = val < cur->val ? cur->left : cur->right;
        return cur;
    }
};""",
)

add(
    id=1962, slug="remove-stones-to-minimize-the-total", title="Remove Stones to Minimize the Total", difficulty="Medium",
    world="heap", tags=["array", "greedy", "heap"],
    story=dict(
        title="Halving the Biggest Pile",
        text="k times, a worker takes the biggest stone pile and removes half of it (rounded down). The pyramid keeps the "
             "biggest pile on top.",
        goal="Return the fewest stones left after k operations.",
    ),
    spec=dict(method="minStoneSum", ret="int", params=[["vector<int>&", "piles"], ["int", "k"]]),
    tests=[dict(args=[[5, 4, 9], 2], expected=12), dict(args=[[4, 3, 6, 7], 3], expected=12)],
    scene=dict(theme="market", layers=[
        dict(kind="heap", var="pq", label="piles (biggest on top)", color="#9a8c98"),
        dict(kind="values", vars=["k", "top", "total"]),
    ]),
    reference="""class Solution {
public:
    int minStoneSum(vector<int>& piles, int k) {
        priority_queue<int> pq(piles.begin(), piles.end());
        while (k-- > 0) {
            int top = pq.top();
            pq.pop();
            pq.push(top - top / 2);
        }
        int total = 0;
        while (!pq.empty()) {
            total += pq.top();
            pq.pop();
        }
        return total;
    }
};""",
)

add(
    id=997, slug="find-the-town-judge", title="Find the Town Judge", difficulty="Easy", world="graphs", tags=["array", "hash-table", "graph"],
    story=dict(
        title="Who Does Everyone Trust?",
        text="Each trust arrow gives the trusted person a point and costs the truster one. The judge is the one person "
             "with exactly n-1 points: trusted by all, trusting nobody.",
        goal="Return the judge's label, or -1.",
    ),
    spec=dict(method="findJudge", ret="int", params=[["int", "n"], ["vector<vector<int>>&", "trust"]]),
    tests=[dict(args=[2, [[1, 2]]], expected=2), dict(args=[3, [[1, 3], [2, 3]]], expected=3), dict(args=[3, [[1, 3], [2, 3], [3, 1]]], expected=-1)],
    visualTest=1,
    scene=dict(theme="castle", layers=[dict(kind="array", var="score", label="trust score by person", style="tiles", pointers=["p"])]),
    reference="""class Solution {
public:
    int findJudge(int n, vector<vector<int>>& trust) {
        vector<int> score(n + 1, 0);
        for (auto& t : trust) {
            score[t[0]]--;
            score[t[1]]++;
        }
        for (int p = 1; p <= n; p++) {
            if (score[p] == n - 1) return p;
        }
        return -1;
    }
};""",
)

add(
    id=1436, slug="destination-city", title="Destination City", difficulty="Easy", world="graphs", tags=["array", "hash-table", "string"],
    story=dict(
        title="The End of the Road",
        text="Roads form one long route. Every city that has a road leaving it goes into the lockers; the one city with no "
             "way out is the destination.",
        goal="Return the city with no outgoing road.",
    ),
    spec=dict(method="destCity", ret="string", params=[["vector<vector<string>>&", "paths"]]),
    tests=[dict(args=[[["London", "New York"], ["New York", "Lima"], ["Lima", "Sao Paulo"]]], expected="Sao Paulo"),
           dict(args=[[["B", "C"], ["D", "B"], ["C", "A"]]], expected="A")],
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="paths", label="roads [from, to]", style="tiles", pointers=["i"]),
        dict(kind="set", var="leaves", label="cities with a way out"),
    ]),
    reference="""class Solution {
public:
    string destCity(vector<vector<string>>& paths) {
        set<string> leaves;
        for (auto& p : paths) leaves.insert(p[0]);
        for (int i = 0; i < (int)paths.size(); i++) {
            if (!leaves.count(paths[i][1])) return paths[i][1];
        }
        return "";
    }
};""",
)

add(
    id=1219, slug="path-with-maximum-gold", title="Path with Maximum Gold", difficulty="Medium", world="backtracking",
    tags=["array", "backtracking", "matrix"],
    story=dict(
        title="The Gold Mine",
        text="A miner may start in any cell with gold and walk up, down, left or right, never revisiting a cell. Each step "
             "into the tunnels empties the cell; backing out puts the gold back for the next try.",
        goal="Return the most gold one walk can collect.",
    ),
    spec=dict(method="getMaximumGold", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[0, 6, 0], [5, 8, 7], [0, 9, 0]]], expected=24), dict(args=[[[1, 0, 7], [2, 0, 6], [3, 4, 5], [0, 3, 0], [9, 0, 20]]], expected=28)],
    scene=dict(theme="cave", layers=[
        dict(kind="grid", var="grid", palette="dp", label="mine", pointers=[["r", "c"]]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int dig(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size() || grid[r][c] == 0) return 0;
        int gold = grid[r][c];
        grid[r][c] = 0;
        int more = max({dig(grid, r + 1, c), dig(grid, r - 1, c), dig(grid, r, c + 1), dig(grid, r, c - 1)});
        grid[r][c] = gold;
        return gold + more;
    }
    int getMaximumGold(vector<vector<int>>& grid) {
        int best = 0;
        for (int r = 0; r < (int)grid.size(); r++)
            for (int c = 0; c < (int)grid[0].size(); c++)
                best = max(best, dig(grid, r, c));
        return best;
    }
};""",
)

add(
    id=119, slug="pascals-triangle-ii", title="Pascal's Triangle II", difficulty="Easy", world="dp", tags=["array", "dynamic-programming"],
    story=dict(
        title="One Row of Hay Bales",
        text="Only one row of bales fits in the barn. To build the next row in place, the farmer updates it from right to "
             "left so every bale still sees the old values it needs.",
        goal="Return row rowIndex of Pascal's triangle.",
    ),
    spec=dict(method="getRow", ret="vector<int>", params=[["int", "rowIndex"]]),
    tests=[dict(args=[3], expected=[1, 3, 3, 1]), dict(args=[0], expected=[1]), dict(args=[5], expected=[1, 5, 10, 10, 5, 1])],
    visualTest=2,
    scene=dict(theme="farm", layers=[dict(kind="array", var="row", label="bales", style="tiles", pointers=["j"])]),
    reference="""class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<int> row(rowIndex + 1, 0);
        row[0] = 1;
        for (int i = 1; i <= rowIndex; i++) {
            for (int j = i; j > 0; j--) row[j] += row[j - 1];
        }
        return row;
    }
};""",
)

add(
    id=96, slug="unique-binary-search-trees", title="Unique Binary Search Trees", difficulty="Medium", world="dp",
    tags=["math", "dynamic-programming", "tree", "bst"],
    story=dict(
        title="How Many Orchards?",
        text="With n labelled fruits, any one can be the root. The left side then holds the smaller ones and the right "
             "the bigger, so the count is the sum of left ways times right ways.",
        goal="Return how many structurally unique BSTs store 1..n.",
    ),
    spec=dict(method="numTrees", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[3], expected=5), dict(args=[1], expected=1), dict(args=[6], expected=132)],
    visualTest=0,
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="dp", label="orchards per size", style="tiles", pointers=["root", "i"]),
    ]),
    reference="""class Solution {
public:
    int numTrees(int n) {
        vector<long long> dp(n + 1, 0);
        dp[0] = 1;
        for (int i = 1; i <= n; i++) {
            for (int root = 1; root <= i; root++) {
                dp[i] += dp[root - 1] * dp[i - root];
            }
        }
        return dp[n];
    }
};""",
)

add(
    id=931, slug="minimum-falling-path-sum", title="Minimum Falling Path Sum", difficulty="Medium", world="dp",
    tags=["array", "dynamic-programming", "matrix"],
    story=dict(
        title="The Cheapest Fall",
        text="A raindrop falls through a grid of fees, moving straight down or diagonally each row. Row by row, each cell "
             "is overwritten with the cheapest total fall to reach it.",
        goal="Return the cheapest falling path from the top row to the bottom.",
    ),
    spec=dict(method="minFallingPathSum", ret="int", params=[["vector<vector<int>>&", "matrix"]]),
    tests=[dict(args=[[[2, 1, 3], [6, 5, 4], [7, 8, 9]]], expected=13), dict(args=[[[-19, 57], [-40, -5]]], expected=-59)],
    scene=dict(theme="city", layers=[dict(kind="grid", var="matrix", palette="dp", label="fees", pointers=[["r", "c"]])]),
    reference="""class Solution {
public:
    int minFallingPathSum(vector<vector<int>>& matrix) {
        int n = matrix.size();
        for (int r = 1; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int best = matrix[r - 1][c];
                if (c > 0) best = min(best, matrix[r - 1][c - 1]);
                if (c + 1 < n) best = min(best, matrix[r - 1][c + 1]);
                matrix[r][c] += best;
            }
        }
        return *min_element(matrix[n - 1].begin(), matrix[n - 1].end());
    }
};""",
)

add(
    id=1323, slug="maximum-69-number", title="Maximum 69 Number", difficulty="Easy", world="greedy", tags=["math", "greedy"],
    story=dict(
        title="Flipping One Digit Card",
        text="A number is made of 6 and 9 cards. You may flip one card; turning the leftmost 6 into a 9 gains the most.",
        goal="Return the largest number after at most one flip.",
    ),
    spec=dict(method="maximum69Number", ret="int", params=[["int", "num"]]),
    tests=[dict(args=[9669], expected=9969), dict(args=[9996], expected=9999), dict(args=[9999], expected=9999)],
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="digit cards", pointers=["i"]),
    ]),
    reference="""class Solution {
public:
    int maximum69Number(int num) {
        string s = to_string(num);
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '6') {
                s[i] = '9';
                break;
            }
        }
        return stoi(s);
    }
};""",
)

add(
    id=2706, slug="buy-two-chocolates", title="Buy Two Chocolates", difficulty="Easy", world="greedy", tags=["array", "greedy", "sorting"],
    story=dict(
        title="Two Cheapest Treats",
        text="A kid wants exactly two chocolates and must not go into debt. Walking the shelf, they remember the two "
             "cheapest prices seen so far.",
        goal="Return the money left after buying the two cheapest, or the original money if that is impossible.",
    ),
    spec=dict(method="buyChoco", ret="int", params=[["vector<int>&", "prices"], ["int", "money"]]),
    tests=[dict(args=[[1, 2, 2], 3], expected=0), dict(args=[[3, 2, 3], 3], expected=3), dict(args=[[98, 54, 6, 34, 66, 63, 52, 39], 62], expected=22)],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="prices", label="shelf", pointers=["i"]),
        dict(kind="values", vars=["a", "b", "money"]),
    ]),
    reference="""class Solution {
public:
    int buyChoco(vector<int>& prices, int money) {
        int a = INT_MAX, b = INT_MAX;
        for (int i = 0; i < (int)prices.size(); i++) {
            if (prices[i] < a) {
                b = a;
                a = prices[i];
            } else if (prices[i] < b) {
                b = prices[i];
            }
        }
        return a + b <= money ? money - a - b : money;
    }
};""",
)

add(
    id=67, slug="add-binary", title="Add Binary", difficulty="Easy", world="bits", tags=["math", "string", "bit-manipulation", "simulation"],
    story=dict(
        title="Adding Two Lamp Rows",
        text="Two rows of lamps are added from the right, lamp by lamp, carrying a 1 whenever two lit lamps meet.",
        goal="Return the binary sum as a string.",
    ),
    spec=dict(method="addBinary", ret="string", params=[["string", "a"], ["string", "b"]]),
    tests=[dict(args=["11", "1"], expected="100"), dict(args=["1010", "1011"], expected="10101")],
    visualTest=1,
    scene=dict(theme="space", layers=[
        dict(kind="string", var="a", label="row a", pointers=["i"]),
        dict(kind="string", var="b", label="row b", pointers=["j"]),
        dict(kind="values", vars=["carry", "res"]),
    ]),
    reference="""class Solution {
public:
    string addBinary(string a, string b) {
        string res;
        int i = a.size() - 1, j = b.size() - 1, carry = 0;
        while (i >= 0 || j >= 0 || carry) {
            int sum = carry;
            if (i >= 0) sum += a[i--] - '0';
            if (j >= 0) sum += b[j--] - '0';
            res.push_back('0' + sum % 2);
            carry = sum / 2;
        }
        reverse(res.begin(), res.end());
        return res;
    }
};""",
)

add(
    id=476, slug="number-complement", title="Number Complement", difficulty="Easy", world="bits", tags=["bit-manipulation"],
    story=dict(
        title="Flipping Every Lamp",
        text="Build a mask with a lit lamp under every lamp the number uses, then XOR with it so every lamp flips.",
        goal="Return the complement of num (flip every bit of its binary form).",
    ),
    spec=dict(method="findComplement", ret="int", params=[["int", "num"]]),
    tests=[dict(args=[5], expected=2), dict(args=[1], expected=0), dict(args=[100], expected=27)],
    visualTest=2,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["num", "mask"])]),
    reference="""class Solution {
public:
    int findComplement(int num) {
        long long mask = 1;
        while (mask <= num) mask <<= 1;
        return (int)((mask - 1) ^ num);
    }
};""",
)
