"""Fifteenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=507, slug="perfect-number", title="Perfect Number", difficulty="Easy", world="bits", tags=["math"],
    story=dict(title="Divisors That Add Up", text="Walk divisors up to the square root; each one found brings its partner too. A perfect number equals the sum of its proper divisors.",
               goal="Return true if num is a perfect number."),
    spec=dict(method="checkPerfectNumber", ret="bool", params=[["int", "num"]]),
    tests=[dict(args=[28], expected=True), dict(args=[7], expected=False), dict(args=[496], expected=True)],
    visualTest=0,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["num", "d", "sum"])]),
    reference="""class Solution {
public:
    bool checkPerfectNumber(int num) {
        if (num <= 1) return false;
        int sum = 1;
        for (int d = 2; d * d <= num; d++) {
            if (num % d == 0) {
                sum += d;
                if (d * d != num) sum += num / d;
            }
        }
        return sum == num;
    }
};""",
)

add(
    id=509, slug="fibonacci-number", title="Fibonacci Number", difficulty="Easy", world="dp", tags=["math", "dynamic-programming", "recursion", "memoization"],
    story=dict(title="The Rabbit Ledger", text="Each month's count is the sum of the two months before. Two signposts slide forward carrying the last two counts.",
               goal="Return F(n)."),
    spec=dict(method="fib", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[2], expected=1), dict(args=[4], expected=3), dict(args=[10], expected=55)],
    visualTest=2,
    scene=dict(theme="farm", layers=[dict(kind="values", vars=["a", "b", "i"])]),
    reference="""class Solution {
public:
    int fib(int n) {
        int a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return a;
    }
};""",
)

add(
    id=516, slug="longest-palindromic-subsequence", title="Longest Palindromic Subsequence", difficulty="Medium", world="dp", tags=["string", "dynamic-programming"],
    story=dict(title="The Mirror Hidden in the Scroll", text="For each stretch i..j, matching end letters wrap the best answer inside; otherwise drop one end and keep the better.",
               goal="Return the length of the longest palindromic subsequence."),
    spec=dict(method="longestPalindromeSubseq", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["bbbab"], expected=4), dict(args=["cbbd"], expected=2)],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="scroll", pointers=["i", "j"], window=["i", "j"]),
        dict(kind="grid", var="dp", palette="dp", label="best for stretch i..j", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int i = n - 1; i >= 0; i--) {
            dp[i][i] = 1;
            for (int j = i + 1; j < n; j++) {
                if (s[i] == s[j]) dp[i][j] = dp[i + 1][j - 1] + 2;
                else dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]);
            }
        }
        return dp[0][n - 1];
    }
};""",
)

add(
    id=520, slug="detect-capital", title="Detect Capital", difficulty="Easy", world="arrays", tags=["string"],
    story=dict(title="Checking the Sign's Capitals", text="Count the capital letters. All capitals, none, or only the first letter is fine.",
               goal="Return true if the word uses capitals correctly."),
    spec=dict(method="detectCapitalUse", ret="bool", params=[["string", "word"]]),
    tests=[dict(args=["USA"], expected=True), dict(args=["FlaG"], expected=False), dict(args=["Google"], expected=True)],
    scene=dict(theme="market", layers=[
        dict(kind="string", var="word", label="sign", pointers=["i"]),
        dict(kind="values", vars=["caps"]),
    ]),
    reference="""class Solution {
public:
    bool detectCapitalUse(string word) {
        int caps = 0;
        for (int i = 0; i < (int)word.size(); i++) caps += isupper(word[i]) ? 1 : 0;
        return caps == 0 || caps == (int)word.size() || (caps == 1 && isupper(word[0]));
    }
};""",
)

add(
    id=523, slug="continuous-subarray-sum", title="Continuous Subarray Sum", difficulty="Medium", world="arrays", tags=["array", "hash-table", "math", "prefix-sum"],
    story=dict(title="Odometer Remainders", text="Keep the running total modulo k. If the same remainder shows up again at least two depots later, the stretch between is a multiple of k.",
               goal="Return true if some subarray of length ≥ 2 sums to a multiple of k."),
    spec=dict(method="checkSubarraySum", ret="bool", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[23, 2, 4, 6, 7], 6], expected=True), dict(args=[[23, 2, 6, 4, 7], 13], expected=False), dict(args=[[5, 0, 0, 0], 3], expected=True)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="nums", label="depots", pointers=["i"]),
        dict(kind="map", var="first", label="remainder first seen at", lookup=["rem"]),
        dict(kind="values", vars=["rem"]),
    ]),
    reference="""class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) {
        map<int, int> first;
        first[0] = -1;
        int rem = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            rem = (rem + nums[i]) % k;
            if (first.count(rem)) {
                if (i - first[rem] >= 2) return true;
            } else {
                first[rem] = i;
            }
        }
        return false;
    }
};""",
)

