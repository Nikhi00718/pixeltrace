"""Thirteenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=258, slug="add-digits", title="Add Digits", difficulty="Easy", world="bits", tags=["math", "simulation", "number-theory"],
    story=dict(title="Shrinking the Number", text="Add up the digits, then the digits of that, until a single digit is left.",
               goal="Return the single digit reached by repeatedly summing digits."),
    spec=dict(method="addDigits", ret="int", params=[["int", "num"]]),
    tests=[dict(args=[38], expected=2), dict(args=[0], expected=0), dict(args=[987654], expected=3)],
    visualTest=2,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["num", "sum"])]),
    reference="""class Solution {
public:
    int addDigits(int num) {
        while (num >= 10) {
            int sum = 0;
            while (num > 0) {
                sum += num % 10;
                num /= 10;
            }
            num = sum;
        }
        return num;
    }
};""",
)

add(
    id=263, slug="ugly-number", title="Ugly Number", difficulty="Easy", world="bits", tags=["math"],
    story=dict(title="Only Small Prime Bricks", text="Divide out every 2, 3 and 5. If nothing but 1 is left, the number was built only from those bricks.",
               goal="Return true if n's prime factors are only 2, 3 and 5."),
    spec=dict(method="isUgly", ret="bool", params=[["int", "n"]]),
    tests=[dict(args=[6], expected=True), dict(args=[1], expected=True), dict(args=[14], expected=False), dict(args=[300], expected=True)],
    visualTest=3,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n", "p"])]),
    reference="""class Solution {
public:
    bool isUgly(int n) {
        if (n <= 0) return false;
        int primes[3] = {2, 3, 5};
        for (int p : primes) {
            while (n % p == 0) n /= p;
        }
        return n == 1;
    }
};""",
)

add(
    id=264, slug="ugly-number-ii", title="Ugly Number II", difficulty="Medium", world="dp", tags=["hash-table", "math", "dynamic-programming", "heap"],
    story=dict(title="Three Conveyor Belts", text="Three pointers walk the list of ugly numbers, each offering its number times 2, 3 or 5. The smallest offer is the next ugly number, and every pointer that made it steps forward.",
               goal="Return the n-th ugly number."),
    spec=dict(method="nthUglyNumber", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[10], expected=12), dict(args=[1], expected=1), dict(args=[15], expected=24)],
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="u", label="ugly numbers", style="tiles", pointers=["i2", "i3", "i5"]),
        dict(kind="values", vars=["a", "b", "c"]),
    ]),
    reference="""class Solution {
public:
    int nthUglyNumber(int n) {
        vector<int> u(1, 1);
        int i2 = 0, i3 = 0, i5 = 0;
        while ((int)u.size() < n) {
            int a = u[i2] * 2, b = u[i3] * 3, c = u[i5] * 5;
            int next = min({a, b, c});
            u.push_back(next);
            if (next == a) i2++;
            if (next == b) i3++;
            if (next == c) i5++;
        }
        return u[n - 1];
    }
};""",
)

add(
    id=274, slug="h-index", title="H-Index", difficulty="Medium", world="arrays", tags=["array", "sorting", "counting-sort"],
    story=dict(title="The Researcher's Score", text="Papers are sorted by citations, most cited first. Walk down the list while paper number i+1 still has at least i+1 citations.",
               goal="Return the h-index."),
    spec=dict(method="hIndex", ret="int", params=[["vector<int>&", "citations"]]),
    tests=[dict(args=[[3, 0, 6, 1, 5]], expected=3), dict(args=[[1, 3, 1]], expected=1), dict(args=[[100]], expected=1)],
    scene=dict(theme="lab", layers=[
        dict(kind="bars", var="citations", label="citations (sorted)", pointers=["h"]),
    ]),
    reference="""class Solution {
public:
    int hIndex(vector<int>& citations) {
        sort(citations.rbegin(), citations.rend());
        int h = 0;
        while (h < (int)citations.size() && citations[h] >= h + 1) h++;
        return h;
    }
};""",
)

add(
    id=275, slug="h-index-ii", title="H-Index II", difficulty="Medium", world="binary-search", tags=["array", "binary-search"],
    story=dict(title="Binary-Searching the Score", text="Citations are already ascending. The guard finds the first paper whose citation count is at least the number of papers from it to the end.",
               goal="Return the h-index in O(log n)."),
    spec=dict(method="hIndex", ret="int", params=[["vector<int>&", "citations"]]),
    tests=[dict(args=[[0, 1, 3, 5, 6]], expected=3), dict(args=[[1, 2, 100]], expected=2)],
    scene=dict(theme="cave", layers=[dict(kind="bars", var="citations", label="citations", pointers=["lo", "mid", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    int hIndex(vector<int>& citations) {
        int n = citations.size(), lo = 0, hi = n - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (citations[mid] >= n - mid) hi = mid - 1;
            else lo = mid + 1;
        }
        return n - lo;
    }
};""",
)

