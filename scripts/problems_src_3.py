"""Third batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=27, slug="remove-element", title="Remove Element", difficulty="Easy", world="two-pointers",
    tags=["array", "two-pointers"],
    story=dict(
        title="Clearing the Rotten Crates",
        text="Crates marked with a bad number must go. A reader checks every crate; a writer keeps only the good ones, "
             "packing them to the front of the dock.",
        goal="Return how many crates are left after removing every crate equal to val.",
    ),
    spec=dict(method="removeElement", ret="int", params=[["vector<int>&", "nums"], ["int", "val"]]),
    tests=[dict(args=[[3, 2, 2, 3], 3], expected=2), dict(args=[[0, 1, 2, 2, 3, 0, 4, 2], 2], expected=5), dict(args=[[], 1], expected=0)],
    visualTest=1,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="dock", pointers=["k", "i"]),
        dict(kind="values", vars=["val"]),
    ]),
    reference="""class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int k = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (nums[i] != val) {
                nums[k] = nums[i];
                k++;
            }
        }
        return k;
    }
};""",
)

add(
    id=75, slug="sort-colors", title="Sort Colors", difficulty="Medium", world="two-pointers",
    tags=["array", "two-pointers", "sorting"],
    story=dict(
        title="The Flag Painter",
        text="Paint pots of three colours (0, 1, 2) are jumbled on a shelf. One worker pushes 0s to the left wall, "
             "another pushes 2s to the right wall, and the middle walker decides where each pot goes.",
        goal="Sort the pots in place in one pass.",
    ),
    spec=dict(method="sortColors", ret="void", params=[["vector<int>&", "nums"]], output="param:0"),
    tests=[dict(args=[[2, 0, 2, 1, 1, 0]], expected=[0, 0, 1, 1, 2, 2]), dict(args=[[2, 0, 1]], expected=[0, 1, 2]), dict(args=[[0]], expected=[0])],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="paint pots", pointers=["lo", "mid", "hi"], window=["mid", "hi"]),
    ]),
    reference="""class Solution {
public:
    void sortColors(vector<int>& nums) {
        int lo = 0, mid = 0, hi = nums.size() - 1;
        while (mid <= hi) {
            if (nums[mid] == 0) {
                swap(nums[lo], nums[mid]);
                lo++;
                mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                swap(nums[mid], nums[hi]);
                hi--;
            }
        }
    }
};""",
)

add(
    id=169, slug="majority-element", title="Majority Element", difficulty="Easy", world="arrays",
    tags=["array", "hash-table", "counting"],
    story=dict(
        title="The Village Vote",
        text="Villagers walk past a ballot box one by one. A candidate holds the box with a vote count; a different vote "
             "knocks one off, and at zero the next voter takes over. The true majority always survives.",
        goal="Return the value that appears more than half the time.",
    ),
    spec=dict(method="majorityElement", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[3, 2, 3]], expected=3), dict(args=[[2, 2, 1, 1, 1, 2, 2]], expected=2)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="voters", pointers=["i"]),
        dict(kind="values", vars=["cand", "cnt"]),
    ]),
    reference="""class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int cand = nums[0], cnt = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (cnt == 0) cand = nums[i];
            if (nums[i] == cand) cnt++;
            else cnt--;
        }
        return cand;
    }
};""",
)

add(
    id=128, slug="longest-consecutive-sequence", title="Longest Consecutive Sequence", difficulty="Medium", world="arrays",
    tags=["array", "hash-table", "union-find"],
    story=dict(
        title="Counting the House Numbers",
        text="House numbers are scattered on a list. Every number goes into the lockers; then only numbers with no "
             "smaller neighbour start a walk up the street, counting how many houses follow in a row.",
        goal="Return the length of the longest run of consecutive numbers.",
    ),
    spec=dict(method="longestConsecutive", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[100, 4, 200, 1, 3, 2]], expected=4), dict(args=[[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], expected=9), dict(args=[[]], expected=0)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="house numbers", pointers=["i"]),
        dict(kind="set", var="seen", label="lockers", lookup=["cur"]),
        dict(kind="values", vars=["cur", "len", "best"]),
    ]),
    reference="""class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        set<int> seen(nums.begin(), nums.end());
        int best = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (seen.count(nums[i] - 1)) continue;
            int cur = nums[i], len = 1;
            while (seen.count(cur + 1)) {
                cur++;
                len++;
            }
            best = max(best, len);
        }
        return best;
    }
};""",
)

add(
    id=560, slug="subarray-sum-equals-k", title="Subarray Sum Equals K", difficulty="Medium", world="arrays",
    tags=["array", "hash-table", "prefix-sum"],
    story=dict(
        title="The Odometer Logbook",
        text="A courier keeps a running odometer while driving past depots. To find stretches of exactly k miles, they "
             "check the logbook for how many earlier readings were exactly k miles ago.",
        goal="Return how many contiguous stretches add up to k.",
    ),
    spec=dict(method="subarraySum", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[1, 1, 1], 2], expected=2), dict(args=[[1, 2, 3], 3], expected=2), dict(args=[[3, 4, 7, -2, 2, 1, 4, 2], 7], expected=6)],
    visualTest=2,
    scene=dict(theme="city", layers=[
        dict(kind="array", var="nums", label="depots", pointers=["i"]),
        dict(kind="map", var="seen", label="logbook: reading → times", lookup=["need"]),
        dict(kind="values", vars=["sum", "need", "count"]),
    ]),
    reference="""class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        map<int, int> seen;
        seen[0] = 1;
        int sum = 0, count = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            sum += nums[i];
            int need = sum - k;
            if (seen.count(need)) count += seen[need];
            seen[sum]++;
        }
        return count;
    }
};""",
)

add(
    id=438, slug="find-all-anagrams-in-a-string", title="Find All Anagrams in a String", difficulty="Medium",
    world="sliding-window", tags=["string", "sliding-window", "hash-table"],
    story=dict(
        title="Spotting the Scrambled Name",
        text="A beam the exact length of a name sweeps along a banner of letters. Lockers count the letters inside the "
             "beam; whenever they match the name's letter counts, an anagram is spotted.",
        goal="Return every start index where an anagram of p begins.",
    ),
    spec=dict(method="findAnagrams", ret="vector<int>", params=[["string", "s"], ["string", "p"]]),
    tests=[dict(args=["cbaebabacd", "abc"], expected=[0, 6]), dict(args=["abab", "ab"], expected=[0, 1, 2])],
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="banner", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="row", children=[
            dict(kind="map", var="need", label="name letters"),
            dict(kind="map", var="win", label="beam letters"),
        ]),
        dict(kind="array", var="res", label="found at", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        vector<int> res;
        map<char, int> need, win;
        for (char c : p) need[c]++;
        int m = p.size();
        for (int r = 0; r < (int)s.size(); r++) {
            win[s[r]]++;
            int l = r - m + 1;
            if (l < 0) continue;
            if (win == need) res.push_back(l);
            if (--win[s[l]] == 0) win.erase(s[l]);
        }
        return res;
    }
};""",
)

