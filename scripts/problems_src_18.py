"""Eighteenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=897, slug="increasing-order-search-tree", title="Increasing Order Search Tree", difficulty="Easy", world="trees", tags=["stack", "tree", "dfs", "bst"],
    story=dict(title="Re-hanging the Orchard as a Vine", text="Visit the sorted orchard left to right and hang each fruit as the right child of the one before, dropping every left branch.",
               goal="Return the tree rearranged into a right-only chain in order."),
    spec=dict(method="increasingBST", ret="TreeNode*", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[5, 3, 6, 2, 4, None, 8, 1, None, None, None, 7, 9]], expected=[1, None, 2, None, 3, None, 4, None, 5, None, 6, None, 7, None, 8, None, 9]),
           dict(args=[[5, 1, 7]], expected=[1, None, 5, None, 7])],
    visualTest=1,
    scene=dict(theme="forest", layers=[dict(kind="tree", var="root", pointers=["node", "tail"], label="orchard")]),
    reference="""class Solution {
public:
    TreeNode* tail = nullptr;
    TreeNode* head = nullptr;
    void walk(TreeNode* node) {
        if (!node) return;
        walk(node->left);
        node->left = nullptr;
        if (tail) tail->right = node;
        else head = node;
        tail = node;
        walk(node->right);
    }
    TreeNode* increasingBST(TreeNode* root) {
        walk(root);
        return head;
    }
};""",
)

add(
    id=907, slug="sum-of-subarray-minimums", title="Sum of Subarray Minimums", difficulty="Medium", world="stack", tags=["array", "dynamic-programming", "stack", "monotonic-stack"],
    story=dict(title="Who Is the Smallest, and for How Long?", text="Each tower is the minimum of every stretch reaching from just past the last smaller tower on its left to just before the next smaller on its right. Monotonic stacks find both edges.",
               goal="Return the sum of min(subarray) over all subarrays, mod 1e9+7."),
    spec=dict(method="sumSubarrayMins", ret="int", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[3, 1, 2, 4]], expected=17), dict(args=[[11, 81, 94, 43, 3]], expected=444)],
    scene=dict(theme="castle", layers=[
        dict(kind="bars", var="arr", label="towers", pointers=["i"]),
        dict(kind="stack", var="st", label="rising towers (index)"),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        const long long MOD = 1000000007;
        int n = arr.size();
        vector<int> left(n), right(n);
        vector<int> st;
        for (int i = 0; i < n; i++) {
            while (!st.empty() && arr[st.back()] > arr[i]) st.pop_back();
            left[i] = st.empty() ? i + 1 : i - st.back();
            st.push_back(i);
        }
        st.clear();
        for (int i = n - 1; i >= 0; i--) {
            while (!st.empty() && arr[st.back()] >= arr[i]) st.pop_back();
            right[i] = st.empty() ? n - i : st.back() - i;
            st.push_back(i);
        }
        long long total = 0;
        for (int i = 0; i < n; i++) total = (total + (long long)arr[i] * left[i] % MOD * right[i]) % MOD;
        return total;
    }
};""",
)

add(
    id=909, slug="snakes-and-ladders", title="Snakes and Ladders", difficulty="Medium", world="graphs", tags=["array", "bfs", "matrix"],
    story=dict(title="The Board Game", text="From each square a die roll reaches the next six; snakes and ladders teleport. Explore squares in rings of one roll each until the last square is reached.",
               goal="Return the fewest rolls to reach square n², or -1."),
    spec=dict(method="snakesAndLadders", ret="int", params=[["vector<vector<int>>&", "board"]]),
    tests=[dict(args=[[[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, 35, -1, -1, 13, -1], [-1, -1, -1, -1, -1, -1], [-1, 15, -1, -1, -1, -1]]], expected=4),
           dict(args=[[[-1, -1], [-1, 3]]], expected=1)],
    scene=dict(theme="castle", layers=[
        dict(kind="grid", var="board", palette="dp", label="board"),
        dict(kind="queue", var="q", label="squares to roll from"),
        dict(kind="values", vars=["rolls"]),
    ]),
    reference="""class Solution {
public:
    int snakesAndLadders(vector<vector<int>>& board) {
        int n = board.size();
        vector<int> dest(n * n + 1);
        int sq = 1;
        for (int r = n - 1, k = 0; r >= 0; r--, k++) {
            for (int c = 0; c < n; c++) {
                int col = k % 2 == 0 ? c : n - 1 - c;
                int to = board[r][col] == -1 ? sq : board[r][col];
                dest[sq] = to;
                sq++;
            }
        }
        vector<bool> seen(n * n + 1, false);
        queue<int> q;
        q.push(1);
        seen[1] = true;
        int rolls = 0;
        while (!q.empty()) {
            int sz = q.size();
            for (int s = 0; s < sz; s++) {
                int cur = q.front();
                q.pop();
                if (cur == n * n) return rolls;
                for (int d = 1; d <= 6 && cur + d <= n * n; d++) {
                    int nxt = dest[cur + d];
                    if (!seen[nxt]) {
                        seen[nxt] = true;
                        q.push(nxt);
                    }
                }
            }
            rolls++;
        }
        return -1;
    }
};""",
)

