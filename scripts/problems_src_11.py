"""Eleventh batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=5, slug="longest-palindromic-substring", title="Longest Palindromic Substring", difficulty="Medium", world="two-pointers",
    tags=["two-pointers", "string", "dynamic-programming"],
    story=dict(
        title="The Widest Mirror",
        text="Stand on every letter (and between every pair of letters) and let two scouts walk outward while the "
             "letters they stand on match. The widest stretch they ever cover is the answer.",
        goal="Return the longest palindromic substring.",
    ),
    spec=dict(method="longestPalindrome", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["cbbd"], expected="bb"), dict(args=["a"], expected="a"), dict(args=["forgeeksskeegfor"], expected="geeksskeeg")],
    visualTest=0,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="letters", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["start", "best"]),
    ]),
    reference="""class Solution {
public:
    int start = 0, best = 0;
    void expand(string& s, int l, int r) {
        while (l >= 0 && r < (int)s.size() && s[l] == s[r]) {
            l--;
            r++;
        }
        if (r - l - 1 > best) {
            best = r - l - 1;
            start = l + 1;
        }
    }
    string longestPalindrome(string s) {
        for (int c = 0; c < (int)s.size(); c++) {
            expand(s, c, c);
            expand(s, c, c + 1);
        }
        return s.substr(start, best);
    }
};""",
    hints=["When two palindromes tie for longest, LeetCode accepts either; these tests have a unique answer."],
)

add(
    id=7, slug="reverse-integer", title="Reverse Integer", difficulty="Medium", world="bits", tags=["math"],
    story=dict(
        title="The Backwards Odometer",
        text="Peel the last digit off and push it onto the reversed number, checking before every push that the result "
             "still fits in 32 bits.",
        goal="Return x with its digits reversed, or 0 if that overflows.",
    ),
    spec=dict(method="reverse", ret="int", params=[["int", "x"]]),
    tests=[dict(args=[123], expected=321), dict(args=[-123], expected=-321), dict(args=[120], expected=21), dict(args=[1534236469], expected=0)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["x", "digit", "rev"])]),
    reference="""class Solution {
public:
    int reverse(int x) {
        int rev = 0;
        while (x != 0) {
            int digit = x % 10;
            x /= 10;
            if (rev > INT_MAX / 10 || rev < INT_MIN / 10) return 0;
            rev = rev * 10 + digit;
        }
        return rev;
    }
};""",
)

add(
    id=8, slug="string-to-integer-atoi", title="String to Integer (atoi)", difficulty="Medium", world="arrays", tags=["string"],
    story=dict(
        title="Reading the Meter",
        text="A meter reader skips leading spaces, notes an optional sign, then reads digits until something else "
             "appears, clamping the value to the 32-bit range.",
        goal="Convert the string to a 32-bit signed integer.",
    ),
    spec=dict(method="myAtoi", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["42"], expected=42), dict(args=["   -042"], expected=-42), dict(args=["1337c0d3"], expected=1337), dict(args=["0-1"], expected=0),
           dict(args=["-91283472332"], expected=-2147483648)],
    visualTest=1,
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="meter", pointers=["i"]),
        dict(kind="values", vars=["sign", "val"]),
    ]),
    reference="""class Solution {
public:
    int myAtoi(string s) {
        int i = 0, n = s.size(), sign = 1;
        while (i < n && s[i] == ' ') i++;
        if (i < n && (s[i] == '+' || s[i] == '-')) {
            if (s[i] == '-') sign = -1;
            i++;
        }
        long long val = 0;
        while (i < n && isdigit(s[i])) {
            val = val * 10 + (s[i] - '0');
            if (val * sign > INT_MAX) return INT_MAX;
            if (val * sign < INT_MIN) return INT_MIN;
            i++;
        }
        return val * sign;
    }
};""",
)

add(
    id=12, slug="integer-to-roman", title="Integer to Roman", difficulty="Medium", world="greedy", tags=["hash-table", "math", "string"],
    story=dict(
        title="Carving the Stone Tablet",
        text="The carver always uses the biggest Roman symbol that still fits (including pairs like CM and IV), carving it "
             "and subtracting its value until nothing is left.",
        goal="Return the Roman numeral for num.",
    ),
    spec=dict(method="intToRoman", ret="string", params=[["int", "num"]]),
    tests=[dict(args=[3749], expected="MMMDCCXLIX"), dict(args=[58], expected="LVIII"), dict(args=[1994], expected="MCMXCIV")],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="vals", label="symbol values", style="tiles", pointers=["k"]),
        dict(kind="values", vars=["num", "res"]),
    ]),
    reference="""class Solution {
public:
    string intToRoman(int num) {
        vector<int> vals = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        vector<string> syms = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
        string res;
        for (int k = 0; k < (int)vals.size(); k++) {
            while (num >= vals[k]) {
                res += syms[k];
                num -= vals[k];
            }
        }
        return res;
    }
};""",
)

add(
    id=18, slug="4sum", title="4Sum", difficulty="Medium", world="two-pointers", tags=["array", "two-pointers", "sorting"],
    story=dict(
        title="Four-Crate Balance",
        text="Two foremen stand on crates i and j of the sorted dock; two dockhands squeeze inward over the rest looking "
             "for a pair that balances all four to the target. Duplicates are skipped at every level.",
        goal="Return every unique quadruplet summing to target (any order).",
    ),
    spec=dict(method="fourSum", ret="vector<vector<int>>", params=[["vector<int>&", "nums"], ["int", "target"]]),
    compare="unordered-deep",
    tests=[dict(args=[[1, 0, -1, 0, -2, 2], 0], expected=[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]), dict(args=[[2, 2, 2, 2, 2], 8], expected=[[2, 2, 2, 2]])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="sorted crates", pointers=["i", "j", "l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["sum"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            for (int j = i + 1; j < n; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;
                int l = j + 1, r = n - 1;
                while (l < r) {
                    long long sum = (long long)nums[i] + nums[j] + nums[l] + nums[r];
                    if (sum < target) l++;
                    else if (sum > target) r--;
                    else {
                        res.push_back({nums[i], nums[j], nums[l], nums[r]});
                        while (l < r && nums[l] == nums[l + 1]) l++;
                        while (l < r && nums[r] == nums[r - 1]) r--;
                        l++;
                        r--;
                    }
                }
            }
        }
        return res;
    }
};""",
)