add(
    id=289, slug="game-of-life", title="Game of Life", difficulty="Medium", world="arrays", tags=["array", "matrix", "simulation"],
    story=dict(title="The Living Garden", text="Each plant counts its eight neighbours. In place, cells are marked 2 for \"alive now, dies\" and 3 for \"dead now, lives\" so the old state can still be read, then everything settles.",
               goal="Advance the board one generation, in place."),
    spec=dict(method="gameOfLife", ret="void", params=[["vector<vector<int>>&", "board"]], output="param:0"),
    tests=[dict(args=[[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]], expected=[[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]), dict(args=[[[1, 1], [1, 0]]], expected=[[1, 1], [1, 1]])],
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="board", palette="dp", label="garden (2 dies, 3 is born)", pointers=[["r", "c"]]),
        dict(kind="values", vars=["live"]),
    ]),
    reference="""class Solution {
public:
    void gameOfLife(vector<vector<int>>& board) {
        int m = board.size(), n = board[0].size();
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                int live = 0;
                for (int dr = -1; dr <= 1; dr++)
                    for (int dc = -1; dc <= 1; dc++) {
                        if (!dr && !dc) continue;
                        int nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nc >= 0 && nr < m && nc < n && (board[nr][nc] == 1 || board[nr][nc] == 2)) live++;
                    }
                if (board[r][c] == 1 && (live < 2 || live > 3)) board[r][c] = 2;
                if (board[r][c] == 0 && live == 3) board[r][c] = 3;
            }
        }
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++) board[r][c] = board[r][c] == 1 || board[r][c] == 3;
    }
};""",
)

add(
    id=299, slug="bulls-and-cows", title="Bulls and Cows", difficulty="Medium", world="arrays", tags=["hash-table", "string", "counting"],
    story=dict(title="The Code-Breaking Game", text="Right digit in the right place is a bull. For the rest, lockers count each digit on both sides; matches between leftover counts are cows.",
               goal="Return the hint as \"xAyB\"."),
    spec=dict(method="getHint", ret="string", params=[["string", "secret"], ["string", "guess"]]),
    tests=[dict(args=["1807", "7810"], expected="1A3B"), dict(args=["1123", "0111"], expected="1A1B")],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="secret", label="secret", pointers=["i"]),
        dict(kind="string", var="guess", label="guess", pointers=["i"]),
        dict(kind="row", children=[dict(kind="array", var="cs", label="secret leftovers", style="tiles"), dict(kind="array", var="cg", label="guess leftovers", style="tiles")]),
        dict(kind="values", vars=["bulls", "cows"]),
    ]),
    reference="""class Solution {
public:
    string getHint(string secret, string guess) {
        vector<int> cs(10, 0), cg(10, 0);
        int bulls = 0, cows = 0;
        for (int i = 0; i < (int)secret.size(); i++) {
            if (secret[i] == guess[i]) bulls++;
            else {
                cs[secret[i] - '0']++;
                cg[guess[i] - '0']++;
            }
        }
        for (int d = 0; d < 10; d++) cows += min(cs[d], cg[d]);
        return to_string(bulls) + "A" + to_string(cows) + "B";
    }
};""",
)

