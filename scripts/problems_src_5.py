"""Fifth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=189, slug="rotate-array", title="Rotate Array", difficulty="Medium", world="arrays", tags=["array", "math", "two-pointers"],
    story=dict(
        title="The Conveyor Belt Shift",
        text="Crates on a looped conveyor must shift k places to the right. The trick: flip the whole row, then flip "
             "the first k crates and the rest separately; two workers swap from both ends each time.",
        goal="Rotate the array right by k steps in place.",
    ),
    spec=dict(method="rotate", ret="void", params=[["vector<int>&", "nums"], ["int", "k"]], output="param:0"),
    tests=[dict(args=[[1, 2, 3, 4, 5, 6, 7], 3], expected=[5, 6, 7, 1, 2, 3, 4]), dict(args=[[-1, -100, 3, 99], 2], expected=[3, 99, -1, -100])],
    scene=dict(theme="dock", layers=[dict(kind="array", var="nums", label="conveyor", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    void flip(vector<int>& nums, int l, int r) {
        while (l < r) {
            swap(nums[l], nums[r]);
            l++;
            r--;
        }
    }
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k %= n;
        flip(nums, 0, n - 1);
        flip(nums, 0, k - 1);
        flip(nums, k, n - 1);
    }
};""",
)

add(
    id=48, slug="rotate-image", title="Rotate Image", difficulty="Medium", world="arrays", tags=["array", "math", "matrix"],
    story=dict(
        title="Turning the Mosaic",
        text="A square mosaic must be turned a quarter clockwise without lifting it off the wall. First every tile swaps "
             "with its mirror across the diagonal, then each row is flipped left to right.",
        goal="Rotate the matrix 90 degrees clockwise in place.",
    ),
    spec=dict(method="rotate", ret="void", params=[["vector<vector<int>>&", "matrix"]], output="param:0"),
    tests=[dict(args=[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], expected=[[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
           dict(args=[[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]], expected=[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]])],
    scene=dict(theme="lab", layers=[dict(kind="grid", var="matrix", palette="dp", label="mosaic", pointers=[["i", "j"]])]),
    reference="""class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) swap(matrix[i][j], matrix[j][i]);
        for (int i = 0; i < n; i++) reverse(matrix[i].begin(), matrix[i].end());
    }
};""",
)

add(
    id=54, slug="spiral-matrix", title="Spiral Matrix", difficulty="Medium", world="arrays", tags=["array", "matrix", "simulation"],
    story=dict(
        title="The Snail's Garden Walk",
        text="A snail walks the garden beds in a spiral: along the top, down the right, back along the bottom, up the "
             "left, then the walls close in by one bed and it goes round again.",
        goal="Return every value in spiral order.",
    ),
    spec=dict(method="spiralOrder", ret="vector<int>", params=[["vector<vector<int>>&", "matrix"]]),
    tests=[dict(args=[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], expected=[1, 2, 3, 6, 9, 8, 7, 4, 5]),
           dict(args=[[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], expected=[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="grid", var="matrix", palette="dp", label="garden beds", pointers=[["r", "c"]]),
        dict(kind="values", vars=["top", "bottom", "left", "right"]),
        dict(kind="array", var="res", label="snail's path", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> res;
        int top = 0, bottom = matrix.size() - 1, left = 0, right = matrix[0].size() - 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) res.push_back(matrix[top][c]);
            top++;
            for (int r = top; r <= bottom; r++) res.push_back(matrix[r][right]);
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) res.push_back(matrix[bottom][c]);
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) res.push_back(matrix[r][left]);
                left++;
            }
        }
        return res;
    }
};""",
)

add(
    id=73, slug="set-matrix-zeroes", title="Set Matrix Zeroes", difficulty="Medium", world="arrays", tags=["array", "hash-table", "matrix"],
    story=dict(
        title="The Blight Spreads",
        text="Any blighted plot (0) ruins its whole row and column. An inspector first notes which rows and columns are "
             "blighted, then a second pass clears every plot in them.",
        goal="Set every row and column containing a 0 to all zeroes, in place.",
    ),
    spec=dict(method="setZeroes", ret="void", params=[["vector<vector<int>>&", "matrix"]], output="param:0"),
    tests=[dict(args=[[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], expected=[[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
           dict(args=[[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]], expected=[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="grid", var="matrix", palette="dp", label="field", pointers=[["i", "j"]]),
        dict(kind="row", children=[
            dict(kind="array", var="row", label="blighted rows", style="tiles"),
            dict(kind="array", var="col", label="blighted cols", style="tiles"),
        ]),
    ]),
    reference="""class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<bool> row(m, false), col(n, false);
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (matrix[i][j] == 0) {
                    row[i] = true;
                    col[j] = true;
                }
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (row[i] || col[j]) matrix[i][j] = 0;
    }
};""",
)

add(
    id=680, slug="valid-palindrome-ii", title="Valid Palindrome II", difficulty="Easy", world="two-pointers",
    tags=["two-pointers", "string", "greedy"],
    story=dict(
        title="One Loose Tile",
        text="Two inspectors walk the bridge from both ends. They are allowed to pull up one bad tile: at the first "
             "mismatch they try skipping the left tile, and if that fails, the right one.",
        goal="Return true if the string can be a palindrome after deleting at most one character.",
    ),
    spec=dict(method="validPalindrome", ret="bool", params=[["string", "s"]]),
    tests=[dict(args=["aba"], expected=True), dict(args=["abca"], expected=True), dict(args=["abc"], expected=False), dict(args=["deeee"], expected=True)],
    visualTest=1,
    scene=dict(theme="dock", layers=[dict(kind="string", var="s", label="bridge", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    bool check(string& s, int l, int r) {
        while (l < r) {
            if (s[l] != s[r]) return false;
            l++;
            r--;
        }
        return true;
    }
    bool validPalindrome(string s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            if (s[l] != s[r]) return check(s, l + 1, r) || check(s, l, r - 1);
            l++;
            r--;
        }
        return true;
    }
};""",
)

