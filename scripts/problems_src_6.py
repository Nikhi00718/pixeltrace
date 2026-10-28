"""Sixth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=1480, slug="running-sum-of-1d-array", title="Running Sum of 1d Array", difficulty="Easy", world="arrays",
    tags=["array", "prefix-sum"],
    story=dict(
        title="The Piggy Bank Ledger",
        text="Each day's savings are written on a crate. A clerk walks the row and rewrites every crate with the total "
             "saved up to and including that day.",
        goal="Return the running totals.",
    ),
    spec=dict(method="runningSum", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 4]], expected=[1, 3, 6, 10]), dict(args=[[3, 1, 2, 10, 1]], expected=[3, 4, 6, 16, 17])],
    visualTest=1,
    scene=dict(theme="dock", layers=[dict(kind="array", var="nums", label="savings", pointers=["i"])]),
    reference="""class Solution {
public:
    vector<int> runningSum(vector<int>& nums) {
        for (int i = 1; i < (int)nums.size(); i++) nums[i] += nums[i - 1];
        return nums;
    }
};""",
)

add(
    id=724, slug="find-pivot-index", title="Find Pivot Index", difficulty="Easy", world="arrays", tags=["array", "prefix-sum"],
    story=dict(
        title="Balancing the Seesaw",
        text="Weights sit along a seesaw. A worker walks it, carrying the weight already behind them; the pivot is where "
             "that equals everything still ahead.",
        goal="Return the leftmost index where the left and right sums match, or -1.",
    ),
    spec=dict(method="pivotIndex", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 7, 3, 6, 5, 6]], expected=3), dict(args=[[1, 2, 3]], expected=-1), dict(args=[[2, 1, -1]], expected=0)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="seesaw", pointers=["i"]),
        dict(kind="values", vars=["left", "total"]),
    ]),
    reference="""class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        int total = 0;
        for (int x : nums) total += x;
        int left = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (left == total - left - nums[i]) return i;
            left += nums[i];
        }
        return -1;
    }
};""",
)

add(
    id=448, slug="find-all-numbers-disappeared-in-an-array", title="Find All Numbers Disappeared in an Array", difficulty="Easy",
    world="arrays", tags=["array", "hash-table"],
    story=dict(
        title="The Roll Call",
        text="Badges 1..n should all be present. For every badge seen, the clerk flips the crate at that number's "
             "position to negative. Crates left positive mark the badges nobody brought.",
        goal="Return every number in 1..n that is missing.",
    ),
    spec=dict(method="findDisappearedNumbers", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[4, 3, 2, 7, 8, 2, 3, 1]], expected=[5, 6]), dict(args=[[1, 1]], expected=[2])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates", pointers=["i", "j"]),
        dict(kind="array", var="res", label="missing", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        for (int i = 0; i < (int)nums.size(); i++) {
            int j = abs(nums[i]) - 1;
            if (nums[j] > 0) nums[j] = -nums[j];
        }
        vector<int> res;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (nums[i] > 0) res.push_back(i + 1);
        }
        return res;
    }
};""",
)

add(
    id=1679, slug="max-number-of-k-sum-pairs", title="Max Number of K-Sum Pairs", difficulty="Medium", world="two-pointers",
    tags=["array", "hash-table", "two-pointers", "sorting"],
    story=dict(
        title="Packing Pairs of Crates",
        text="Crates are shipped in pairs that must weigh exactly k. On the sorted dock, two dockhands at the ends pair "
             "up matching crates and step in; too light, the left moves; too heavy, the right moves.",
        goal="Return how many pairs summing to k can be removed.",
    ),
    spec=dict(method="maxOperations", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 3, 4], 5], expected=2), dict(args=[[3, 1, 3, 4, 3], 6], expected=1), dict(args=[[2, 5, 4, 4, 1, 3, 4, 4, 1, 4, 4, 1, 2, 1, 2, 2, 3, 2, 4, 2], 3], expected=4)],
    visualTest=0,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="sorted crates", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["k", "ops"]),
    ]),
    reference="""class Solution {
public:
    int maxOperations(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        int l = 0, r = nums.size() - 1, ops = 0;
        while (l < r) {
            int s = nums[l] + nums[r];
            if (s == k) {
                ops++;
                l++;
                r--;
            } else if (s < k) {
                l++;
            } else {
                r--;
            }
        }
        return ops;
    }
};""",
)

