"""Second batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=26, slug="remove-duplicates-from-sorted-array", title="Remove Duplicates from Sorted Array", difficulty="Easy",
    world="two-pointers", tags=["array", "two-pointers"],
    story=dict(
        title="The Sticker Album",
        text="Sorted stickers sit in a row, some repeated. A collector walks the row; a keeper stands at the end of the "
             "unique stickers and only moves forward when the collector finds one the keeper hasn't got yet.",
        goal="Return how many unique stickers there are (they end up at the front).",
    ),
    spec=dict(method="removeDuplicates", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 1, 2]], expected=2), dict(args=[[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]], expected=5), dict(args=[[7]], expected=1)],
    visualTest=1,
    scene=dict(theme="dock", layers=[dict(kind="array", var="nums", label="album", pointers=["k", "i"])]),
    reference="""class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int k = 1;
        for (int i = 1; i < (int)nums.size(); i++) {
            if (nums[i] != nums[k - 1]) {
                nums[k] = nums[i];
                k++;
            }
        }
        return k;
    }
};""",
)

add(
    id=88, slug="merge-sorted-array", title="Merge Sorted Array", difficulty="Easy", world="two-pointers",
    tags=["array", "two-pointers", "sorting"],
    story=dict(
        title="Filling the Warehouse from the Back",
        text="The first shelf has empty slots at the end; a second sorted shelf must fit in. Workers compare the "
             "heaviest remaining crate on each shelf and place it in the last free slot, walking backwards.",
        goal="Merge the second shelf into the first so it stays sorted.",
    ),
    spec=dict(method="merge", ret="void", params=[["vector<int>&", "nums1"], ["int", "m"], ["vector<int>&", "nums2"], ["int", "n"]], output="param:0"),
    tests=[dict(args=[[1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3], expected=[1, 2, 2, 3, 5, 6]),
           dict(args=[[1], 1, [], 0], expected=[1]), dict(args=[[0], 0, [1], 1], expected=[1])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums1", label="shelf 1", pointers=["i", "w"]),
        dict(kind="array", var="nums2", label="shelf 2", pointers=["j"]),
    ]),
    reference="""class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int i = m - 1, j = n - 1, w = m + n - 1;
        while (j >= 0) {
            if (i >= 0 && nums1[i] > nums2[j]) {
                nums1[w] = nums1[i];
                i--;
            } else {
                nums1[w] = nums2[j];
                j--;
            }
            w--;
        }
    }
};""",
)

add(
    id=344, slug="reverse-string", title="Reverse String", difficulty="Easy", world="two-pointers",
    tags=["string", "two-pointers"],
    story=dict(
        title="The Sign Painter's Mistake",
        text="A sign was painted backwards. Two painters start at either end and swap letter tiles, stepping inward "
             "until they meet.",
        goal="Reverse the letters in place.",
    ),
    spec=dict(method="reverseString", ret="void", params=[["vector<char>&", "s"]], output="param:0"),
    tests=[dict(args=[["h", "e", "l", "l", "o"]], expected=["o", "l", "l", "e", "h"]),
           dict(args=[["H", "a", "n", "n", "a", "h"]], expected=["h", "a", "n", "n", "a", "H"])],
    scene=dict(theme="market", layers=[dict(kind="array", var="s", label="sign", style="letters", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    void reverseString(vector<char>& s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            swap(s[l], s[r]);
            l++;
            r--;
        }
    }
};""",
)

add(
    id=977, slug="squares-of-a-sorted-array", title="Squares of a Sorted Array", difficulty="Easy", world="two-pointers",
    tags=["array", "two-pointers", "sorting"],
    story=dict(
        title="The Tallest Tower First",
        text="Signed numbers are sorted, but squaring flips the negatives. The biggest square is always at one end, so "
             "two builders compare the ends and stack the bigger square at the back of the new row.",
        goal="Return the squares in sorted order.",
    ),
    spec=dict(method="sortedSquares", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[-4, -1, 0, 3, 10]], expected=[0, 1, 9, 16, 100]), dict(args=[[-7, -3, 2, 3, 11]], expected=[4, 9, 9, 49, 121])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="numbers", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="array", var="res", label="squares", style="tiles", pointers=["w"]),
    ]),
    reference="""class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n);
        int l = 0, r = n - 1;
        for (int w = n - 1; w >= 0; w--) {
            if (abs(nums[l]) > abs(nums[r])) {
                res[w] = nums[l] * nums[l];
                l++;
            } else {
                res[w] = nums[r] * nums[r];
                r--;
            }
        }
        return res;
    }
};""",
)