add(
    id=392, slug="is-subsequence", title="Is Subsequence", difficulty="Easy", world="two-pointers",
    tags=["two-pointers", "string", "dynamic-programming"],
    story=dict(
        title="Spotting the Secret Word",
        text="A secret word is hidden in a long letter, in order but with other letters between. One finger points at "
             "the next secret letter needed, the other reads along the letter.",
        goal="Return true if s appears in t in order (not necessarily together).",
    ),
    spec=dict(method="isSubsequence", ret="bool", params=[["string", "s"], ["string", "t"]]),
    tests=[dict(args=["abc", "ahbgdc"], expected=True), dict(args=["axc", "ahbgdc"], expected=False), dict(args=["", "abc"], expected=True)],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="secret", pointers=["i"]),
        dict(kind="string", var="t", label="letter", pointers=["j"]),
    ]),
    reference="""class Solution {
public:
    bool isSubsequence(string s, string t) {
        int i = 0;
        for (int j = 0; j < (int)t.size() && i < (int)s.size(); j++) {
            if (s[i] == t[j]) i++;
        }
        return i == (int)s.size();
    }
};""",
)

add(
    id=1768, slug="merge-strings-alternately", title="Merge Strings Alternately", difficulty="Easy", world="two-pointers",
    tags=["two-pointers", "string"],
    story=dict(
        title="Zipping Two Banners",
        text="Two banners are stitched into one, taking a letter from each in turn. When one banner runs out, the rest "
             "of the other is sewn on the end.",
        goal="Return the merged string.",
    ),
    spec=dict(method="mergeAlternately", ret="string", params=[["string", "word1"], ["string", "word2"]]),
    tests=[dict(args=["abc", "pqr"], expected="apbqcr"), dict(args=["ab", "pqrs"], expected="apbqrs"), dict(args=["abcd", "pq"], expected="apbqcd")],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="string", var="word1", label="banner 1", pointers=["i"]),
        dict(kind="string", var="word2", label="banner 2", pointers=["i"]),
        dict(kind="string", var="res", label="stitched"),
    ]),
    reference="""class Solution {
public:
    string mergeAlternately(string word1, string word2) {
        string res;
        int n = max(word1.size(), word2.size());
        for (int i = 0; i < n; i++) {
            if (i < (int)word1.size()) res.push_back(word1[i]);
            if (i < (int)word2.size()) res.push_back(word2[i]);
        }
        return res;
    }
};""",
)

