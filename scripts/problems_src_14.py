"""Fourteenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=406, slug="queue-reconstruction-by-height", title="Queue Reconstruction by Height", difficulty="Medium", world="greedy",
    tags=["array", "binary-indexed-tree", "segment-tree", "sorting"],
    story=dict(title="Lining Up for the Photo", text="Each person says their height and how many taller-or-equal people stand in front. Seat the tallest first; each shorter person is inserted at exactly their count, since nobody shorter is in their way yet.",
               goal="Return the reconstructed queue."),
    spec=dict(method="reconstructQueue", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "people"]]),
    tests=[dict(args=[[[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]], expected=[[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]]),
           dict(args=[[[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]]], expected=[[4, 0], [5, 0], [2, 2], [3, 2], [1, 4], [6, 0]])],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="people", label="people (tallest first)", style="tiles", pointers=["i"]),
        dict(kind="array", var="line", label="the line", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> reconstructQueue(vector<vector<int>>& people) {
        sort(people.begin(), people.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[0] != b[0] ? a[0] > b[0] : a[1] < b[1];
        });
        vector<vector<int>> line;
        for (int i = 0; i < (int)people.size(); i++) line.insert(line.begin() + people[i][1], people[i]);
        return line;
    }
};""",
)

add(
    id=409, slug="longest-palindrome", title="Longest Palindrome", difficulty="Easy", world="greedy", tags=["hash-table", "string", "greedy"],
    story=dict(title="Building a Mirror Word", text="Every pair of matching tiles can go on both sides of the mirror. One leftover odd tile may sit in the middle.",
               goal="Return the length of the longest palindrome you can build."),
    spec=dict(method="longestPalindrome", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["abccccdd"], expected=7), dict(args=["a"], expected=1), dict(args=["Aa"], expected=1)],
    scene=dict(theme="lab", layers=[
        dict(kind="map", var="cnt", label="tiles"),
        dict(kind="values", vars=["len", "odd"]),
    ]),
    reference="""class Solution {
public:
    int longestPalindrome(string s) {
        map<char, int> cnt;
        for (char c : s) cnt[c]++;
        int len = 0;
        bool odd = false;
        for (auto& [c, n] : cnt) {
            len += n / 2 * 2;
            if (n % 2) odd = true;
        }
        return len + (odd ? 1 : 0);
    }
};""",
)

add(
    id=412, slug="fizz-buzz", title="Fizz Buzz", difficulty="Easy", world="arrays", tags=["math", "string", "simulation"],
    story=dict(title="The Counting Game", text="Count up to n out loud, but say Fizz for multiples of 3, Buzz for multiples of 5, and FizzBuzz for both.",
               goal="Return the list of what is said."),
    spec=dict(method="fizzBuzz", ret="vector<string>", params=[["int", "n"]]),
    tests=[dict(args=[3], expected=["1", "2", "Fizz"]), dict(args=[5], expected=["1", "2", "Fizz", "4", "Buzz"]),
           dict(args=[15], expected=["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"])],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="res", label="what is said", style="tiles"),
        dict(kind="values", vars=["i"]),
    ]),
    reference="""class Solution {
public:
    vector<string> fizzBuzz(int n) {
        vector<string> res;
        for (int i = 1; i <= n; i++) {
            if (i % 15 == 0) res.push_back("FizzBuzz");
            else if (i % 3 == 0) res.push_back("Fizz");
            else if (i % 5 == 0) res.push_back("Buzz");
            else res.push_back(to_string(i));
        }
        return res;
    }
};""",
)

add(
    id=413, slug="arithmetic-slices", title="Arithmetic Slices", difficulty="Medium", world="dp", tags=["array", "dynamic-programming", "sliding-window"],
    story=dict(title="Evenly Spaced Fence Posts", text="If a post continues the same step as the two before it, every evenly spaced run ending at the previous post extends by one, plus one new run of three.",
               goal="Return the number of arithmetic subarrays of length at least 3."),
    spec=dict(method="numberOfArithmeticSlices", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 4]], expected=3), dict(args=[[1]], expected=0), dict(args=[[1, 3, 5, 7, 9, 2, 4, 6]], expected=7)],
    visualTest=2,
    scene=dict(theme="farm", layers=[
        dict(kind="bars", var="nums", label="posts", pointers=["i"]),
        dict(kind="values", vars=["cur", "total"]),
    ]),
    reference="""class Solution {
public:
    int numberOfArithmeticSlices(vector<int>& nums) {
        int cur = 0, total = 0;
        for (int i = 2; i < (int)nums.size(); i++) {
            if (nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]) {
                cur++;
                total += cur;
            } else {
                cur = 0;
            }
        }
        return total;
    }
};""",
)