add(
    id=74, slug="search-a-2d-matrix", title="Search a 2D Matrix", difficulty="Medium", world="binary-search",
    tags=["array", "binary-search", "matrix"],
    story=dict(
        title="The Sorted Vault",
        text="The vault's drawers are numbered row by row in increasing order, so the whole vault is one long sorted "
             "corridor. The guard binary-searches it, turning each middle position into a row and column.",
        goal="Return true if the target is in the vault.",
    ),
    spec=dict(method="searchMatrix", ret="bool", params=[["vector<vector<int>>&", "matrix"], ["int", "target"]]),
    tests=[dict(args=[[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3], expected=True),
           dict(args=[[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13], expected=False),
           dict(args=[[[1]], 1], expected=True)],
    scene=dict(theme="cave", layers=[
        dict(kind="grid", var="matrix", palette="dp", label="vault", pointers=[["r", "c"]]),
        dict(kind="values", vars=["lo", "mid", "hi", "target"]),
    ]),
    reference="""class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int rows = matrix.size(), cols = matrix[0].size();
        int lo = 0, hi = rows * cols - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            int r = mid / cols, c = mid % cols;
            if (matrix[r][c] == target) return true;
            if (matrix[r][c] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
};""",
)

add(
    id=875, slug="koko-eating-bananas", title="Koko Eating Bananas", difficulty="Medium", world="binary-search",
    tags=["array", "binary-search"],
    story=dict(
        title="The Banana Guard's Speed",
        text="A monkey must finish every banana pile before the guards return. Too slow fails, too fast is wasteful. "
             "The monkey binary-searches its eating speed, timing each guess pile by pile.",
        goal="Return the slowest speed that finishes within h hours.",
    ),
    spec=dict(method="minEatingSpeed", ret="int", params=[["vector<int>&", "piles"], ["int", "h"]]),
    tests=[dict(args=[[3, 6, 7, 11], 8], expected=4), dict(args=[[30, 11, 23, 4, 20], 5], expected=30),
           dict(args=[[30, 11, 23, 4, 20], 6], expected=23)],
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="piles", label="banana piles", pointers=["i"]),
        dict(kind="values", vars=["lo", "mid", "hi", "hours", "h"]),
    ]),
    reference="""class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int lo = 1, hi = *max_element(piles.begin(), piles.end());
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            long long hours = 0;
            for (int i = 0; i < (int)piles.size(); i++) hours += (piles[i] + mid - 1) / mid;
            if (hours <= h) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};""",
)