add(
    id=309, slug="best-time-to-buy-and-sell-stock-with-cooldown", title="Best Time to Buy and Sell Stock with Cooldown", difficulty="Medium",
    world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Trading with a Rest Day", text="After selling, the trader must rest a day. Three purses are tracked daily: holding a share, just sold, and resting.",
               goal="Return the maximum profit."),
    spec=dict(method="maxProfit", ret="int", params=[["vector<int>&", "prices"]]),
    tests=[dict(args=[[1, 2, 3, 0, 2]], expected=3), dict(args=[[1]], expected=0)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="prices", label="price towers", pointers=["i"]),
        dict(kind="values", vars=["hold", "sold", "rest"]),
    ]),
    reference="""class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int hold = INT_MIN / 2, sold = 0, rest = 0;
        for (int i = 0; i < (int)prices.size(); i++) {
            int prevSold = sold;
            sold = hold + prices[i];
            hold = max(hold, rest - prices[i]);
            rest = max(rest, prevSold);
        }
        return max(sold, rest);
    }
};""",
)

add(
    id=316, slug="remove-duplicate-letters", title="Remove Duplicate Letters", difficulty="Medium", world="stack", tags=["string", "stack", "greedy", "monotonic-stack"],
    story=dict(title="The Smallest Word Tower", text="Each letter must appear once, as early-alphabet as possible. A bigger letter on top of the tower is knocked off if a copy of it still comes later.",
               goal="Return the lexicographically smallest result with each letter once."),
    spec=dict(method="removeDuplicateLetters", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["bcabc"], expected="abc"), dict(args=["cbacdcbc"], expected="acdb")],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="letters", pointers=["i"]),
        dict(kind="stack", var="st", label="tower"),
        dict(kind="map", var="last", label="last seen at"),
    ]),
    reference="""class Solution {
public:
    string removeDuplicateLetters(string s) {
        map<char, int> last;
        for (int i = 0; i < (int)s.size(); i++) last[s[i]] = i;
        string st;
        set<char> inStack;
        for (int i = 0; i < (int)s.size(); i++) {
            char c = s[i];
            if (inStack.count(c)) continue;
            while (!st.empty() && st.back() > c && last[st.back()] > i) {
                inStack.erase(st.back());
                st.pop_back();
            }
            st.push_back(c);
            inStack.insert(c);
        }
        return st;
    }
};""",
)