add(
    id=567, slug="permutation-in-string", title="Permutation in String", difficulty="Medium", world="sliding-window",
    tags=["string", "sliding-window", "hash-table", "two-pointers"],
    story=dict(
        title="The Hidden Password",
        text="A password's letters were shuffled and hidden somewhere in a long message. A beam the password's length "
             "slides along, keeping letter counts, until the counts match exactly.",
        goal="Return true if some window of s2 is a permutation of s1.",
    ),
    spec=dict(method="checkInclusion", ret="bool", params=[["string", "s1"], ["string", "s2"]]),
    tests=[dict(args=["ab", "eidbaooo"], expected=True), dict(args=["ab", "eidboaoo"], expected=False), dict(args=["adc", "dcda"], expected=True)],
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s2", label="message", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="row", children=[
            dict(kind="map", var="need", label="password letters"),
            dict(kind="map", var="win", label="beam letters"),
        ]),
    ]),
    reference="""class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        map<char, int> need, win;
        for (char c : s1) need[c]++;
        int m = s1.size();
        for (int r = 0; r < (int)s2.size(); r++) {
            win[s2[r]]++;
            int l = r - m + 1;
            if (l < 0) continue;
            if (win == need) return true;
            if (--win[s2[l]] == 0) win.erase(s2[l]);
        }
        return false;
    }
};""",
)