add(
    id=23, slug="merge-k-sorted-lists", title="Merge k Sorted Lists", difficulty="Hard", world="heap", tags=["linked-list", "divide-and-conquer", "heap", "merge-sort"],
    story=dict(
        title="The Great Rail Junction",
        text="k sorted trains wait at a junction. A pyramid holds the front car of every train, lightest on top; that car "
             "is coupled onto the new train and the next car of its train takes its place in the pyramid.",
        goal="Merge all the lists into one sorted list.",
    ),
    spec=dict(method="mergeKLists", ret="ListNode*", params=[["vector<ListNode*>&", "lists"]]),
    tests=[dict(args=[[[1, 4, 5], [1, 3, 4], [2, 6]]], expected=[1, 1, 2, 3, 4, 4, 5, 6]), dict(args=[[]], expected=[]), dict(args=[[[]]], expected=[])],
    scene=dict(theme="farm", layers=[
        dict(kind="heap", var="pq", label="front cars [value, track]"),
        dict(kind="list", vars=["tail"], label="merged train"),
    ]),
    reference="""class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        for (int t = 0; t < (int)lists.size(); t++) {
            if (lists[t]) pq.push({lists[t]->val, t});
        }
        ListNode* dummy = new ListNode(0);
        ListNode* tail = dummy;
        while (!pq.empty()) {
            int t = pq.top().second;
            pq.pop();
            tail->next = lists[t];
            tail = tail->next;
            lists[t] = lists[t]->next;
            if (lists[t]) pq.push({lists[t]->val, t});
        }
        return dummy->next;
    }
};""",
)