add(
    id=153, slug="find-minimum-in-rotated-sorted-array", title="Find Minimum in Rotated Sorted Array", difficulty="Medium",
    world="binary-search", tags=["array", "binary-search"],
    story=dict(
        title="Where the Corridor Was Cut",
        text="The sorted corridor was cut and the pieces swapped. The guard compares the middle chest with the last one: "
             "if the middle is bigger, the cut (and the smallest chest) is to the right.",
        goal="Return the smallest value.",
    ),
    spec=dict(method="findMin", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[3, 4, 5, 1, 2]], expected=1), dict(args=[[4, 5, 6, 7, 0, 1, 2]], expected=0), dict(args=[[11, 13, 15, 17]], expected=11)],
    visualTest=1,
    scene=dict(theme="cave", layers=[dict(kind="array", var="nums", label="chests", pointers=["lo", "mid", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    int findMin(vector<int>& nums) {
        int lo = 0, hi = nums.size() - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1;
            else hi = mid;
        }
        return nums[lo];
    }
};""",
)

add(
    id=424, slug="longest-repeating-character-replacement", title="Longest Repeating Character Replacement",
    difficulty="Medium", world="sliding-window", tags=["string", "sliding-window", "hash-table"],
    story=dict(
        title="Repainting the Buoys",
        text="The lighthouse beam may hold any buoys as long as at most k of them need repainting to match the most "
             "common colour inside the beam. When more than k would need paint, the beam's left edge moves up.",
        goal="Return the longest stretch that can be made one colour with at most k repaints.",
    ),
    spec=dict(method="characterReplacement", ret="int", params=[["string", "s"], ["int", "k"]]),
    tests=[dict(args=["ABAB", 2], expected=4), dict(args=["AABABBA", 1], expected=4), dict(args=["AAAA", 0], expected=4)],
    visualTest=1,
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="buoys", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="map", var="cnt", label="colours in beam"),
        dict(kind="values", vars=["k", "most", "best"]),
    ]),
    reference="""class Solution {
public:
    int characterReplacement(string s, int k) {
        map<char, int> cnt;
        int l = 0, most = 0, best = 0;
        for (int r = 0; r < (int)s.size(); r++) {
            most = max(most, ++cnt[s[r]]);
            while (r - l + 1 - most > k) {
                cnt[s[l]]--;
                l++;
            }
            best = max(best, r - l + 1);
        }
        return best;
    }
};""",
)

add(
    id=496, slug="next-greater-element-i", title="Next Greater Element I", difficulty="Easy", world="stack",
    tags=["array", "hash-table", "stack", "monotonic-stack"],
    story=dict(
        title="Who Can See Over You?",
        text="People stand in a line by height. Walking along, anyone shorter than the newcomer finally sees someone "
             "taller and leaves the waiting tower; the lockers remember who they saw.",
        goal="For each value in nums1, return the first taller value to its right in nums2 (or -1).",
    ),
    spec=dict(method="nextGreaterElement", ret="vector<int>", params=[["vector<int>&", "nums1"], ["vector<int>&", "nums2"]]),
    tests=[dict(args=[[4, 1, 2], [1, 3, 4, 2]], expected=[-1, 3, -1]), dict(args=[[2, 4], [1, 2, 3, 4]], expected=[3, -1])],
    scene=dict(theme="castle", layers=[
        dict(kind="bars", var="nums2", label="line of people", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="st", label="still waiting"), dict(kind="map", var="nxt", label="saw taller", weight=2)]),
    ]),
    reference="""class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        map<int, int> nxt;
        stack<int> st;
        for (int i = 0; i < (int)nums2.size(); i++) {
            while (!st.empty() && st.top() < nums2[i]) {
                nxt[st.top()] = nums2[i];
                st.pop();
            }
            st.push(nums2[i]);
        }
        vector<int> res;
        for (int x : nums1) res.push_back(nxt.count(x) ? nxt[x] : -1);
        return res;
    }
};""",
)

add(
    id=84, slug="largest-rectangle-in-histogram", title="Largest Rectangle in Histogram", difficulty="Hard", world="stack",
    tags=["array", "stack", "monotonic-stack"],
    story=dict(
        title="The Billboard Under the Skyline",
        text="A billboard must fit under a row of towers. The tower stack keeps towers in rising height; when a shorter "
             "tower arrives, every taller one is popped and measures the widest billboard it could support.",
        goal="Return the area of the largest rectangle under the towers.",
    ),
    spec=dict(method="largestRectangleArea", ret="int", params=[["vector<int>&", "heights"]]),
    tests=[dict(args=[[2, 1, 5, 6, 2, 3]], expected=10), dict(args=[[2, 4]], expected=4), dict(args=[[6, 2, 5, 4, 5, 1, 6]], expected=12)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="heights", label="towers", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="st", label="rising towers (index)"), dict(kind="values", vars=["h", "w", "best"], weight=2)]),
    ]),
    reference="""class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> st;
        int best = 0, n = heights.size();
        for (int i = 0; i <= n; i++) {
            int cur = i == n ? 0 : heights[i];
            while (!st.empty() && heights[st.top()] >= cur) {
                int h = heights[st.top()];
                st.pop();
                int w = st.empty() ? i : i - st.top() - 1;
                best = max(best, h * w);
            }
            st.push(i);
        }
        return best;
    }
};""",
)

add(
    id=234, slug="palindrome-linked-list", title="Palindrome Linked List", difficulty="Easy", world="linked-list",
    tags=["linked-list", "two-pointers", "stack"],
    story=dict(
        title="The Mirror Train",
        text="Is the train the same from both ends? A hare and a tortoise find the middle, the back half is turned "
             "around, then two inspectors walk in from both ends comparing cars.",
        goal="Return true if the values read the same forwards and backwards.",
    ),
    spec=dict(method="isPalindrome", ret="bool", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 2, 2, 1]], expected=True), dict(args=[[1, 2]], expected=False), dict(args=[[1, 2, 3, 2, 1]], expected=True)],
    visualTest=2,
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "slow", "fast", "prev", "a", "b"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    bool isPalindrome(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode* prev = nullptr;
        while (slow) {
            ListNode* nxt = slow->next;
            slow->next = prev;
            prev = slow;
            slow = nxt;
        }
        ListNode* a = head;
        ListNode* b = prev;
        while (b) {
            if (a->val != b->val) return false;
            a = a->next;
            b = b->next;
        }
        return true;
    }
};""",
)