add(
    id=881, slug="boats-to-save-people", title="Boats to Save People", difficulty="Medium", world="two-pointers",
    tags=["array", "two-pointers", "greedy", "sorting"],
    story=dict(
        title="The Rescue Boats",
        text="Each boat holds two people up to a weight limit. Sorted by weight, the heaviest waiting person always gets "
             "a boat, and takes the lightest along if they fit.",
        goal="Return the fewest boats needed.",
    ),
    spec=dict(method="numRescueBoats", ret="int", params=[["vector<int>&", "people"], ["int", "limit"]]),
    tests=[dict(args=[[1, 2], 3], expected=1), dict(args=[[3, 2, 2, 1], 3], expected=3), dict(args=[[3, 5, 3, 4], 5], expected=4)],
    visualTest=1,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="people", label="waiting (sorted)", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["limit", "boats"]),
    ]),
    reference="""class Solution {
public:
    int numRescueBoats(vector<int>& people, int limit) {
        sort(people.begin(), people.end());
        int l = 0, r = people.size() - 1, boats = 0;
        while (l <= r) {
            if (people[l] + people[r] <= limit) l++;
            r--;
            boats++;
        }
        return boats;
    }
};""",
)

add(
    id=1493, slug="longest-subarray-of-1s-after-deleting-one-element", title="Longest Subarray of 1's After Deleting One Element",
    difficulty="Medium", world="sliding-window", tags=["array", "dynamic-programming", "sliding-window"],
    story=dict(
        title="One Broken Lamp",
        text="A row of lamps has some broken ones (0). You must pull out exactly one lamp. The window may hold at most one "
             "broken lamp; its length minus the pulled lamp is the lit stretch.",
        goal="Return the longest run of 1s after deleting one element.",
    ),
    spec=dict(method="longestSubarray", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 1, 0, 1]], expected=3), dict(args=[[0, 1, 1, 1, 0, 1, 1, 0, 1]], expected=5), dict(args=[[1, 1, 1]], expected=2)],
    visualTest=1,
    scene=dict(theme="space", layers=[
        dict(kind="array", var="nums", label="lamps", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["zeros", "best"]),
    ]),
    reference="""class Solution {
public:
    int longestSubarray(vector<int>& nums) {
        int l = 0, zeros = 0, best = 0;
        for (int r = 0; r < (int)nums.size(); r++) {
            if (nums[r] == 0) zeros++;
            while (zeros > 1) {
                if (nums[l] == 0) zeros--;
                l++;
            }
            best = max(best, r - l);
        }
        return best;
    }
};""",
)

add(
    id=1423, slug="maximum-points-you-can-obtain-from-cards", title="Maximum Points You Can Obtain from Cards", difficulty="Medium",
    world="sliding-window", tags=["array", "sliding-window", "prefix-sum"],
    story=dict(
        title="Cards from Both Ends",
        text="You may take k cards from either end of a row. Whatever you take, the cards left behind form one middle "
             "block of n-k cards, so slide that block along and keep it as small as possible.",
        goal="Return the most points you can take.",
    ),
    spec=dict(method="maxScore", ret="int", params=[["vector<int>&", "cardPoints"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5, 6, 1], 3], expected=12), dict(args=[[2, 2, 2], 2], expected=4), dict(args=[[9, 7, 7, 9, 7, 7, 9], 7], expected=55)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="cardPoints", label="cards", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["total", "mid", "least"]),
    ]),
    reference="""class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        int n = cardPoints.size(), w = n - k, total = 0, mid = 0;
        for (int x : cardPoints) total += x;
        for (int r = 0; r < w; r++) mid += cardPoints[r];
        int least = mid;
        for (int r = w; r < n; r++) {
            int l = r - w + 1;
            mid += cardPoints[r] - cardPoints[l - 1];
            least = min(least, mid);
        }
        return total - least;
    }
};""",
)