add(
    id=25, slug="reverse-nodes-in-k-group", title="Reverse Nodes in k-Group", difficulty="Hard", world="linked-list", tags=["linked-list", "recursion"],
    story=dict(
        title="Turning the Train k Cars at a Time",
        text="A brakeman checks that k cars are left ahead, then turns that group around by repeatedly pulling the next "
             "car to the front of the group, and moves on. A short tail group stays as it is.",
        goal="Reverse every group of k nodes and return the list.",
    ),
    spec=dict(method="reverseKGroup", ret="ListNode*", params=[["ListNode*", "head"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], 2], expected=[2, 1, 4, 3, 5]), dict(args=[[1, 2, 3, 4, 5], 3], expected=[3, 2, 1, 4, 5])],
    visualTest=1,
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "prev", "cur", "nxt", "check"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* prev = dummy;
        while (true) {
            ListNode* check = prev;
            for (int s = 0; s < k && check; s++) check = check->next;
            if (!check) break;
            ListNode* cur = prev->next;
            for (int s = 1; s < k; s++) {
                ListNode* nxt = cur->next;
                cur->next = nxt->next;
                nxt->next = prev->next;
                prev->next = nxt;
            }
            prev = cur;
        }
        return dummy->next;
    }
};""",
)

add(
    id=31, slug="next-permutation", title="Next Permutation", difficulty="Medium", world="two-pointers", tags=["array", "two-pointers"],
    story=dict(
        title="The Next Combination Lock Setting",
        text="From the right, find the first dial that is smaller than the one after it. Swap it with the smallest bigger "
             "dial to its right, then flip the tail into ascending order.",
        goal="Rearrange nums into the next lexicographic permutation, in place.",
    ),
    spec=dict(method="nextPermutation", ret="void", params=[["vector<int>&", "nums"]], output="param:0"),
    tests=[dict(args=[[1, 2, 3]], expected=[1, 3, 2]), dict(args=[[3, 2, 1]], expected=[1, 2, 3]), dict(args=[[1, 3, 5, 4, 2]], expected=[1, 4, 2, 3, 5])],
    visualTest=2,
    scene=dict(theme="lab", layers=[dict(kind="array", var="nums", label="dials", style="tiles", pointers=["i", "j", "l", "r"])]),
    reference="""class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        int n = nums.size(), i = n - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) i--;
        if (i >= 0) {
            int j = n - 1;
            while (nums[j] <= nums[i]) j--;
            swap(nums[i], nums[j]);
        }
        int l = i + 1, r = n - 1;
        while (l < r) {
            swap(nums[l], nums[r]);
            l++;
            r--;
        }
    }
};""",
)

add(
    id=32, slug="longest-valid-parentheses", title="Longest Valid Parentheses", difficulty="Hard", world="stack", tags=["string", "dynamic-programming", "stack"],
    story=dict(
        title="The Longest Sealed Corridor",
        text="The tower keeps the index of every unmatched bracket, with a floor marker at the bottom. Each closing "
             "bracket pops its partner; the gap down to whatever is now on top is a sealed stretch.",
        goal="Return the length of the longest valid parentheses substring.",
    ),
    spec=dict(method="longestValidParentheses", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["(()"], expected=2), dict(args=[")()())"], expected=4), dict(args=[""], expected=0), dict(args=["()(())"], expected=6)],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="brackets", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="st", label="unmatched (index)"), dict(kind="values", vars=["best"])]),
    ]),
    reference="""class Solution {
public:
    int longestValidParentheses(string s) {
        stack<int> st;
        st.push(-1);
        int best = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') {
                st.push(i);
            } else {
                st.pop();
                if (st.empty()) st.push(i);
                else best = max(best, i - st.top());
            }
        }
        return best;
    }
};""",
)

add(
    id=36, slug="valid-sudoku", title="Valid Sudoku", difficulty="Medium", world="arrays", tags=["array", "hash-table", "matrix"],
    story=dict(
        title="The Puzzle Inspector",
        text="An inspector walks every filled cell and files its digit under its row, its column and its 3x3 box. A digit "
             "already filed in any of the three breaks the rules.",
        goal="Return true if the filled cells follow Sudoku rules.",
    ),
    spec=dict(method="isValidSudoku", ret="bool", params=[["vector<vector<char>>&", "board"]]),
    tests=[
        dict(args=[[["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."], [".", "9", "8", ".", ".", ".", ".", "6", "."],
                    ["8", ".", ".", ".", "6", ".", ".", ".", "3"], ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                    [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"], [".", ".", ".", ".", "8", ".", ".", "7", "9"]]], expected=True),
        dict(args=[[["8", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."], [".", "9", "8", ".", ".", ".", ".", "6", "."],
                    ["8", ".", ".", ".", "6", ".", ".", ".", "3"], ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                    [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"], [".", ".", ".", ".", "8", ".", ".", "7", "9"]]], expected=False),
    ],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="grid", var="board", palette="board", label="puzzle", pointers=[["r", "c"]]),
        dict(kind="set", var="seen", label="filed", lookup=["rowKey"]),
    ]),
    reference="""class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        set<string> seen;
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                char d = board[r][c];
                if (d == '.') continue;
                string rowKey = string(1, d) + " in row " + to_string(r);
                string colKey = string(1, d) + " in col " + to_string(c);
                string boxKey = string(1, d) + " in box " + to_string(r / 3) + to_string(c / 3);
                if (seen.count(rowKey) || seen.count(colKey) || seen.count(boxKey)) return false;
                seen.insert(rowKey);
                seen.insert(colKey);
                seen.insert(boxKey);
            }
        }
        return true;
    }
};""",
)

add(
    id=38, slug="count-and-say", title="Count and Say", difficulty="Medium", world="arrays", tags=["string"],
    story=dict(
        title="The Town Crier's Chant",
        text="Each line of the chant describes the previous one aloud: \"one 1\", \"two 1s\", … The crier walks each line "
             "counting runs of the same digit.",
        goal="Return the n-th line of the count-and-say sequence.",
    ),
    spec=dict(method="countAndSay", ret="string", params=[["int", "n"]]),
    tests=[dict(args=[1], expected="1"), dict(args=[4], expected="1211"), dict(args=[6], expected="312211")],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="cur", label="current line", pointers=["i", "j"]),
        dict(kind="values", vars=["next"]),
    ]),
    reference="""class Solution {
public:
    string countAndSay(int n) {
        string cur = "1";
        for (int line = 1; line < n; line++) {
            string next;
            int i = 0;
            while (i < (int)cur.size()) {
                int j = i;
                while (j < (int)cur.size() && cur[j] == cur[i]) j++;
                next += to_string(j - i) + cur[i];
                i = j;
            }
            cur = next;
        }
        return cur;
    }
};""",
)

add(
    id=41, slug="first-missing-positive", title="First Missing Positive", difficulty="Hard", world="arrays", tags=["array", "hash-table"],
    story=dict(
        title="Every Crate to Its Own Slot",
        text="Crate v belongs in slot v-1. A worker keeps swapping each crate into its home slot until it's home, out of "
             "range, or a duplicate. The first slot holding the wrong crate gives the answer.",
        goal="Return the smallest missing positive integer, in O(n) time and O(1) extra space.",
    ),
    spec=dict(method="firstMissingPositive", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 0]], expected=3), dict(args=[[3, 4, -1, 1]], expected=2), dict(args=[[7, 8, 9, 11, 12]], expected=1)],
    visualTest=1,
    scene=dict(theme="dock", layers=[dict(kind="array", var="nums", label="slots", pointers=["i"])]),
    reference="""class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            while (nums[i] > 0 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) swap(nums[i], nums[nums[i] - 1]);
        }
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
};""",
)

add(
    id=43, slug="multiply-strings", title="Multiply Strings", difficulty="Medium", world="arrays", tags=["math", "string", "simulation"],
    story=dict(
        title="Long Multiplication on the Chalkboard",
        text="Every pair of digits is multiplied and dropped into its column on the chalkboard, carrying into the column "
             "to its left, exactly like long multiplication by hand.",
        goal="Return the product of two non-negative numbers given as strings.",
    ),
    spec=dict(method="multiply", ret="string", params=[["string", "num1"], ["string", "num2"]]),
    tests=[dict(args=["2", "3"], expected="6"), dict(args=["123", "456"], expected="56088"), dict(args=["0", "52"], expected="0")],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[dict(kind="string", var="num1", label="num1", pointers=["i"]), dict(kind="string", var="num2", label="num2", pointers=["j"])]),
        dict(kind="array", var="cols", label="chalkboard columns", style="tiles"),
    ]),
    reference="""class Solution {
public:
    string multiply(string num1, string num2) {
        int n = num1.size(), m = num2.size();
        vector<int> cols(n + m, 0);
        for (int i = n - 1; i >= 0; i--) {
            for (int j = m - 1; j >= 0; j--) {
                int sum = (num1[i] - '0') * (num2[j] - '0') + cols[i + j + 1];
                cols[i + j + 1] = sum % 10;
                cols[i + j] += sum / 10;
            }
        }
        string res;
        for (int d : cols) {
            if (!(res.empty() && d == 0)) res.push_back('0' + d);
        }
        return res.empty() ? "0" : res;
    }
};""",
)

add(
    id=47, slug="permutations-ii", title="Permutations II", difficulty="Medium", world="backtracking", tags=["array", "backtracking", "sorting"],
    story=dict(
        title="Seating Identical Twins",
        text="Some guests are identical twins. Sorted side by side, a twin is only seated if the twin before them is "
             "already seated, so no seating plan is counted twice.",
        goal="Return every unique ordering (any order).",
    ),
    spec=dict(method="permuteUnique", ret="vector<vector<int>>", params=[["vector<int>&", "nums"]]),
    compare="unordered",
    tests=[dict(args=[[1, 1, 2]], expected=[[1, 1, 2], [1, 2, 1], [2, 1, 1]]), dict(args=[[1, 2, 3]], expected=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="guests (sorted)", pointers=["i"]),
        dict(kind="array", var="used", label="seated?", style="tiles"),
        dict(kind="array", var="path", label="chairs", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    vector<bool> used;
    void go(vector<int>& nums) {
        if (path.size() == nums.size()) {
            res.push_back(path);
            return;
        }
        for (int i = 0; i < (int)nums.size(); i++) {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
            used[i] = true;
            path.push_back(nums[i]);
            go(nums);
            path.pop_back();
            used[i] = false;
        }
    }
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        used.assign(nums.size(), false);
        go(nums);
        return res;
    }
};""",
)