add(
    id=912, slug="sort-an-array", title="Sort an Array", difficulty="Medium", world="arrays", tags=["array", "divide-and-conquer", "sorting", "heap", "merge-sort"],
    story=dict(title="Merge-Sorting the Dock", text="Split the crates in half, sort each half behind its own door, then zip the two sorted halves back together through a buffer.",
               goal="Return the array sorted in ascending order."),
    spec=dict(method="sortArray", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[5, 2, 3, 1]], expected=[1, 2, 3, 5]), dict(args=[[5, 1, 1, 2, 0, 0]], expected=[0, 0, 1, 1, 2, 5])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates", pointers=["lo", "hi"], window=["lo", "hi"]),
        dict(kind="array", var="buf", label="merge buffer", style="tiles"),
    ]),
    reference="""class Solution {
public:
    void sortRange(vector<int>& nums, int lo, int hi) {
        if (lo >= hi) return;
        int mid = (lo + hi) / 2;
        sortRange(nums, lo, mid);
        sortRange(nums, mid + 1, hi);
        vector<int> buf;
        int i = lo, j = mid + 1;
        while (i <= mid || j <= hi) {
            if (j > hi || (i <= mid && nums[i] <= nums[j])) buf.push_back(nums[i++]);
            else buf.push_back(nums[j++]);
        }
        for (int k = 0; k < (int)buf.size(); k++) nums[lo + k] = buf[k];
    }
    vector<int> sortArray(vector<int>& nums) {
        sortRange(nums, 0, nums.size() - 1);
        return nums;
    }
};""",
)

add(
    id=921, slug="minimum-add-to-make-parentheses-valid", title="Minimum Add to Make Parentheses Valid", difficulty="Medium", world="stack", tags=["string", "stack", "greedy"],
    story=dict(title="Patching the Bracket Wall", text="Count open brackets still waiting. A ) with nothing open needs a patch; at the end every open bracket still waiting needs one too.",
               goal="Return the minimum number of brackets to add."),
    spec=dict(method="minAddToMakeValid", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["())"], expected=1), dict(args=["((("], expected=3), dict(args=["()))(("], expected=4)],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="brackets", pointers=["i"]),
        dict(kind="values", vars=["open", "adds"]),
    ]),
    reference="""class Solution {
public:
    int minAddToMakeValid(string s) {
        int open = 0, adds = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') open++;
            else if (open > 0) open--;
            else adds++;
        }
        return adds + open;
    }
};""",
)

add(
    id=925, slug="long-pressed-name", title="Long Pressed Name", difficulty="Easy", world="two-pointers", tags=["two-pointers", "string"],
    story=dict(title="The Sticky Keyboard", text="Two readers walk the real name and the typed one. A typed letter must match the next name letter, or repeat the typed letter just before it.",
               goal="Return true if typed could be name with some keys held down."),
    spec=dict(method="isLongPressedName", ret="bool", params=[["string", "name"], ["string", "typed"]]),
    tests=[dict(args=["alex", "aaleex"], expected=True), dict(args=["saeed", "ssaaedd"], expected=False), dict(args=["leelee", "lleeelee"], expected=True)],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="name", label="name", pointers=["i"]),
        dict(kind="string", var="typed", label="typed", pointers=["j"]),
    ]),
    reference="""class Solution {
public:
    bool isLongPressedName(string name, string typed) {
        int i = 0;
        for (int j = 0; j < (int)typed.size(); j++) {
            if (i < (int)name.size() && name[i] == typed[j]) i++;
            else if (j == 0 || typed[j] != typed[j - 1]) return false;
        }
        return i == (int)name.size();
    }
};""",
)