add(
    id=414, slug="third-maximum-number", title="Third Maximum Number", difficulty="Easy", world="arrays", tags=["array", "sorting"],
    story=dict(title="Bronze Medal", text="Three podium spots hold the top three distinct values seen so far; each new value slots in and pushes the others down.",
               goal="Return the third distinct maximum, or the maximum if there isn't one."),
    spec=dict(method="thirdMax", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[3, 2, 1]], expected=1), dict(args=[[1, 2]], expected=2), dict(args=[[2, 2, 3, 1]], expected=1)],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="scores", pointers=["i"]),
        dict(kind="values", vars=["a", "b", "c"]),
    ]),
    reference="""class Solution {
public:
    int thirdMax(vector<int>& nums) {
        long long a = LLONG_MIN, b = LLONG_MIN, c = LLONG_MIN;
        for (int i = 0; i < (int)nums.size(); i++) {
            long long x = nums[i];
            if (x == a || x == b || x == c) continue;
            if (x > a) {
                c = b;
                b = a;
                a = x;
            } else if (x > b) {
                c = b;
                b = x;
            } else if (x > c) {
                c = x;
            }
        }
        return c == LLONG_MIN ? a : c;
    }
};""",
)

add(
    id=415, slug="add-strings", title="Add Strings", difficulty="Easy", world="arrays", tags=["math", "string", "simulation"],
    story=dict(title="Adding on the Chalkboard", text="Add the two numbers column by column from the right, carrying a 1 whenever a column reaches 10.",
               goal="Return the sum of two numbers given as strings."),
    spec=dict(method="addStrings", ret="string", params=[["string", "num1"], ["string", "num2"]]),
    tests=[dict(args=["11", "123"], expected="134"), dict(args=["456", "77"], expected="533"), dict(args=["0", "0"], expected="0")],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="num1", label="num1", pointers=["i"]),
        dict(kind="string", var="num2", label="num2", pointers=["j"]),
        dict(kind="values", vars=["carry", "res"]),
    ]),
    reference="""class Solution {
public:
    string addStrings(string num1, string num2) {
        string res;
        int i = num1.size() - 1, j = num2.size() - 1, carry = 0;
        while (i >= 0 || j >= 0 || carry) {
            int sum = carry;
            if (i >= 0) sum += num1[i--] - '0';
            if (j >= 0) sum += num2[j--] - '0';
            res.push_back('0' + sum % 10);
            carry = sum / 10;
        }
        reverse(res.begin(), res.end());
        return res;
    }
};""",
)