add(
    id=50, slug="powx-n", title="Pow(x, n)", difficulty="Medium", world="bits", tags=["math", "recursion"],
    story=dict(
        title="Squaring Up the Tower",
        text="Read the exponent's lamps from the right. Each step the base is squared; whenever the current lamp is lit, "
             "the base so far is multiplied into the answer.",
        goal="Return x raised to the power n.",
    ),
    spec=dict(method="myPow", ret="double", params=[["double", "x"], ["int", "n"]]),
    compare="float",
    tests=[dict(args=[2.0, 10], expected=1024.0), dict(args=[2.1, 3], expected=9.261), dict(args=[2.0, -2], expected=0.25)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["base", "e", "res"])]),
    reference="""class Solution {
public:
    double myPow(double x, int n) {
        long long e = n;
        double base = x, res = 1.0;
        if (e < 0) {
            base = 1 / base;
            e = -e;
        }
        while (e > 0) {
            if (e & 1) res *= base;
            base *= base;
            e >>= 1;
        }
        return res;
    }
};""",
)

add(
    id=59, slug="spiral-matrix-ii", title="Spiral Matrix II", difficulty="Medium", world="arrays", tags=["array", "matrix", "simulation"],
    story=dict(
        title="The Snail Plants a Garden",
        text="This time the snail plants numbered seeds as it spirals in: along the top, down the right, back along the "
             "bottom, up the left, then the walls close in.",
        goal="Return an n x n matrix filled 1..n² in spiral order.",
    ),
    spec=dict(method="generateMatrix", ret="vector<vector<int>>", params=[["int", "n"]]),
    tests=[dict(args=[3], expected=[[1, 2, 3], [8, 9, 4], [7, 6, 5]]), dict(args=[1], expected=[[1]])],
    scene=dict(theme="farm", layers=[
        dict(kind="grid", var="m", palette="dp", label="garden", pointers=[["r", "c"]]),
        dict(kind="values", vars=["k", "top", "bottom", "left", "right"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> m(n, vector<int>(n, 0));
        int top = 0, bottom = n - 1, left = 0, right = n - 1, k = 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) m[top][c] = k++;
            top++;
            for (int r = top; r <= bottom; r++) m[r][right] = k++;
            right--;
            for (int c = right; c >= left && top <= bottom; c--) m[bottom][c] = k++;
            bottom--;
            for (int r = bottom; r >= top && left <= right; r--) m[r][left] = k++;
            left++;
        }
        return m;
    }
};""",
)

add(
    id=60, slug="permutation-sequence", title="Permutation Sequence", difficulty="Hard", world="backtracking", tags=["math", "recursion"],
    story=dict(
        title="Skipping Whole Blocks of Orders",
        text="Each choice of first digit owns (n-1)! orderings. Divide k by that block size to pick the digit, remove it "
             "from the pool, and repeat on the remainder.",
        goal="Return the k-th permutation of 1..n.",
    ),
    spec=dict(method="getPermutation", ret="string", params=[["int", "n"], ["int", "k"]]),
    tests=[dict(args=[3, 3], expected="213"), dict(args=[4, 9], expected="2314"), dict(args=[3, 1], expected="123")],
    visualTest=1,
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="pool", label="digits left", style="tiles", pointers=["idx"]),
        dict(kind="values", vars=["k", "block", "res"]),
    ]),
    reference="""class Solution {
public:
    string getPermutation(int n, int k) {
        vector<int> pool;
        int block = 1;
        for (int d = 1; d <= n; d++) {
            pool.push_back(d);
            block *= d;
        }
        k--;
        string res;
        for (int left = n; left > 0; left--) {
            block /= left;
            int idx = k / block;
            k %= block;
            res += to_string(pool[idx]);
            pool.erase(pool.begin() + idx);
        }
        return res;
    }
};""",
)

add(
    id=63, slug="unique-paths-ii", title="Unique Paths II", difficulty="Medium", world="dp", tags=["array", "dynamic-programming", "matrix"],
    story=dict(
        title="The Robot Field with Rocks",
        text="Rocks (1) block some plots. Each open plot counts the routes into it from above and from the left; a rock "
             "plot counts zero.",
        goal="Return the number of routes to the bottom-right corner.",
    ),
    spec=dict(method="uniquePathsWithObstacles", ret="int", params=[["vector<vector<int>>&", "obstacleGrid"]]),
    tests=[dict(args=[[[0, 0, 0], [0, 1, 0], [0, 0, 0]]], expected=2), dict(args=[[[0, 1], [0, 0]]], expected=1), dict(args=[[[1]]], expected=0)],
    scene=dict(theme="farm", layers=[
        dict(kind="row", children=[
            dict(kind="grid", var="obstacleGrid", palette="maze", label="rocks"),
            dict(kind="grid", var="dp", palette="dp", label="routes", pointers=[["i", "j"]]),
        ]),
    ]),
    reference="""class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
        int m = obstacleGrid.size(), n = obstacleGrid[0].size();
        vector<vector<long long>> dp(m, vector<long long>(n, 0));
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (obstacleGrid[i][j]) continue;
                if (i == 0 && j == 0) dp[i][j] = 1;
                else dp[i][j] = (i > 0 ? dp[i - 1][j] : 0) + (j > 0 ? dp[i][j - 1] : 0);
            }
        }
        return dp[m - 1][n - 1];
    }
};""",
)

add(
    id=71, slug="simplify-path", title="Simplify Path", difficulty="Medium", world="stack", tags=["string", "stack"],
    story=dict(
        title="Walking the Folder Tower",
        text="A path is read one folder name at a time. A name is stacked on the tower, .. knocks the top folder off, and "
             ". or empty names are ignored.",
        goal="Return the simplified canonical path.",
    ),
    spec=dict(method="simplifyPath", ret="string", params=[["string", "path"]]),
    tests=[dict(args=["/home/"], expected="/home"), dict(args=["/home//foo/"], expected="/home/foo"), dict(args=["/home/user/Documents/../Pictures"], expected="/home/user/Pictures"),
           dict(args=["/../"], expected="/"), dict(args=["/.../a/../b/c/../d/./"], expected="/.../b/d")],
    visualTest=4,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="path", label="path", pointers=["i"]),
        dict(kind="values", vars=["name"]),
        dict(kind="stack", var="st", label="folder tower"),
    ]),
    reference="""class Solution {
public:
    string simplifyPath(string path) {
        vector<string> st;
        int i = 0, n = path.size();
        while (i < n) {
            while (i < n && path[i] == '/') i++;
            string name;
            while (i < n && path[i] != '/') name.push_back(path[i++]);
            if (name.empty() || name == ".") continue;
            if (name == "..") {
                if (!st.empty()) st.pop_back();
            } else {
                st.push_back(name);
            }
        }
        string res;
        for (auto& s : st) res += "/" + s;
        return res.empty() ? "/" : res;
    }
};""",
)

add(
    id=80, slug="remove-duplicates-from-sorted-array-ii", title="Remove Duplicates from Sorted Array II", difficulty="Medium",
    world="two-pointers", tags=["array", "two-pointers"],
    story=dict(
        title="At Most Two of Each Sticker",
        text="The album may hold each sticker at most twice. The keeper accepts a sticker only if it differs from the one "
             "two places back in the album.",
        goal="Keep at most two copies of each value at the front and return the new length.",
    ),
    spec=dict(method="removeDuplicates", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 1, 1, 2, 2, 3]], expected=5), dict(args=[[0, 0, 1, 1, 1, 1, 2, 3, 3]], expected=7)],
    visualTest=1,
    scene=dict(theme="dock", layers=[dict(kind="array", var="nums", label="album", pointers=["k", "i"])]),
    reference="""class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int k = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (k < 2 || nums[i] != nums[k - 2]) {
                nums[k] = nums[i];
                k++;
            }
        }
        return k;
    }
};""",
)

add(
    id=81, slug="search-in-rotated-sorted-array-ii", title="Search in Rotated Sorted Array II", difficulty="Medium",
    world="binary-search", tags=["array", "binary-search"],
    story=dict(
        title="The Turned Corridor with Twins",
        text="The rotated corridor may now have repeated chests. When the ends and the middle all look the same, the guard "
             "can't tell which half is sorted, so they shrink both ends by one and try again.",
        goal="Return true if target is in the array.",
    ),
    spec=dict(method="search", ret="bool", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[2, 5, 6, 0, 0, 1, 2], 0], expected=True), dict(args=[[2, 5, 6, 0, 0, 1, 2], 3], expected=False), dict(args=[[1, 0, 1, 1, 1], 0], expected=True)],
    visualTest=2,
    scene=dict(theme="cave", layers=[dict(kind="array", var="nums", label="chests", pointers=["lo", "mid", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    bool search(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size() - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] == target) return true;
            if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) {
                lo++;
                hi--;
            } else if (nums[lo] <= nums[mid]) {
                if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
                else lo = mid + 1;
            } else {
                if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
                else hi = mid - 1;
            }
        }
        return false;
    }
};""",
)