add(
    id=318, slug="maximum-product-of-word-lengths", title="Maximum Product of Word Lengths", difficulty="Medium", world="bits",
    tags=["array", "string", "bit-manipulation"],
    story=dict(title="Words Without Shared Letters", text="Each word lights a 26-lamp mask of its letters. Two words share no letter exactly when their masks AND to zero.",
               goal="Return the max length product of two words with no common letters."),
    spec=dict(method="maxProduct", ret="int", params=[["vector<string>&", "words"]]),
    tests=[dict(args=[["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]], expected=16), dict(args=[["a", "ab", "abc", "d", "cd", "bcd", "abcd"]], expected=4), dict(args=[["a", "aa", "aaa", "aaaa"]], expected=0)],
    scene=dict(theme="space", layers=[
        dict(kind="array", var="words", label="words", style="tiles", pointers=["i", "j"]),
        dict(kind="array", var="mask", label="letter masks", style="tiles"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int maxProduct(vector<string>& words) {
        int n = words.size(), best = 0;
        vector<int> mask(n, 0);
        for (int i = 0; i < n; i++)
            for (char c : words[i]) mask[i] |= 1 << (c - 'a');
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if ((mask[i] & mask[j]) == 0) best = max(best, (int)(words[i].size() * words[j].size()));
        return best;
    }
};""",
)

add(
    id=326, slug="power-of-three", title="Power of Three", difficulty="Easy", world="bits", tags=["math", "recursion"],
    story=dict(title="Dividing by Three", text="Keep dividing by three while it divides evenly. Only a power of three ends at exactly 1.",
               goal="Return true if n is a power of three."),
    spec=dict(method="isPowerOfThree", ret="bool", params=[["int", "n"]]),
    tests=[dict(args=[27], expected=True), dict(args=[0], expected=False), dict(args=[-1], expected=False), dict(args=[45], expected=False)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n"])]),
    reference="""class Solution {
public:
    bool isPowerOfThree(int n) {
        if (n <= 0) return false;
        while (n % 3 == 0) n /= 3;
        return n == 1;
    }
};""",
)

add(
    id=334, slug="increasing-triplet-subsequence", title="Increasing Triplet Subsequence", difficulty="Medium", world="greedy", tags=["array", "greedy"],
    story=dict(title="Three Rising Steps", text="Keep the smallest first step and the smallest second step seen so far. Any number bigger than both completes a rising triplet.",
               goal="Return true if some i < j < k has nums[i] < nums[j] < nums[k]."),
    spec=dict(method="increasingTriplet", ret="bool", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5]], expected=True), dict(args=[[5, 4, 3, 2, 1]], expected=False), dict(args=[[2, 1, 5, 0, 4, 6]], expected=True)],
    visualTest=2,
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="nums", label="steps", pointers=["i"]),
        dict(kind="values", vars=["first", "second"]),
    ]),
    reference="""class Solution {
public:
    bool increasingTriplet(vector<int>& nums) {
        int first = INT_MAX, second = INT_MAX;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (nums[i] <= first) first = nums[i];
            else if (nums[i] <= second) second = nums[i];
            else return true;
        }
        return false;
    }
};""",
)

add(
    id=337, slug="house-robber-iii", title="House Robber III", difficulty="Medium", world="trees", tags=["dynamic-programming", "tree", "dfs"],
    story=dict(title="The Fox in the Orchard Village", text="Houses form a tree and the fox can't rob a house and its parent. Every house reports two hauls: robbing it (children skipped) or skipping it (children free).",
               goal="Return the best haul."),
    spec=dict(method="rob", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 2, 3, None, 3, None, 1]], expected=7), dict(args=[[3, 4, 5, 1, 3, None, 1]], expected=9)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="village"),
        dict(kind="values", vars=["take", "skip"]),
    ]),
    reference="""class Solution {
public:
    pair<int, int> best(TreeNode* node) {
        if (!node) return {0, 0};
        auto l = best(node->left);
        auto r = best(node->right);
        int take = node->val + l.second + r.second;
        int skip = max(l.first, l.second) + max(r.first, r.second);
        return {take, skip};
    }
    int rob(TreeNode* root) {
        auto res = best(root);
        return max(res.first, res.second);
    }
};""",
)

add(
    id=342, slug="power-of-four", title="Power of Four", difficulty="Easy", world="bits", tags=["math", "bit-manipulation", "recursion"],
    story=dict(title="One Lamp in an Even Spot", text="A power of four has exactly one lamp lit, and it sits in an even position. Check both with masks.",
               goal="Return true if n is a power of four."),
    spec=dict(method="isPowerOfFour", ret="bool", params=[["int", "n"]]),
    tests=[dict(args=[16], expected=True), dict(args=[5], expected=False), dict(args=[1], expected=True), dict(args=[8], expected=False)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n", "one", "even"])]),
    reference="""class Solution {
public:
    bool isPowerOfFour(int n) {
        bool one = n > 0 && (n & (n - 1)) == 0;
        bool even = (n & 0x55555555) != 0;
        return one && even;
    }
};""",
)

add(
    id=343, slug="integer-break", title="Integer Break", difficulty="Medium", world="dp", tags=["math", "dynamic-programming"],
    story=dict(title="Cutting the Rope", text="A rope of length n is cut into at least two pieces to maximise the product of the lengths. The ledger tries every first cut, keeping the rest whole or cut further.",
               goal="Return the maximum product."),
    spec=dict(method="integerBreak", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[2], expected=1), dict(args=[10], expected=36), dict(args=[8], expected=18)],
    visualTest=2,
    scene=dict(theme="farm", layers=[dict(kind="array", var="dp", label="best product per length", style="tiles", pointers=["i", "j"])]),
    reference="""class Solution {
public:
    int integerBreak(int n) {
        vector<int> dp(n + 1, 0);
        dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            for (int j = 1; j < i; j++) dp[i] = max(dp[i], j * max(i - j, dp[i - j]));
        }
        return dp[n];
    }
};""",
)

add(
    id=349, slug="intersection-of-two-arrays", title="Intersection of Two Arrays", difficulty="Easy", world="arrays",
    tags=["array", "hash-table", "two-pointers", "binary-search", "sorting"],
    story=dict(title="Stamps Both Collectors Own", text="The first collection goes into lockers. Walking the second, any stamp found in the lockers is written down once.",
               goal="Return the unique values in both arrays (any order)."),
    spec=dict(method="intersection", ret="vector<int>", params=[["vector<int>&", "nums1"], ["vector<int>&", "nums2"]]),
    compare="unordered",
    tests=[dict(args=[[1, 2, 2, 1], [2, 2]], expected=[2]), dict(args=[[4, 9, 5], [9, 4, 9, 8, 4]], expected=[4, 9])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums2", label="second collection", pointers=["i"]),
        dict(kind="set", var="a", label="first collection"),
        dict(kind="set", var="both", label="in both"),
    ]),
    reference="""class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        set<int> a(nums1.begin(), nums1.end()), both;
        for (int i = 0; i < (int)nums2.size(); i++) {
            if (a.count(nums2[i])) both.insert(nums2[i]);
        }
        return vector<int>(both.begin(), both.end());
    }
};""",
)

add(
    id=350, slug="intersection-of-two-arrays-ii", title="Intersection of Two Arrays II", difficulty="Easy", world="two-pointers",
    tags=["array", "hash-table", "two-pointers", "binary-search", "sorting"],
    story=dict(title="Matching Stamps One for One", text="Both collections are sorted. Two clerks compare the stamps they hold: equal means a match for both, otherwise the smaller one steps forward.",
               goal="Return the intersection with multiplicity (any order)."),
    spec=dict(method="intersect", ret="vector<int>", params=[["vector<int>&", "nums1"], ["vector<int>&", "nums2"]]),
    compare="unordered",
    tests=[dict(args=[[1, 2, 2, 1], [2, 2]], expected=[2, 2]), dict(args=[[4, 9, 5], [9, 4, 9, 8, 4]], expected=[4, 9])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums1", label="collection 1 (sorted)", pointers=["i"]),
        dict(kind="array", var="nums2", label="collection 2 (sorted)", pointers=["j"]),
        dict(kind="array", var="res", label="matches", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> intersect(vector<int>& nums1, vector<int>& nums2) {
        sort(nums1.begin(), nums1.end());
        sort(nums2.begin(), nums2.end());
        vector<int> res;
        int i = 0, j = 0;
        while (i < (int)nums1.size() && j < (int)nums2.size()) {
            if (nums1[i] == nums2[j]) {
                res.push_back(nums1[i]);
                i++;
                j++;
            } else if (nums1[i] < nums2[j]) {
                i++;
            } else {
                j++;
            }
        }
        return res;
    }
};""",
)

add(
    id=367, slug="valid-perfect-square", title="Valid Perfect Square", difficulty="Easy", world="binary-search", tags=["math", "binary-search"],
    story=dict(title="Is It a Square Plot?", text="The gardener binary-searches a side length whose square is exactly the number of tiles.",
               goal="Return true if num is a perfect square, without sqrt."),
    spec=dict(method="isPerfectSquare", ret="bool", params=[["int", "num"]]),
    tests=[dict(args=[16], expected=True), dict(args=[14], expected=False), dict(args=[808201], expected=True)],
    visualTest=2,
    scene=dict(theme="farm", layers=[dict(kind="values", vars=["num", "lo", "mid", "hi", "sq"])]),
    reference="""class Solution {
public:
    bool isPerfectSquare(int num) {
        long long lo = 1, hi = num;
        while (lo <= hi) {
            long long mid = (lo + hi) / 2;
            long long sq = mid * mid;
            if (sq == num) return true;
            if (sq < num) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
};""",
)

add(
    id=371, slug="sum-of-two-integers", title="Sum of Two Integers", difficulty="Medium", world="bits", tags=["math", "bit-manipulation"],
    story=dict(title="Adding Without Plus", text="XOR adds the lamps without carrying; AND, shifted left, gives the carries. Repeat until there are no carries left.",
               goal="Return a + b without using + or -."),
    spec=dict(method="getSum", ret="int", params=[["int", "a"], ["int", "b"]]),
    tests=[dict(args=[1, 2], expected=3), dict(args=[2, 3], expected=5), dict(args=[-7, 12], expected=5)],
    visualTest=2,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["a", "b", "carry"])]),
    reference="""class Solution {
public:
    int getSum(int a, int b) {
        while (b != 0) {
            unsigned carry = (unsigned)(a & b) << 1;
            a = a ^ b;
            b = (int)carry;
        }
        return a;
    }
};""",
)