add(
    id=417, slug="pacific-atlantic-water-flow", title="Pacific Atlantic Water Flow", difficulty="Medium", world="graphs",
    tags=["array", "dfs", "bfs", "matrix"],
    story=dict(title="Rain That Reaches Both Oceans", text="Instead of following rain downhill, climb uphill from each coast. Cells reached from the Pacific edge and from the Atlantic edge can drain to both.",
               goal="Return every cell that can flow to both oceans (any order)."),
    spec=dict(method="pacificAtlantic", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "heights"]]),
    compare="unordered",
    tests=[dict(args=[[[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]], expected=[[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]),
           dict(args=[[[1]]], expected=[[0, 0]])],
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="heights", palette="dp", label="island heights", pointers=[["r", "c"]]),
        dict(kind="row", children=[
            dict(kind="grid", var="pac", palette="bool", label="reaches Pacific"),
            dict(kind="grid", var="atl", palette="bool", label="reaches Atlantic"),
        ]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> pac, atl;
    void climb(vector<vector<int>>& heights, vector<vector<int>>& seen, int r, int c) {
        seen[r][c] = 1;
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nc < 0 || nr >= (int)heights.size() || nc >= (int)heights[0].size()) continue;
            if (seen[nr][nc] || heights[nr][nc] < heights[r][c]) continue;
            climb(heights, seen, nr, nc);
        }
    }
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int m = heights.size(), n = heights[0].size();
        pac.assign(m, vector<int>(n, 0));
        atl.assign(m, vector<int>(n, 0));
        for (int r = 0; r < m; r++) {
            climb(heights, pac, r, 0);
            climb(heights, atl, r, n - 1);
        }
        for (int c = 0; c < n; c++) {
            climb(heights, pac, 0, c);
            climb(heights, atl, m - 1, c);
        }
        vector<vector<int>> res;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                if (pac[r][c] && atl[r][c]) res.push_back({r, c});
        return res;
    }
};""",
)

add(
    id=419, slug="battleships-in-a-board", title="Battleships in a Board", difficulty="Medium", world="graphs", tags=["array", "dfs", "matrix"],
    story=dict(title="Counting the Fleet", text="Ships are straight lines of X. Count only each ship's top-left cell: an X with no X above it and none to its left.",
               goal="Return the number of battleships."),
    spec=dict(method="countBattleships", ret="int", params=[["vector<vector<char>>&", "board"]]),
    tests=[dict(args=[[["X", ".", ".", "X"], [".", ".", ".", "X"], [".", ".", ".", "X"]]], expected=2), dict(args=[[["."]]], expected=0)],
    scene=dict(theme="dock", layers=[
        dict(kind="grid", var="board", palette="board", label="sea", pointers=[["r", "c"]]),
        dict(kind="values", vars=["ships"]),
    ]),
    reference="""class Solution {
public:
    int countBattleships(vector<vector<char>>& board) {
        int ships = 0;
        for (int r = 0; r < (int)board.size(); r++) {
            for (int c = 0; c < (int)board[0].size(); c++) {
                if (board[r][c] != 'X') continue;
                if (r > 0 && board[r - 1][c] == 'X') continue;
                if (c > 0 && board[r][c - 1] == 'X') continue;
                ships++;
            }
        }
        return ships;
    }
};""",
)

add(
    id=434, slug="number-of-segments-in-a-string", title="Number of Segments in a String", difficulty="Easy", world="arrays", tags=["string"],
    story=dict(title="Counting Words on the Sign", text="A word starts wherever a non-space letter follows a space (or the very start).",
               goal="Return the number of space-separated segments."),
    spec=dict(method="countSegments", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["Hello, my name is John"], expected=5), dict(args=["Hello"], expected=1), dict(args=["   "], expected=0)],
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="sign", pointers=["i"]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int countSegments(string s) {
        int count = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] != ' ' && (i == 0 || s[i - 1] == ' ')) count++;
        }
        return count;
    }
};""",
)

add(
    id=437, slug="path-sum-iii", title="Path Sum III", difficulty="Medium", world="trees", tags=["tree", "dfs"],
    story=dict(title="Any Downward Vine", text="A vine can start at any fruit and go down. Carrying a running total, each fruit asks the logbook how many earlier totals were exactly target less than now.",
               goal="Return the number of downward paths that sum to targetSum."),
    spec=dict(method="pathSum", ret="int", params=[["TreeNode*", "root"], ["int", "targetSum"]]),
    tests=[dict(args=[[10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8], expected=3), dict(args=[[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22], expected=3)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="map", var="seen", label="running totals so far"),
        dict(kind="values", vars=["sum", "count"]),
    ]),
    reference="""class Solution {
public:
    map<long long, int> seen;
    int count = 0;
    void walk(TreeNode* node, long long sum, int target) {
        if (!node) return;
        sum += node->val;
        if (seen.count(sum - target)) count += seen[sum - target];
        seen[sum]++;
        walk(node->left, sum, target);
        walk(node->right, sum, target);
        seen[sum]--;
    }
    int pathSum(TreeNode* root, int targetSum) {
        seen[0] = 1;
        walk(root, 0, targetSum);
        return count;
    }
};""",
)

