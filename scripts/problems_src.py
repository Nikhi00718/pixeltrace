"""Hand-crafted situation files. Run build_problems.py to compile references and emit JSON.

Each entry: story + scene mapping + tests + C++ reference. Expected outputs can be
omitted; the build computes them from the reference (and checks any that are given).
"""

P = []


def add(**kw):
    P.append(kw)


# ============================================================ arrays / hashing

add(
    id=1, slug="two-sum", title="Two Sum", difficulty="Easy", world="arrays", tags=["array", "hash-table"],
    story=dict(
        title="The Exact Change Market",
        text="A shopper walks down a row of price crates. Each time they pick up a crate, they ask the locker wall: "
             "\"Has anyone stored the price I still need?\" Lockers are labelled by price and hold the crate's index.",
        goal="Return the indices of the two crates whose prices add up to the target.",
    ),
    legend=[dict(sprite="crates", meaning="nums"), dict(sprite="lockers", meaning="seen: price → index"),
            dict(sprite="i", meaning="the shopper")],
    spec=dict(method="twoSum", ret="vector<int>", params=[["vector<int>&", "nums"], ["int", "target"]]),
    compare="unordered",
    tests=[
        dict(args=[[2, 7, 11, 15], 9], expected=[0, 1]),
        dict(args=[[3, 2, 4], 6], expected=[1, 2]),
        dict(args=[[3, 3], 6], expected=[0, 1]),
        dict(args=[[5, 1, 8, 3, 9, 4], 12], expected=[3, 4]),
    ],
    visualTest=3,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="price crates", pointers=["i"]),
        dict(kind="map", var="seen", label="locker wall", lookup=["need"]),
        dict(kind="values", vars=["target", "need"]),
    ]),
    reference="""class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;
        for (int i = 0; i < (int)nums.size(); i++) {
            int need = target - nums[i];
            if (seen.count(need)) return {seen[need], i};
            seen[nums[i]] = i;
        }
        return {};
    }
};""",
    hints=["For each number, the partner you need is target - nums[i].", "Store what you've seen in a hash map."],
)

add(
    id=217, slug="contains-duplicate", title="Contains Duplicate", difficulty="Easy", world="arrays",
    tags=["array", "hash-table"],
    story=dict(
        title="The Coat Check",
        text="Guests hand their tickets to a coat-check clerk. The clerk keeps one locker per ticket number. "
             "If a guest shows up with a number that already has a locker, something is off.",
        goal="Return true if any ticket number appears twice.",
    ),
    spec=dict(method="containsDuplicate", ret="bool", params=[["vector<int>&", "nums"]]),
    tests=[
        dict(args=[[1, 2, 3, 1]], expected=True),
        dict(args=[[1, 2, 3, 4]], expected=False),
        dict(args=[[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]], expected=True),
    ],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="tickets", pointers=["i"]),
        dict(kind="set", var="seen", label="lockers"),
    ]),
    reference="""class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (seen.count(nums[i])) return true;
            seen.insert(nums[i]);
        }
        return false;
    }
};""",
)

add(
    id=242, slug="valid-anagram", title="Valid Anagram", difficulty="Easy", world="arrays",
    tags=["string", "hash-table", "counting"],
    story=dict(
        title="The Letter Tile Swap",
        text="Two scrabble racks arrive at the market. A clerk counts every tile from the first rack into lockers, "
             "then removes one count per tile from the second rack.",
        goal="Return true if both racks hold exactly the same tiles.",
    ),
    spec=dict(method="isAnagram", ret="bool", params=[["string", "s"], ["string", "t"]]),
    tests=[
        dict(args=["anagram", "nagaram"], expected=True),
        dict(args=["rat", "car"], expected=False),
        dict(args=["ab", "a"], expected=False),
    ],
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="rack s", pointers=["i"]),
        dict(kind="string", var="t", label="rack t", pointers=["i"]),
        dict(kind="map", var="cnt", label="tile counts"),
    ]),
    reference="""class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.size() != t.size()) return false;
        map<char, int> cnt;
        for (int i = 0; i < (int)s.size(); i++) cnt[s[i]]++;
        for (int i = 0; i < (int)t.size(); i++) {
            if (--cnt[t[i]] < 0) return false;
        }
        return true;
    }
};""",
)

add(
    id=49, slug="group-anagrams", title="Group Anagrams", difficulty="Medium", world="arrays",
    tags=["string", "hash-table", "sorting"],
    story=dict(
        title="The Post Office Sorter",
        text="Letters arrive with scrambled words. The sorter alphabetises each word to get its key, then drops the "
             "letter into the locker with that key. Words that are anagrams land in the same locker.",
        goal="Return the groups of anagrams (any order).",
    ),
    spec=dict(method="groupAnagrams", ret="vector<vector<string>>", params=[["vector<string>&", "strs"]]),
    compare="unordered-deep",
    tests=[
        dict(args=[["eat", "tea", "tan", "ate", "nat", "bat"]]),
        dict(args=[[""]]),
        dict(args=[["a"]]),
    ],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="strs", label="mail bag", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["key"]),
        dict(kind="map", var="groups", label="sorting lockers", lookup=["key"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        map<string, vector<string>> groups;
        for (int i = 0; i < (int)strs.size(); i++) {
            string key = strs[i];
            sort(key.begin(), key.end());
            groups[key].push_back(strs[i]);
        }
        vector<vector<string>> res;
        for (auto& [k, v] : groups) res.push_back(v);
        return res;
    }
};""",
)

add(
    id=238, slug="product-of-array-except-self", title="Product of Array Except Self", difficulty="Medium",
    world="arrays", tags=["array", "prefix-sum"],
    story=dict(
        title="Two Passes Down the Dock",
        text="A worker walks the dock left to right writing the product of every crate behind them, then walks back "
             "right to left multiplying in the product of every crate ahead.",
        goal="For each crate, the product of all the other crates, without using division.",
    ),
    spec=dict(method="productExceptSelf", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 4]], expected=[24, 12, 8, 6]), dict(args=[[-1, 1, 0, -3, 3]], expected=[0, 0, 9, 0, 0])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates", pointers=["i"]),
        dict(kind="array", var="res", label="answer board", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["prefix", "suffix"]),
    ]),
    reference="""class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 1);
        int prefix = 1;
        for (int i = 0; i < n; i++) {
            res[i] = prefix;
            prefix *= nums[i];
        }
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            res[i] *= suffix;
            suffix *= nums[i];
        }
        return res;
    }
};""",
)

add(
    id=53, slug="maximum-subarray", title="Maximum Subarray", difficulty="Medium", world="arrays",
    tags=["array", "dynamic-programming", "kadane"],
    story=dict(
        title="The Treasure Walk",
        text="An explorer walks along chests of gold and debt. They carry a running purse; whenever the purse goes "
             "negative it is better to drop it and start fresh at the next chest.",
        goal="Return the largest sum of any contiguous run of chests.",
    ),
    spec=dict(method="maxSubArray", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[-2, 1, -3, 4, -1, 2, 1, -5, 4]], expected=6), dict(args=[[1]], expected=1),
           dict(args=[[5, 4, -1, 7, 8]], expected=23), dict(args=[[-3, -1, -2]], expected=-1)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="chests", pointers=["i"]),
        dict(kind="values", vars=["cur", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int cur = 0, best = nums[0];
        for (int i = 0; i < (int)nums.size(); i++) {
            cur = max(nums[i], cur + nums[i]);
            best = max(best, cur);
        }
        return best;
    }
};""",
)