add(
    id=643, slug="maximum-average-subarray-i", title="Maximum Average Subarray I", difficulty="Easy", world="sliding-window",
    tags=["array", "sliding-window"],
    story=dict(
        title="The Best Week of Sales",
        text="A shop's daily sales are on the wall. A frame exactly k days wide slides along; each step adds the new day "
             "and drops the oldest, remembering the best total.",
        goal="Return the largest average over any k consecutive days.",
    ),
    spec=dict(method="findMaxAverage", ret="double", params=[["vector<int>&", "nums"], ["int", "k"]]),
    compare="float",
    tests=[dict(args=[[1, 12, -5, -6, 50, 3], 4], expected=12.75), dict(args=[[5], 1], expected=5.0)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="daily sales", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["k", "sum", "best"]),
    ]),
    reference="""class Solution {
public:
    double findMaxAverage(vector<int>& nums, int k) {
        int sum = 0;
        for (int r = 0; r < k; r++) sum += nums[r];
        int best = sum;
        for (int r = k; r < (int)nums.size(); r++) {
            int l = r - k + 1;
            sum += nums[r] - nums[l - 1];
            best = max(best, sum);
        }
        return (double)best / k;
    }
};""",
)

add(
    id=1456, slug="maximum-number-of-vowels-in-a-substring-of-given-length", title="Maximum Number of Vowels in a Substring of Given Length",
    difficulty="Medium", world="sliding-window", tags=["string", "sliding-window"],
    story=dict(
        title="The Singing Window",
        text="A window k letters wide slides along a song's lyrics, counting the vowels inside. Each step the new letter "
             "comes in and the oldest goes out.",
        goal="Return the most vowels any window of length k holds.",
    ),
    spec=dict(method="maxVowels", ret="int", params=[["string", "s"], ["int", "k"]]),
    tests=[dict(args=["abciiidef", 3], expected=3), dict(args=["aeiou", 2], expected=2), dict(args=["leetcode", 3], expected=2)],
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="lyrics", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["k", "cnt", "best"]),
    ]),
    reference="""class Solution {
public:
    bool vowel(char c) {
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }
    int maxVowels(string s, int k) {
        int cnt = 0, best = 0;
        for (int r = 0; r < (int)s.size(); r++) {
            if (vowel(s[r])) cnt++;
            int l = r - k + 1;
            if (l > 0 && vowel(s[l - 1])) cnt--;
            if (l >= 0) best = max(best, cnt);
        }
        return best;
    }
};""",
)

add(
    id=503, slug="next-greater-element-ii", title="Next Greater Element II", difficulty="Medium", world="stack",
    tags=["array", "stack", "monotonic-stack"],
    story=dict(
        title="The Round Table",
        text="Guests sit around a round table. Each wants to know the next taller guest going clockwise. Walk the table "
             "twice; guests still waiting sit on a tower until someone taller comes by.",
        goal="Return the next greater value for each element in the circular array (or -1).",
    ),
    spec=dict(method="nextGreaterElements", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 1]], expected=[2, -1, 2]), dict(args=[[1, 2, 3, 4, 3]], expected=[2, 3, 4, -1, 4])],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="bars", var="nums", label="guests", pointers=["j"]),
        dict(kind="row", children=[
            dict(kind="stack", var="st", label="waiting (index)"),
            dict(kind="array", var="res", label="answers", style="tiles", weight=2),
        ]),
        dict(kind="values", vars=["i"]),
    ]),
    reference="""class Solution {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, -1);
        stack<int> st;
        for (int i = 0; i < 2 * n; i++) {
            int j = i % n;
            while (!st.empty() && nums[st.top()] < nums[j]) {
                res[st.top()] = nums[j];
                st.pop();
            }
            if (i < n) st.push(j);
        }
        return res;
    }
};""",
)