add(
    id=682, slug="baseball-game", title="Baseball Game", difficulty="Easy", world="stack",
    tags=["array", "stack", "simulation"],
    story=dict(
        title="The Scorekeeper's Tower",
        text="Each card says what to do with the score tower: a number stacks a new score, + stacks the sum of the top "
             "two, D doubles the top, and C knocks the top score off.",
        goal="Return the sum of the scores left in the tower.",
    ),
    spec=dict(method="calPoints", ret="int", params=[["vector<string>&", "operations"]]),
    tests=[dict(args=[["5", "2", "C", "D", "+"]], expected=30), dict(args=[["5", "-2", "4", "C", "D", "9", "+", "+"]], expected=27),
           dict(args=[["1", "C"]], expected=0)],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="operations", label="cards", style="tiles", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="st", label="score tower"), dict(kind="values", vars=["total"])]),
    ]),
    reference="""class Solution {
public:
    int calPoints(vector<string>& operations) {
        stack<int> st;
        for (int i = 0; i < (int)operations.size(); i++) {
            string& op = operations[i];
            if (op == "C") {
                st.pop();
            } else if (op == "D") {
                st.push(st.top() * 2);
            } else if (op == "+") {
                int a = st.top();
                st.pop();
                int b = st.top();
                st.push(a);
                st.push(a + b);
            } else {
                st.push(stoi(op));
            }
        }
        int total = 0;
        while (!st.empty()) {
            total += st.top();
            st.pop();
        }
        return total;
    }
};""",
)

add(
    id=162, slug="find-peak-element", title="Find Peak Element", difficulty="Medium", world="binary-search",
    tags=["array", "binary-search"],
    story=dict(
        title="Climbing to a Summit",
        text="A hiker in fog only sees the step ahead. If the ground rises to the right, a summit must be that way; "
             "otherwise one is here or to the left. Halving the trail each time finds a peak fast.",
        goal="Return the index of a peak (an element bigger than its neighbours).",
    ),
    spec=dict(method="findPeakElement", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 1]], expected=2), dict(args=[[1, 3, 5, 7, 6, 4, 2]], expected=3), dict(args=[[5]], expected=0)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="nums", label="trail heights", pointers=["lo", "mid", "hi"], window=["lo", "hi"]),
    ]),
    reference="""class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int lo = 0, hi = nums.size() - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] < nums[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
};""",
    hints=["Any peak is accepted on LeetCode; the tests here have a single peak so the answer is unique."],
)

add(
    id=83, slug="remove-duplicates-from-sorted-list", title="Remove Duplicates from Sorted List", difficulty="Easy",
    world="linked-list", tags=["linked-list"],
    story=dict(
        title="Unhooking Twin Cars",
        text="Cars on a sorted train sometimes repeat. A yard worker walks the train; whenever the next car matches the "
             "current one, it is unhooked and the coupling skips over it.",
        goal="Return the train with each value kept once.",
    ),
    spec=dict(method="deleteDuplicates", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 1, 2]], expected=[1, 2]), dict(args=[[1, 1, 2, 3, 3]], expected=[1, 2, 3]), dict(args=[[]], expected=[])],
    visualTest=1,
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "cur"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        ListNode* cur = head;
        while (cur && cur->next) {
            if (cur->next->val == cur->val) cur->next = cur->next->next;
            else cur = cur->next;
        }
        return head;
    }
};""",
)

add(
    id=143, slug="reorder-list", title="Reorder List", difficulty="Medium", world="linked-list",
    tags=["linked-list", "two-pointers", "stack", "recursion"],
    story=dict(
        title="Shuffling the Train",
        text="The station wants cars in the order first, last, second, second-to-last… Find the middle, turn the back "
             "half around, then zip the two halves together car by car.",
        goal="Reorder the train in place.",
    ),
    spec=dict(method="reorderList", ret="void", params=[["ListNode*", "head"]], output="param:0"),
    tests=[dict(args=[[1, 2, 3, 4]], expected=[1, 4, 2, 3]), dict(args=[[1, 2, 3, 4, 5]], expected=[1, 5, 2, 4, 3])],
    visualTest=1,
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "slow", "fast", "prev", "a", "b"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    void reorderList(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast->next && fast->next->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode* prev = nullptr;
        ListNode* cur = slow->next;
        slow->next = nullptr;
        while (cur) {
            ListNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        ListNode* a = head;
        ListNode* b = prev;
        while (b) {
            ListNode* an = a->next;
            ListNode* bn = b->next;
            a->next = b;
            b->next = an;
            a = an;
            b = bn;
        }
    }
};""",
)