add(
    id=930, slug="binary-subarrays-with-sum", title="Binary Subarrays With Sum", difficulty="Medium", world="sliding-window", tags=["array", "hash-table", "sliding-window", "prefix-sum"],
    story=dict(title="Stretches with Exactly g Lamps", text="Keep a running count of lit lamps. The logbook says how many earlier positions were exactly goal lamps behind.",
               goal="Return how many subarrays sum to goal."),
    spec=dict(method="numSubarraysWithSum", ret="int", params=[["vector<int>&", "nums"], ["int", "goal"]]),
    tests=[dict(args=[[1, 0, 1, 0, 1], 2], expected=4), dict(args=[[0, 0, 0, 0, 0], 0], expected=15)],
    scene=dict(theme="space", layers=[
        dict(kind="array", var="nums", label="lamps", pointers=["i"]),
        dict(kind="map", var="seen", label="running count → times", lookup=["need"]),
        dict(kind="values", vars=["sum", "need", "count"]),
    ]),
    reference="""class Solution {
public:
    int numSubarraysWithSum(vector<int>& nums, int goal) {
        map<int, int> seen;
        seen[0] = 1;
        int sum = 0, count = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            sum += nums[i];
            int need = sum - goal;
            if (seen.count(need)) count += seen[need];
            seen[sum]++;
        }
        return count;
    }
};""",
)

add(
    id=935, slug="knight-dialer", title="Knight Dialer", difficulty="Medium", world="dp", tags=["dynamic-programming"],
    story=dict(title="The Knight on the Phone Pad", text="A chess knight hops across a phone keypad. Each round, the ways to stand on every digit are the sum of the ways to be on digits that can hop there.",
               goal="Return how many distinct numbers of length n can be dialled, mod 1e9+7."),
    spec=dict(method="knightDialer", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[1], expected=10), dict(args=[2], expected=20), dict(args=[3131], expected=136006598)],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="ways", label="ways ending on each digit", style="tiles", pointers=["d"]),
        dict(kind="values", vars=["step"]),
    ]),
    reference="""class Solution {
public:
    int knightDialer(int n) {
        const long long MOD = 1000000007;
        vector<vector<int>> from = {{4, 6}, {6, 8}, {7, 9}, {4, 8}, {0, 3, 9}, {}, {0, 1, 7}, {2, 6}, {1, 3}, {2, 4}};
        vector<long long> ways(10, 1);
        for (int step = 1; step < n; step++) {
            vector<long long> next(10, 0);
            for (int d = 0; d < 10; d++)
                for (int p : from[d]) next[d] = (next[d] + ways[p]) % MOD;
            ways = next;
        }
        long long total = 0;
        for (long long w : ways) total = (total + w) % MOD;
        return total;
    }
};""",
)

add(
    id=938, slug="range-sum-of-bst", title="Range Sum of BST", difficulty="Easy", world="trees", tags=["tree", "dfs", "bst"],
    story=dict(title="Weighing Only the Middle Fruit", text="In a sorted orchard, branches entirely below low or above high can be skipped. Add up only fruit inside the range.",
               goal="Return the sum of values in [low, high]."),
    spec=dict(method="rangeSumBST", ret="int", params=[["TreeNode*", "root"], ["int", "low"], ["int", "high"]]),
    tests=[dict(args=[[10, 5, 15, 3, 7, None, 18], 7, 15], expected=32), dict(args=[[10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10], expected=23)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["root"], label="orchard"),
        dict(kind="values", vars=["low", "high"]),
    ]),
    reference="""class Solution {
public:
    int rangeSumBST(TreeNode* root, int low, int high) {
        if (!root) return 0;
        if (root->val < low) return rangeSumBST(root->right, low, high);
        if (root->val > high) return rangeSumBST(root->left, low, high);
        return root->val + rangeSumBST(root->left, low, high) + rangeSumBST(root->right, low, high);
    }
};""",
)