add(
    id=69, slug="sqrtx", title="Sqrt(x)", difficulty="Easy", world="binary-search", tags=["math", "binary-search"],
    story=dict(
        title="The Square Garden",
        text="A gardener wants the largest square plot that fits x tiles. They guess a side length in the middle of the "
             "possible range and halve the range depending on whether the square fits.",
        goal="Return the integer square root of x (rounded down).",
    ),
    spec=dict(method="mySqrt", ret="int", params=[["int", "x"]]),
    tests=[dict(args=[4], expected=2), dict(args=[8], expected=2), dict(args=[2147395599], expected=46339)],
    visualTest=1,
    scene=dict(theme="farm", layers=[dict(kind="values", vars=["x", "lo", "mid", "hi", "ans"])]),
    reference="""class Solution {
public:
    int mySqrt(int x) {
        long long lo = 0, hi = x, ans = 0;
        while (lo <= hi) {
            long long mid = (lo + hi) / 2;
            if (mid * mid <= x) {
                ans = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return ans;
    }
};""",
)

add(
    id=1011, slug="capacity-to-ship-packages-within-d-days", title="Capacity To Ship Packages Within D Days", difficulty="Medium",
    world="binary-search", tags=["array", "binary-search"],
    story=dict(
        title="The Smallest Ferry",
        text="Parcels must cross the river in order within a number of days. The harbour master guesses a ferry size, "
             "loads parcels day by day to see how many days it takes, and halves the range of sizes.",
        goal="Return the smallest ferry capacity that ships everything in time.",
    ),
    spec=dict(method="shipWithinDays", ret="int", params=[["vector<int>&", "weights"], ["int", "days"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5], expected=15), dict(args=[[3, 2, 2, 4, 1, 4], 3], expected=6),
           dict(args=[[1, 2, 3, 1, 1], 4], expected=3)],
    visualTest=1,
    scene=dict(theme="dock", layers=[
        dict(kind="bars", var="weights", label="parcels", pointers=["i"]),
        dict(kind="values", vars=["lo", "mid", "hi", "need", "load", "days"]),
    ]),
    reference="""class Solution {
public:
    int shipWithinDays(vector<int>& weights, int days) {
        int lo = *max_element(weights.begin(), weights.end());
        int hi = accumulate(weights.begin(), weights.end(), 0);
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            int need = 1, load = 0;
            for (int i = 0; i < (int)weights.size(); i++) {
                if (load + weights[i] > mid) {
                    need++;
                    load = 0;
                }
                load += weights[i];
            }
            if (need <= days) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};""",
)

add(
    id=61, slug="rotate-list", title="Rotate List", difficulty="Medium", world="linked-list", tags=["linked-list", "two-pointers"],
    story=dict(
        title="Moving the Last Cars to the Front",
        text="The last k cars must move to the front. A worker counts the train, couples the caboose to the engine to "
             "make a loop, then walks to the new end and uncouples there.",
        goal="Rotate the list right by k places.",
    ),
    spec=dict(method="rotateRight", ret="ListNode*", params=[["ListNode*", "head"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], 2], expected=[4, 5, 1, 2, 3]), dict(args=[[0, 1, 2], 4], expected=[2, 0, 1]), dict(args=[[], 1], expected=[])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "tail", "newTail"], heads=["head"], label="train"),
        dict(kind="values", vars=["n", "k"]),
    ]),
    reference="""class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
        if (!head) return head;
        int n = 1;
        ListNode* tail = head;
        while (tail->next) {
            tail = tail->next;
            n++;
        }
        k %= n;
        if (k == 0) return head;
        tail->next = head;
        ListNode* newTail = head;
        for (int s = 0; s < n - k - 1; s++) newTail = newTail->next;
        head = newTail->next;
        newTail->next = nullptr;
        return head;
    }
};""",
)