add(
    id=376, slug="wiggle-subsequence", title="Wiggle Subsequence", difficulty="Medium", world="greedy", tags=["array", "dynamic-programming", "greedy"],
    story=dict(title="The Zigzag Hike", text="Track the longest wiggle ending on an up-step and on a down-step. Each rise extends the down count, each fall extends the up count.",
               goal="Return the length of the longest wiggle subsequence."),
    spec=dict(method="wiggleMaxLength", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 7, 4, 9, 2, 5]], expected=6), dict(args=[[1, 17, 5, 10, 13, 15, 10, 5, 16, 8]], expected=7), dict(args=[[1, 2, 3, 4, 5, 6, 7, 8, 9]], expected=2)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="nums", label="trail", pointers=["i"]),
        dict(kind="values", vars=["up", "down"]),
    ]),
    reference="""class Solution {
public:
    int wiggleMaxLength(vector<int>& nums) {
        int up = 1, down = 1;
        for (int i = 1; i < (int)nums.size(); i++) {
            if (nums[i] > nums[i - 1]) up = down + 1;
            else if (nums[i] < nums[i - 1]) down = up + 1;
        }
        return max(up, down);
    }
};""",
)

add(
    id=378, slug="kth-smallest-element-in-a-sorted-matrix", title="Kth Smallest Element in a Sorted Matrix", difficulty="Medium", world="heap",
    tags=["array", "binary-search", "sorting", "heap", "matrix"],
    story=dict(title="Popping the Smallest Drawer", text="A pyramid starts with the first drawer of every row. Each pop takes the smallest, and the next drawer in that row joins the pyramid; the k-th pop is the answer.",
               goal="Return the k-th smallest value."),
    spec=dict(method="kthSmallest", ret="int", params=[["vector<vector<int>>&", "matrix"], ["int", "k"]]),
    tests=[dict(args=[[[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8], expected=13), dict(args=[[[-5]], 1], expected=-5)],
    scene=dict(theme="market", layers=[
        dict(kind="grid", var="matrix", palette="dp", label="drawers"),
        dict(kind="heap", var="pq", label="pyramid [value,row,col]"),
        dict(kind="values", vars=["k"]),
    ]),
    reference="""class Solution {
public:
    int kthSmallest(vector<vector<int>>& matrix, int k) {
        int n = matrix.size();
        priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>, greater<tuple<int, int, int>>> pq;
        for (int r = 0; r < n; r++) pq.push({matrix[r][0], r, 0});
        while (--k > 0) {
            auto [v, r, c] = pq.top();
            pq.pop();
            if (c + 1 < n) pq.push({matrix[r][c + 1], r, c + 1});
        }
        return get<0>(pq.top());
    }
};""",
)

add(
    id=387, slug="first-unique-character-in-a-string", title="First Unique Character in a String", difficulty="Easy", world="arrays",
    tags=["hash-table", "string", "queue", "counting"],
    story=dict(title="The Lonely Letter", text="Count every letter into lockers, then walk the string again and stop at the first letter whose locker holds 1.",
               goal="Return the index of the first non-repeating character, or -1."),
    spec=dict(method="firstUniqChar", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["leetcode"], expected=0), dict(args=["loveleetcode"], expected=2), dict(args=["aabb"], expected=-1)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="letters", pointers=["i"]),
        dict(kind="map", var="cnt", label="counts"),
    ]),
    reference="""class Solution {
public:
    int firstUniqChar(string s) {
        map<char, int> cnt;
        for (char c : s) cnt[c]++;
        for (int i = 0; i < (int)s.size(); i++) {
            if (cnt[s[i]] == 1) return i;
        }
        return -1;
    }
};""",
)