add(
    id=941, slug="valid-mountain-array", title="Valid Mountain Array", difficulty="Easy", world="two-pointers", tags=["array"],
    story=dict(title="Is It a Real Peak?", text="Climb while the trail rises, then descend while it falls. A real mountain climbs at least once, descends at least once, and ends exactly at the last step.",
               goal="Return true if arr is a mountain."),
    spec=dict(method="validMountainArray", ret="bool", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[2, 1]], expected=False), dict(args=[[3, 5, 5]], expected=False), dict(args=[[0, 3, 2, 1]], expected=True)],
    visualTest=2,
    scene=dict(theme="forest", layers=[dict(kind="bars", var="arr", label="trail", pointers=["i"])]),
    reference="""class Solution {
public:
    bool validMountainArray(vector<int>& arr) {
        int n = arr.size(), i = 0;
        while (i + 1 < n && arr[i] < arr[i + 1]) i++;
        if (i == 0 || i == n - 1) return false;
        while (i + 1 < n && arr[i] > arr[i + 1]) i++;
        return i == n - 1;
    }
};""",
)

add(
    id=945, slug="minimum-increment-to-make-array-unique", title="Minimum Increment to Make Array Unique", difficulty="Medium", world="greedy", tags=["array", "greedy", "sorting", "counting"],
    story=dict(title="Every Badge a Different Number", text="Sorted badges are walked in order; any badge not bigger than the one before is bumped to one more than it, and the bumps are counted.",
               goal="Return the fewest +1 moves to make all values unique."),
    spec=dict(method="minIncrementForUnique", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 2]], expected=1), dict(args=[[3, 2, 1, 2, 1, 7]], expected=6)],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="nums", label="badges (sorted)", pointers=["i"]),
        dict(kind="values", vars=["moves"]),
    ]),
    reference="""class Solution {
public:
    int minIncrementForUnique(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int moves = 0;
        for (int i = 1; i < (int)nums.size(); i++) {
            if (nums[i] <= nums[i - 1]) {
                moves += nums[i - 1] + 1 - nums[i];
                nums[i] = nums[i - 1] + 1;
            }
        }
        return moves;
    }
};""",
)

add(
    id=948, slug="bag-of-tokens", title="Bag of Tokens", difficulty="Medium", world="greedy", tags=["array", "two-pointers", "greedy", "sorting"],
    story=dict(title="Spending Power for Points", text="Tokens are sorted. Spend power on the cheapest token for a point; when stuck, cash in a point for the priciest token's power, keeping the best score seen.",
               goal="Return the largest score possible."),
    spec=dict(method="bagOfTokensScore", ret="int", params=[["vector<int>&", "tokens"], ["int", "power"]]),
    tests=[dict(args=[[100], 50], expected=0), dict(args=[[200, 100], 150], expected=1), dict(args=[[100, 200, 300, 400], 200], expected=2)],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="tokens", label="tokens (sorted)", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["power", "score", "best"]),
    ]),
    reference="""class Solution {
public:
    int bagOfTokensScore(vector<int>& tokens, int power) {
        sort(tokens.begin(), tokens.end());
        int l = 0, r = tokens.size() - 1, score = 0, best = 0;
        while (l <= r) {
            if (power >= tokens[l]) {
                power -= tokens[l++];
                best = max(best, ++score);
            } else if (score > 0) {
                power += tokens[r--];
                score--;
            } else {
                break;
            }
        }
        return best;
    }
};""",
)