add(
    id=844, slug="backspace-string-compare", title="Backspace String Compare", difficulty="Easy", world="stack",
    tags=["two-pointers", "string", "stack", "simulation"],
    story=dict(
        title="Two Clumsy Typists",
        text="Two typists hit # whenever they make a mistake, which erases the last letter. Each builds a stack of the "
             "letters that survive, and the two stacks are compared.",
        goal="Return true if both end up with the same text.",
    ),
    spec=dict(method="backspaceCompare", ret="bool", params=[["string", "s"], ["string", "t"]]),
    tests=[dict(args=["ab#c", "ad#c"], expected=True), dict(args=["ab##", "c#d#"], expected=True), dict(args=["a#c", "b"], expected=False)],
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="text", label="keys typed", pointers=["i"]),
        dict(kind="stack", var="out", label="letters kept"),
        dict(kind="row", children=[dict(kind="values", vars=["a", "b"])]),
    ]),
    reference="""class Solution {
public:
    string build(string& text) {
        string out;
        for (int i = 0; i < (int)text.size(); i++) {
            if (text[i] == '#') {
                if (!out.empty()) out.pop_back();
            } else {
                out.push_back(text[i]);
            }
        }
        return out;
    }
    bool backspaceCompare(string s, string t) {
        string a = build(s);
        string b = build(t);
        return a == b;
    }
};""",
)

add(
    id=946, slug="validate-stack-sequences", title="Validate Stack Sequences", difficulty="Medium", world="stack",
    tags=["array", "stack", "simulation"],
    story=dict(
        title="Can the Crane Do It?",
        text="A crane stacks crates in the pushed order. After each push it lifts off as many crates as possible while "
             "the top crate is the next one the popped order expects.",
        goal="Return true if the popped order is possible with one stack.",
    ),
    spec=dict(method="validateStackSequences", ret="bool", params=[["vector<int>&", "pushed"], ["vector<int>&", "popped"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], [4, 5, 3, 2, 1]], expected=True), dict(args=[[1, 2, 3, 4, 5], [4, 3, 5, 1, 2]], expected=False)],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="pushed", label="arrives", pointers=["i"]),
        dict(kind="array", var="popped", label="must leave", pointers=["j"]),
        dict(kind="stack", var="st", label="crane stack"),
    ]),
    reference="""class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        stack<int> st;
        int j = 0;
        for (int i = 0; i < (int)pushed.size(); i++) {
            st.push(pushed[i]);
            while (!st.empty() && st.top() == popped[j]) {
                st.pop();
                j++;
            }
        }
        return st.empty();
    }
};""",
)