add(
    id=24, slug="swap-nodes-in-pairs", title="Swap Nodes in Pairs", difficulty="Medium", world="linked-list",
    tags=["linked-list", "recursion"],
    story=dict(
        title="Swapping Cars Two by Two",
        text="Every pair of neighbouring cars must trade places. A brakeman stands just before each pair and re-hooks "
             "three couplings to swap them, then moves on two cars.",
        goal="Return the train with every pair swapped.",
    ),
    spec=dict(method="swapPairs", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 2, 3, 4]], expected=[2, 1, 4, 3]), dict(args=[[]], expected=[]), dict(args=[[1, 2, 3]], expected=[2, 1, 3])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["prev", "a", "b"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* swapPairs(ListNode* head) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* prev = dummy;
        while (prev->next && prev->next->next) {
            ListNode* a = prev->next;
            ListNode* b = a->next;
            a->next = b->next;
            b->next = a;
            prev->next = b;
            prev = a;
        }
        return dummy->next;
    }
};""",
)

add(
    id=101, slug="symmetric-tree", title="Symmetric Tree", difficulty="Easy", world="trees", tags=["tree", "dfs", "bfs"],
    story=dict(
        title="The Mirror Hedge",
        text="A gardener wants the hedge to be a perfect mirror. Two squirrels climb from the top, one going left while "
             "the other goes right, checking that every pair of fruits matches.",
        goal="Return true if the tree is a mirror of itself.",
    ),
    spec=dict(method="isSymmetric", ret="bool", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 2, 3, 4, 4, 3]], expected=True), dict(args=[[1, 2, 2, None, 3, None, 3]], expected=False)],
    scene=dict(theme="forest", layers=[dict(kind="tree", var="root", pointers=["a", "b"], label="hedge")]),
    reference="""class Solution {
public:
    bool mirror(TreeNode* a, TreeNode* b) {
        if (!a && !b) return true;
        if (!a || !b || a->val != b->val) return false;
        return mirror(a->left, b->right) && mirror(a->right, b->left);
    }
    bool isSymmetric(TreeNode* root) {
        return mirror(root->left, root->right);
    }
};""",
)

add(
    id=110, slug="balanced-binary-tree", title="Balanced Binary Tree", difficulty="Easy", world="trees", tags=["tree", "dfs"],
    story=dict(
        title="The Leaning Tree Check",
        text="A tree inspector climbs to every fruit and asks both branches how tall they are. If they differ by more "
             "than one anywhere, the tree is leaning and the answer -1 is passed all the way up.",
        goal="Return true if every node's subtrees differ in height by at most one.",
    ),
    spec=dict(method="isBalanced", ret="bool", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 9, 20, None, None, 15, 7]], expected=True), dict(args=[[1, 2, 2, 3, 3, None, None, 4, 4]], expected=False),
           dict(args=[[]], expected=True)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["l", "r"]),
    ]),
    reference="""class Solution {
public:
    int height(TreeNode* node) {
        if (!node) return 0;
        int l = height(node->left);
        if (l < 0) return -1;
        int r = height(node->right);
        if (r < 0 || abs(l - r) > 1) return -1;
        return 1 + max(l, r);
    }
    bool isBalanced(TreeNode* root) {
        return height(root) >= 0;
    }
};""",
)

add(
    id=199, slug="binary-tree-right-side-view", title="Binary Tree Right Side View", difficulty="Medium", world="trees",
    tags=["tree", "bfs", "dfs"],
    story=dict(
        title="The View from the East Window",
        text="Standing to the right of the orchard, you only see the last fruit on each row. Pickers queue row by row and "
             "the last one out of each row gets written down.",
        goal="Return the values visible from the right side, top to bottom.",
    ),
    spec=dict(method="rightSideView", ret="vector<int>", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3, None, 5, None, 4]], expected=[1, 3, 4]), dict(args=[[1, None, 3]], expected=[1, 3]), dict(args=[[]], expected=[])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="pickers"),
        dict(kind="array", var="res", label="seen from the right", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int> res;
        if (!root) return res;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            int sz = q.size();
            for (int k = 0; k < sz; k++) {
                TreeNode* node = q.front();
                q.pop();
                if (k == sz - 1) res.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
        }
        return res;
    }
};""",
)