add(
    id=121, slug="best-time-to-buy-and-sell-stock", title="Best Time to Buy and Sell Stock", difficulty="Easy",
    world="arrays", tags=["array", "greedy"],
    story=dict(
        title="The Skyline Trader",
        text="Each tower is a day's price. A trader walks the skyline remembering the lowest tower so far and checking "
             "how much they would earn selling at today's tower.",
        goal="Return the best profit from one buy followed by one sell (or 0).",
    ),
    spec=dict(method="maxProfit", ret="int", params=[["vector<int>&", "prices"]]),
    tests=[dict(args=[[7, 1, 5, 3, 6, 4]], expected=5), dict(args=[[7, 6, 4, 3, 1]], expected=0)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="prices", label="price towers", pointers=["i"]),
        dict(kind="values", vars=["minPrice", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int minPrice = INT_MAX, best = 0;
        for (int i = 0; i < (int)prices.size(); i++) {
            minPrice = min(minPrice, prices[i]);
            best = max(best, prices[i] - minPrice);
        }
        return best;
    }
};""",
)

# ============================================================ two pointers

add(
    id=167, slug="two-sum-ii-input-array-is-sorted", title="Two Sum II - Input Array Is Sorted", difficulty="Medium",
    world="two-pointers", tags=["array", "two-pointers", "binary-search"],
    story=dict(
        title="Twin Dockhands",
        text="Crates on the dock are sorted by weight. Two dockhands start at opposite ends. If their crates are too "
             "light together, the left one steps right; too heavy, the right one steps left.",
        goal="Return the 1-based positions of the two crates that weigh exactly the target together.",
    ),
    legend=[dict(sprite="l / r", meaning="the two dockhands"), dict(sprite="spotlight", meaning="crates still in play")],
    spec=dict(method="twoSum", ret="vector<int>", params=[["vector<int>&", "numbers"], ["int", "target"]]),
    tests=[dict(args=[[2, 7, 11, 15], 9], expected=[1, 2]), dict(args=[[2, 3, 4], 6], expected=[1, 3]),
           dict(args=[[-1, 0], -1], expected=[1, 2]), dict(args=[[1, 3, 4, 5, 7, 10, 11], 9], expected=[3, 4])],
    visualTest=3,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="numbers", label="sorted crates", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["target", "s"]),
    ]),
    reference="""class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int l = 0, r = numbers.size() - 1;
        while (l < r) {
            int s = numbers[l] + numbers[r];
            if (s == target) return {l + 1, r + 1};
            if (s < target) l++;
            else r--;
        }
        return {};
    }
};""",
)

add(
    id=125, slug="valid-palindrome", title="Valid Palindrome", difficulty="Easy", world="two-pointers",
    tags=["string", "two-pointers"],
    story=dict(
        title="The Mirror Bridge",
        text="Two inspectors walk in from both ends of a bridge of letter tiles, skipping anything that is not a letter "
             "or digit, and compare what they stand on (ignoring case).",
        goal="Return true if the phrase reads the same both ways.",
    ),
    spec=dict(method="isPalindrome", ret="bool", params=[["string", "s"]]),
    tests=[dict(args=["A man, a plan, a canal: Panama"], expected=True), dict(args=["race a car"], expected=False),
           dict(args=[" "], expected=True), dict(args=["No lemon, no melon"], expected=True)],
    visualTest=3,
    scene=dict(theme="dock", layers=[
        dict(kind="string", var="s", label="bridge", pointers=["l", "r"], window=["l", "r"]),
    ]),
    reference="""class Solution {
public:
    bool isPalindrome(string s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            while (l < r && !isalnum(s[l])) l++;
            while (l < r && !isalnum(s[r])) r--;
            if (tolower(s[l]) != tolower(s[r])) return false;
            l++;
            r--;
        }
        return true;
    }
};""",
)

add(
    id=11, slug="container-with-most-water", title="Container With Most Water", difficulty="Medium",
    world="two-pointers", tags=["array", "two-pointers", "greedy"],
    story=dict(
        title="The Reservoir Walls",
        text="Walls of different heights stand in a valley. Two engineers stand on the outermost walls; the water they "
             "can hold is limited by the shorter wall, so the shorter one always moves inward.",
        goal="Return the largest amount of water any two walls can hold.",
    ),
    spec=dict(method="maxArea", ret="int", params=[["vector<int>&", "height"]]),
    tests=[dict(args=[[1, 8, 6, 2, 5, 4, 8, 3, 7]], expected=49), dict(args=[[1, 1]], expected=1)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="height", label="walls", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["area", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxArea(vector<int>& height) {
        int l = 0, r = height.size() - 1, best = 0;
        while (l < r) {
            int area = min(height[l], height[r]) * (r - l);
            best = max(best, area);
            if (height[l] < height[r]) l++;
            else r--;
        }
        return best;
    }
};""",
)

add(
    id=42, slug="trapping-rain-water", title="Trapping Rain Water", difficulty="Hard", world="two-pointers",
    tags=["array", "two-pointers", "stack"],
    story=dict(
        title="Storm Over the Pixel City",
        text="Rain falls on a row of brick towers. Two surveyors start at both ends, each remembering the tallest tower "
             "they have passed. The side with the shorter tallest tower is safe to settle: water there is that height "
             "minus the tower.",
        goal="Return how many water tiles get trapped between the towers.",
    ),
    legend=[dict(sprite="blue tiles", meaning="water already settled behind the surveyors")],
    spec=dict(method="trap", ret="int", params=[["vector<int>&", "height"]]),
    tests=[dict(args=[[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], expected=6), dict(args=[[4, 2, 0, 3, 2, 5]], expected=9)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="height", label="towers", pointers=["l", "r"], water=["l", "r"]),
        dict(kind="values", vars=["leftMax", "rightMax", "water"]),
    ]),
    reference="""class Solution {
public:
    int trap(vector<int>& height) {
        int l = 0, r = height.size() - 1;
        int leftMax = 0, rightMax = 0, water = 0;
        while (l < r) {
            if (height[l] < height[r]) {
                leftMax = max(leftMax, height[l]);
                water += leftMax - height[l];
                l++;
            } else {
                rightMax = max(rightMax, height[r]);
                water += rightMax - height[r];
                r--;
            }
        }
        return water;
    }
};""",
)