add(
    id=525, slug="contiguous-array", title="Contiguous Array", difficulty="Medium", world="arrays", tags=["array", "hash-table", "prefix-sum"],
    story=dict(title="Balanced Lamps", text="Count +1 for a lit lamp and -1 for a dark one. Two positions with the same running balance bound a stretch with equal lit and dark lamps.",
               goal="Return the length of the longest subarray with equal 0s and 1s."),
    spec=dict(method="findMaxLength", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[0, 1]], expected=2), dict(args=[[0, 1, 0]], expected=2), dict(args=[[0, 1, 1, 1, 1, 1, 0, 0, 0]], expected=6)],
    visualTest=2,
    scene=dict(theme="space", layers=[
        dict(kind="array", var="nums", label="lamps", pointers=["i"]),
        dict(kind="map", var="first", label="balance first seen at", lookup=["bal"]),
        dict(kind="values", vars=["bal", "best"]),
    ]),
    reference="""class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        map<int, int> first;
        first[0] = -1;
        int bal = 0, best = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            bal += nums[i] ? 1 : -1;
            if (first.count(bal)) best = max(best, i - first[bal]);
            else first[bal] = i;
        }
        return best;
    }
};""",
)

add(
    id=530, slug="minimum-absolute-difference-in-bst", title="Minimum Absolute Difference in BST", difficulty="Easy", world="trees", tags=["tree", "dfs", "bst"],
    story=dict(title="The Closest Two Fruits", text="Visiting a sorted orchard left-to-right lists the fruit in order, so the closest pair is always neighbours in that walk.",
               goal="Return the minimum difference between any two nodes."),
    spec=dict(method="getMinimumDifference", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[4, 2, 6, 1, 3]], expected=1), dict(args=[[1, 0, 48, None, None, 12, 49]], expected=1)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["prev", "best"]),
    ]),
    reference="""class Solution {
public:
    int prev = -1, best = INT_MAX;
    void walk(TreeNode* node) {
        if (!node) return;
        walk(node->left);
        if (prev >= 0) best = min(best, node->val - prev);
        prev = node->val;
        walk(node->right);
    }
    int getMinimumDifference(TreeNode* root) {
        walk(root);
        return best;
    }
};""",
)

add(
    id=532, slug="k-diff-pairs-in-an-array", title="K-diff Pairs in an Array", difficulty="Medium", world="arrays", tags=["array", "hash-table", "two-pointers", "binary-search", "sorting"],
    story=dict(title="Pairs a Fixed Distance Apart", text="Count every value. For k = 0 a pair needs a value seen twice; otherwise each value pairs with value + k if it exists.",
               goal="Return the number of unique k-diff pairs."),
    spec=dict(method="findPairs", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[3, 1, 4, 1, 5], 2], expected=2), dict(args=[[1, 2, 3, 4, 5], 1], expected=4), dict(args=[[1, 3, 1, 5, 4], 0], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="map", var="cnt", label="counts", lookup=["want"]),
        dict(kind="values", vars=["k", "want", "pairs"]),
    ]),
    reference="""class Solution {
public:
    int findPairs(vector<int>& nums, int k) {
        map<int, int> cnt;
        for (int x : nums) cnt[x]++;
        int pairs = 0;
        for (auto& [v, c] : cnt) {
            int want = v + k;
            if (k == 0) pairs += c > 1;
            else if (cnt.count(want)) pairs++;
        }
        return pairs;
    }
};""",
)