add(
    id=2095, slug="delete-the-middle-node-of-a-linked-list", title="Delete the Middle Node of a Linked List", difficulty="Medium",
    world="linked-list", tags=["linked-list", "two-pointers"],
    story=dict(
        title="Dropping the Middle Car",
        text="The middle car is broken. A hare starts two cars ahead of the tortoise; when the hare runs out of train, "
             "the tortoise is just before the middle car and unhooks it.",
        goal="Remove the middle node and return the train.",
    ),
    spec=dict(method="deleteMiddle", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 3, 4, 7, 1, 2, 6]], expected=[1, 3, 4, 1, 2, 6]), dict(args=[[1, 2, 3, 4]], expected=[1, 2, 4]), dict(args=[[2, 1]], expected=[2]),
           dict(args=[[1]], expected=[])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "slow", "fast"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* deleteMiddle(ListNode* head) {
        if (!head->next) return nullptr;
        ListNode* slow = head;
        ListNode* fast = head->next->next;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        slow->next = slow->next->next;
        return head;
    }
};""",
)

add(
    id=94, slug="binary-tree-inorder-traversal", title="Binary Tree Inorder Traversal", difficulty="Easy", world="trees",
    tags=["stack", "tree", "dfs"],
    story=dict(
        title="Left, Me, Right",
        text="A squirrel visits fruit in order: everything on the left first, then the fruit itself, then the right. It "
             "slides down-left stacking each fruit it passes, and writes a fruit down when it pops it.",
        goal="Return the values in inorder.",
    ),
    spec=dict(method="inorderTraversal", ret="vector<int>", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, None, 2, 3]], expected=[1, 3, 2]), dict(args=[[4, 2, 6, 1, 3, 5, 7]], expected=[1, 2, 3, 4, 5, 6, 7]), dict(args=[[]], expected=[])],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["cur"], label="orchard"),
        dict(kind="row", children=[dict(kind="stack", var="st", label="fruit passed"), dict(kind="array", var="res", label="visited", style="tiles", weight=2)]),
    ]),
    reference="""class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        stack<TreeNode*> st;
        TreeNode* cur = root;
        while (cur || !st.empty()) {
            while (cur) {
                st.push(cur);
                cur = cur->left;
            }
            cur = st.top();
            st.pop();
            res.push_back(cur->val);
            cur = cur->right;
        }
        return res;
    }
};""",
)

add(
    id=701, slug="insert-into-a-binary-search-tree", title="Insert into a Binary Search Tree", difficulty="Medium", world="trees",
    tags=["tree", "bst"],
    story=dict(
        title="Planting a New Fruit",
        text="A new fruit must hang where a search for it would look. The gardener walks down, going left for smaller "
             "and right for bigger, and grafts it onto the first empty branch.",
        goal="Insert val into the BST and return the root.",
    ),
    spec=dict(method="insertIntoBST", ret="TreeNode*", params=[["TreeNode*", "root"], ["int", "val"]]),
    tests=[dict(args=[[4, 2, 7, 1, 3], 5], expected=[4, 2, 7, 1, 3, 5]), dict(args=[[40, 20, 60, 10, 30, 50, 70], 25], expected=[40, 20, 60, 10, 30, 50, 70, None, None, 25]),
           dict(args=[[], 5], expected=[5])],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["cur"], label="orchard"),
        dict(kind="values", vars=["val"]),
    ]),
    reference="""class Solution {
public:
    TreeNode* insertIntoBST(TreeNode* root, int val) {
        if (!root) return new TreeNode(val);
        TreeNode* cur = root;
        while (true) {
            if (val < cur->val) {
                if (!cur->left) {
                    cur->left = new TreeNode(val);
                    break;
                }
                cur = cur->left;
            } else {
                if (!cur->right) {
                    cur->right = new TreeNode(val);
                    break;
                }
                cur = cur->right;
            }
        }
        return root;
    }
};""",
)

add(
    id=1337, slug="the-k-weakest-rows-in-a-matrix", title="The K Weakest Rows in a Matrix", difficulty="Easy", world="heap",
    tags=["array", "binary-search", "sorting", "heap", "matrix"],
    story=dict(
        title="The Weakest Platoons",
        text="Each row of the parade ground lists soldiers (1) before civilians (0). A sergeant counts each row and keeps "
             "a pyramid of the k weakest so far, strongest of them on top to be replaced.",
        goal="Return the indices of the k weakest rows, weakest first (ties by index).",
    ),
    spec=dict(method="kWeakestRows", ret="vector<int>", params=[["vector<vector<int>>&", "mat"], ["int", "k"]]),
    tests=[dict(args=[[[1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]], 3], expected=[2, 0, 3]),
           dict(args=[[[1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0]], 2], expected=[0, 2])],
    scene=dict(theme="castle", layers=[
        dict(kind="grid", var="mat", palette="bool", label="parade ground", pointers=[["i", "j"]]),
        dict(kind="heap", var="pq", label="k weakest [soldiers,row]"),
        dict(kind="values", vars=["k", "soldiers"]),
    ]),
    reference="""class Solution {
public:
    vector<int> kWeakestRows(vector<vector<int>>& mat, int k) {
        priority_queue<pair<int, int>> pq;
        for (int i = 0; i < (int)mat.size(); i++) {
            int soldiers = 0;
            for (int j = 0; j < (int)mat[i].size() && mat[i][j] == 1; j++) soldiers++;
            pq.push({soldiers, i});
            if ((int)pq.size() > k) pq.pop();
        }
        vector<int> res;
        while (!pq.empty()) {
            res.push_back(pq.top().second);
            pq.pop();
        }
        reverse(res.begin(), res.end());
        return res;
    }
};""",
)

add(
    id=451, slug="sort-characters-by-frequency", title="Sort Characters By Frequency", difficulty="Medium", world="heap",
    tags=["hash-table", "string", "sorting", "heap", "counting"],
    story=dict(
        title="The Most Popular Letters",
        text="Letter tiles are counted into lockers, then a pyramid with the most common letter on top hands out tiles: "
             "all copies of the top letter go first, then the next.",
        goal="Return the string sorted by how often each letter appears, most frequent first.",
    ),
    spec=dict(method="frequencySort", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["zzzyyx"], expected="zzzyyx"), dict(args=["abbccc"], expected="cccbba"), dict(args=["aabbbbc"], expected="bbbbaac")],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="map", var="cnt", label="letter counts"),
        dict(kind="heap", var="pq", label="pyramid [count,letter]"),
        dict(kind="string", var="res", label="sorted"),
    ]),
    reference="""class Solution {
public:
    string frequencySort(string s) {
        map<char, int> cnt;
        for (char c : s) cnt[c]++;
        priority_queue<pair<int, char>> pq;
        for (auto& [c, f] : cnt) pq.push({f, c});
        string res;
        while (!pq.empty()) {
            auto [f, c] = pq.top();
            pq.pop();
            res += string(f, c);
        }
        return res;
    }
};""",
    hints=["Any order of equally frequent letters is accepted on LeetCode; the tests here have no ties."],
)

add(
    id=1020, slug="number-of-enclaves", title="Number of Enclaves", difficulty="Medium", world="graphs",
    tags=["array", "dfs", "bfs", "matrix"],
    story=dict(
        title="Landlocked Fields",
        text="Fields touching the map's edge can walk off the map. A surveyor floods inward from every edge field and "
             "marks everything reachable; whatever land is left unmarked is landlocked.",
        goal="Return the number of land cells that cannot walk off the edge.",
    ),
    spec=dict(method="numEnclaves", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]], expected=3),
           dict(args=[[[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="grid", palette="islands", label="map", pointers=[["r", "c"]]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    void sink(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size() || grid[r][c] != 1) return;
        grid[r][c] = 2;
        sink(grid, r + 1, c);
        sink(grid, r - 1, c);
        sink(grid, r, c + 1);
        sink(grid, r, c - 1);
    }
    int numEnclaves(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                if (r == 0 || c == 0 || r == m - 1 || c == n - 1) sink(grid, r, c);
        int count = 0;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                if (grid[r][c] == 1) count++;
        return count;
    }
};""",
)