add(
    id=283, slug="move-zeroes", title="Move Zeroes", difficulty="Easy", world="two-pointers",
    tags=["array", "two-pointers"],
    story=dict(
        title="Clearing Empty Crates",
        text="Empty crates (0) are clogging the dock. A reader walks every crate; a writer stays at the next free slot "
             "and swaps each full crate it is handed into place, so empties drift to the back.",
        goal="Move all zeroes to the end in place, keeping the order of the others.",
    ),
    spec=dict(method="moveZeroes", ret="void", params=[["vector<int>&", "nums"]], output="param:0"),
    tests=[dict(args=[[0, 1, 0, 3, 12]], expected=[1, 3, 12, 0, 0]), dict(args=[[0]], expected=[0])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="dock", pointers=["write", "read"]),
    ]),
    reference="""class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int write = 0;
        for (int read = 0; read < (int)nums.size(); read++) {
            if (nums[read] != 0) {
                swap(nums[write], nums[read]);
                write++;
            }
        }
    }
};""",
)

add(
    id=15, slug="3sum", title="3Sum", difficulty="Medium", world="two-pointers",
    tags=["array", "two-pointers", "sorting"],
    story=dict(
        title="Three-Crate Balance",
        text="After sorting the dock, a foreman stands on crate i and sends two dockhands to search the rest for a pair "
             "that balances the foreman's crate to exactly zero. Duplicate crates are skipped.",
        goal="Return every unique triple of crates that sums to zero.",
    ),
    spec=dict(method="threeSum", ret="vector<vector<int>>", params=[["vector<int>&", "nums"]]),
    compare="unordered-deep",
    tests=[dict(args=[[-1, 0, 1, 2, -1, -4]]), dict(args=[[0, 1, 1]]), dict(args=[[0, 0, 0]])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="sorted crates", pointers=["i", "l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["sum"]),
        dict(kind="array", var="res", label="found", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        int n = nums.size();
        for (int i = 0; i < n - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int l = i + 1, r = n - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum < 0) l++;
                else if (sum > 0) r--;
                else {
                    res.push_back({nums[i], nums[l], nums[r]});
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++;
                    r--;
                }
            }
        }
        return res;
    }
};""",
)

# ============================================================ sliding window

add(
    id=3, slug="longest-substring-without-repeating-characters", title="Longest Substring Without Repeating Characters",
    difficulty="Medium", world="sliding-window", tags=["string", "sliding-window", "hash-table"],
    story=dict(
        title="The Lighthouse Beam",
        text="A lighthouse beam sweeps along a row of letter buoys. The beam keeps stretching right; when it lights a "
             "letter it already holds, its left edge jumps past the earlier copy.",
        goal="Return the length of the longest stretch with no repeated letters.",
    ),
    spec=dict(method="lengthOfLongestSubstring", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["abcabcbb"], expected=3), dict(args=["bbbbb"], expected=1), dict(args=["pwwkew"], expected=3),
           dict(args=[""], expected=0)],
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="buoys", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="map", var="last", label="last seen at", lookup=["c"]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        map<char, int> last;
        int l = 0, best = 0;
        for (int r = 0; r < (int)s.size(); r++) {
            char c = s[r];
            if (last.count(c) && last[c] >= l) l = last[c] + 1;
            last[c] = r;
            best = max(best, r - l + 1);
        }
        return best;
    }
};""",
)

add(
    id=209, slug="minimum-size-subarray-sum", title="Minimum Size Subarray Sum", difficulty="Medium",
    world="sliding-window", tags=["array", "sliding-window", "prefix-sum"],
    story=dict(
        title="The Cargo Net",
        text="A crane lowers a stretchy net over the dock. It grows to the right until the crates inside weigh at least "
             "the target, then squeezes from the left as long as it still holds enough.",
        goal="Return the smallest number of adjacent crates weighing at least target (0 if impossible).",
    ),
    spec=dict(method="minSubArrayLen", ret="int", params=[["int", "target"], ["vector<int>&", "nums"]]),
    tests=[dict(args=[7, [2, 3, 1, 2, 4, 3]], expected=2), dict(args=[4, [1, 4, 4]], expected=1),
           dict(args=[11, [1, 1, 1, 1, 1, 1, 1, 1]], expected=0)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["target", "sum", "best"]),
    ]),
    reference="""class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int l = 0, sum = 0, best = INT_MAX;
        for (int r = 0; r < (int)nums.size(); r++) {
            sum += nums[r];
            while (sum >= target) {
                best = min(best, r - l + 1);
                sum -= nums[l];
                l++;
            }
        }
        return best == INT_MAX ? 0 : best;
    }
};""",
)

# ============================================================ stack

add(
    id=20, slug="valid-parentheses", title="Valid Parentheses", difficulty="Easy", world="stack",
    tags=["string", "stack"],
    story=dict(
        title="The Bracket Tower",
        text="A builder reads a blueprint of brackets. Every opening bracket becomes a block on the tower; every closing "
             "bracket must match the block on top, which is then removed.",
        goal="Return true if every bracket is closed in the right order.",
    ),
    spec=dict(method="isValid", ret="bool", params=[["string", "s"]]),
    tests=[dict(args=["()"], expected=True), dict(args=["()[]{}"], expected=True), dict(args=["(]"], expected=False),
           dict(args=["{[()]}([])"], expected=True), dict(args=["([)]"], expected=False)],
    visualTest=3,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="blueprint", pointers=["i"]),
        dict(kind="row", children=[
            dict(kind="stack", var="st", label="tower"),
            dict(kind="values", vars=["c"]),
        ]),
    ]),
    reference="""class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        for (int i = 0; i < (int)s.size(); i++) {
            char c = s[i];
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.empty()) return false;
                char top = st.top();
                if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{')) return false;
                st.pop();
            }
        }
        return st.empty();
    }
};""",
)

add(
    id=739, slug="daily-temperatures", title="Daily Temperatures", difficulty="Medium", world="stack",
    tags=["array", "stack", "monotonic-stack"],
    story=dict(
        title="Waiting for a Warmer Day",
        text="Days are towers of temperature. Unanswered days wait on a stack of signs. Each new warmer day knocks off "
             "every colder sign on top and writes how many days they waited.",
        goal="For each day, how many days until a warmer one (0 if never).",
    ),
    spec=dict(method="dailyTemperatures", ret="vector<int>", params=[["vector<int>&", "temperatures"]]),
    tests=[dict(args=[[73, 74, 75, 71, 69, 72, 76, 73]], expected=[1, 1, 4, 2, 1, 1, 0, 0]),
           dict(args=[[30, 40, 50, 60]], expected=[1, 1, 1, 0]), dict(args=[[30, 60, 90]], expected=[1, 1, 0])],
    scene=dict(theme="castle", layers=[
        dict(kind="bars", var="temperatures", label="temperature towers", pointers=["i"]),
        dict(kind="row", children=[
            dict(kind="stack", var="st", label="waiting days (index)"),
            dict(kind="array", var="ans", label="answers", style="tiles", weight=2),
        ]),
    ]),
    reference="""class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> ans(n, 0);
        stack<int> st;
        for (int i = 0; i < n; i++) {
            while (!st.empty() && temperatures[st.top()] < temperatures[i]) {
                int j = st.top();
                st.pop();
                ans[j] = i - j;
            }
            st.push(i);
        }
        return ans;
    }
};""",
)