add(
    id=538, slug="convert-bst-to-greater-tree", title="Convert BST to Greater Tree", difficulty="Medium", world="trees", tags=["tree", "dfs", "bst"],
    story=dict(title="Adding Up from the Heaviest", text="Visit the orchard right-to-left (heaviest first), carrying a running total. Each fruit becomes itself plus every heavier fruit.",
               goal="Return the greater tree."),
    spec=dict(method="convertBST", ret="TreeNode*", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8]], expected=[30, 36, 21, 36, 35, 26, 15, None, None, None, 33, None, None, None, 8]),
           dict(args=[[0, None, 1]], expected=[1, None, 1])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int total = 0;
    void walk(TreeNode* node) {
        if (!node) return;
        walk(node->right);
        total += node->val;
        node->val = total;
        walk(node->left);
    }
    TreeNode* convertBST(TreeNode* root) {
        walk(root);
        return root;
    }
};""",
)

add(
    id=539, slug="minimum-time-difference", title="Minimum Time Difference", difficulty="Medium", world="arrays", tags=["array", "math", "string", "sorting"],
    story=dict(title="The Closest Two Alarms", text="Turn every clock time into minutes and sort. Neighbours are the closest candidates, plus the wrap-around from the last back to the first.",
               goal="Return the minimum minutes between any two times."),
    spec=dict(method="findMinDifference", ret="int", params=[["vector<string>&", "timePoints"]]),
    tests=[dict(args=[["23:59", "00:00"]], expected=1), dict(args=[["00:00", "23:59", "00:00"]], expected=0), dict(args=[["01:10", "12:30", "06:45"]], expected=335)],
    visualTest=2,
    scene=dict(theme="city", layers=[
        dict(kind="array", var="mins", label="minutes (sorted)", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int findMinDifference(vector<string>& timePoints) {
        vector<int> mins;
        for (auto& t : timePoints) mins.push_back(stoi(t.substr(0, 2)) * 60 + stoi(t.substr(3, 2)));
        sort(mins.begin(), mins.end());
        int best = 1440 - mins.back() + mins[0];
        for (int i = 1; i < (int)mins.size(); i++) best = min(best, mins[i] - mins[i - 1]);
        return best;
    }
};""",
)

add(
    id=541, slug="reverse-string-ii", title="Reverse String II", difficulty="Easy", world="two-pointers", tags=["two-pointers", "string"],
    story=dict(title="Flipping Every Other Block", text="Split the banner into blocks of 2k letters. In each block, two painters flip the first k letters.",
               goal="Reverse the first k characters of every 2k chunk."),
    spec=dict(method="reverseStr", ret="string", params=[["string", "s"], ["int", "k"]]),
    tests=[dict(args=["abcdefg", 2], expected="bacdfeg"), dict(args=["abcd", 2], expected="bacd")],
    scene=dict(theme="market", layers=[dict(kind="string", var="s", label="banner", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    string reverseStr(string s, int k) {
        for (int start = 0; start < (int)s.size(); start += 2 * k) {
            int l = start, r = min(start + k, (int)s.size()) - 1;
            while (l < r) {
                swap(s[l], s[r]);
                l++;
                r--;
            }
        }
        return s;
    }
};""",
)

add(
    id=551, slug="student-attendance-record-i", title="Student Attendance Record I", difficulty="Easy", world="arrays", tags=["string"],
    story=dict(title="The Attendance Sheet", text="Walk the sheet counting absences and the current run of lates. Two absences, or three lates in a row, lose the award.",
               goal="Return true if the student is eligible for the award."),
    spec=dict(method="checkRecord", ret="bool", params=[["string", "s"]]),
    tests=[dict(args=["PPALLP"], expected=True), dict(args=["PPALLL"], expected=False), dict(args=["APLPA"], expected=False)],
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="sheet", pointers=["i"]),
        dict(kind="values", vars=["absent", "late"]),
    ]),
    reference="""class Solution {
public:
    bool checkRecord(string s) {
        int absent = 0, late = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == 'A') absent++;
            late = s[i] == 'L' ? late + 1 : 0;
            if (absent >= 2 || late >= 3) return false;
        }
        return true;
    }
};""",
)

add(
    id=557, slug="reverse-words-in-a-string-iii", title="Reverse Words in a String III", difficulty="Easy", world="two-pointers", tags=["two-pointers", "string"],
    story=dict(title="Mirroring Each Word", text="Words stay in place but each one is read backwards: two painters flip each word between its spaces.",
               goal="Reverse the letters of every word."),
    spec=dict(method="reverseWords", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["Let's take LeetCode contest"], expected="s'teL ekat edoCteeL tsetnoc"), dict(args=["Mr Ding"], expected="rM gniD")],
    visualTest=1,
    scene=dict(theme="market", layers=[dict(kind="string", var="s", label="sign", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    string reverseWords(string s) {
        int n = s.size(), start = 0;
        while (start < n) {
            int end = start;
            while (end < n && s[end] != ' ') end++;
            int l = start, r = end - 1;
            while (l < r) swap(s[l++], s[r--]);
            start = end + 1;
        }
        return s;
    }
};""",
)