add(
    id=542, slug="01-matrix", title="01 Matrix", difficulty="Medium", world="graphs",
    tags=["array", "dynamic-programming", "bfs", "matrix"],
    story=dict(
        title="Distance to the Nearest Well",
        text="Every well (0) sends out water carriers at once. Each round they step one tile further, writing on every "
             "dry tile they reach how many steps it is from the nearest well.",
        goal="Return the distance from every cell to the nearest 0.",
    ),
    spec=dict(method="updateMatrix", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "mat"]]),
    tests=[dict(args=[[[0, 0, 0], [0, 1, 0], [0, 0, 0]]], expected=[[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
           dict(args=[[[0, 0, 0], [0, 1, 0], [1, 1, 1]]], expected=[[0, 0, 0], [0, 1, 0], [1, 2, 1]])],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="grid", var="dist", palette="dp", label="steps to a well", pointers=[["r", "c"]]),
        dict(kind="queue", var="q", label="carriers (r,c)"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
        int m = mat.size(), n = mat[0].size();
        vector<vector<int>> dist(m, vector<int>(n, -1));
        queue<pair<int, int>> q;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                if (mat[r][c] == 0) {
                    dist[r][c] = 0;
                    q.push({r, c});
                }
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= m || nc >= n || dist[nr][nc] != -1) continue;
                dist[nr][nc] = dist[r][c] + 1;
                q.push({nr, nc});
            }
        }
        return dist;
    }
};""",
)

add(
    id=77, slug="combinations", title="Combinations", difficulty="Medium", world="backtracking", tags=["backtracking"],
    story=dict(
        title="Picking a Team",
        text="A coach picks k players from numbers 1 to n. At each door they add the next possible player to the team, "
             "go deeper, then send the player back to try the one after.",
        goal="Return every team of k numbers from 1..n (any order).",
    ),
    spec=dict(method="combine", ret="vector<vector<int>>", params=[["int", "n"], ["int", "k"]]),
    compare="unordered-deep",
    tests=[dict(args=[4, 2], expected=[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]), dict(args=[1, 1], expected=[[1]])],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="path", label="team", style="tiles"),
        dict(kind="values", vars=["start", "x", "n", "k"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void go(int start, int n, int k) {
        if ((int)path.size() == k) {
            res.push_back(path);
            return;
        }
        for (int x = start; x <= n; x++) {
            path.push_back(x);
            go(x + 1, n, k);
            path.pop_back();
        }
    }
    vector<vector<int>> combine(int n, int k) {
        go(1, n, k);
        return res;
    }
};""",
)