add(
    id=442, slug="find-all-duplicates-in-an-array", title="Find All Duplicates in an Array", difficulty="Medium", world="arrays", tags=["array", "hash-table"],
    story=dict(title="Flipping the Crate Marks", text="For each value v, flip the crate at slot v-1 to negative. If it's already negative, v was seen before.",
               goal="Return every value that appears twice (any order)."),
    spec=dict(method="findDuplicates", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    compare="unordered",
    tests=[dict(args=[[4, 3, 2, 7, 8, 2, 3, 1]], expected=[2, 3]), dict(args=[[1, 1, 2]], expected=[1]), dict(args=[[1]], expected=[])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates", pointers=["i", "j"]),
        dict(kind="array", var="res", label="seen twice", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        vector<int> res;
        for (int i = 0; i < (int)nums.size(); i++) {
            int j = abs(nums[i]) - 1;
            if (nums[j] < 0) res.push_back(j + 1);
            else nums[j] = -nums[j];
        }
        return res;
    }
};""",
)

add(
    id=445, slug="add-two-numbers-ii", title="Add Two Numbers II", difficulty="Medium", world="linked-list", tags=["linked-list", "math", "stack"],
    story=dict(title="Counting Trains, Biggest Digit First", text="This time digits run most significant first. Both trains are unloaded onto towers so the ones digits come off first, then the sum is built by coupling new cars at the front.",
               goal="Return the sum as a list, most significant digit first."),
    spec=dict(method="addTwoNumbers", ret="ListNode*", params=[["ListNode*", "l1"], ["ListNode*", "l2"]]),
    tests=[dict(args=[[7, 2, 4, 3], [5, 6, 4]], expected=[7, 8, 0, 7]), dict(args=[[2, 4, 3], [5, 6, 4]], expected=[8, 0, 7]), dict(args=[[0], [0]], expected=[0])],
    scene=dict(theme="farm", layers=[
        dict(kind="row", children=[dict(kind="stack", var="a", label="train 1 digits"), dict(kind="stack", var="b", label="train 2 digits")]),
        dict(kind="list", vars=["head"], label="sum train"),
        dict(kind="values", vars=["carry"]),
    ]),
    reference="""class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        stack<int> a, b;
        for (ListNode* p = l1; p; p = p->next) a.push(p->val);
        for (ListNode* p = l2; p; p = p->next) b.push(p->val);
        ListNode* head = nullptr;
        int carry = 0;
        while (!a.empty() || !b.empty() || carry) {
            int sum = carry;
            if (!a.empty()) {
                sum += a.top();
                a.pop();
            }
            if (!b.empty()) {
                sum += b.top();
                b.pop();
            }
            head = new ListNode(sum % 10, head);
            carry = sum / 10;
        }
        return head;
    }
};""",
)

add(
    id=447, slug="number-of-boomerangs", title="Number of Boomerangs", difficulty="Medium", world="arrays", tags=["array", "hash-table", "math"],
    story=dict(title="Equidistant Campfires", text="Stand at each campfire and count the others by squared distance. Any two at the same distance form a boomerang in both orders.",
               goal="Return the number of boomerangs (i, j, k)."),
    spec=dict(method="numberOfBoomerangs", ret="int", params=[["vector<vector<int>>&", "points"]]),
    tests=[dict(args=[[[0, 0], [1, 0], [2, 0]]], expected=2), dict(args=[[[1, 1], [2, 2], [3, 3]]], expected=2), dict(args=[[[1, 1]]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="points", label="campfires", style="tiles", pointers=["i"]),
        dict(kind="map", var="dist", label="others by distance²"),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int numberOfBoomerangs(vector<vector<int>>& points) {
        int total = 0;
        for (int i = 0; i < (int)points.size(); i++) {
            map<int, int> dist;
            for (int j = 0; j < (int)points.size(); j++) {
                int dx = points[i][0] - points[j][0], dy = points[i][1] - points[j][1];
                dist[dx * dx + dy * dy]++;
            }
            for (auto& [d, c] : dist) total += c * (c - 1);
        }
        return total;
    }
};""",
)

add(
    id=453, slug="minimum-moves-to-equal-array-elements", title="Minimum Moves to Equal Array Elements", difficulty="Medium", world="greedy", tags=["array", "math"],
    story=dict(title="Raising All but One", text="Adding one to every crate but one is the same as lowering that one crate. So the answer is how far every crate is above the smallest.",
               goal="Return the minimum number of moves to make all elements equal."),
    spec=dict(method="minMoves", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3]], expected=3), dict(args=[[1, 1, 1]], expected=0), dict(args=[[5, 6, 8, 8, 5]], expected=7)],
    visualTest=2,
    scene=dict(theme="dock", layers=[
        dict(kind="bars", var="nums", label="crates", pointers=["i"]),
        dict(kind="values", vars=["low", "moves"]),
    ]),
    reference="""class Solution {
public:
    int minMoves(vector<int>& nums) {
        int low = *min_element(nums.begin(), nums.end());
        long long moves = 0;
        for (int i = 0; i < (int)nums.size(); i++) moves += nums[i] - low;
        return moves;
    }
};""",
)