add(
    id=561, slug="array-partition", title="Array Partition", difficulty="Easy", world="greedy", tags=["array", "greedy", "sorting", "counting-sort"],
    story=dict(title="Pairing the Crates", text="Pair crates so the sum of each pair's lighter crate is as big as possible: sort, and pair neighbours.",
               goal="Return the max sum of min(a, b) over n pairs."),
    spec=dict(method="arrayPairSum", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 4, 3, 2]], expected=4), dict(args=[[6, 2, 6, 5, 1, 2]], expected=9)],
    visualTest=1,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates (sorted)", pointers=["i"]),
        dict(kind="values", vars=["sum"]),
    ]),
    reference="""class Solution {
public:
    int arrayPairSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int sum = 0;
        for (int i = 0; i < (int)nums.size(); i += 2) sum += nums[i];
        return sum;
    }
};""",
)

add(
    id=563, slug="binary-tree-tilt", title="Binary Tree Tilt", difficulty="Easy", world="trees", tags=["tree", "dfs"],
    story=dict(title="How Lopsided Is Each Branch?", text="Each fruit asks both branches for their total weight; the difference is its tilt, and it reports its own subtree's weight upward.",
               goal="Return the sum of every node's tilt."),
    spec=dict(method="findTilt", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3]], expected=1), dict(args=[[4, 2, 9, 3, 5, None, 7]], expected=15), dict(args=[[21, 7, 14, 1, 1, 2, 2, 3, 3]], expected=9)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["l", "r", "tilt"]),
    ]),
    reference="""class Solution {
public:
    int tilt = 0;
    int weigh(TreeNode* node) {
        if (!node) return 0;
        int l = weigh(node->left);
        int r = weigh(node->right);
        tilt += abs(l - r);
        return node->val + l + r;
    }
    int findTilt(TreeNode* root) {
        weigh(root);
        return tilt;
    }
};""",
)

add(
    id=566, slug="reshape-the-matrix", title="Reshape the Matrix", difficulty="Easy", world="arrays", tags=["array", "matrix", "simulation"],
    story=dict(title="Rearranging the Tile Wall", text="Read the tiles row by row as one long line, then lay them out again c to a row, as long as the tile counts match.",
               goal="Return the reshaped r x c matrix, or the original if impossible."),
    spec=dict(method="matrixReshape", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "mat"], ["int", "r"], ["int", "c"]]),
    tests=[dict(args=[[[1, 2], [3, 4]], 1, 4], expected=[[1, 2, 3, 4]]), dict(args=[[[1, 2], [3, 4]], 2, 4], expected=[[1, 2], [3, 4]]), dict(args=[[[1, 2, 3, 4, 5, 6]], 3, 2], expected=[[1, 2], [3, 4], [5, 6]])],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[
            dict(kind="grid", var="mat", palette="dp", label="old wall"),
            dict(kind="grid", var="res", palette="dp", label="new wall"),
        ]),
        dict(kind="values", vars=["k"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> matrixReshape(vector<vector<int>>& mat, int r, int c) {
        int m = mat.size(), n = mat[0].size();
        if (m * n != r * c) return mat;
        vector<vector<int>> res(r, vector<int>(c));
        for (int k = 0; k < m * n; k++) res[k / c][k % c] = mat[k / n][k % n];
        return res;
    }
};""",
)

add(
    id=575, slug="distribute-candies", title="Distribute Candies", difficulty="Easy", world="arrays", tags=["array", "hash-table"],
    story=dict(title="As Many Kinds as Possible", text="Alice may eat half the candies. She can taste at most that many kinds, and at most as many kinds as exist.",
               goal="Return the maximum number of different candy types she can eat."),
    spec=dict(method="distributeCandies", ret="int", params=[["vector<int>&", "candyType"]]),
    tests=[dict(args=[[1, 1, 2, 2, 3, 3]], expected=3), dict(args=[[1, 1, 2, 3]], expected=2), dict(args=[[6, 6, 6, 6]], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="candyType", label="candies"),
        dict(kind="set", var="kinds", label="kinds"),
    ]),
    reference="""class Solution {
public:
    int distributeCandies(vector<int>& candyType) {
        set<int> kinds(candyType.begin(), candyType.end());
        return min(kinds.size(), candyType.size() / 2);
    }
};""",
)

add(
    id=583, slug="delete-operation-for-two-strings", title="Delete Operation for Two Strings", difficulty="Medium", world="dp", tags=["string", "dynamic-programming"],
    story=dict(title="Trimming Two Scrolls to Match", text="Whatever they keep must be a common subsequence, so keep the longest one; every other letter is deleted.",
               goal="Return the minimum deletions to make both words equal."),
    spec=dict(method="minDistance", ret="int", params=[["string", "word1"], ["string", "word2"]]),
    tests=[dict(args=["sea", "eat"], expected=2), dict(args=["leetcode", "etco"], expected=4)],
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[dict(kind="string", var="word1", label="scroll 1"), dict(kind="string", var="word2", label="scroll 2")]),
        dict(kind="grid", var="dp", palette="dp", label="common subsequence table", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    int minDistance(string word1, string word2) {
        int n = word1.size(), m = word2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                dp[i][j] = word1[i - 1] == word2[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
        return n + m - 2 * dp[n][m];
    }
};""",
)