add(
    id=230, slug="kth-smallest-element-in-a-bst", title="Kth Smallest Element in a BST", difficulty="Medium", world="trees",
    tags=["tree", "dfs", "bst"],
    story=dict(
        title="Picking Fruit in Order",
        text="In a sorted orchard the smallest fruit is always as far left as you can go. A picker slides down-left, "
             "stacking every fruit passed, then picks from the stack in increasing order, counting to k.",
        goal="Return the k-th smallest value.",
    ),
    spec=dict(method="kthSmallest", ret="int", params=[["TreeNode*", "root"], ["int", "k"]]),
    tests=[dict(args=[[3, 1, 4, None, 2], 1], expected=1), dict(args=[[5, 3, 6, 2, 4, None, None, 1], 3], expected=3)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["cur"], label="orchard"),
        dict(kind="row", children=[dict(kind="stack", var="st", label="fruit passed"), dict(kind="values", vars=["k"])]),
    ]),
    reference="""class Solution {
public:
    int kthSmallest(TreeNode* root, int k) {
        stack<TreeNode*> st;
        TreeNode* cur = root;
        while (cur || !st.empty()) {
            while (cur) {
                st.push(cur);
                cur = cur->left;
            }
            cur = st.top();
            st.pop();
            if (--k == 0) return cur->val;
            cur = cur->right;
        }
        return -1;
    }
};""",
)

add(
    id=973, slug="k-closest-points-to-origin", title="K Closest Points to Origin", difficulty="Medium", world="heap",
    tags=["array", "math", "heap", "sorting"],
    story=dict(
        title="The Nearest Campfires",
        text="Scouts report campfires on a map. A ranger keeps a pyramid of the k nearest so far with the farthest of "
             "them on top, ready to be swapped out for anything closer.",
        goal="Return the k points closest to (0, 0), in any order.",
    ),
    spec=dict(method="kClosest", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "points"], ["int", "k"]]),
    compare="unordered",
    tests=[dict(args=[[[1, 3], [-2, 2]], 1], expected=[[-2, 2]]), dict(args=[[[3, 3], [5, -1], [-2, 4]], 2], expected=[[3, 3], [-2, 4]])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="points", label="campfires", style="tiles", pointers=["i"]),
        dict(kind="heap", var="pq", label="k nearest [dist², index], farthest on top"),
        dict(kind="values", vars=["d", "k"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        priority_queue<pair<int, int>> pq;
        for (int i = 0; i < (int)points.size(); i++) {
            int d = points[i][0] * points[i][0] + points[i][1] * points[i][1];
            pq.push({d, i});
            if ((int)pq.size() > k) pq.pop();
        }
        vector<vector<int>> res;
        while (!pq.empty()) {
            res.push_back(points[pq.top().second]);
            pq.pop();
        }
        return res;
    }
};""",
)

add(
    id=547, slug="number-of-provinces", title="Number of Provinces", difficulty="Medium", world="graphs",
    tags=["graph", "dfs", "bfs", "union-find"],
    story=dict(
        title="Counting the Kingdoms",
        text="A table says which towns share a road. An envoy visits every unvisited town, following roads to stamp every "
             "town it can reach; each fresh start is a new kingdom.",
        goal="Return how many separate groups of connected towns there are.",
    ),
    spec=dict(method="findCircleNum", ret="int", params=[["vector<vector<int>>&", "isConnected"]]),
    tests=[dict(args=[[[1, 1, 0], [1, 1, 0], [0, 0, 1]]], expected=2), dict(args=[[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], expected=3),
           dict(args=[[[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1]]], expected=1)],
    visualTest=2,
    scene=dict(theme="forest", layers=[
        dict(kind="row", children=[
            dict(kind="grid", var="isConnected", palette="dp", label="road table", pointers=[["u", "v"]]),
            dict(kind="array", var="seen", label="stamped", style="tiles", pointers=["u"]),
        ]),
        dict(kind="values", vars=["provinces"]),
    ]),
    reference="""class Solution {
public:
    vector<bool> seen;
    void visit(vector<vector<int>>& isConnected, int u) {
        seen[u] = true;
        for (int v = 0; v < (int)isConnected.size(); v++) {
            if (isConnected[u][v] && !seen[v]) visit(isConnected, v);
        }
    }
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size(), provinces = 0;
        seen.assign(n, false);
        for (int u = 0; u < n; u++) {
            if (!seen[u]) {
                provinces++;
                visit(isConnected, u);
            }
        }
        return provinces;
    }
};""",
)

add(
    id=17, slug="letter-combinations-of-a-phone-number", title="Letter Combinations of a Phone Number", difficulty="Medium",
    world="backtracking", tags=["hash-table", "string", "backtracking"],
    story=dict(
        title="The Old Keypad",
        text="Each key on an old phone holds a few letters. Behind every door you pick one letter for the next digit, "
             "spell as far as you can, then step back out to try the next letter.",
        goal="Return every word the digits could spell (any order).",
    ),
    spec=dict(method="letterCombinations", ret="vector<string>", params=[["string", "digits"]]),
    compare="unordered",
    tests=[dict(args=["23"], expected=["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]), dict(args=[""], expected=[]), dict(args=["2"], expected=["a", "b", "c"])],
    scene=dict(theme="cave", layers=[
        dict(kind="string", var="digits", label="digits", pointers=["i"]),
        dict(kind="values", vars=["path", "keys"]),
        dict(kind="array", var="res", label="words", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> pad = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> res;
    string path;
    void go(string& digits, int i) {
        if (i == (int)digits.size()) {
            res.push_back(path);
            return;
        }
        string keys = pad[digits[i] - '0'];
        for (char c : keys) {
            path.push_back(c);
            go(digits, i + 1);
            path.pop_back();
        }
    }
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};
        go(digits, 0);
        return res;
    }
};""",
)