add(
    id=2, slug="add-two-numbers", title="Add Two Numbers", difficulty="Medium", world="linked-list",
    tags=["linked-list", "math", "recursion"],
    story=dict(
        title="The Counting Trains",
        text="Two trains carry the digits of two numbers, ones digit first. A clerk walks both trains together, adds the "
             "digits and the carry, and couples a new car with the result digit onto a third train.",
        goal="Return the train holding the sum.",
    ),
    spec=dict(method="addTwoNumbers", ret="ListNode*", params=[["ListNode*", "l1"], ["ListNode*", "l2"]]),
    tests=[dict(args=[[2, 4, 3], [5, 6, 4]], expected=[7, 0, 8]), dict(args=[[0], [0]], expected=[0]),
           dict(args=[[9, 9, 9, 9], [9, 9]], expected=[8, 9, 0, 0, 1])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["l1", "l2", "tail"], heads=["l1", "l2"], label="trains"),
        dict(kind="values", vars=["sum", "carry"]),
    ]),
    reference="""class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* dummy = new ListNode(0);
        ListNode* tail = dummy;
        int carry = 0;
        while (l1 || l2 || carry) {
            int sum = carry;
            if (l1) { sum += l1->val; l1 = l1->next; }
            if (l2) { sum += l2->val; l2 = l2->next; }
            carry = sum / 10;
            tail->next = new ListNode(sum % 10);
            tail = tail->next;
        }
        return dummy->next;
    }
};""",
)

add(
    id=100, slug="same-tree", title="Same Tree", difficulty="Easy", world="trees", tags=["tree", "dfs"],
    story=dict(
        title="Twin Orchards",
        text="Two orchards were planted from the same plan, or were they? Two squirrels climb both trees in lockstep "
             "and compare each fruit and branch.",
        goal="Return true if both trees have the same shape and values.",
    ),
    spec=dict(method="isSameTree", ret="bool", params=[["TreeNode*", "p"], ["TreeNode*", "q"]]),
    tests=[dict(args=[[1, 2, 3], [1, 2, 3]], expected=True), dict(args=[[1, 2], [1, None, 2]], expected=False),
           dict(args=[[1, 2, 1], [1, 1, 2]], expected=False)],
    scene=dict(theme="forest", layers=[dict(kind="row", children=[
        dict(kind="tree", var="p", pointers=["p"], label="orchard p"),
        dict(kind="tree", var="q", pointers=["q"], label="orchard q"),
    ])]),
    reference="""class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (!p && !q) return true;
        if (!p || !q || p->val != q->val) return false;
        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};""",
)