add(
    id=389, slug="find-the-difference", title="Find the Difference", difficulty="Easy", world="bits", tags=["hash-table", "string", "bit-manipulation", "sorting"],
    story=dict(title="The Extra Tile", text="t is s shuffled with one extra letter. XOR every letter of both; matching pairs cancel and the extra letter remains lit.",
               goal="Return the letter added to t."),
    spec=dict(method="findTheDifference", ret="char", params=[["string", "s"], ["string", "t"]]),
    tests=[dict(args=["abcd", "abcde"], expected="e"), dict(args=["", "y"], expected="y"), dict(args=["ae", "aea"], expected="a")],
    scene=dict(theme="space", layers=[
        dict(kind="string", var="t", label="shuffled", pointers=["i"]),
        dict(kind="values", vars=["x"]),
    ]),
    reference="""class Solution {
public:
    char findTheDifference(string s, string t) {
        int x = 0;
        for (char c : s) x ^= c;
        for (int i = 0; i < (int)t.size(); i++) x ^= t[i];
        return (char)x;
    }
};""",
)

add(
    id=394, slug="decode-string", title="Decode String", difficulty="Medium", world="stack", tags=["string", "stack", "recursion"],
    story=dict(title="Unpacking Nested Crates", text="A number before [ says how many copies to make. On [, the current text and count are stacked; on ], the inner text is repeated and appended to what was stacked.",
               goal="Return the decoded string."),
    spec=dict(method="decodeString", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["3[a]2[bc]"], expected="aaabcbc"), dict(args=["3[a2[c]]"], expected="accaccacc"), dict(args=["2[abc]3[cd]ef"], expected="abcabccdcdcdef")],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="packed", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="counts", label="counts"), dict(kind="stack", var="texts", label="saved text")]),
        dict(kind="values", vars=["cur", "num"]),
    ]),
    reference="""class Solution {
public:
    string decodeString(string s) {
        stack<int> counts;
        stack<string> texts;
        string cur;
        int num = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            char c = s[i];
            if (isdigit(c)) {
                num = num * 10 + (c - '0');
            } else if (c == '[') {
                counts.push(num);
                texts.push(cur);
                num = 0;
                cur = "";
            } else if (c == ']') {
                string inner = cur;
                cur = texts.top();
                texts.pop();
                for (int k = counts.top(); k > 0; k--) cur += inner;
                counts.pop();
            } else {
                cur.push_back(c);
            }
        }
        return cur;
    }
};""",
)