add(
    id=2300, slug="successful-pairs-of-spells-and-potions", title="Successful Pairs of Spells and Potions", difficulty="Medium",
    world="binary-search", tags=["array", "two-pointers", "binary-search", "sorting"],
    story=dict(
        title="The Potion Shelf",
        text="Potions are sorted by strength. For each spell, a guard binary-searches the shelf for the weakest potion "
             "that still reaches the needed power; everything to its right works too.",
        goal="For each spell, return how many potions make a successful pair.",
    ),
    spec=dict(method="successfulPairs", ret="vector<int>", params=[["vector<int>&", "spells"], ["vector<int>&", "potions"], ["long long", "success"]]),
    tests=[dict(args=[[5, 1, 3], [1, 2, 3, 4, 5], 7], expected=[4, 0, 3]), dict(args=[[3, 1, 2], [8, 5, 8], 16], expected=[2, 0, 2])],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="spells", label="spells", pointers=["i"]),
        dict(kind="array", var="potions", label="potion shelf (sorted)", pointers=["lo", "mid", "hi"], window=["lo", "hi"], windowExclusive=True),
        dict(kind="array", var="res", label="pairs", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        sort(potions.begin(), potions.end());
        int m = potions.size();
        vector<int> res;
        for (int i = 0; i < (int)spells.size(); i++) {
            int lo = 0, hi = m;
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                if ((long long)spells[i] * potions[mid] >= success) hi = mid;
                else lo = mid + 1;
            }
            res.push_back(m - lo);
        }
        return res;
    }
};""",
)

add(
    id=441, slug="arranging-coins", title="Arranging Coins", difficulty="Easy", world="binary-search", tags=["math", "binary-search"],
    story=dict(
        title="The Coin Staircase",
        text="Coins are stacked into a staircase: 1 in the first row, 2 in the next, and so on. A guard binary-searches "
             "how many full rows fit, since k rows need k(k+1)/2 coins.",
        goal="Return the number of complete rows.",
    ),
    spec=dict(method="arrangeCoins", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[5], expected=2), dict(args=[8], expected=3), dict(args=[1804289383], expected=60070)],
    visualTest=2,
    scene=dict(theme="cave", layers=[dict(kind="values", vars=["n", "lo", "mid", "hi", "need"])]),
    reference="""class Solution {
public:
    int arrangeCoins(int n) {
        long long lo = 0, hi = n;
        while (lo < hi) {
            long long mid = (lo + hi + 1) / 2;
            long long need = mid * (mid + 1) / 2;
            if (need <= n) lo = mid;
            else hi = mid - 1;
        }
        return lo;
    }
};""",
)

add(
    id=203, slug="remove-linked-list-elements", title="Remove Linked List Elements", difficulty="Easy", world="linked-list",
    tags=["linked-list", "recursion"],
    story=dict(
        title="Unhooking the Bad Cars",
        text="Every car carrying the banned cargo must go. A worker walks from a dummy engine, and whenever the next car "
             "is banned, couples straight past it.",
        goal="Remove every node with value val and return the train.",
    ),
    spec=dict(method="removeElements", ret="ListNode*", params=[["ListNode*", "head"], ["int", "val"]]),
    tests=[dict(args=[[1, 2, 6, 3, 4, 5, 6], 6], expected=[1, 2, 3, 4, 5]), dict(args=[[], 1], expected=[]), dict(args=[[7, 7, 7, 7], 7], expected=[])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "cur"], heads=["head"], label="train"),
        dict(kind="values", vars=["val"]),
    ]),
    reference="""class Solution {
public:
    ListNode* removeElements(ListNode* head, int val) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* cur = dummy;
        while (cur->next) {
            if (cur->next->val == val) cur->next = cur->next->next;
            else cur = cur->next;
        }
        return dummy->next;
    }
};""",
)

add(
    id=1721, slug="swapping-nodes-in-a-linked-list", title="Swapping Nodes in a Linked List", difficulty="Medium",
    world="linked-list", tags=["linked-list", "two-pointers"],
    story=dict(
        title="Swapping the Cargo",
        text="The cargo of the k-th car from the front and the k-th from the back must trade places. A scout walks k "
             "cars ahead; when it hits the end, a second walker is on the k-th from the back.",
        goal="Swap the values of the two nodes and return the train.",
    ),
    spec=dict(method="swapNodes", ret="ListNode*", params=[["ListNode*", "head"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], 2], expected=[1, 4, 3, 2, 5]), dict(args=[[7, 9, 6, 6, 7, 8, 3, 0, 9, 5], 5], expected=[7, 9, 6, 6, 8, 7, 3, 0, 9, 5])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "first", "scout", "second"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* swapNodes(ListNode* head, int k) {
        ListNode* first = head;
        for (int s = 1; s < k; s++) first = first->next;
        ListNode* scout = first;
        ListNode* second = head;
        while (scout->next) {
            scout = scout->next;
            second = second->next;
        }
        swap(first->val, second->val);
        return head;
    }
};""",
)