add(
    id=543, slug="diameter-of-binary-tree", title="Diameter of Binary Tree", difficulty="Easy", world="trees",
    tags=["tree", "dfs"],
    story=dict(
        title="The Longest Vine",
        text="A vine can run between any two fruits along the branches. Every fruit asks its two branches how deep they "
             "go; the two depths together are the longest vine passing through it.",
        goal="Return the number of branches on the longest path between any two fruits.",
    ),
    spec=dict(method="diameterOfBinaryTree", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5]], expected=3), dict(args=[[1, 2]], expected=1)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["l", "r", "best"]),
    ]),
    reference="""class Solution {
public:
    int best = 0;
    int depth(TreeNode* node) {
        if (!node) return 0;
        int l = depth(node->left);
        int r = depth(node->right);
        best = max(best, l + r);
        return 1 + max(l, r);
    }
    int diameterOfBinaryTree(TreeNode* root) {
        depth(root);
        return best;
    }
};""",
)

add(
    id=112, slug="path-sum", title="Path Sum", difficulty="Easy", world="trees", tags=["tree", "dfs"],
    story=dict(
        title="The Exact-Weight Basket",
        text="A picker climbs from the top to a leaf, adding each fruit's weight to a basket. They want a path whose "
             "basket weighs exactly the target; each branch is asked for what is still missing.",
        goal="Return true if some root-to-leaf path adds up to targetSum.",
    ),
    spec=dict(method="hasPathSum", ret="bool", params=[["TreeNode*", "root"], ["int", "targetSum"]]),
    tests=[dict(args=[[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22], expected=True),
           dict(args=[[1, 2, 3], 5], expected=False), dict(args=[[], 0], expected=False)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["root"], label="orchard"),
        dict(kind="values", vars=["targetSum"]),
    ]),
    reference="""class Solution {
public:
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (!root) return false;
        if (!root->left && !root->right) return root->val == targetSum;
        return hasPathSum(root->left, targetSum - root->val) || hasPathSum(root->right, targetSum - root->val);
    }
};""",
)

add(
    id=695, slug="max-area-of-island", title="Max Area of Island", difficulty="Medium", world="graphs",
    tags=["array", "dfs", "matrix"],
    story=dict(
        title="Measuring the Islands",
        text="A surveyor lands on every unexplored island and paces out each land tile, marking it so it isn't counted "
             "twice. The biggest tally wins.",
        goal="Return the area of the largest island (0 if none).",
    ),
    spec=dict(method="maxAreaOfIsland", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]]], expected=4),
           dict(args=[[[0, 1, 0], [1, 1, 1], [0, 1, 0]]], expected=5), dict(args=[[[0, 0, 0]]], expected=0)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="grid", palette="islands", label="sea chart", pointers=[["r", "c"]]),
        dict(kind="values", vars=["area", "best"]),
    ]),
    reference="""class Solution {
public:
    int walk(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size() || grid[r][c] != 1) return 0;
        grid[r][c] = 2;
        return 1 + walk(grid, r + 1, c) + walk(grid, r - 1, c) + walk(grid, r, c + 1) + walk(grid, r, c - 1);
    }
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int best = 0;
        for (int r = 0; r < (int)grid.size(); r++)
            for (int c = 0; c < (int)grid[0].size(); c++)
                if (grid[r][c] == 1) {
                    int area = walk(grid, r, c);
                    best = max(best, area);
                }
        return best;
    }
};""",
)