add(
    id=594, slug="longest-harmonious-subsequence", title="Longest Harmonious Subsequence", difficulty="Easy", world="arrays", tags=["array", "hash-table", "sliding-window", "sorting", "counting"],
    story=dict(title="Notes One Apart", text="A harmonious choir uses only two neighbouring pitches. Count every pitch; each pitch plus the one above it is a candidate choir.",
               goal="Return the longest subsequence whose max and min differ by exactly 1."),
    spec=dict(method="findLHS", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 3, 2, 2, 5, 2, 3, 7]], expected=5), dict(args=[[1, 2, 3, 4]], expected=2), dict(args=[[1, 1, 1, 1]], expected=0)],
    scene=dict(theme="castle", layers=[
        dict(kind="map", var="cnt", label="pitch counts"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int findLHS(vector<int>& nums) {
        map<int, int> cnt;
        for (int x : nums) cnt[x]++;
        int best = 0;
        for (auto& [v, c] : cnt) {
            if (cnt.count(v + 1)) best = max(best, c + cnt[v + 1]);
        }
        return best;
    }
};""",
)

add(
    id=606, slug="construct-string-from-binary-tree", title="Construct String from Binary Tree", difficulty="Medium", world="trees", tags=["string", "tree", "dfs"],
    story=dict(title="Writing the Orchard Down", text="Each fruit writes its value, then its branches in brackets. An empty left branch still needs () if there is a right branch; empty brackets are skipped otherwise.",
               goal="Return the preorder string with minimal parentheses."),
    spec=dict(method="tree2str", ret="string", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3, 4]], expected="1(2(4))(3)"), dict(args=[[1, 2, 3, None, 4]], expected="1(2()(4))(3)")],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["s"]),
    ]),
    reference="""class Solution {
public:
    string write(TreeNode* node) {
        if (!node) return "";
        string s = to_string(node->val);
        if (node->left || node->right) s += "(" + write(node->left) + ")";
        if (node->right) s += "(" + write(node->right) + ")";
        return s;
    }
    string tree2str(TreeNode* root) {
        return write(root);
    }
};""",
)

add(
    id=611, slug="valid-triangle-number", title="Valid Triangle Number", difficulty="Medium", world="two-pointers", tags=["array", "two-pointers", "binary-search", "greedy", "sorting"],
    story=dict(title="Sticks That Make a Triangle", text="Sticks are sorted. Fix the longest stick; two pointers find pairs whose sum beats it. If the outer pair works, every pair between does too.",
               goal="Return how many triplets can form a triangle."),
    spec=dict(method="triangleNumber", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 2, 3, 4]], expected=3), dict(args=[[4, 2, 3, 4]], expected=4)],
    scene=dict(theme="dock", layers=[
        dict(kind="bars", var="nums", label="sticks (sorted)", pointers=["l", "r", "k"]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int triangleNumber(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int count = 0;
        for (int k = nums.size() - 1; k >= 2; k--) {
            int l = 0, r = k - 1;
            while (l < r) {
                if (nums[l] + nums[r] > nums[k]) {
                    count += r - l;
                    r--;
                } else {
                    l++;
                }
            }
        }
        return count;
    }
};""",
)

add(
    id=621, slug="task-scheduler", title="Task Scheduler", difficulty="Medium", world="greedy", tags=["array", "hash-table", "greedy", "sorting", "heap", "counting"],
    story=dict(title="Spacing Out the Chores", text="The most frequent chore sets the frame: maxCount blocks of n+1 slots, with the last block holding only the chores that tie for most frequent.",
               goal="Return the fewest time units to finish all tasks with cooldown n."),
    spec=dict(method="leastInterval", ret="int", params=[["vector<char>&", "tasks"], ["int", "n"]]),
    tests=[dict(args=[["A", "A", "A", "B", "B", "B"], 2], expected=8), dict(args=[["A", "C", "A", "B", "D", "B"], 1], expected=6), dict(args=[["A", "A", "A", "B", "B", "B"], 3], expected=10)],
    scene=dict(theme="castle", layers=[
        dict(kind="map", var="cnt", label="chore counts"),
        dict(kind="values", vars=["most", "ties", "frame"]),
    ]),
    reference="""class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        map<char, int> cnt;
        for (char t : tasks) cnt[t]++;
        int most = 0, ties = 0;
        for (auto& [t, c] : cnt) most = max(most, c);
        for (auto& [t, c] : cnt) ties += c == most;
        int frame = (most - 1) * (n + 1) + ties;
        return max(frame, (int)tasks.size());
    }
};""",
)

add(
    id=628, slug="maximum-product-of-three-numbers", title="Maximum Product of Three Numbers", difficulty="Easy", world="arrays", tags=["array", "math", "sorting"],
    story=dict(title="The Best Three Crates", text="After sorting, the best product is either the three biggest crates, or the two most negative times the biggest.",
               goal="Return the maximum product of three numbers."),
    spec=dict(method="maximumProduct", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3]], expected=6), dict(args=[[1, 2, 3, 4]], expected=24), dict(args=[[-10, -10, 1, 3, 2]], expected=300)],
    visualTest=2,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates (sorted)"),
        dict(kind="values", vars=["a", "b"]),
    ]),
    reference="""class Solution {
public:
    int maximumProduct(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int a = nums[n - 1] * nums[n - 2] * nums[n - 3];
        int b = nums[0] * nums[1] * nums[n - 1];
        return max(a, b);
    }
};""",
)