add(
    id=617, slug="merge-two-binary-trees", title="Merge Two Binary Trees", difficulty="Easy", world="trees",
    tags=["tree", "dfs", "bfs"],
    story=dict(
        title="Grafting Two Orchards",
        text="Two orchards are laid on top of each other. Where both have a fruit, the weights add up on the first tree; "
             "where only the second has a branch, it is grafted onto the first.",
        goal="Return the merged tree.",
    ),
    spec=dict(method="mergeTrees", ret="TreeNode*", params=[["TreeNode*", "root1"], ["TreeNode*", "root2"]]),
    tests=[dict(args=[[1, 3, 2, 5], [2, 1, 3, None, 4, None, 7]], expected=[3, 4, 5, 5, 4, None, 7]), dict(args=[[1], [1, 2]], expected=[2, 2])],
    scene=dict(theme="forest", layers=[dict(kind="row", children=[
        dict(kind="tree", var="root1", pointers=["root1"], label="orchard 1"),
        dict(kind="tree", var="root2", pointers=["root2"], label="orchard 2"),
    ])]),
    reference="""class Solution {
public:
    TreeNode* mergeTrees(TreeNode* root1, TreeNode* root2) {
        if (!root1) return root2;
        if (!root2) return root1;
        root1->val += root2->val;
        root1->left = mergeTrees(root1->left, root2->left);
        root1->right = mergeTrees(root1->right, root2->right);
        return root1;
    }
};""",
)