add(
    id=950, slug="reveal-cards-in-increasing-order", title="Reveal Cards In Increasing Order", difficulty="Medium", world="stack", tags=["array", "queue", "sorting", "simulation"],
    story=dict(title="Stacking the Magician's Deck", text="Simulate the reveal with a queue of positions: the front position gets the next smallest card, then the following position moves to the back.",
               goal="Return a deck order that reveals cards in increasing order."),
    spec=dict(method="deckRevealedIncreasing", ret="vector<int>", params=[["vector<int>&", "deck"]]),
    tests=[dict(args=[[17, 13, 11, 2, 3, 5, 7]], expected=[2, 13, 3, 11, 5, 17, 7]), dict(args=[[1, 1000]], expected=[1, 1000])],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="deck", label="cards (sorted)", pointers=["k"]),
        dict(kind="queue", var="q", label="positions"),
        dict(kind="array", var="res", label="deck order", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> deckRevealedIncreasing(vector<int>& deck) {
        sort(deck.begin(), deck.end());
        int n = deck.size();
        queue<int> q;
        for (int i = 0; i < n; i++) q.push(i);
        vector<int> res(n);
        for (int k = 0; k < n; k++) {
            res[q.front()] = deck[k];
            q.pop();
            if (!q.empty()) {
                q.push(q.front());
                q.pop();
            }
        }
        return res;
    }
};""",
)

add(
    id=951, slug="flip-equivalent-binary-trees", title="Flip Equivalent Binary Trees", difficulty="Medium", world="trees", tags=["tree", "dfs"],
    story=dict(title="Twins Up to Mirror Swaps", text="Two orchards are equivalent if every fruit matches and its branches match either straight or swapped.",
               goal="Return true if the trees are flip equivalent."),
    spec=dict(method="flipEquiv", ret="bool", params=[["TreeNode*", "root1"], ["TreeNode*", "root2"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5, 6, None, None, None, 7, 8], [1, 3, 2, None, 6, 4, 5, None, None, None, None, 8, 7]], expected=True), dict(args=[[], []], expected=True), dict(args=[[], [1]], expected=False)],
    scene=dict(theme="forest", layers=[dict(kind="row", children=[
        dict(kind="tree", var="root1", pointers=["a"], label="orchard 1"),
        dict(kind="tree", var="root2", pointers=["b"], label="orchard 2"),
    ])]),
    reference="""class Solution {
public:
    bool same(TreeNode* a, TreeNode* b) {
        if (!a || !b) return a == b;
        if (a->val != b->val) return false;
        return (same(a->left, b->left) && same(a->right, b->right)) || (same(a->left, b->right) && same(a->right, b->left));
    }
    bool flipEquiv(TreeNode* root1, TreeNode* root2) {
        return same(root1, root2);
    }
};""",
)

add(
    id=953, slug="verifying-an-alien-dictionary", title="Verifying an Alien Dictionary", difficulty="Easy", world="arrays", tags=["array", "hash-table", "string"],
    story=dict(title="The Alien Alphabet", text="Each alien letter gets its rank in the lockers. Neighbouring words are compared at their first different letter; a shorter prefix must come first.",
               goal="Return true if the words are sorted in the alien order."),
    spec=dict(method="isAlienSorted", ret="bool", params=[["vector<string>&", "words"], ["string", "order"]]),
    tests=[dict(args=[["hello", "leetcode"], "hlabcdefgijkmnopqrstuvwxyz"], expected=True), dict(args=[["word", "world", "row"], "worldabcefghijkmnpqstuvxyz"], expected=False),
           dict(args=[["apple", "app"], "abcdefghijklmnopqrstuvwxyz"], expected=False)],
    visualTest=1,
    scene=dict(theme="space", layers=[
        dict(kind="array", var="words", label="words", style="tiles", pointers=["k"]),
        dict(kind="map", var="rank", label="alien rank"),
    ]),
    reference="""class Solution {
public:
    bool isAlienSorted(vector<string>& words, string order) {
        map<char, int> rank;
        for (int i = 0; i < 26; i++) rank[order[i]] = i;
        for (int k = 1; k < (int)words.size(); k++) {
            string& a = words[k - 1];
            string& b = words[k];
            int i = 0;
            while (i < (int)a.size() && i < (int)b.size() && a[i] == b[i]) i++;
            if (i == (int)b.size() && i < (int)a.size()) return false;
            if (i < (int)a.size() && rank[a[i]] > rank[b[i]]) return false;
        }
        return true;
    }
};""",
)

add(
    id=958, slug="check-completeness-of-a-binary-tree", title="Check Completeness of a Binary Tree", difficulty="Medium", world="trees", tags=["tree", "bfs"],
    story=dict(title="No Gaps in the Rows", text="Pickers sweep row by row, queueing even empty branches. Once an empty slot is seen, no real fruit may appear after it.",
               goal="Return true if the tree is complete."),
    spec=dict(method="isCompleteTree", ret="bool", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5, 6]], expected=True), dict(args=[[1, 2, 3, 4, 5, None, 7]], expected=False)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="pickers"),
        dict(kind="values", vars=["gap"]),
    ]),
    reference="""class Solution {
public:
    bool isCompleteTree(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);
        bool gap = false;
        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            if (!node) {
                gap = true;
                continue;
            }
            if (gap) return false;
            q.push(node->left);
            q.push(node->right);
        }
        return true;
    }
};""",
)

add(
    id=962, slug="maximum-width-ramp", title="Maximum Width Ramp", difficulty="Medium", world="stack", tags=["array", "stack", "monotonic-stack"],
    story=dict(title="The Longest Ramp", text="Stack every new low point from the left. Then walk from the right: while the current point is at least the stack's low point, that ramp is a candidate and the low point is used up.",
               goal="Return the maximum j - i with nums[i] <= nums[j]."),
    spec=dict(method="maxWidthRamp", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[6, 0, 8, 2, 1, 5]], expected=4), dict(args=[[9, 8, 1, 0, 1, 9, 4, 0, 4, 1]], expected=7)],
    scene=dict(theme="castle", layers=[
        dict(kind="bars", var="nums", label="heights", pointers=["j"]),
        dict(kind="stack", var="st", label="low points (index)"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int maxWidthRamp(vector<int>& nums) {
        vector<int> st;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (st.empty() || nums[i] < nums[st.back()]) st.push_back(i);
        }
        int best = 0;
        for (int j = nums.size() - 1; j >= 0; j--) {
            while (!st.empty() && nums[st.back()] <= nums[j]) {
                best = max(best, j - st.back());
                st.pop_back();
            }
        }
        return best;
    }
};""",
)