add(
    id=82, slug="remove-duplicates-from-sorted-list-ii", title="Remove Duplicates from Sorted List II", difficulty="Medium",
    world="linked-list", tags=["linked-list", "two-pointers"],
    story=dict(
        title="Dropping Every Twin Car",
        text="Any value that appears more than once must vanish entirely. A worker behind the dummy engine looks ahead; "
             "when the next cars repeat, the whole run is skipped.",
        goal="Keep only values that appear exactly once.",
    ),
    spec=dict(method="deleteDuplicates", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 2, 3, 3, 4, 4, 5]], expected=[1, 2, 5]), dict(args=[[1, 1, 1, 2, 3]], expected=[2, 3])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "prev", "cur"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* prev = dummy;
        while (prev->next) {
            ListNode* cur = prev->next;
            if (cur->next && cur->next->val == cur->val) {
                int v = cur->val;
                while (cur && cur->val == v) cur = cur->next;
                prev->next = cur;
            } else {
                prev = cur;
            }
        }
        return dummy->next;
    }
};""",
)

add(
    id=91, slug="decode-ways", title="Decode Ways", difficulty="Medium", world="dp", tags=["string", "dynamic-programming"],
    story=dict(
        title="Reading the Coded Message",
        text="Letters were sent as numbers 1–26. The ledger counts the ways to read each prefix: a valid single digit "
             "extends the previous count, and a valid two-digit code extends the count from two back.",
        goal="Return how many ways the digits can be decoded.",
    ),
    spec=dict(method="numDecodings", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["12"], expected=2), dict(args=["226"], expected=3), dict(args=["06"], expected=0), dict(args=["11106"], expected=2)],
    visualTest=3,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="digits", pointers=["i"]),
        dict(kind="array", var="dp", label="ways per prefix", style="tiles", pointers=["i"]),
    ]),
    reference="""class Solution {
public:
    int numDecodings(string s) {
        int n = s.size();
        vector<int> dp(n + 1, 0);
        dp[0] = 1;
        for (int i = 1; i <= n; i++) {
            if (s[i - 1] != '0') dp[i] += dp[i - 1];
            if (i >= 2) {
                int two = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
                if (two >= 10 && two <= 26) dp[i] += dp[i - 2];
            }
        }
        return dp[n];
    }
};""",
)

add(
    id=93, slug="restore-ip-addresses", title="Restore IP Addresses", difficulty="Medium", world="backtracking", tags=["string", "backtracking"],
    story=dict(
        title="Cutting the Address Ribbon",
        text="A ribbon of digits must be cut into four parts, each 0–255 without leading zeros. At every door the cutter "
             "tries a 1-, 2- or 3-digit piece, goes deeper, and tapes it back.",
        goal="Return every valid IP address (any order).",
    ),
    spec=dict(method="restoreIpAddresses", ret="vector<string>", params=[["string", "s"]]),
    compare="unordered",
    tests=[dict(args=["25525511135"], expected=["255.255.11.135", "255.255.111.35"]), dict(args=["0000"], expected=["0.0.0.0"]),
           dict(args=["101023"], expected=["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"])],
    visualTest=2,
    scene=dict(theme="cave", layers=[
        dict(kind="string", var="s", label="digits", pointers=["start"]),
        dict(kind="array", var="parts", label="pieces", style="tiles"),
        dict(kind="array", var="res", label="addresses", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> res;
    vector<string> parts;
    void go(string& s, int start) {
        if (parts.size() == 4) {
            if (start == (int)s.size()) res.push_back(parts[0] + "." + parts[1] + "." + parts[2] + "." + parts[3]);
            return;
        }
        for (int len = 1; len <= 3 && start + len <= (int)s.size(); len++) {
            string piece = s.substr(start, len);
            if ((piece.size() > 1 && piece[0] == '0') || stoi(piece) > 255) continue;
            parts.push_back(piece);
            go(s, start + len);
            parts.pop_back();
        }
    }
    vector<string> restoreIpAddresses(string s) {
        go(s, 0);
        return res;
    }
};""",
)