add(
    id=103, slug="binary-tree-zigzag-level-order-traversal", title="Binary Tree Zigzag Level Order Traversal", difficulty="Medium",
    world="trees", tags=["tree", "bfs"],
    story=dict(
        title="The Zigzag Harvest",
        text="Pickers harvest the orchard row by row, but every other row they write their basket down backwards, so "
             "the record zigzags left-right, right-left.",
        goal="Return the values level by level, alternating direction.",
    ),
    spec=dict(method="zigzagLevelOrder", ret="vector<vector<int>>", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 9, 20, None, None, 15, 7]], expected=[[3], [20, 9], [15, 7]]), dict(args=[[1, 2, 3, 4, None, None, 5]], expected=[[1], [3, 2], [4, 5]]),
           dict(args=[[]], expected=[])],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="pickers"),
        dict(kind="array", var="level", label="this row", style="tiles"),
        dict(kind="values", vars=["leftToRight"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> res;
        if (!root) return res;
        queue<TreeNode*> q;
        q.push(root);
        bool leftToRight = true;
        while (!q.empty()) {
            int sz = q.size();
            vector<int> level;
            for (int k = 0; k < sz; k++) {
                TreeNode* node = q.front();
                q.pop();
                level.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            if (!leftToRight) reverse(level.begin(), level.end());
            res.push_back(level);
            leftToRight = !leftToRight;
        }
        return res;
    }
};""",
)

add(
    id=2558, slug="take-gifts-from-the-richest-pile", title="Take Gifts From the Richest Pile", difficulty="Easy", world="heap",
    tags=["array", "heap", "simulation"],
    story=dict(
        title="Robin Hood's Rounds",
        text="Every second, Robin takes from the richest pile, leaving only the square root of it behind. A pyramid keeps "
             "the richest pile on top.",
        goal="Return how many gifts are left after k seconds.",
    ),
    spec=dict(method="pickGifts", ret="long long", params=[["vector<int>&", "gifts"], ["int", "k"]]),
    tests=[dict(args=[[25, 64, 9, 4, 100], 4], expected=29), dict(args=[[1, 1, 1, 1], 4], expected=4)],
    scene=dict(theme="market", layers=[
        dict(kind="heap", var="pq", label="piles (richest on top)"),
        dict(kind="values", vars=["k", "top", "left"]),
    ]),
    reference="""class Solution {
public:
    long long pickGifts(vector<int>& gifts, int k) {
        priority_queue<int> pq(gifts.begin(), gifts.end());
        while (k-- > 0) {
            int top = pq.top();
            pq.pop();
            pq.push((int)sqrt(top));
        }
        long long left = 0;
        while (!pq.empty()) {
            left += pq.top();
            pq.pop();
        }
        return left;
    }
};""",
)

add(
    id=841, slug="keys-and-rooms", title="Keys and Rooms", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "graph"],
    story=dict(
        title="The Castle of Locked Rooms",
        text="Only room 0 is open. Each room holds keys to other rooms. A knight explores room by room with the keys "
             "found so far; green rooms have been visited.",
        goal="Return true if every room can be visited.",
    ),
    spec=dict(method="canVisitAllRooms", ret="bool", params=[["vector<vector<int>>&", "rooms"]]),
    tests=[dict(args=[[[1], [2], [3], []]], expected=True), dict(args=[[[1, 3], [3, 0, 1], [2], [0]]], expected=False)],
    scene=dict(theme="castle", layers=[
        dict(kind="graph", adj="rooms", directed=True, state="seen", pointers=["u"], label="rooms"),
        dict(kind="stack", var="st", label="keys in hand"),
    ]),
    reference="""class Solution {
public:
    bool canVisitAllRooms(vector<vector<int>>& rooms) {
        int n = rooms.size();
        vector<int> seen(n, 0);
        stack<int> st;
        st.push(0);
        seen[0] = 2;
        while (!st.empty()) {
            int u = st.top();
            st.pop();
            for (int v : rooms[u]) {
                if (!seen[v]) {
                    seen[v] = 2;
                    st.push(v);
                }
            }
        }
        for (int s : seen) {
            if (!s) return false;
        }
        return true;
    }
};""",
)

add(
    id=1926, slug="nearest-exit-from-entrance-in-maze", title="Nearest Exit from Entrance in Maze", difficulty="Medium",
    world="graphs", tags=["array", "bfs", "matrix"],
    story=dict(
        title="Escape the Hedge Maze",
        text="You start inside a hedge maze (+ are hedges). Footsteps spread outward one ring at a time; the first open "
             "tile on the border (other than where you started) is the nearest exit.",
        goal="Return the fewest steps to an exit, or -1.",
    ),
    spec=dict(method="nearestExit", ret="int", params=[["vector<vector<char>>&", "maze"], ["vector<int>&", "entrance"]]),
    tests=[dict(args=[[["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]], [1, 2]], expected=1),
           dict(args=[[["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]], [1, 0]], expected=2),
           dict(args=[[[".", "+"]], [0, 0]], expected=-1)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="maze", palette="board", label="hedge maze", pointers=[["r", "c"]]),
        dict(kind="queue", var="q", label="frontier (r,c)"),
        dict(kind="values", vars=["steps"]),
    ]),
    reference="""class Solution {
public:
    int nearestExit(vector<vector<char>>& maze, vector<int>& entrance) {
        int m = maze.size(), n = maze[0].size();
        queue<pair<int, int>> q;
        q.push({entrance[0], entrance[1]});
        maze[entrance[0]][entrance[1]] = '+';
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        int steps = 0;
        while (!q.empty()) {
            steps++;
            int sz = q.size();
            for (int k = 0; k < sz; k++) {
                auto [r, c] = q.front();
                q.pop();
                for (int d = 0; d < 4; d++) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nc < 0 || nr >= m || nc >= n || maze[nr][nc] == '+') continue;
                    if (nr == 0 || nc == 0 || nr == m - 1 || nc == n - 1) return steps;
                    maze[nr][nc] = '+';
                    q.push({nr, nc});
                }
            }
        }
        return -1;
    }
};""",
)

add(
    id=40, slug="combination-sum-ii", title="Combination Sum II", difficulty="Medium", world="backtracking",
    tags=["array", "backtracking"],
    story=dict(
        title="Exact Change, Each Coin Once",
        text="This time each coin can be used once, and some coins are twins. Sorted, the shopkeeper skips a twin at the "
             "same door so no combination repeats, and stops early once coins get too big.",
        goal="Return every unique combination that adds up to target (any order).",
    ),
    spec=dict(method="combinationSum2", ret="vector<vector<int>>", params=[["vector<int>&", "candidates"], ["int", "target"]]),
    compare="unordered-deep",
    tests=[dict(args=[[10, 1, 2, 7, 6, 1, 5], 8], expected=[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]), dict(args=[[2, 5, 2, 1, 2], 5], expected=[[1, 2, 2], [5]])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="candidates", label="coins (sorted)", pointers=["start", "i"]),
        dict(kind="array", var="path", label="bag", style="tiles"),
        dict(kind="values", vars=["remain"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void go(vector<int>& candidates, int start, int remain) {
        if (remain == 0) {
            res.push_back(path);
            return;
        }
        for (int i = start; i < (int)candidates.size(); i++) {
            if (i > start && candidates[i] == candidates[i - 1]) continue;
            if (candidates[i] > remain) break;
            path.push_back(candidates[i]);
            go(candidates, i + 1, remain - candidates[i]);
            path.pop_back();
        }
    }
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        go(candidates, 0, target);
        return res;
    }
};""",
)