add(
    id=150, slug="evaluate-reverse-polish-notation", title="Evaluate Reverse Polish Notation", difficulty="Medium",
    world="stack", tags=["array", "stack", "math"],
    story=dict(
        title="The Calculator Tower",
        text="Number tokens are stacked as blocks. An operator token pulls the top two blocks off, combines them, and "
             "puts the result back on top.",
        goal="Return the value of the expression.",
    ),
    spec=dict(method="evalRPN", ret="int", params=[["vector<string>&", "tokens"]]),
    tests=[dict(args=[["2", "1", "+", "3", "*"]], expected=9), dict(args=[["4", "13", "5", "/", "+"]], expected=6),
           dict(args=[["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]], expected=22)],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="tokens", label="tokens", style="tiles", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="st", label="tower"), dict(kind="values", vars=["a", "b"])]),
    ]),
    reference="""class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<long long> st;
        for (int i = 0; i < (int)tokens.size(); i++) {
            string& t = tokens[i];
            if (t == "+" || t == "-" || t == "*" || t == "/") {
                long long b = st.top(); st.pop();
                long long a = st.top(); st.pop();
                if (t == "+") st.push(a + b);
                else if (t == "-") st.push(a - b);
                else if (t == "*") st.push(a * b);
                else st.push(a / b);
            } else {
                st.push(stoll(t));
            }
        }
        return st.top();
    }
};""",
)

# ============================================================ binary search

add(
    id=704, slug="binary-search", title="Binary Search", difficulty="Easy", world="binary-search",
    tags=["array", "binary-search"],
    story=dict(
        title="The Guarded Corridor",
        text="Sorted treasure chests line a dark corridor. A guard checks the middle chest and closes off the half that "
             "cannot hold the target, again and again.",
        goal="Return the index of target, or -1.",
    ),
    spec=dict(method="search", ret="int", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[-1, 0, 3, 5, 9, 12], 9], expected=4), dict(args=[[-1, 0, 3, 5, 9, 12], 2], expected=-1),
           dict(args=[[1, 4, 6, 9, 13, 18, 21, 27, 33, 40, 46], 33], expected=8)],
    visualTest=2,
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="chests", pointers=["lo", "mid", "hi"], window=["lo", "hi"]),
        dict(kind="values", vars=["target"]),
    ]),
    reference="""class Solution {
public:
    int search(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }
};""",
)

add(
    id=35, slug="search-insert-position", title="Search Insert Position", difficulty="Easy", world="binary-search",
    tags=["array", "binary-search"],
    story=dict(
        title="The Library Shelf",
        text="A librarian looks for where a new book belongs on a sorted shelf, halving the shelf each time.",
        goal="Return the index of target, or where it would be inserted.",
    ),
    spec=dict(method="searchInsert", ret="int", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[1, 3, 5, 6], 5], expected=2), dict(args=[[1, 3, 5, 6], 2], expected=1),
           dict(args=[[1, 3, 5, 6], 7], expected=4)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="shelf", pointers=["lo", "mid", "hi"], window=["lo", "hi"], windowExclusive=True),
    ]),
    reference="""class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size();
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] < target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
};""",
)

add(
    id=33, slug="search-in-rotated-sorted-array", title="Search in Rotated Sorted Array", difficulty="Medium",
    world="binary-search", tags=["array", "binary-search"],
    story=dict(
        title="The Turned Corridor",
        text="Someone rotated the corridor of sorted chests. At every middle chest, one half is still in order; the guard "
             "checks whether the target lives in that ordered half.",
        goal="Return the index of target, or -1.",
    ),
    spec=dict(method="search", ret="int", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[4, 5, 6, 7, 0, 1, 2], 0], expected=4), dict(args=[[4, 5, 6, 7, 0, 1, 2], 3], expected=-1),
           dict(args=[[1], 0], expected=-1)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="chests", pointers=["lo", "mid", "hi"], window=["lo", "hi"]),
    ]),
    reference="""class Solution {
public:
    int search(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size() - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] == target) return mid;
            if (nums[lo] <= nums[mid]) {
                if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
                else lo = mid + 1;
            } else {
                if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
                else hi = mid - 1;
            }
        }
        return -1;
    }
};""",
)

# ============================================================ linked list

add(
    id=206, slug="reverse-linked-list", title="Reverse Linked List", difficulty="Easy", world="linked-list",
    tags=["linked-list", "recursion"],
    story=dict(
        title="Turning the Train Around",
        text="A train must leave the yard in the opposite direction. Three yard workers walk along it: prev holds the "
             "already-reversed part, curr unhooks its car and re-hooks it backwards, next remembers the rest.",
        goal="Return the head of the reversed train.",
    ),
    legend=[dict(sprite="cars", meaning="ListNode"), dict(sprite="purple loops", meaning="links pointing backwards")],
    spec=dict(method="reverseList", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5]], expected=[5, 4, 3, 2, 1]), dict(args=[[1, 2]], expected=[2, 1]),
           dict(args=[[]], expected=[])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "prev", "curr", "next"], heads=["head"], label="train"),
    ]),
    reference="""class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;
        while (curr) {
            ListNode* next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }
};""",
)

add(
    id=21, slug="merge-two-sorted-lists", title="Merge Two Sorted Lists", difficulty="Easy", world="linked-list",
    tags=["linked-list", "recursion"],
    story=dict(
        title="Zipping Two Trains",
        text="Two sorted trains wait on parallel tracks. A coupler at the tail of the new train always takes the lighter "
             "front car from either track.",
        goal="Return one sorted train made from all the cars.",
    ),
    spec=dict(method="mergeTwoLists", ret="ListNode*", params=[["ListNode*", "list1"], ["ListNode*", "list2"]]),
    tests=[dict(args=[[1, 2, 4], [1, 3, 4]], expected=[1, 1, 2, 3, 4, 4]), dict(args=[[], []], expected=[]),
           dict(args=[[], [0]], expected=[0])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["list1", "list2", "tail"], heads=["list1", "list2"], label="tracks"),
    ]),
    reference="""class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode* dummy = new ListNode(0);
        ListNode* tail = dummy;
        while (list1 && list2) {
            if (list1->val <= list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }
        tail->next = list1 ? list1 : list2;
        return dummy->next;
    }
};""",
)