add(
    id=402, slug="remove-k-digits", title="Remove K Digits", difficulty="Medium", world="stack", tags=["string", "stack", "greedy", "monotonic-stack"],
    story=dict(title="Shaving the Number Down", text="Digits stack up. While removals are left and the top digit is bigger than the new one, the top is knocked off, keeping the number as small as possible.",
               goal="Return the smallest number after removing k digits."),
    spec=dict(method="removeKdigits", ret="string", params=[["string", "num"], ["int", "k"]]),
    tests=[dict(args=["1432219", 3], expected="1219"), dict(args=["10200", 1], expected="200"), dict(args=["10", 2], expected="0")],
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="num", label="digits", pointers=["i"]),
        dict(kind="stack", var="st", label="kept"),
        dict(kind="values", vars=["k"]),
    ]),
    reference="""class Solution {
public:
    string removeKdigits(string num, int k) {
        string st;
        for (int i = 0; i < (int)num.size(); i++) {
            while (k > 0 && !st.empty() && st.back() > num[i]) {
                st.pop_back();
                k--;
            }
            st.push_back(num[i]);
        }
        while (k > 0 && !st.empty()) {
            st.pop_back();
            k--;
        }
        int start = 0;
        while (start < (int)st.size() && st[start] == '0') start++;
        string res = st.substr(start);
        return res.empty() ? "0" : res;
    }
};""",
)