add(
    id=462, slug="minimum-moves-to-equal-array-elements-ii", title="Minimum Moves to Equal Array Elements II", difficulty="Medium",
    world="greedy", tags=["array", "math", "sorting"],
    story=dict(title="Meeting at the Middle Crate", text="Every crate can go up or down by one per move. Meeting at the median is cheapest: after sorting, pair the ends and add their gaps.",
               goal="Return the minimum number of moves."),
    spec=dict(method="minMoves2", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3]], expected=2), dict(args=[[1, 10, 2, 9]], expected=16)],
    visualTest=1,
    scene=dict(theme="dock", layers=[
        dict(kind="bars", var="nums", label="crates (sorted)", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["moves"]),
    ]),
    reference="""class Solution {
public:
    int minMoves2(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int l = 0, r = nums.size() - 1, moves = 0;
        while (l < r) {
            moves += nums[r] - nums[l];
            l++;
            r--;
        }
        return moves;
    }
};""",
)

add(
    id=454, slug="4sum-ii", title="4Sum II", difficulty="Medium", world="arrays", tags=["array", "hash-table"],
    story=dict(title="Meet in the Middle", text="Every sum of one from A and one from B goes into the lockers. For each pair from C and D, look up how many A+B sums would cancel it out.",
               goal="Return how many tuples sum to zero."),
    spec=dict(method="fourSumCount", ret="int", params=[["vector<int>&", "nums1"], ["vector<int>&", "nums2"], ["vector<int>&", "nums3"], ["vector<int>&", "nums4"]]),
    tests=[dict(args=[[1, 2], [-2, -1], [-1, 2], [0, 2]], expected=2), dict(args=[[0], [0], [0], [0]], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="map", var="ab", label="A+B sums", lookup=["need"]),
        dict(kind="values", vars=["need", "count"]),
    ]),
    reference="""class Solution {
public:
    int fourSumCount(vector<int>& nums1, vector<int>& nums2, vector<int>& nums3, vector<int>& nums4) {
        map<int, int> ab;
        for (int a : nums1)
            for (int b : nums2) ab[a + b]++;
        int count = 0;
        for (int c : nums3)
            for (int d : nums4) {
                int need = -(c + d);
                if (ab.count(need)) count += ab[need];
            }
        return count;
    }
};""",
)

add(
    id=455, slug="assign-cookies", title="Assign Cookies", difficulty="Easy", world="greedy", tags=["array", "two-pointers", "greedy", "sorting"],
    story=dict(title="Handing Out Cookies", text="Kids and cookies are both sorted. Walk the cookies smallest first; each cookie goes to the least greedy kid it can satisfy.",
               goal="Return the most kids you can make content."),
    spec=dict(method="findContentChildren", ret="int", params=[["vector<int>&", "g"], ["vector<int>&", "s"]]),
    tests=[dict(args=[[1, 2, 3], [1, 1]], expected=1), dict(args=[[1, 2], [1, 2, 3]], expected=2)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="g", label="kids' greed (sorted)", pointers=["kid"]),
        dict(kind="array", var="s", label="cookies (sorted)", pointers=["c"]),
    ]),
    reference="""class Solution {
public:
    int findContentChildren(vector<int>& g, vector<int>& s) {
        sort(g.begin(), g.end());
        sort(s.begin(), s.end());
        int kid = 0;
        for (int c = 0; c < (int)s.size() && kid < (int)g.size(); c++) {
            if (s[c] >= g[kid]) kid++;
        }
        return kid;
    }
};""",
)

add(
    id=459, slug="repeated-substring-pattern", title="Repeated Substring Pattern", difficulty="Easy", world="arrays", tags=["string", "string-matching"],
    story=dict(title="Is the Wallpaper a Repeating Tile?", text="Try every tile length that divides the wallpaper. If every letter matches the letter one tile earlier, the wallpaper is that tile repeated.",
               goal="Return true if s is a substring repeated at least twice."),
    spec=dict(method="repeatedSubstringPattern", ret="bool", params=[["string", "s"]]),
    tests=[dict(args=["abab"], expected=True), dict(args=["aba"], expected=False), dict(args=["abcabcabcabc"], expected=True)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="wallpaper", pointers=["i"]),
        dict(kind="values", vars=["len"]),
    ]),
    reference="""class Solution {
public:
    bool repeatedSubstringPattern(string s) {
        int n = s.size();
        for (int len = 1; len <= n / 2; len++) {
            if (n % len) continue;
            int i = len;
            while (i < n && s[i] == s[i - len]) i++;
            if (i == n) return true;
        }
        return false;
    }
};""",
)