add(
    id=876, slug="middle-of-the-linked-list", title="Middle of the Linked List", difficulty="Easy",
    world="linked-list", tags=["linked-list", "two-pointers"],
    story=dict(
        title="Tortoise and Hare on the Rails",
        text="Two runners race along the train roof: the hare jumps two cars at a time, the tortoise one. When the hare "
             "runs out of train, the tortoise is in the middle.",
        goal="Return the middle car (the second middle if there are two).",
    ),
    spec=dict(method="middleNode", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5]], expected=[3, 4, 5]), dict(args=[[1, 2, 3, 4, 5, 6]], expected=[4, 5, 6])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "slow", "fast"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* middleNode(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow;
    }
};""",
)

add(
    id=19, slug="remove-nth-node-from-end-of-list", title="Remove Nth Node From End of List", difficulty="Medium",
    world="linked-list", tags=["linked-list", "two-pointers"],
    story=dict(
        title="Dropping a Car",
        text="The scout runs n cars ahead of the brakeman. When the scout reaches the end, the brakeman is standing right "
             "before the car to drop and unhooks it.",
        goal="Remove the n-th car from the end and return the train.",
    ),
    spec=dict(method="removeNthFromEnd", ret="ListNode*", params=[["ListNode*", "head"], ["int", "n"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], 2], expected=[1, 2, 3, 5]), dict(args=[[1], 1], expected=[]),
           dict(args=[[1, 2], 1], expected=[1])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "fast", "slow"], heads=["head"], label="train"),
        dict(kind="values", vars=["n", "k"]),
    ]),
    reference="""class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* fast = dummy;
        ListNode* slow = dummy;
        for (int k = 0; k <= n; k++) fast = fast->next;
        while (fast) {
            fast = fast->next;
            slow = slow->next;
        }
        slow->next = slow->next->next;
        return dummy->next;
    }
};""",
)

# ============================================================ trees

add(
    id=104, slug="maximum-depth-of-binary-tree", title="Maximum Depth of Binary Tree", difficulty="Easy",
    world="trees", tags=["tree", "dfs", "recursion"],
    story=dict(
        title="How Tall Is the Apple Tree?",
        text="A squirrel climbs to every fruit. At each fruit it asks both branches how deep they go, and reports one "
             "more than the deeper answer. Each question opens a new door in the call stack.",
        goal="Return the number of fruits on the longest root-to-leaf path.",
    ),
    spec=dict(method="maxDepth", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 9, 20, None, None, 15, 7]], expected=3), dict(args=[[1, None, 2]], expected=2),
           dict(args=[[]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["root"], label="apple tree"),
        dict(kind="values", vars=["l", "r"]),
    ]),
    reference="""class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (!root) return 0;
        int l = maxDepth(root->left);
        int r = maxDepth(root->right);
        return 1 + max(l, r);
    }
};""",
)

add(
    id=226, slug="invert-binary-tree", title="Invert Binary Tree", difficulty="Easy", world="trees",
    tags=["tree", "dfs", "recursion"],
    story=dict(
        title="The Mirror Orchard",
        text="A gardener visits each fruit and swaps its left and right branches, then does the same for both "
             "branches. Watch whole subtrees glide to the other side.",
        goal="Return the mirrored tree.",
    ),
    spec=dict(method="invertTree", ret="TreeNode*", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[4, 2, 7, 1, 3, 6, 9]], expected=[4, 7, 2, 9, 6, 3, 1]), dict(args=[[2, 1, 3]], expected=[2, 3, 1]),
           dict(args=[[]], expected=[])],
    scene=dict(theme="forest", layers=[dict(kind="tree", var="root", pointers=["root"], label="orchard")]),
    reference="""class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (!root) return nullptr;
        TreeNode* tmp = root->left;
        root->left = root->right;
        root->right = tmp;
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};""",
)

add(
    id=102, slug="binary-tree-level-order-traversal", title="Binary Tree Level Order Traversal", difficulty="Medium",
    world="trees", tags=["tree", "bfs"],
    story=dict(
        title="Harvest Row by Row",
        text="Pickers line up at the orchard gate. Each picker takes one fruit, records it on today's row, and sends its "
             "children to the back of the line for the next row.",
        goal="Return the fruit values level by level.",
    ),
    spec=dict(method="levelOrder", ret="vector<vector<int>>", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 9, 20, None, None, 15, 7]], expected=[[3], [9, 20], [15, 7]]), dict(args=[[1]], expected=[[1]]),
           dict(args=[[]], expected=[])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="pickers"),
        dict(kind="array", var="level", label="this row", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> res;
        if (!root) return res;
        queue<TreeNode*> q;
        q.push(root);
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
            res.push_back(level);
        }
        return res;
    }
};""",
)

add(
    id=98, slug="validate-binary-search-tree", title="Validate Binary Search Tree", difficulty="Medium",
    world="trees", tags=["tree", "dfs", "bst"],
    story=dict(
        title="The Orchard Inspector",
        text="Every fruit must be heavier than everything on its left branch and lighter than everything on its right. "
             "The inspector carries the allowed range down each branch.",
        goal="Return true if the tree is a valid binary search tree.",
    ),
    spec=dict(method="isValidBST", ret="bool", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[2, 1, 3]], expected=True), dict(args=[[5, 1, 4, None, None, 3, 6]], expected=False),
           dict(args=[[8, 4, 12, 2, 6, 10, 14]], expected=True)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["lo", "hi"]),
    ]),
    reference="""class Solution {
public:
    bool check(TreeNode* node, long long lo, long long hi) {
        if (!node) return true;
        if (node->val <= lo || node->val >= hi) return false;
        return check(node->left, lo, node->val) && check(node->right, node->val, hi);
    }
    bool isValidBST(TreeNode* root) {
        return check(root, LLONG_MIN, LLONG_MAX);
    }
};""",
)

add(
    id=235, slug="lowest-common-ancestor-of-a-binary-search-tree", title="Lowest Common Ancestor of a Binary Search Tree",
    difficulty="Medium", world="trees", tags=["tree", "bst"],
    story=dict(
        title="Where Two Paths Split",
        text="Two birds want to meet on the lowest branch above both of their fruits. Starting at the top, a scout moves "
             "left if both fruits are smaller, right if both are bigger, and stops where they split.",
        goal="Return the value of the lowest common ancestor of p and q.",
    ),
    spec=dict(method="lowestCommonAncestor", ret="int", params=[["TreeNode*", "root"], ["int", "p"], ["int", "q"]]),
    tests=[dict(args=[[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8], expected=6),
           dict(args=[[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5], expected=4),
           dict(args=[[2, 1], 2, 1], expected=2)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["cur"], label="orchard"),
        dict(kind="values", vars=["p", "q"]),
    ]),
    reference="""class Solution {
public:
    int lowestCommonAncestor(TreeNode* root, int p, int q) {
        TreeNode* cur = root;
        while (cur) {
            if (p < cur->val && q < cur->val) cur = cur->left;
            else if (p > cur->val && q > cur->val) cur = cur->right;
            else return cur->val;
        }
        return -1;
    }
};""",
    hints=["LeetCode passes TreeNode* p and q; here they are the values, which is all the BST walk needs."],
)

# ============================================================ heap

add(
    id=215, slug="kth-largest-element-in-an-array", title="Kth Largest Element in an Array", difficulty="Medium",
    world="heap", tags=["array", "heap", "sorting"],
    story=dict(
        title="The K-Fruit Pyramid",
        text="A vendor keeps only the k heaviest fruits in a pyramid where the lightest sits on top. A heavier newcomer "
             "knocks the top fruit off.",
        goal="Return the k-th largest value.",
    ),
    spec=dict(method="findKthLargest", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[3, 2, 1, 5, 6, 4], 2], expected=5), dict(args=[[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], expected=4)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="fruit cart", pointers=["i"]),
        dict(kind="heap", var="pq", label="pyramid (min on top)"),
        dict(kind="values", vars=["k"]),
    ]),
    reference="""class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        priority_queue<int, vector<int>, greater<int>> pq;
        for (int i = 0; i < (int)nums.size(); i++) {
            pq.push(nums[i]);
            if ((int)pq.size() > k) pq.pop();
        }
        return pq.top();
    }
};""",
)