add(
    id=22, slug="generate-parentheses", title="Generate Parentheses", difficulty="Medium", world="backtracking",
    tags=["string", "dynamic-programming", "backtracking"],
    story=dict(
        title="Balanced Doorways",
        text="A builder lays n opening and n closing arches. At each door they may open a new arch if any are left, or "
             "close one if more are open than closed, backing out to try the other choice.",
        goal="Return every balanced arrangement of n pairs (any order).",
    ),
    spec=dict(method="generateParenthesis", ret="vector<string>", params=[["int", "n"]]),
    compare="unordered",
    tests=[dict(args=[3], expected=["((()))", "(()())", "(())()", "()(())", "()()()"]), dict(args=[1], expected=["()"])],
    visualTest=0,
    scene=dict(theme="cave", layers=[
        dict(kind="values", vars=["path", "open", "close", "n"]),
        dict(kind="array", var="res", label="finished", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> res;
    string path;
    void go(int open, int close, int n) {
        if ((int)path.size() == 2 * n) {
            res.push_back(path);
            return;
        }
        if (open < n) {
            path.push_back('(');
            go(open + 1, close, n);
            path.pop_back();
        }
        if (close < open) {
            path.push_back(')');
            go(open, close + 1, n);
            path.pop_back();
        }
    }
    vector<string> generateParenthesis(int n) {
        go(0, 0, n);
        return res;
    }
};""",
)

add(
    id=746, slug="min-cost-climbing-stairs", title="Min Cost Climbing Stairs", difficulty="Easy", world="dp",
    tags=["array", "dynamic-programming"],
    story=dict(
        title="The Toll Staircase",
        text="Every stair charges a toll and you may climb one or two at a time, starting on stair 0 or 1. The farmer "
             "chalks on each step the cheapest way to arrive there.",
        goal="Return the cheapest cost to get past the top stair.",
    ),
    spec=dict(method="minCostClimbingStairs", ret="int", params=[["vector<int>&", "cost"]]),
    tests=[dict(args=[[10, 15, 20]], expected=15), dict(args=[[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]], expected=6)],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="cost", label="tolls", pointers=["i"]),
        dict(kind="array", var="dp", label="cheapest arrival", style="tiles", pointers=["i"]),
    ]),
    reference="""class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int n = cost.size();
        vector<int> dp(n + 1, 0);
        for (int i = 2; i <= n; i++) {
            dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
        }
        return dp[n];
    }
};""",
)

add(
    id=64, slug="minimum-path-sum", title="Minimum Path Sum", difficulty="Medium", world="dp",
    tags=["array", "dynamic-programming", "matrix"],
    story=dict(
        title="The Cheapest Field Crossing",
        text="Each plot charges a fee and the cart only rolls right or down. Plot by plot, the farmer overwrites each fee "
             "with the cheapest total to reach it.",
        goal="Return the cheapest total from the top-left to the bottom-right plot.",
    ),
    spec=dict(method="minPathSum", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[1, 3, 1], [1, 5, 1], [4, 2, 1]]], expected=7), dict(args=[[[1, 2, 3], [4, 5, 6]]], expected=12)],
    scene=dict(theme="farm", layers=[dict(kind="grid", var="grid", palette="dp", label="field fees", pointers=[["i", "j"]])]),
    reference="""class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (i == 0 && j == 0) continue;
                int up = i > 0 ? grid[i - 1][j] : INT_MAX;
                int left = j > 0 ? grid[i][j - 1] : INT_MAX;
                grid[i][j] += min(up, left);
            }
        }
        return grid[m - 1][n - 1];
    }
};""",
)

add(
    id=45, slug="jump-game-ii", title="Jump Game II", difficulty="Medium", world="greedy",
    tags=["array", "greedy", "dynamic-programming"],
    story=dict(
        title="Fewest Leaps Across the River",
        text="Stones say how far you can leap. The hiker treats each leap as a range of stones; while walking through "
             "the current range they note the farthest next range, and leap when the current one runs out.",
        goal="Return the fewest leaps to reach the last stone.",
    ),
    spec=dict(method="jump", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 3, 1, 1, 4]], expected=2), dict(args=[[2, 3, 0, 1, 4]], expected=2), dict(args=[[0]], expected=0)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="stones", pointers=["i", "end", "far"]),
        dict(kind="values", vars=["jumps"]),
    ]),
    reference="""class Solution {
public:
    int jump(vector<int>& nums) {
        int jumps = 0, end = 0, far = 0;
        for (int i = 0; i + 1 < (int)nums.size(); i++) {
            far = max(far, i + nums[i]);
            if (i == end) {
                jumps++;
                end = far;
            }
        }
        return jumps;
    }
};""",
)

add(
    id=134, slug="gas-station", title="Gas Station", difficulty="Medium", world="greedy", tags=["array", "greedy"],
    story=dict(
        title="The Round-Trip Road",
        text="Stations sit on a ring road, each giving some fuel and costing some to reach the next. A driver keeps a "
             "tank; whenever it runs dry, every station so far was a bad start, so they restart from the next one.",
        goal="Return the station to start from to finish the loop, or -1.",
    ),
    spec=dict(method="canCompleteCircuit", ret="int", params=[["vector<int>&", "gas"], ["vector<int>&", "cost"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], expected=3), dict(args=[[2, 3, 4], [3, 4, 3]], expected=-1)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="gas", label="fuel given", pointers=["i", "start"]),
        dict(kind="array", var="cost", label="fuel to next", pointers=["i"]),
        dict(kind="values", vars=["tank", "total"]),
    ]),
    reference="""class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int total = 0, tank = 0, start = 0;
        for (int i = 0; i < (int)gas.size(); i++) {
            int diff = gas[i] - cost[i];
            total += diff;
            tank += diff;
            if (tank < 0) {
                start = i + 1;
                tank = 0;
            }
        }
        return total < 0 ? -1 : start;
    }
};""",
)

add(
    id=268, slug="missing-number", title="Missing Number", difficulty="Easy", world="bits",
    tags=["array", "math", "bit-manipulation"],
    story=dict(
        title="The Missing Lamp",
        text="Lamps numbered 0..n should all be here, but one is missing. Toggle the lamps of every index and every "
             "number; pairs cancel out and only the missing number stays lit.",
        goal="Return the number in 0..n that is not in the array.",
    ),
    spec=dict(method="missingNumber", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[3, 0, 1]], expected=2), dict(args=[[0, 1]], expected=2), dict(args=[[9, 6, 4, 2, 3, 5, 7, 0, 1]], expected=8)],
    scene=dict(theme="space", layers=[
        dict(kind="array", var="nums", label="lamps found", pointers=["i"]),
        dict(kind="values", vars=["x"]),
    ]),
    reference="""class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size(), x = n;
        for (int i = 0; i < n; i++) x ^= i ^ nums[i];
        return x;
    }
};""",
)