add(
    id=485, slug="max-consecutive-ones", title="Max Consecutive Ones", difficulty="Easy", world="arrays", tags=["array"],
    story=dict(title="The Longest Lit Stretch", text="Walk the row of lamps counting the current lit run; a dark lamp resets it.",
               goal="Return the longest run of 1s."),
    spec=dict(method="findMaxConsecutiveOnes", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 1, 0, 1, 1, 1]], expected=3), dict(args=[[1, 0, 1, 1, 0, 1]], expected=2)],
    scene=dict(theme="space", layers=[
        dict(kind="array", var="nums", label="lamps", pointers=["i"]),
        dict(kind="values", vars=["run", "best"]),
    ]),
    reference="""class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {
        int run = 0, best = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            run = nums[i] ? run + 1 : 0;
            best = max(best, run);
        }
        return best;
    }
};""",
)

add(
    id=486, slug="predict-the-winner", title="Predict the Winner", difficulty="Medium", world="dp", tags=["array", "math", "dynamic-programming", "recursion", "game-theory"],
    story=dict(title="Taking Coins from Either End", text="Two players take coins from either end of a row. The table records, for every stretch i..j, how far ahead the player to move can finish.",
               goal="Return true if player 1 can win (ties count as a win)."),
    spec=dict(method="predictTheWinner", ret="bool", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 5, 2]], expected=False), dict(args=[[1, 5, 233, 7]], expected=True)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="coins", pointers=["i", "j"], window=["i", "j"]),
        dict(kind="grid", var="dp", palette="dp", label="lead for stretch i..j", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    bool predictTheWinner(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int i = 0; i < n; i++) dp[i][i] = nums[i];
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                dp[i][j] = max(nums[i] - dp[i + 1][j], nums[j] - dp[i][j - 1]);
            }
        }
        return dp[0][n - 1] >= 0;
    }
};""",
)

add(
    id=494, slug="target-sum", title="Target Sum", difficulty="Medium", world="dp", tags=["array", "dynamic-programming", "backtracking"],
    story=dict(title="Plus or Minus Every Coin", text="Each coin gets a + or a -. The lockers track, after each coin, how many sign choices reach every running total.",
               goal="Return how many sign assignments make the total equal target."),
    spec=dict(method="findTargetSumWays", ret="int", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[1, 1, 1, 1, 1], 3], expected=5), dict(args=[[1], 1], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="coins", pointers=["i"]),
        dict(kind="map", var="ways", label="ways to reach total"),
    ]),
    reference="""class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        map<int, int> ways;
        ways[0] = 1;
        for (int i = 0; i < (int)nums.size(); i++) {
            map<int, int> next;
            for (auto& [sum, c] : ways) {
                next[sum + nums[i]] += c;
                next[sum - nums[i]] += c;
            }
            ways = next;
        }
        return ways.count(target) ? ways[target] : 0;
    }
};""",
)

add(
    id=495, slug="teemo-attacking", title="Teemo Attacking", difficulty="Easy", world="intervals", tags=["array", "simulation"],
    story=dict(title="Overlapping Poison Clouds", text="Each attack poisons for duration seconds, but a new attack resets the timer. Add whichever is shorter: the full duration or the gap to the next attack.",
               goal="Return the total seconds poisoned."),
    spec=dict(method="findPoisonedDuration", ret="int", params=[["vector<int>&", "timeSeries"], ["int", "duration"]]),
    tests=[dict(args=[[1, 4], 2], expected=4), dict(args=[[1, 2], 2], expected=3), dict(args=[[1, 2, 3, 4, 5, 9], 3], expected=10)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="timeSeries", label="attack times", pointers=["i"]),
        dict(kind="values", vars=["duration", "total"]),
    ]),
    reference="""class Solution {
public:
    int findPoisonedDuration(vector<int>& timeSeries, int duration) {
        int total = 0;
        for (int i = 0; i < (int)timeSeries.size(); i++) {
            if (i + 1 < (int)timeSeries.size()) total += min(duration, timeSeries[i + 1] - timeSeries[i]);
            else total += duration;
        }
        return total;
    }
};""",
)

add(
    id=498, slug="diagonal-traverse", title="Diagonal Traverse", difficulty="Medium", world="arrays", tags=["array", "matrix", "simulation"],
    story=dict(title="The Zigzag Gardener", text="The gardener walks diagonals of the field, going up-right on even diagonals and down-left on odd ones, bouncing off the edges.",
               goal="Return all elements in diagonal zigzag order."),
    spec=dict(method="findDiagonalOrder", ret="vector<int>", params=[["vector<vector<int>>&", "mat"]]),
    tests=[dict(args=[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], expected=[1, 2, 4, 7, 5, 3, 6, 8, 9]), dict(args=[[[1, 2], [3, 4]]], expected=[1, 2, 3, 4])],
    scene=dict(theme="farm", layers=[
        dict(kind="grid", var="mat", palette="dp", label="field", pointers=[["r", "c"]]),
        dict(kind="array", var="res", label="visit order", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> findDiagonalOrder(vector<vector<int>>& mat) {
        int m = mat.size(), n = mat[0].size();
        vector<int> res;
        for (int d = 0; d < m + n - 1; d++) {
            if (d % 2 == 0) {
                int r = min(d, m - 1), c = d - r;
                while (r >= 0 && c < n) res.push_back(mat[r--][c++]);
            } else {
                int c = min(d, n - 1), r = d - c;
                while (c >= 0 && r < m) res.push_back(mat[r++][c--]);
            }
        }
        return res;
    }
};""",
)