add(
    id=967, slug="numbers-with-same-consecutive-differences", title="Numbers With Same Consecutive Differences", difficulty="Medium", world="backtracking", tags=["backtracking", "bfs"],
    story=dict(title="Stepping Digits", text="Start from each non-zero digit and keep adding a next digit that is exactly k away, up or down, until the number has n digits.",
               goal="Return every n-digit number whose neighbouring digits differ by k (any order)."),
    spec=dict(method="numsSameConsecDiff", ret="vector<int>", params=[["int", "n"], ["int", "k"]]),
    compare="unordered",
    tests=[dict(args=[3, 7], expected=[181, 292, 707, 818, 929]), dict(args=[2, 1], expected=[10, 12, 21, 23, 32, 34, 43, 45, 54, 56, 65, 67, 76, 78, 87, 89, 98])],
    scene=dict(theme="cave", layers=[
        dict(kind="values", vars=["num", "len", "last"]),
        dict(kind="array", var="res", label="found", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> res;
    void go(int num, int len, int n, int k) {
        if (len == n) {
            res.push_back(num);
            return;
        }
        int last = num % 10;
        if (last + k <= 9) go(num * 10 + last + k, len + 1, n, k);
        if (k > 0 && last - k >= 0) go(num * 10 + last - k, len + 1, n, k);
    }
    vector<int> numsSameConsecDiff(int n, int k) {
        for (int d = 1; d <= 9; d++) go(d, 1, n, k);
        return res;
    }
};""",
)

add(
    id=974, slug="subarray-sums-divisible-by-k", title="Subarray Sums Divisible by K", difficulty="Medium", world="arrays", tags=["array", "hash-table", "prefix-sum"],
    story=dict(title="Matching Remainders", text="Two running totals with the same remainder mod k bound a stretch divisible by k. The lockers count each remainder seen.",
               goal="Return how many subarrays sum to a multiple of k."),
    spec=dict(method="subarraysDivByK", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[4, 5, 0, -2, -3, 1], 5], expected=7), dict(args=[[5], 9], expected=0)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="nums", label="depots", pointers=["i"]),
        dict(kind="map", var="seen", label="remainder → times", lookup=["rem"]),
        dict(kind="values", vars=["rem", "count"]),
    ]),
    reference="""class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) {
        map<int, int> seen;
        seen[0] = 1;
        int rem = 0, count = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            rem = ((rem + nums[i]) % k + k) % k;
            count += seen[rem];
            seen[rem]++;
        }
        return count;
    }
};""",
)

add(
    id=976, slug="largest-perimeter-triangle", title="Largest Perimeter Triangle", difficulty="Easy", world="greedy", tags=["array", "math", "greedy", "sorting"],
    story=dict(title="The Biggest Triangle of Sticks", text="Sorted from longest, the first three neighbours where the two shorter beat the longest make the biggest triangle.",
               goal="Return the largest perimeter of a valid triangle, or 0."),
    spec=dict(method="largestPerimeter", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 1, 2]], expected=5), dict(args=[[1, 2, 1, 10]], expected=0), dict(args=[[3, 6, 2, 3]], expected=8)],
    visualTest=2,
    scene=dict(theme="dock", layers=[dict(kind="bars", var="nums", label="sticks (longest first)", pointers=["i"])]),
    reference="""class Solution {
public:
    int largestPerimeter(vector<int>& nums) {
        sort(nums.rbegin(), nums.rend());
        for (int i = 0; i + 2 < (int)nums.size(); i++) {
            if (nums[i + 1] + nums[i + 2] > nums[i]) return nums[i] + nums[i + 1] + nums[i + 2];
        }
        return 0;
    }
};""",
)

add(
    id=978, slug="longest-turbulent-subarray", title="Longest Turbulent Subarray", difficulty="Medium", world="sliding-window", tags=["array", "dynamic-programming", "sliding-window"],
    story=dict(title="The Choppiest Water", text="Track the longest zigzag ending here going up and going down. A rise extends the previous down-run; a fall extends the previous up-run.",
               goal="Return the length of the longest turbulent subarray."),
    spec=dict(method="maxTurbulenceSize", ret="int", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[9, 4, 2, 10, 7, 8, 8, 1, 9]], expected=5), dict(args=[[4, 8, 12, 16]], expected=2), dict(args=[[100]], expected=1)],
    scene=dict(theme="dock", layers=[
        dict(kind="bars", var="arr", label="waves", pointers=["i"]),
        dict(kind="values", vars=["up", "down", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxTurbulenceSize(vector<int>& arr) {
        int up = 1, down = 1, best = 1;
        for (int i = 1; i < (int)arr.size(); i++) {
            if (arr[i] > arr[i - 1]) {
                up = down + 1;
                down = 1;
            } else if (arr[i] < arr[i - 1]) {
                down = up + 1;
                up = 1;
            } else {
                up = down = 1;
            }
            best = max({best, up, down});
        }
        return best;
    }
};""",
)