add(
    id=216, slug="combination-sum-iii", title="Combination Sum III", difficulty="Medium", world="backtracking",
    tags=["array", "backtracking"],
    story=dict(
        title="Nine Numbered Tiles",
        text="Tiles numbered 1 to 9 can each be used once. Pick exactly k of them adding up to n: at each door try the "
             "next tile, go deeper, then put it back.",
        goal="Return every set of k distinct digits summing to n (any order).",
    ),
    spec=dict(method="combinationSum3", ret="vector<vector<int>>", params=[["int", "k"], ["int", "n"]]),
    compare="unordered-deep",
    tests=[dict(args=[3, 7], expected=[[1, 2, 4]]), dict(args=[3, 9], expected=[[1, 2, 6], [1, 3, 5], [2, 3, 4]]), dict(args=[4, 1], expected=[])],
    visualTest=1,
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="path", label="tiles picked", style="tiles"),
        dict(kind="values", vars=["start", "x", "remain", "k"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void go(int start, int remain, int k) {
        if ((int)path.size() == k) {
            if (remain == 0) res.push_back(path);
            return;
        }
        for (int x = start; x <= 9 && x <= remain; x++) {
            path.push_back(x);
            go(x + 1, remain - x, k);
            path.pop_back();
        }
    }
    vector<vector<int>> combinationSum3(int k, int n) {
        go(1, n, k);
        return res;
    }
};""",
)

add(
    id=1137, slug="n-th-tribonacci-number", title="N-th Tribonacci Number", difficulty="Easy", world="dp",
    tags=["math", "dynamic-programming", "memoization"],
    story=dict(
        title="The Three-Step Frog",
        text="This frog's stair count is the sum of the three stairs below it. The farmer chalks each stair as the frog "
             "climbs.",
        goal="Return T(n), where T(0)=0, T(1)=1, T(2)=1.",
    ),
    spec=dict(method="tribonacci", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[4], expected=4), dict(args=[25], expected=1389537), dict(args=[0], expected=0)],
    scene=dict(theme="farm", layers=[dict(kind="array", var="t", label="stairs", style="tiles", pointers=["i"])]),
    reference="""class Solution {
public:
    int tribonacci(int n) {
        vector<int> t(max(n + 1, 3), 0);
        t[1] = 1;
        t[2] = 1;
        for (int i = 3; i <= n; i++) t[i] = t[i - 1] + t[i - 2] + t[i - 3];
        return t[n];
    }
};""",
)

add(
    id=518, slug="coin-change-ii", title="Coin Change II", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(
        title="How Many Ways to Pay",
        text="The ledger counts the ways to make every amount. Coins are added one type at a time; each amount gains "
             "the ways to make the amount one coin smaller.",
        goal="Return the number of combinations that make up amount.",
    ),
    spec=dict(method="change", ret="int", params=[["int", "amount"], ["vector<int>&", "coins"]]),
    tests=[dict(args=[5, [1, 2, 5]], expected=4), dict(args=[3, [2]], expected=0), dict(args=[10, [10]], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="coins", label="coin types", pointers=["c"]),
        dict(kind="array", var="ways", label="ways to make each amount", style="tiles", pointers=["a"]),
    ]),
    reference="""class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<unsigned long long> ways(amount + 1, 0);
        ways[0] = 1;
        for (int c = 0; c < (int)coins.size(); c++) {
            for (int a = coins[c]; a <= amount; a++) ways[a] += ways[a - coins[c]];
        }
        return ways[amount];
    }
};""",
)

add(
    id=1288, slug="remove-covered-intervals", title="Remove Covered Intervals", difficulty="Medium", world="intervals",
    tags=["array", "sorting"],
    story=dict(
        title="Overlapping Bookings",
        text="Bookings sorted by start (longest first on ties). The clerk tracks the furthest end seen; any booking "
             "ending inside it is fully covered and dropped.",
        goal="Return how many bookings remain after removing covered ones.",
    ),
    spec=dict(method="removeCoveredIntervals", ret="int", params=[["vector<vector<int>>&", "intervals"]]),
    tests=[dict(args=[[[1, 4], [3, 6], [2, 8]]], expected=2), dict(args=[[[1, 4], [2, 3]]], expected=1), dict(args=[[[1, 2], [1, 4], [3, 4]]], expected=1)],
    scene=dict(theme="lab", layers=[
        dict(kind="intervals", vars=["intervals"], pointers=["i"], label="bookings"),
        dict(kind="values", vars=["reach", "kept"]),
    ]),
    reference="""class Solution {
public:
    int removeCoveredIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[0] != b[0] ? a[0] < b[0] : a[1] > b[1];
        });
        int reach = 0, kept = 0;
        for (int i = 0; i < (int)intervals.size(); i++) {
            if (intervals[i][1] > reach) {
                kept++;
                reach = intervals[i][1];
            }
        }
        return kept;
    }
};""",
)

add(
    id=1710, slug="maximum-units-on-a-truck", title="Maximum Units on a Truck", difficulty="Easy", world="greedy",
    tags=["array", "greedy", "sorting"],
    story=dict(
        title="Loading the Truck",
        text="Box types list how many boxes there are and how many units each holds. The loader packs the richest boxes "
             "first until the truck is full.",
        goal="Return the most units that fit on the truck.",
    ),
    spec=dict(method="maximumUnits", ret="int", params=[["vector<vector<int>>&", "boxTypes"], ["int", "truckSize"]]),
    tests=[dict(args=[[[1, 3], [2, 2], [3, 1]], 4], expected=8), dict(args=[[[5, 10], [2, 5], [4, 7], [3, 9]], 10], expected=91)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="boxTypes", label="box types [count, units]", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["truckSize", "take", "units"]),
    ]),
    reference="""class Solution {
public:
    int maximumUnits(vector<vector<int>>& boxTypes, int truckSize) {
        sort(boxTypes.begin(), boxTypes.end(), [](const vector<int>& a, const vector<int>& b) { return a[1] > b[1]; });
        int units = 0;
        for (int i = 0; i < (int)boxTypes.size() && truckSize > 0; i++) {
            int take = min(truckSize, boxTypes[i][0]);
            units += take * boxTypes[i][1];
            truckSize -= take;
        }
        return units;
    }
};""",
)

add(
    id=1342, slug="number-of-steps-to-reduce-a-number-to-zero", title="Number of Steps to Reduce a Number to Zero",
    difficulty="Easy", world="bits", tags=["math", "bit-manipulation"],
    story=dict(
        title="Dimming the Lamps",
        text="If the last lamp is lit, switch it off (subtract 1); otherwise shift every lamp one place right (halve). "
             "Count the moves until the row is dark.",
        goal="Return the number of steps to reach zero.",
    ),
    spec=dict(method="numberOfSteps", ret="int", params=[["int", "num"]]),
    tests=[dict(args=[14], expected=6), dict(args=[8], expected=4), dict(args=[123], expected=12)],
    visualTest=2,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["num", "steps"])]),
    reference="""class Solution {
public:
    int numberOfSteps(int num) {
        int steps = 0;
        while (num > 0) {
            if (num & 1) num--;
            else num >>= 1;
            steps++;
        }
        return steps;
    }
};""",
)