add(
    id=1046, slug="last-stone-weight", title="Last Stone Weight", difficulty="Easy", world="heap",
    tags=["array", "heap"],
    story=dict(
        title="The Stone Smasher",
        text="Stones sit in a pyramid with the heaviest on top. Each round the two heaviest are smashed; if they differ, "
             "the leftover chunk goes back into the pyramid.",
        goal="Return the weight of the last stone (or 0).",
    ),
    spec=dict(method="lastStoneWeight", ret="int", params=[["vector<int>&", "stones"]]),
    tests=[dict(args=[[2, 7, 4, 1, 8, 1]], expected=1), dict(args=[[1]], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="heap", var="pq", label="stone pyramid (max on top)", color="#9a8c98"),
        dict(kind="values", vars=["a", "b"]),
    ]),
    reference="""class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        priority_queue<int> pq(stones.begin(), stones.end());
        while (pq.size() > 1) {
            int a = pq.top(); pq.pop();
            int b = pq.top(); pq.pop();
            if (a != b) pq.push(a - b);
        }
        return pq.empty() ? 0 : pq.top();
    }
};""",
)

add(
    id=347, slug="top-k-frequent-elements", title="Top K Frequent Elements", difficulty="Medium", world="heap",
    tags=["array", "hash-table", "heap"],
    story=dict(
        title="The Popularity Contest",
        text="The market counts how often each item is bought (lockers), then keeps a small pyramid of the k most bought "
             "items, with the least popular of them on top ready to be bumped.",
        goal="Return the k most frequent values (any order).",
    ),
    spec=dict(method="topKFrequent", ret="vector<int>", params=[["vector<int>&", "nums"], ["int", "k"]]),
    compare="unordered",
    tests=[dict(args=[[1, 1, 1, 2, 2, 3], 2], expected=[1, 2]), dict(args=[[1], 1], expected=[1])],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="receipts"),
        dict(kind="map", var="cnt", label="counts"),
        dict(kind="heap", var="pq", label="top-k pyramid [count,value]"),
    ]),
    reference="""class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        map<int, int> cnt;
        for (int x : nums) cnt[x]++;
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        for (auto& [v, c] : cnt) {
            pq.push({c, v});
            if ((int)pq.size() > k) pq.pop();
        }
        vector<int> res;
        while (!pq.empty()) {
            res.push_back(pq.top().second);
            pq.pop();
        }
        return res;
    }
};""",
)

# ============================================================ graphs

add(
    id=200, slug="number-of-islands", title="Number of Islands", difficulty="Medium", world="graphs",
    tags=["array", "dfs", "bfs", "matrix"],
    story=dict(
        title="Charting the Archipelago",
        text="A cartographer sails over a map of land (green) and sea (blue). Each time they land on unexplored ground "
             "they count a new island and walk all of it, marking footprints in the sand.",
        goal="Return the number of islands.",
    ),
    spec=dict(method="numIslands", ret="int", params=[["vector<vector<char>>&", "grid"]]),
    tests=[
        dict(args=[[["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]], expected=1),
        dict(args=[[["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]], expected=3),
    ],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="grid", palette="islands", label="sea chart", pointers=[["r", "c"]]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    void sink(vector<vector<char>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size() || grid[r][c] != '1') return;
        grid[r][c] = '#';
        sink(grid, r + 1, c);
        sink(grid, r - 1, c);
        sink(grid, r, c + 1);
        sink(grid, r, c - 1);
    }
    int numIslands(vector<vector<char>>& grid) {
        int count = 0;
        for (int r = 0; r < (int)grid.size(); r++) {
            for (int c = 0; c < (int)grid[0].size(); c++) {
                if (grid[r][c] == '1') {
                    count++;
                    sink(grid, r, c);
                }
            }
        }
        return count;
    }
};""",
)

add(
    id=994, slug="rotting-oranges", title="Rotting Oranges", difficulty="Medium", world="graphs",
    tags=["array", "bfs", "matrix"],
    story=dict(
        title="The Orange Crate Blight",
        text="Rotten oranges (green) infect their fresh neighbours every minute. All the rotten ones queue at the gate "
             "and spread together, one wave per minute.",
        goal="Return the minutes until no fresh orange is left, or -1 if some never rot.",
    ),
    spec=dict(method="orangesRotting", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], expected=4), dict(args=[[[2, 1, 1], [0, 1, 1], [1, 0, 1]]], expected=-1),
           dict(args=[[[0, 2]]], expected=0)],
    scene=dict(theme="farm", layers=[
        dict(kind="grid", var="grid", palette="oranges", label="crate", pointers=[["r", "c"]]),
        dict(kind="queue", var="q", label="rotten queue (r,c)"),
        dict(kind="values", vars=["minutes", "fresh"]),
    ]),
    reference="""class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int R = grid.size(), C = grid[0].size(), fresh = 0, minutes = 0;
        queue<pair<int, int>> q;
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                if (grid[r][c] == 2) q.push({r, c});
                if (grid[r][c] == 1) fresh++;
            }
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        while (!q.empty() && fresh > 0) {
            int sz = q.size();
            for (int k = 0; k < sz; k++) {
                auto [r, c] = q.front();
                q.pop();
                for (int d = 0; d < 4; d++) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nc < 0 || nr >= R || nc >= C || grid[nr][nc] != 1) continue;
                    grid[nr][nc] = 2;
                    fresh--;
                    q.push({nr, nc});
                }
            }
            minutes++;
        }
        return fresh == 0 ? minutes : -1;
    }
};""",
)

add(
    id=207, slug="course-schedule", title="Course Schedule", difficulty="Medium", world="graphs",
    tags=["graph", "dfs", "topological-sort"],
    story=dict(
        title="The Quest Board",
        text="Every quest unlocks others. A herald walks the roads between quest towns: yellow towns are on the current "
             "path, green ones are finished. Walking into a yellow town again means a loop of quests that can never start.",
        goal="Return true if every quest can be finished.",
    ),
    spec=dict(method="canFinish", ret="bool", params=[["int", "numCourses"], ["vector<vector<int>>&", "prerequisites"]]),
    tests=[dict(args=[2, [[1, 0]]], expected=True), dict(args=[2, [[1, 0], [0, 1]]], expected=False),
           dict(args=[6, [[1, 0], [2, 1], [3, 1], [4, 3], [5, 2], [5, 4]]], expected=True),
           dict(args=[4, [[1, 0], [2, 1], [3, 2], [1, 3]]], expected=False)],
    visualTest=2,
    scene=dict(theme="forest", layers=[
        dict(kind="graph", edges="prerequisites", n="numCourses", reverse=True, directed=True, state="state",
             pointers=["u"], label="quest towns"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> adj;
    vector<int> state;
    bool dfs(int u) {
        if (state[u] == 1) return false;
        if (state[u] == 2) return true;
        state[u] = 1;
        for (int v : adj[u]) {
            if (!dfs(v)) return false;
        }
        state[u] = 2;
        return true;
    }
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        adj.assign(numCourses, {});
        state.assign(numCourses, 0);
        for (auto& p : prerequisites) adj[p[1]].push_back(p[0]);
        for (int u = 0; u < numCourses; u++) {
            if (!dfs(u)) return false;
        }
        return true;
    }
};""",
)

add(
    id=733, slug="flood-fill", title="Flood Fill", difficulty="Easy", world="graphs",
    tags=["array", "dfs", "matrix"],
    story=dict(
        title="The Paint Bucket",
        text="A painter tips a bucket on one tile. The paint runs to every neighbouring tile of the same old colour.",
        goal="Return the picture after the fill.",
    ),
    spec=dict(method="floodFill", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "image"], ["int", "sr"], ["int", "sc"], ["int", "color"]]),
    tests=[dict(args=[[[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2], expected=[[2, 2, 2], [2, 2, 0], [2, 0, 1]]),
           dict(args=[[[0, 0, 0], [0, 0, 0]], 0, 0, 0], expected=[[0, 0, 0], [0, 0, 0]])],
    scene=dict(theme="lab", layers=[dict(kind="grid", var="image", palette="dp", label="canvas", pointers=[["r", "c"]])]),
    reference="""class Solution {
public:
    void fill(vector<vector<int>>& image, int r, int c, int from, int to) {
        if (r < 0 || c < 0 || r >= (int)image.size() || c >= (int)image[0].size() || image[r][c] != from) return;
        image[r][c] = to;
        fill(image, r + 1, c, from, to);
        fill(image, r - 1, c, from, to);
        fill(image, r, c + 1, from, to);
        fill(image, r, c - 1, from, to);
    }
    vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {
        if (image[sr][sc] != color) fill(image, sr, sc, image[sr][sc], color);
        return image;
    }
};""",
)

# ============================================================ backtracking

add(
    id=78, slug="subsets", title="Subsets", difficulty="Medium", world="backtracking",
    tags=["array", "backtracking"],
    story=dict(
        title="The Door Maze of Choices",
        text="At every door the adventurer decides whether to take the next item into their bag. Each choice opens a "
             "deeper door; coming back out means putting the item down again.",
        goal="Return every possible subset (any order).",
    ),
    spec=dict(method="subsets", ret="vector<vector<int>>", params=[["vector<int>&", "nums"]]),
    compare="unordered-deep",
    tests=[dict(args=[[1, 2, 3]]), dict(args=[[0]])],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="items", pointers=["start", "i"]),
        dict(kind="array", var="path", label="bag", style="tiles"),
        dict(kind="values", vars=["start"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void go(vector<int>& nums, int start) {
        res.push_back(path);
        for (int i = start; i < (int)nums.size(); i++) {
            path.push_back(nums[i]);
            go(nums, i + 1);
            path.pop_back();
        }
    }
    vector<vector<int>> subsets(vector<int>& nums) {
        go(nums, 0);
        return res;
    }
};""",
)

add(
    id=46, slug="permutations", title="Permutations", difficulty="Medium", world="backtracking",
    tags=["array", "backtracking"],
    story=dict(
        title="Seating the Guests",
        text="Guests are seated one chair at a time. At each door the host tries every guest not yet seated, then stands "
             "them back up to try the next.",
        goal="Return every ordering of the guests (any order).",
    ),
    spec=dict(method="permute", ret="vector<vector<int>>", params=[["vector<int>&", "nums"]]),
    compare="unordered",
    tests=[dict(args=[[1, 2, 3]]), dict(args=[[0, 1]]), dict(args=[[1]])],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="guests", pointers=["i"]),
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
            used[i] = true;
            path.push_back(nums[i]);
            go(nums);
            path.pop_back();
            used[i] = false;
        }
    }
    vector<vector<int>> permute(vector<int>& nums) {
        used.assign(nums.size(), false);
        go(nums);
        return res;
    }
};""",
)

# ============================================================ dynamic programming

add(
    id=70, slug="climbing-stairs", title="Climbing Stairs", difficulty="Easy", world="dp",
    tags=["dynamic-programming", "math"],
    story=dict(
        title="The Frog on the Barn Stairs",
        text="A frog hops up the barn stairs one or two steps at a time. The farmer chalks on each stair how many ways "
             "the frog could have arrived there: the sum of the two stairs below.",
        goal="Return the number of distinct ways to reach the top stair.",
    ),
    spec=dict(method="climbStairs", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[2], expected=2), dict(args=[3], expected=3), dict(args=[8], expected=34)],
    visualTest=2,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="dp", label="stairs (ways)", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["n"]),
    ]),
    reference="""class Solution {
public:
    int climbStairs(int n) {
        vector<int> dp(n + 1, 0);
        dp[0] = 1;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) dp[i] = dp[i - 1] + dp[i - 2];
        return dp[n];
    }
};""",
)