add(
    id=979, slug="distribute-coins-in-binary-tree", title="Distribute Coins in Binary Tree", difficulty="Medium", world="trees", tags=["tree", "dfs"],
    story=dict(title="Every Fruit Gets One Coin", text="Each branch reports its surplus or shortage of coins. That many coins must cross the branch's edge, so add its size to the moves.",
               goal="Return the number of moves to give every node exactly one coin."),
    spec=dict(method="distributeCoins", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 0, 0]], expected=2), dict(args=[[0, 3, 0]], expected=3), dict(args=[[1, 0, 0, None, 3]], expected=4)],
    visualTest=2,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard of coins"),
        dict(kind="values", vars=["l", "r", "moves"]),
    ]),
    reference="""class Solution {
public:
    int moves = 0;
    int extra(TreeNode* node) {
        if (!node) return 0;
        int l = extra(node->left);
        int r = extra(node->right);
        moves += abs(l) + abs(r);
        return node->val + l + r - 1;
    }
    int distributeCoins(TreeNode* root) {
        extra(root);
        return moves;
    }
};""",
)

add(
    id=980, slug="unique-paths-iii", title="Unique Paths III", difficulty="Hard", world="backtracking", tags=["array", "backtracking", "bit-manipulation", "matrix"],
    story=dict(title="Walk Every Open Tile Once", text="From the start, the explorer visits every empty tile exactly once before the end. Each tile walked onto is blocked, and unblocked on the way back out.",
               goal="Return the number of such walks."),
    spec=dict(method="uniquePathsIII", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]]], expected=2), dict(args=[[[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]]], expected=4), dict(args=[[[0, 1], [2, 0]]], expected=0)],
    visualTest=2,
    scene=dict(theme="cave", layers=[
        dict(kind="grid", var="grid", palette="dp", label="cave (−1 rock, 3 walked)", pointers=[["r", "c"]]),
        dict(kind="values", vars=["left", "ways"]),
    ]),
    reference="""class Solution {
public:
    int ways = 0;
    void walk(vector<vector<int>>& grid, int r, int c, int left) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size() || grid[r][c] == -1 || grid[r][c] == 3) return;
        if (grid[r][c] == 2) {
            if (left == 0) ways++;
            return;
        }
        int keep = grid[r][c];
        grid[r][c] = 3;
        walk(grid, r + 1, c, left - 1);
        walk(grid, r - 1, c, left - 1);
        walk(grid, r, c + 1, left - 1);
        walk(grid, r, c - 1, left - 1);
        grid[r][c] = keep;
    }
    int uniquePathsIII(vector<vector<int>>& grid) {
        int sr = 0, sc = 0, empty = 0;
        for (int r = 0; r < (int)grid.size(); r++)
            for (int c = 0; c < (int)grid[0].size(); c++) {
                if (grid[r][c] == 1) {
                    sr = r;
                    sc = c;
                }
                if (grid[r][c] != -1) empty++;
            }
        walk(grid, sr, sc, empty - 1);
        return ways;
    }
};""",
)