add(
    id=645, slug="set-mismatch", title="Set Mismatch", difficulty="Easy", world="arrays", tags=["array", "hash-table", "bit-manipulation", "sorting"],
    story=dict(title="One Badge Copied, One Lost", text="Badges 1..n should each appear once. Tally them; the badge counted twice is the duplicate and the badge counted zero times is the missing one.",
               goal="Return [duplicate, missing]."),
    spec=dict(method="findErrorNums", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 2, 4]], expected=[2, 3]), dict(args=[[1, 1]], expected=[1, 2]), dict(args=[[3, 2, 3, 4, 6, 5]], expected=[3, 1])],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="nums", label="badges"),
        dict(kind="array", var="cnt", label="tally by badge", style="tiles", pointers=["v"]),
        dict(kind="values", vars=["dup", "miss"]),
    ]),
    reference="""class Solution {
public:
    vector<int> findErrorNums(vector<int>& nums) {
        int n = nums.size(), dup = 0, miss = 0;
        vector<int> cnt(n + 1, 0);
        for (int x : nums) cnt[x]++;
        for (int v = 1; v <= n; v++) {
            if (cnt[v] == 2) dup = v;
            if (cnt[v] == 0) miss = v;
        }
        return {dup, miss};
    }
};""",
)

add(
    id=647, slug="palindromic-substrings", title="Palindromic Substrings", difficulty="Medium", world="two-pointers", tags=["two-pointers", "string", "dynamic-programming"],
    story=dict(title="Counting Every Mirror", text="From every centre (each letter and each gap), two scouts walk outward while the letters match; every step out is one more palindrome.",
               goal="Return the number of palindromic substrings."),
    spec=dict(method="countSubstrings", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["abc"], expected=3), dict(args=["aaa"], expected=6), dict(args=["abba"], expected=6)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="letters", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int count = 0;
    void expand(string& s, int l, int r) {
        while (l >= 0 && r < (int)s.size() && s[l] == s[r]) {
            count++;
            l--;
            r++;
        }
    }
    int countSubstrings(string s) {
        for (int c = 0; c < (int)s.size(); c++) {
            expand(s, c, c);
            expand(s, c, c + 1);
        }
        return count;
    }
};""",
)