add(
    id=198, slug="house-robber", title="House Robber", difficulty="Medium", world="dp",
    tags=["array", "dynamic-programming"],
    story=dict(
        title="The Fox and the Henhouses",
        text="A fox raids a row of henhouses but cannot hit two neighbours in one night. On each plot the farmer writes the "
             "best haul so far: skip this house, or take it plus the best from two houses back.",
        goal="Return the most eggs the fox can take.",
    ),
    spec=dict(method="rob", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 1]], expected=4), dict(args=[[2, 7, 9, 3, 1]], expected=12)],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="nums", label="henhouses", pointers=["i"]),
        dict(kind="array", var="dp", label="best haul", style="tiles", pointers=["i"]),
    ]),
    reference="""class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        vector<int> dp(n + 1, 0);
        dp[1] = nums[0];
        for (int i = 2; i <= n; i++) dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1]);
        return dp[n];
    }
};""",
)

add(
    id=322, slug="coin-change", title="Coin Change", difficulty="Medium", world="dp",
    tags=["array", "dynamic-programming", "bfs"],
    story=dict(
        title="The Vending Machine Ledger",
        text="A vending machine fills a ledger: for every amount from 1 up, the fewest coins that make it, trying each "
             "coin as the last one dropped in.",
        goal="Return the fewest coins for the amount, or -1.",
    ),
    spec=dict(method="coinChange", ret="int", params=[["vector<int>&", "coins"], ["int", "amount"]]),
    tests=[dict(args=[[1, 2, 5], 11], expected=3), dict(args=[[2], 3], expected=-1), dict(args=[[1], 0], expected=0)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="coins", label="coins", style="tiles"),
        dict(kind="array", var="dp", label="ledger (fewest coins per amount)", style="tiles", pointers=["a"]),
        dict(kind="values", vars=["c", "amount"]),
    ]),
    reference="""class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        const int INF = 1e9;
        vector<int> dp(amount + 1, INF);
        dp[0] = 0;
        for (int a = 1; a <= amount; a++) {
            for (int c : coins) {
                if (c <= a && dp[a - c] + 1 < dp[a]) dp[a] = dp[a - c] + 1;
            }
        }
        return dp[amount] >= INF ? -1 : dp[amount];
    }
};""",
)