add(
    id=79, slug="word-search", title="Word Search", difficulty="Medium", world="backtracking",
    tags=["array", "string", "backtracking", "matrix"],
    story=dict(
        title="The Letter Tile Maze",
        text="An explorer must spell a word by stepping between neighbouring tiles. Each tile used is chalked so it isn't "
             "reused; at a dead end the chalk is wiped off and the explorer backs out through the door.",
        goal="Return true if the word can be traced on the board.",
    ),
    spec=dict(method="exist", ret="bool", params=[["vector<vector<char>>&", "board"], ["string", "word"]]),
    tests=[
        dict(args=[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"], expected=True),
        dict(args=[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"], expected=True),
        dict(args=[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"], expected=False),
    ],
    scene=dict(theme="cave", layers=[
        dict(kind="grid", var="board", palette="board", label="tile maze", pointers=[["r", "c"]]),
        dict(kind="string", var="word", label="word", pointers=["k"]),
    ]),
    reference="""class Solution {
public:
    bool go(vector<vector<char>>& board, string& word, int k, int r, int c) {
        if (k == (int)word.size()) return true;
        if (r < 0 || c < 0 || r >= (int)board.size() || c >= (int)board[0].size() || board[r][c] != word[k]) return false;
        char saved = board[r][c];
        board[r][c] = '#';
        bool found = go(board, word, k + 1, r + 1, c) || go(board, word, k + 1, r - 1, c) ||
                     go(board, word, k + 1, r, c + 1) || go(board, word, k + 1, r, c - 1);
        board[r][c] = saved;
        return found;
    }
    bool exist(vector<vector<char>>& board, string word) {
        for (int r = 0; r < (int)board.size(); r++)
            for (int c = 0; c < (int)board[0].size(); c++)
                if (go(board, word, 0, r, c)) return true;
        return false;
    }
};""",
)

add(
    id=39, slug="combination-sum", title="Combination Sum", difficulty="Medium", world="backtracking",
    tags=["array", "backtracking"],
    story=dict(
        title="Exact Change, Any Coins",
        text="A shopkeeper may reuse any coin as often as they like. At each door they try adding a coin no smaller than "
             "the last one; if the bag goes over the price, they put the coin back and try the next.",
        goal="Return every combination of coins that adds up to target (any order).",
    ),
    spec=dict(method="combinationSum", ret="vector<vector<int>>", params=[["vector<int>&", "candidates"], ["int", "target"]]),
    compare="unordered-deep",
    tests=[dict(args=[[2, 3, 6, 7], 7], expected=[[2, 2, 3], [7]]), dict(args=[[2, 3, 5], 8], expected=[[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
           dict(args=[[2], 1], expected=[])],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="candidates", label="coins", pointers=["i"]),
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
            if (candidates[i] > remain) continue;
            path.push_back(candidates[i]);
            go(candidates, i, remain - candidates[i]);
            path.pop_back();
        }
    }
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        go(candidates, 0, target);
        return res;
    }
};""",
)

add(
    id=300, slug="longest-increasing-subsequence", title="Longest Increasing Subsequence", difficulty="Medium", world="dp",
    tags=["array", "binary-search", "dynamic-programming"],
    story=dict(
        title="The Growing Beanstalks",
        text="Each plot remembers the longest run of ever-taller beanstalks that can end there: look back at every "
             "shorter beanstalk and extend its run by one.",
        goal="Return the length of the longest strictly increasing subsequence.",
    ),
    spec=dict(method="lengthOfLIS", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[10, 9, 2, 5, 3, 7, 101, 18]], expected=4), dict(args=[[0, 1, 0, 3, 2, 3]], expected=4),
           dict(args=[[7, 7, 7, 7]], expected=1)],
    scene=dict(theme="farm", layers=[
        dict(kind="bars", var="nums", label="beanstalks", pointers=["j", "i"]),
        dict(kind="array", var="dp", label="longest run ending here", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size(), best = 1;
        vector<int> dp(n, 1);
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) dp[i] = max(dp[i], dp[j] + 1);
            }
            best = max(best, dp[i]);
        }
        return best;
    }
};""",
)

add(
    id=416, slug="partition-equal-subset-sum", title="Partition Equal Subset Sum", difficulty="Medium", world="dp",
    tags=["array", "dynamic-programming"],
    story=dict(
        title="Two Fair Harvest Carts",
        text="The harvest must be split into two carts of equal weight. A ledger marks every weight one cart could reach; "
             "each new sack is tried on top of every weight already reachable, scanning from heavy to light.",
        goal="Return true if the sacks can be split into two equal halves.",
    ),
    spec=dict(method="canPartition", ret="bool", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 5, 11, 5]], expected=True), dict(args=[[1, 2, 3, 5]], expected=False), dict(args=[[2, 2, 3, 5]], expected=False)],
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="nums", label="sacks", pointers=["k"]),
        dict(kind="array", var="can", label="reachable cart weights", style="tiles", pointers=["s"]),
        dict(kind="values", vars=["half"]),
    ]),
    reference="""class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int total = 0;
        for (int x : nums) total += x;
        if (total % 2) return false;
        int half = total / 2;
        vector<bool> can(half + 1, false);
        can[0] = true;
        for (int k = 0; k < (int)nums.size(); k++) {
            for (int s = half; s >= nums[k]; s--) {
                if (can[s - nums[k]]) can[s] = true;
            }
        }
        return can[half];
    }
};""",
)