add(
    id=983, slug="minimum-cost-for-tickets", title="Minimum Cost For Tickets", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Day, Week or Month Pass?", text="The ledger records the cheapest cost to cover every travel day up to today: a 1-day pass from yesterday, a 7-day from a week ago, or a 30-day from a month ago.",
               goal="Return the minimum cost to travel on every listed day."),
    spec=dict(method="mincostTickets", ret="int", params=[["vector<int>&", "days"], ["vector<int>&", "costs"]]),
    tests=[dict(args=[[1, 4, 6, 7, 8, 20], [2, 7, 15]], expected=11), dict(args=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15]], expected=17)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="dp", label="cheapest cover up to day", style="tiles", pointers=["d"]),
        dict(kind="set", var="travel", label="travel days"),
    ]),
    reference="""class Solution {
public:
    int mincostTickets(vector<int>& days, vector<int>& costs) {
        set<int> travel(days.begin(), days.end());
        int last = days.back();
        vector<int> dp(last + 1, 0);
        for (int d = 1; d <= last; d++) {
            if (!travel.count(d)) {
                dp[d] = dp[d - 1];
                continue;
            }
            dp[d] = min({dp[d - 1] + costs[0], dp[max(0, d - 7)] + costs[1], dp[max(0, d - 30)] + costs[2]});
        }
        return dp[last];
    }
};""",
)

add(
    id=986, slug="interval-list-intersections", title="Interval List Intersections", difficulty="Medium", world="intervals", tags=["array", "two-pointers", "sweep-line"],
    story=dict(title="When Are Both Rooms Booked?", text="Two sorted calendars are walked together. The overlap of the two current bookings is recorded, and whichever booking ends first is moved past.",
               goal="Return the intersections of the two interval lists."),
    spec=dict(method="intervalIntersection", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "firstList"], ["vector<vector<int>>&", "secondList"]]),
    tests=[dict(args=[[[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]], expected=[[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]),
           dict(args=[[[1, 3], [5, 9]], []], expected=[])],
    scene=dict(theme="lab", layers=[dict(kind="intervals", vars=["firstList", "secondList", "res"], pointers=["i"], label="calendars")]),
    reference="""class Solution {
public:
    vector<vector<int>> intervalIntersection(vector<vector<int>>& firstList, vector<vector<int>>& secondList) {
        vector<vector<int>> res;
        int i = 0, j = 0;
        while (i < (int)firstList.size() && j < (int)secondList.size()) {
            int lo = max(firstList[i][0], secondList[j][0]);
            int hi = min(firstList[i][1], secondList[j][1]);
            if (lo <= hi) res.push_back({lo, hi});
            if (firstList[i][1] < secondList[j][1]) i++;
            else j++;
        }
        return res;
    }
};""",
)