add(
    id=213, slug="house-robber-ii", title="House Robber II", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(
        title="The Fox and the Circle of Henhouses",
        text="This time the henhouses stand in a circle, so the first and last are neighbours. The fox plans two raids: "
             "one skipping the last house and one skipping the first, and keeps the better.",
        goal="Return the most eggs the fox can take without hitting two neighbours.",
    ),
    spec=dict(method="rob", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 3, 2]], expected=3), dict(args=[[1, 2, 3, 1]], expected=4), dict(args=[[1, 2, 3]], expected=3), dict(args=[[200, 3, 140, 20, 10]], expected=340)],
    visualTest=3,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="nums", label="henhouses (circle)", pointers=["lo", "i", "hi"], window=["lo", "hi"]),
        dict(kind="values", vars=["take", "skip"]),
    ]),
    reference="""class Solution {
public:
    int line(vector<int>& nums, int lo, int hi) {
        int take = 0, skip = 0;
        for (int i = lo; i <= hi; i++) {
            int nt = skip + nums[i];
            skip = max(skip, take);
            take = nt;
        }
        return max(take, skip);
    }
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        return max(line(nums, 0, n - 2), line(nums, 1, n - 1));
    }
};""",
)

add(
    id=452, slug="minimum-number-of-arrows-to-burst-balloons", title="Minimum Number of Arrows to Burst Balloons", difficulty="Medium",
    world="intervals", tags=["array", "greedy", "sorting"],
    story=dict(
        title="The Balloon Festival",
        text="Balloons stretch across ranges of the sky. Sorted by where they end, an archer shoots at the end of the "
             "first unburst balloon, popping every balloon that covers that spot.",
        goal="Return the fewest arrows needed to burst every balloon.",
    ),
    spec=dict(method="findMinArrowShots", ret="int", params=[["vector<vector<int>>&", "points"]]),
    tests=[dict(args=[[[10, 16], [2, 8], [1, 6], [7, 12]]], expected=2), dict(args=[[[1, 2], [3, 4], [5, 6], [7, 8]]], expected=4),
           dict(args=[[[1, 2], [2, 3], [3, 4], [4, 5]]], expected=2)],
    scene=dict(theme="lab", layers=[
        dict(kind="intervals", vars=["points"], pointers=["i"], label="balloons"),
        dict(kind="values", vars=["arrow", "arrows"]),
    ]),
    reference="""class Solution {
public:
    int findMinArrowShots(vector<vector<int>>& points) {
        sort(points.begin(), points.end(), [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
        int arrows = 1;
        long long arrow = points[0][1];
        for (int i = 1; i < (int)points.size(); i++) {
            if (points[i][0] > arrow) {
                arrows++;
                arrow = points[i][1];
            }
        }
        return arrows;
    }
};""",
)