add(
    id=435, slug="non-overlapping-intervals", title="Non-overlapping Intervals", difficulty="Medium", world="intervals",
    tags=["array", "greedy", "sorting", "dynamic-programming"],
    story=dict(
        title="Clearing the Double Bookings",
        text="The hall is double-booked. Sorted by end time, the manager keeps every booking that starts after the last "
             "kept one ends and cancels the rest, so the hall frees up as early as possible.",
        goal="Return the fewest bookings to cancel so none overlap.",
    ),
    spec=dict(method="eraseOverlapIntervals", ret="int", params=[["vector<vector<int>>&", "intervals"]]),
    tests=[dict(args=[[[1, 2], [2, 3], [3, 4], [1, 3]]], expected=1), dict(args=[[[1, 2], [1, 2], [1, 2]]], expected=2),
           dict(args=[[[1, 2], [2, 3]]], expected=0)],
    scene=dict(theme="lab", layers=[
        dict(kind="intervals", vars=["intervals"], pointers=["i"], label="bookings"),
        dict(kind="values", vars=["end", "removed"]),
    ]),
    reference="""class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
        int end = INT_MIN, removed = 0;
        for (int i = 0; i < (int)intervals.size(); i++) {
            if (intervals[i][0] >= end) end = intervals[i][1];
            else removed++;
        }
        return removed;
    }
};""",
)

add(
    id=122, slug="best-time-to-buy-and-sell-stock-ii", title="Best Time to Buy and Sell Stock II", difficulty="Medium",
    world="greedy", tags=["array", "greedy", "dynamic-programming"],
    story=dict(
        title="Catching Every Uphill",
        text="A trader may buy and sell as often as they like. Walking the skyline, they pocket every rise from one day "
             "to the next and ignore every drop.",
        goal="Return the maximum total profit.",
    ),
    spec=dict(method="maxProfit", ret="int", params=[["vector<int>&", "prices"]]),
    tests=[dict(args=[[7, 1, 5, 3, 6, 4]], expected=7), dict(args=[[1, 2, 3, 4, 5]], expected=4), dict(args=[[7, 6, 4, 3, 1]], expected=0)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="prices", label="price towers", pointers=["i"]),
        dict(kind="values", vars=["profit"]),
    ]),
    reference="""class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int profit = 0;
        for (int i = 1; i < (int)prices.size(); i++) {
            if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];
        }
        return profit;
    }
};""",
)

add(
    id=191, slug="number-of-1-bits", title="Number of 1 Bits", difficulty="Easy", world="bits",
    tags=["divide-and-conquer", "bit-manipulation"],
    story=dict(
        title="Switching Off the Lamps",
        text="A row of lamps shows a number in binary. Each trick n & (n - 1) switches off the lowest lit lamp; count how "
             "many tricks it takes to go dark.",
        goal="Return how many 1 bits n has.",
    ),
    spec=dict(method="hammingWeight", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[11], expected=3), dict(args=[128], expected=1), dict(args=[2147483645], expected=30)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n", "count"])]),
    reference="""class Solution {
public:
    int hammingWeight(int n) {
        int count = 0;
        while (n) {
            n &= n - 1;
            count++;
        }
        return count;
    }
};""",
)