add(
    id=500, slug="keyboard-row", title="Keyboard Row", difficulty="Easy", world="arrays", tags=["array", "hash-table", "string"],
    story=dict(title="One-Row Words", text="Each letter is labelled with its keyboard row. A word is kept if every letter has the same row label as its first.",
               goal="Return the words typeable using one keyboard row."),
    spec=dict(method="findWords", ret="vector<string>", params=[["vector<string>&", "words"]]),
    tests=[dict(args=[["Hello", "Alaska", "Dad", "Peace"]], expected=["Alaska", "Dad"]), dict(args=[["omk"]], expected=[]), dict(args=[["adsdf", "sfd"]], expected=["adsdf", "sfd"])],
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="words", label="words", style="tiles", pointers=["k"]),
        dict(kind="map", var="row", label="letter → row"),
        dict(kind="array", var="res", label="one-row words", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> findWords(vector<string>& words) {
        vector<string> rows = {"qwertyuiop", "asdfghjkl", "zxcvbnm"};
        map<char, int> row;
        for (int r = 0; r < 3; r++)
            for (char c : rows[r]) row[c] = r;
        vector<string> res;
        for (int k = 0; k < (int)words.size(); k++) {
            int want = row[tolower(words[k][0])];
            bool ok = true;
            for (char c : words[k]) {
                if (row[tolower(c)] != want) ok = false;
            }
            if (ok) res.push_back(words[k]);
        }
        return res;
    }
};""",
)

add(
    id=506, slug="relative-ranks", title="Relative Ranks", difficulty="Easy", world="heap", tags=["array", "sorting", "heap"],
    story=dict(title="Handing Out Medals", text="A pyramid holds every athlete by score, best on top. Pop them one by one: gold, silver, bronze, then numbers.",
               goal="Return each athlete's rank as a string."),
    spec=dict(method="findRelativeRanks", ret="vector<string>", params=[["vector<int>&", "score"]]),
    tests=[dict(args=[[5, 4, 3, 2, 1]], expected=["Gold Medal", "Silver Medal", "Bronze Medal", "4", "5"]),
           dict(args=[[10, 3, 8, 9, 4]], expected=["Gold Medal", "5", "Bronze Medal", "Silver Medal", "4"])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="heap", var="pq", label="athletes [score, index]"),
        dict(kind="array", var="res", label="ranks", style="tiles"),
        dict(kind="values", vars=["place"]),
    ]),
    reference="""class Solution {
public:
    vector<string> findRelativeRanks(vector<int>& score) {
        priority_queue<pair<int, int>> pq;
        for (int i = 0; i < (int)score.size(); i++) pq.push({score[i], i});
        vector<string> res(score.size());
        int place = 1;
        while (!pq.empty()) {
            int i = pq.top().second;
            pq.pop();
            if (place == 1) res[i] = "Gold Medal";
            else if (place == 2) res[i] = "Silver Medal";
            else if (place == 3) res[i] = "Bronze Medal";
            else res[i] = to_string(place);
            place++;
        }
        return res;
    }
};""",
)