add(
    id=62, slug="unique-paths", title="Unique Paths", difficulty="Medium", world="dp",
    tags=["math", "dynamic-programming", "combinatorics"],
    story=dict(
        title="The Robot Field",
        text="A robot crosses a field moving only right or down. Each plot gets the number of routes into it: the plot "
             "above plus the plot to the left.",
        goal="Return the number of routes to the bottom-right plot.",
    ),
    spec=dict(method="uniquePaths", ret="int", params=[["int", "m"], ["int", "n"]]),
    tests=[dict(args=[3, 7], expected=28), dict(args=[3, 2], expected=3), dict(args=[4, 4], expected=20)],
    visualTest=2,
    scene=dict(theme="farm", layers=[dict(kind="grid", var="dp", palette="dp", label="field", pointers=[["i", "j"]])]),
    reference="""class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<vector<int>> dp(m, vector<int>(n, 1));
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        return dp[m - 1][n - 1];
    }
};""",
)

add(
    id=1143, slug="longest-common-subsequence", title="Longest Common Subsequence", difficulty="Medium", world="dp",
    tags=["string", "dynamic-programming"],
    story=dict(
        title="Two Scrolls, One Story",
        text="Two scribes compare scrolls letter by letter on a grid. Matching letters extend the diagonal story; "
             "otherwise each cell keeps the better of skipping a letter from either scroll.",
        goal="Return the length of the longest common subsequence.",
    ),
    spec=dict(method="longestCommonSubsequence", ret="int", params=[["string", "text1"], ["string", "text2"]]),
    tests=[dict(args=["abcde", "ace"], expected=3), dict(args=["abc", "abc"], expected=3), dict(args=["abc", "def"], expected=0)],
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[
            dict(kind="string", var="text1", label="scroll 1"),
            dict(kind="string", var="text2", label="scroll 2"),
        ]),
        dict(kind="grid", var="dp", palette="dp", label="table", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int n = text1.size(), m = text2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                dp[i][j] = text1[i - 1] == text2[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
        return dp[n][m];
    }
};""",
)

# ============================================================ intervals / greedy / bits

add(
    id=56, slug="merge-intervals", title="Merge Intervals", difficulty="Medium", world="intervals",
    tags=["array", "sorting"],
    story=dict(
        title="The Booking Calendar",
        text="Room bookings are sorted by start time. A clerk walks through them; any booking that starts before the last "
             "merged one ends gets folded into it.",
        goal="Return the merged bookings.",
    ),
    spec=dict(method="merge", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "intervals"]]),
    tests=[dict(args=[[[1, 3], [2, 6], [8, 10], [15, 18]]], expected=[[1, 6], [8, 10], [15, 18]]),
           dict(args=[[[1, 4], [4, 5]]], expected=[[1, 5]]), dict(args=[[[4, 7], [1, 4]]], expected=[[1, 7]])],
    scene=dict(theme="lab", layers=[dict(kind="intervals", vars=["intervals", "res"], pointers=["i"], label="calendar")]),
    reference="""class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        vector<vector<int>> res;
        for (int i = 0; i < (int)intervals.size(); i++) {
            if (!res.empty() && intervals[i][0] <= res.back()[1]) {
                res.back()[1] = max(res.back()[1], intervals[i][1]);
            } else {
                res.push_back(intervals[i]);
            }
        }
        return res;
    }
};""",
)

add(
    id=57, slug="insert-interval", title="Insert Interval", difficulty="Medium", world="intervals",
    tags=["array"],
    story=dict(
        title="Squeezing in a Meeting",
        text="A new meeting must go into a sorted calendar. Meetings fully before it are copied, overlapping ones are "
             "swallowed into it, and the rest follow.",
        goal="Return the calendar with the new meeting merged in.",
    ),
    spec=dict(method="insert", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "intervals"], ["vector<int>&", "newInterval"]]),
    tests=[dict(args=[[[1, 3], [6, 9]], [2, 5]], expected=[[1, 5], [6, 9]]),
           dict(args=[[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]], expected=[[1, 2], [3, 10], [12, 16]])],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="intervals", vars=["intervals", "res"], pointers=["i"], label="calendar"),
        dict(kind="array", var="newInterval", label="new meeting", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> res;
        int i = 0, n = intervals.size();
        while (i < n && intervals[i][1] < newInterval[0]) res.push_back(intervals[i++]);
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = min(newInterval[0], intervals[i][0]);
            newInterval[1] = max(newInterval[1], intervals[i][1]);
            i++;
        }
        res.push_back(newInterval);
        while (i < n) res.push_back(intervals[i++]);
        return res;
    }
};""",
)

add(
    id=55, slug="jump-game", title="Jump Game", difficulty="Medium", world="greedy",
    tags=["array", "greedy", "dynamic-programming"],
    story=dict(
        title="Stepping Stones",
        text="Each stone says how far you may jump from it. A hiker walks forward tracking the farthest stone reachable "
             "so far; if they ever stand beyond it, the river wins.",
        goal="Return true if the last stone is reachable.",
    ),
    spec=dict(method="canJump", ret="bool", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 3, 1, 1, 4]], expected=True), dict(args=[[3, 2, 1, 0, 4]], expected=False)],
    visualTest=1,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="stones", pointers=["i", "reach"]),
    ]),
    reference="""class Solution {
public:
    bool canJump(vector<int>& nums) {
        int reach = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (i > reach) return false;
            reach = max(reach, i + nums[i]);
        }
        return true;
    }
};""",
)

add(
    id=136, slug="single-number", title="Single Number", difficulty="Easy", world="bits",
    tags=["array", "bit-manipulation"],
    story=dict(
        title="The Lamp of Pairs",
        text="Every number toggles the lamps of its bits. Pairs switch the same lamps twice and cancel out; only the "
             "lonely number leaves lamps lit.",
        goal="Every value appears twice except one. Return it.",
    ),
    spec=dict(method="singleNumber", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 2, 1]], expected=1), dict(args=[[4, 1, 2, 1, 2]], expected=4), dict(args=[[1]], expected=1)],
    visualTest=1,
    scene=dict(theme="space", layers=[
        dict(kind="array", var="nums", label="numbers", pointers=["i"]),
        dict(kind="values", vars=["x"]),
    ]),
    reference="""class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int x = 0;
        for (int i = 0; i < (int)nums.size(); i++) x ^= nums[i];
        return x;
    }
};""",
)

add(
    id=338, slug="counting-bits", title="Counting Bits", difficulty="Easy", world="bits",
    tags=["dynamic-programming", "bit-manipulation"],
    story=dict(
        title="Counting Lit Lamps",
        text="For each number, the count of lit lamps equals the count for the number with its last lamp shifted away, "
             "plus that last lamp.",
        goal="Return the number of 1 bits for every number from 0 to n.",
    ),
    spec=dict(method="countBits", ret="vector<int>", params=[["int", "n"]]),
    tests=[dict(args=[2], expected=[0, 1, 1]), dict(args=[5], expected=[0, 1, 1, 2, 1, 2])],
    visualTest=1,
    scene=dict(theme="space", layers=[dict(kind="array", var="ans", label="lit lamps", style="tiles", pointers=["i"])]),
    reference="""class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> ans(n + 1, 0);
        for (int i = 1; i <= n; i++) ans[i] = ans[i >> 1] + (i & 1);
        return ans;
    }
};""",
)