add(
    id=97, slug="interleaving-string", title="Interleaving String", difficulty="Medium", world="dp", tags=["string", "dynamic-programming"],
    story=dict(
        title="Braiding Two Ropes",
        text="Can rope s3 be braided from s1 and s2 without reordering either? Each grid cell asks whether the first i "
             "strands of s1 and j of s2 braid into the first i+j of s3, by taking the next strand from either rope.",
        goal="Return true if s3 is an interleaving of s1 and s2.",
    ),
    spec=dict(method="isInterleave", ret="bool", params=[["string", "s1"], ["string", "s2"], ["string", "s3"]]),
    tests=[dict(args=["aabcc", "dbbca", "aadbbcbcac"], expected=True), dict(args=["aabcc", "dbbca", "aadbbbaccc"], expected=False), dict(args=["", "", ""], expected=True)],
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[dict(kind="string", var="s1", label="rope 1"), dict(kind="string", var="s2", label="rope 2")]),
        dict(kind="grid", var="dp", palette="bool", label="can braid?", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int n = s1.size(), m = s2.size();
        if (n + m != (int)s3.size()) return false;
        vector<vector<bool>> dp(n + 1, vector<bool>(m + 1, false));
        dp[0][0] = true;
        for (int i = 0; i <= n; i++) {
            for (int j = 0; j <= m; j++) {
                if (i > 0 && s1[i - 1] == s3[i + j - 1] && dp[i - 1][j]) dp[i][j] = true;
                if (j > 0 && s2[j - 1] == s3[i + j - 1] && dp[i][j - 1]) dp[i][j] = true;
            }
        }
        return dp[n][m];
    }
};""",
)