add(
    id=860, slug="lemonade-change", title="Lemonade Change", difficulty="Easy", world="greedy", tags=["array", "greedy"],
    story=dict(
        title="The Lemonade Stand Till",
        text="Lemonade costs 5. Customers pay with 5, 10 or 20 notes and the till starts empty. For change, the seller "
             "always hands back a 10 first if they can, keeping 5s for later.",
        goal="Return true if every customer can get correct change.",
    ),
    spec=dict(method="lemonadeChange", ret="bool", params=[["vector<int>&", "bills"]]),
    tests=[dict(args=[[5, 5, 5, 10, 20]], expected=True), dict(args=[[5, 5, 10, 10, 20]], expected=False), dict(args=[[5, 5, 10, 20, 5, 5, 5, 20]], expected=True)],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="bills", label="customers", pointers=["i"]),
        dict(kind="values", vars=["five", "ten"]),
    ]),
    reference="""class Solution {
public:
    bool lemonadeChange(vector<int>& bills) {
        int five = 0, ten = 0;
        for (int i = 0; i < (int)bills.size(); i++) {
            if (bills[i] == 5) {
                five++;
            } else if (bills[i] == 10) {
                if (five == 0) return false;
                five--;
                ten++;
            } else {
                if (ten > 0 && five > 0) {
                    ten--;
                    five--;
                } else if (five >= 3) {
                    five -= 3;
                } else {
                    return false;
                }
            }
        }
        return true;
    }
};""",
)

add(
    id=9, slug="palindrome-number", title="Palindrome Number", difficulty="Easy", world="bits", tags=["math"],
    story=dict(
        title="The Mirror Odometer",
        text="Does the odometer read the same backwards? Peel digits off the right end and build the reversed half; when "
             "the halves meet, compare them.",
        goal="Return true if x is a palindrome.",
    ),
    spec=dict(method="isPalindrome", ret="bool", params=[["int", "x"]]),
    tests=[dict(args=[121], expected=True), dict(args=[-121], expected=False), dict(args=[10], expected=False), dict(args=[1234321], expected=True)],
    visualTest=3,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["x", "rev"])]),
    reference="""class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) return false;
        int rev = 0;
        while (x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }
        return x == rev || x == rev / 10;
    }
};""",
)
