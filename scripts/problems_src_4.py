"""Fourth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=13, slug="roman-to-integer", title="Roman to Integer", difficulty="Easy", world="arrays",
    tags=["hash-table", "math", "string"],
    story=dict(
        title="The Old Stone Tablet",
        text="A scholar reads Roman numerals off a tablet, looking each letter up in the lockers. A smaller letter "
             "standing before a bigger one is subtracted instead of added.",
        goal="Return the number the numeral stands for.",
    ),
    spec=dict(method="romanToInt", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["III"], expected=3), dict(args=["LVIII"], expected=58), dict(args=["MCMXCIV"], expected=1994)],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="tablet", pointers=["i"]),
        dict(kind="map", var="val", label="letter values"),
        dict(kind="values", vars=["cur", "total"]),
    ]),
    reference="""class Solution {
public:
    int romanToInt(string s) {
        map<char, int> val = {{'I', 1}, {'V', 5}, {'X', 10}, {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000}};
        int total = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            int cur = val[s[i]];
            if (i + 1 < (int)s.size() && cur < val[s[i + 1]]) total -= cur;
            else total += cur;
        }
        return total;
    }
};""",
)

add(
    id=14, slug="longest-common-prefix", title="Longest Common Prefix", difficulty="Easy", world="arrays",
    tags=["string", "trie"],
    story=dict(
        title="The Shared Family Name",
        text="Several scrolls start with the same family name. A clerk reads the first scroll letter by letter and checks "
             "every other scroll at the same position, stopping at the first mismatch.",
        goal="Return the longest prefix every word shares.",
    ),
    spec=dict(method="longestCommonPrefix", ret="string", params=[["vector<string>&", "strs"]]),
    tests=[dict(args=[["flower", "flow", "flight"]], expected="fl"), dict(args=[["dog", "racecar", "car"]], expected=""),
           dict(args=[["interview", "internet", "interval"]], expected="inter")],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="strs", label="scrolls", style="tiles", pointers=["j"]),
        dict(kind="string", var="prefix", label="shared so far"),
        dict(kind="values", vars=["i"]),
    ]),
    reference="""class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        string prefix = "";
        for (int i = 0; i < (int)strs[0].size(); i++) {
            char c = strs[0][i];
            for (int j = 1; j < (int)strs.size(); j++) {
                if (i >= (int)strs[j].size() || strs[j][i] != c) return prefix;
            }
            prefix.push_back(c);
        }
        return prefix;
    }
};""",
)

add(
    id=66, slug="plus-one", title="Plus One", difficulty="Easy", world="arrays", tags=["array", "math"],
    story=dict(
        title="The Turnstile Counter",
        text="A turnstile shows a number as a row of digit wheels. One more visitor: the last wheel clicks up, and every "
             "9 that rolls over to 0 passes the carry to the wheel on its left.",
        goal="Return the digits after adding one.",
    ),
    spec=dict(method="plusOne", ret="vector<int>", params=[["vector<int>&", "digits"]]),
    tests=[dict(args=[[1, 2, 3]], expected=[1, 2, 4]), dict(args=[[4, 3, 9, 9]], expected=[4, 4, 0, 0]), dict(args=[[9, 9]], expected=[1, 0, 0])],
    visualTest=1,
    scene=dict(theme="city", layers=[dict(kind="array", var="digits", label="wheels", style="tiles", pointers=["i"])]),
    reference="""class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        for (int i = digits.size() - 1; i >= 0; i--) {
            if (digits[i] < 9) {
                digits[i]++;
                return digits;
            }
            digits[i] = 0;
        }
        digits.insert(digits.begin(), 1);
        return digits;
    }
};""",
)

add(
    id=205, slug="isomorphic-strings", title="Isomorphic Strings", difficulty="Easy", world="arrays",
    tags=["hash-table", "string"],
    story=dict(
        title="The Cipher Wheel",
        text="Two messages might be the same text in a letter-for-letter cipher. Two locker walls record the cipher in "
             "both directions; any letter that would need two different partners breaks it.",
        goal="Return true if s can be turned into t by a one-to-one letter swap.",
    ),
    spec=dict(method="isIsomorphic", ret="bool", params=[["string", "s"], ["string", "t"]]),
    tests=[dict(args=["egg", "add"], expected=True), dict(args=["foo", "bar"], expected=False), dict(args=["paper", "title"], expected=True)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="message s", pointers=["i"]),
        dict(kind="string", var="t", label="message t", pointers=["i"]),
        dict(kind="row", children=[dict(kind="map", var="st", label="s → t"), dict(kind="map", var="ts", label="t → s")]),
    ]),
    reference="""class Solution {
public:
    bool isIsomorphic(string s, string t) {
        map<char, char> st, ts;
        for (int i = 0; i < (int)s.size(); i++) {
            char a = s[i], b = t[i];
            if (st.count(a) && st[a] != b) return false;
            if (ts.count(b) && ts[b] != a) return false;
            st[a] = b;
            ts[b] = a;
        }
        return true;
    }
};""",
)

add(
    id=287, slug="find-the-duplicate-number", title="Find the Duplicate Number", difficulty="Medium", world="two-pointers",
    tags=["array", "two-pointers", "binary-search", "bit-manipulation"],
    story=dict(
        title="The Loop in the Signposts",
        text="Each crate's number points to another crate. Following the signposts must eventually loop, and the loop's "
             "entrance is the duplicate. A tortoise and a hare race to find the loop, then walk in step to its entrance.",
        goal="Return the number that appears twice, without changing the array.",
    ),
    spec=dict(method="findDuplicate", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 3, 4, 2, 2]], expected=2), dict(args=[[3, 1, 3, 4, 2]], expected=3), dict(args=[[2, 5, 9, 6, 9, 3, 8, 9, 7, 1]], expected=9)],
    scene=dict(theme="dock", layers=[dict(kind="array", var="nums", label="signpost crates", pointers=["slow", "fast"])]),
    reference="""class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0], fast = nums[nums[0]];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[nums[fast]];
        }
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};""",
)

add(
    id=16, slug="3sum-closest", title="3Sum Closest", difficulty="Medium", world="two-pointers",
    tags=["array", "two-pointers", "sorting"],
    story=dict(
        title="Nearly Balanced",
        text="On a sorted dock a foreman picks one crate, then two dockhands squeeze inward looking for the pair that "
             "brings the three crates closest to the target weight.",
        goal="Return the sum of three crates closest to target.",
    ),
    spec=dict(method="threeSumClosest", ret="int", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[-1, 2, 1, -4], 1], expected=2), dict(args=[[0, 0, 0], 1], expected=0), dict(args=[[4, 0, 5, -5, 3, 3, 0, -4, -5], -2], expected=-2)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="sorted crates", pointers=["i", "l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["target", "sum", "best"]),
    ]),
    reference="""class Solution {
public:
    int threeSumClosest(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int best = nums[0] + nums[1] + nums[2];
        for (int i = 0; i < (int)nums.size() - 2; i++) {
            int l = i + 1, r = nums.size() - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (abs(sum - target) < abs(best - target)) best = sum;
                if (sum < target) l++;
                else if (sum > target) r--;
                else return sum;
            }
        }
        return best;
    }
};""",
)

add(
    id=1004, slug="max-consecutive-ones-iii", title="Max Consecutive Ones III", difficulty="Medium", world="sliding-window",
    tags=["array", "binary-search", "sliding-window", "prefix-sum"],
    story=dict(
        title="Patching the Road",
        text="A road crew may patch at most k potholes (0s). Their work zone stretches forward; once it holds more than "
             "k potholes, the back of the zone moves up past the oldest pothole.",
        goal="Return the longest stretch of smooth road possible.",
    ),
    spec=dict(method="longestOnes", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2], expected=6), dict(args=[[0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3], expected=10)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="nums", label="road", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["k", "zeros", "best"]),
    ]),
    reference="""class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        int l = 0, zeros = 0, best = 0;
        for (int r = 0; r < (int)nums.size(); r++) {
            if (nums[r] == 0) zeros++;
            while (zeros > k) {
                if (nums[l] == 0) zeros--;
                l++;
            }
            best = max(best, r - l + 1);
        }
        return best;
    }
};""",
)

add(
    id=76, slug="minimum-window-substring", title="Minimum Window Substring", difficulty="Hard", world="sliding-window",
    tags=["hash-table", "string", "sliding-window"],
    story=dict(
        title="The Shortest Shopping Trip",
        text="A shopper needs every item on a list from a row of stalls. The trip grows right until the basket covers the "
             "list, then shrinks from the left while it still does, remembering the shortest trip.",
        goal="Return the shortest stretch of s containing every letter of t (with counts), or an empty string.",
    ),
    spec=dict(method="minWindow", ret="string", params=[["string", "s"], ["string", "t"]]),
    tests=[dict(args=["ADOBECODEBANC", "ABC"], expected="BANC"), dict(args=["a", "a"], expected="a"), dict(args=["a", "aa"], expected="")],
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="stalls", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="row", children=[dict(kind="map", var="need", label="shopping list"), dict(kind="map", var="win", label="basket")]),
        dict(kind="values", vars=["have", "required", "bestLen"]),
    ]),
    reference="""class Solution {
public:
    string minWindow(string s, string t) {
        map<char, int> need, win;
        for (char c : t) need[c]++;
        int required = need.size(), have = 0, l = 0, bestLen = INT_MAX, bestL = 0;
        for (int r = 0; r < (int)s.size(); r++) {
            char c = s[r];
            win[c]++;
            if (need.count(c) && win[c] == need[c]) have++;
            while (have == required) {
                if (r - l + 1 < bestLen) {
                    bestLen = r - l + 1;
                    bestL = l;
                }
                char d = s[l];
                win[d]--;
                if (need.count(d) && win[d] < need[d]) have--;
                l++;
            }
        }
        return bestLen == INT_MAX ? "" : s.substr(bestL, bestLen);
    }
};""",
)

add(
    id=2390, slug="removing-stars-from-a-string", title="Removing Stars From a String", difficulty="Medium", world="stack",
    tags=["string", "stack", "simulation"],
    story=dict(
        title="The Eraser Stamps",
        text="A typist stacks letters as they type; every star is an eraser stamp that knocks the last letter off the "
             "stack.",
        goal="Return what is left after every star erases a letter.",
    ),
    spec=dict(method="removeStars", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["leet**cod*e"], expected="lecoe"), dict(args=["erase*****"], expected="")],
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="typed keys", pointers=["i"]),
        dict(kind="stack", var="res", label="letters kept"),
    ]),
    reference="""class Solution {
public:
    string removeStars(string s) {
        string res;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '*') res.pop_back();
            else res.push_back(s[i]);
        }
        return res;
    }
};""",
)

add(
    id=735, slug="asteroid-collision", title="Asteroid Collision", difficulty="Medium", world="stack",
    tags=["array", "stack", "simulation"],
    story=dict(
        title="The Asteroid Belt",
        text="Asteroids drift right (positive) or left (negative). A tower holds the survivors; each left-mover smashes "
             "into right-movers on top of the tower until one side is gone.",
        goal="Return the asteroids left after every collision.",
    ),
    spec=dict(method="asteroidCollision", ret="vector<int>", params=[["vector<int>&", "asteroids"]]),
    tests=[dict(args=[[5, 10, -5]], expected=[5, 10]), dict(args=[[8, -8]], expected=[]), dict(args=[[10, 2, -5]], expected=[10]),
           dict(args=[[-2, -1, 1, 2]], expected=[-2, -1, 1, 2])],
    visualTest=2,
    scene=dict(theme="space", layers=[
        dict(kind="array", var="asteroids", label="belt", pointers=["i"]),
        dict(kind="row", children=[dict(kind="stack", var="st", label="survivors"), dict(kind="values", vars=["a", "alive"])]),
    ]),
    reference="""class Solution {
public:
    vector<int> asteroidCollision(vector<int>& asteroids) {
        vector<int> st;
        for (int i = 0; i < (int)asteroids.size(); i++) {
            int a = asteroids[i];
            bool alive = true;
            while (alive && a < 0 && !st.empty() && st.back() > 0) {
                if (st.back() < -a) {
                    st.pop_back();
                } else {
                    if (st.back() == -a) st.pop_back();
                    alive = false;
                }
            }
            if (alive) st.push_back(a);
        }
        return st;
    }
};""",
)

add(
    id=34, slug="find-first-and-last-position-of-element-in-sorted-array", title="Find First and Last Position of Element in Sorted Array",
    difficulty="Medium", world="binary-search", tags=["array", "binary-search"],
    story=dict(
        title="The Twin Guards",
        text="The same treasure may fill several chests in a row. One guard searches for the first chest that is not "
             "smaller than the target, another for the first chest bigger than it.",
        goal="Return the first and last index of target, or [-1, -1].",
    ),
    spec=dict(method="searchRange", ret="vector<int>", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[5, 7, 7, 8, 8, 10], 8], expected=[3, 4]), dict(args=[[5, 7, 7, 8, 8, 10], 6], expected=[-1, -1]),
           dict(args=[[], 0], expected=[-1, -1])],
    scene=dict(theme="cave", layers=[dict(kind="array", var="nums", label="chests", pointers=["lo", "mid", "hi"], window=["lo", "hi"], windowExclusive=True)]),
    reference="""class Solution {
public:
    int firstAtLeast(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size();
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] < target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
    vector<int> searchRange(vector<int>& nums, int target) {
        int a = firstAtLeast(nums, target);
        if (a == (int)nums.size() || nums[a] != target) return {-1, -1};
        int b = firstAtLeast(nums, target + 1) - 1;
        return {a, b};
    }
};""",
)

add(
    id=540, slug="single-element-in-a-sorted-array", title="Single Element in a Sorted Array", difficulty="Medium",
    world="binary-search", tags=["array", "binary-search"],
    story=dict(
        title="The Missing Pair",
        text="Sorted shoes come in pairs, except one lonely shoe. Before it, every pair starts at an even position; after "
             "it, pairs start at odd ones. The guard checks which side of the break the middle pair is on.",
        goal="Return the value that appears only once.",
    ),
    spec=dict(method="singleNonDuplicate", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 1, 2, 3, 3, 4, 4, 8, 8]], expected=2), dict(args=[[3, 3, 7, 7, 10, 11, 11]], expected=10)],
    scene=dict(theme="cave", layers=[dict(kind="array", var="nums", label="shoes", pointers=["lo", "mid", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int lo = 0, hi = nums.size() - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (mid % 2 == 1) mid--;
            if (nums[mid] == nums[mid + 1]) lo = mid + 2;
            else hi = mid;
        }
        return nums[lo];
    }
};""",
)

add(
    id=92, slug="reverse-linked-list-ii", title="Reverse Linked List II", difficulty="Medium", world="linked-list",
    tags=["linked-list"],
    story=dict(
        title="Turning Part of the Train",
        text="Only the cars between positions left and right must face the other way. A brakeman parks just before the "
             "section and keeps pulling the next car to the front of it until the whole section is turned.",
        goal="Reverse the cars from position left to right and return the train.",
    ),
    spec=dict(method="reverseBetween", ret="ListNode*", params=[["ListNode*", "head"], ["int", "left"], ["int", "right"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5], 2, 4], expected=[1, 4, 3, 2, 5]), dict(args=[[5], 1, 1], expected=[5]), dict(args=[[3, 5], 1, 2], expected=[5, 3])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "prev", "cur", "nxt"], heads=["head"], label="train"),
        dict(kind="values", vars=["left", "right", "k"]),
    ]),
    reference="""class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode* dummy = new ListNode(0, head);
        ListNode* prev = dummy;
        for (int k = 1; k < left; k++) prev = prev->next;
        ListNode* cur = prev->next;
        for (int k = 0; k < right - left; k++) {
            ListNode* nxt = cur->next;
            cur->next = nxt->next;
            nxt->next = prev->next;
            prev->next = nxt;
        }
        return dummy->next;
    }
};""",
)

add(
    id=328, slug="odd-even-linked-list", title="Odd Even Linked List", difficulty="Medium", world="linked-list",
    tags=["linked-list"],
    story=dict(
        title="Splitting the Train by Seat",
        text="Cars in odd positions and cars in even positions must form two trains, then the even train is hooked "
             "behind the odd one. Two couplers leapfrog down the track re-hooking cars.",
        goal="Return the train with all odd-position cars first, then the even ones.",
    ),
    spec=dict(method="oddEvenList", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5]], expected=[1, 3, 5, 2, 4]), dict(args=[[2, 1, 3, 5, 6, 4, 7]], expected=[2, 3, 6, 7, 1, 5, 4]),
           dict(args=[[]], expected=[])],
    scene=dict(theme="farm", layers=[dict(kind="list", vars=["head", "odd", "even", "evenHead"], heads=["head"], label="train")]),
    reference="""class Solution {
public:
    ListNode* oddEvenList(ListNode* head) {
        if (!head) return head;
        ListNode* odd = head;
        ListNode* even = head->next;
        ListNode* evenHead = even;
        while (even && even->next) {
            odd->next = even->next;
            odd = odd->next;
            even->next = odd->next;
            even = even->next;
        }
        odd->next = evenHead;
        return head;
    }
};""",
)

add(
    id=572, slug="subtree-of-another-tree", title="Subtree of Another Tree", difficulty="Easy", world="trees",
    tags=["tree", "dfs", "string-matching"],
    story=dict(
        title="The Grafted Branch",
        text="A gardener holds a small cutting and wants to know if the big orchard already has a branch exactly like it. "
             "At every fruit they hold the cutting against the branch below and compare.",
        goal="Return true if subRoot appears somewhere in root as a whole subtree.",
    ),
    spec=dict(method="isSubtree", ret="bool", params=[["TreeNode*", "root"], ["TreeNode*", "subRoot"]]),
    tests=[dict(args=[[3, 4, 5, 1, 2], [4, 1, 2]], expected=True), dict(args=[[3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2]], expected=False)],
    scene=dict(theme="forest", layers=[dict(kind="row", children=[
        dict(kind="tree", var="root", pointers=["root", "a"], label="orchard", weight=2),
        dict(kind="tree", var="subRoot", pointers=["b"], label="cutting"),
    ])]),
    reference="""class Solution {
public:
    bool same(TreeNode* a, TreeNode* b) {
        if (!a && !b) return true;
        if (!a || !b || a->val != b->val) return false;
        return same(a->left, b->left) && same(a->right, b->right);
    }
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (!root) return false;
        if (same(root, subRoot)) return true;
        return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
    }
};""",
)

add(
    id=1448, slug="count-good-nodes-in-binary-tree", title="Count Good Nodes in Binary Tree", difficulty="Medium", world="trees",
    tags=["tree", "dfs", "bfs"],
    story=dict(
        title="Fruit with a Clear View",
        text="A fruit is good if nothing on the path from the top is heavier. A squirrel climbs down carrying the "
             "heaviest weight seen so far and counts every fruit at least that heavy.",
        goal="Return the number of good nodes.",
    ),
    spec=dict(method="goodNodes", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 1, 4, 3, None, 1, 5]], expected=4), dict(args=[[3, 3, None, 4, 2]], expected=3), dict(args=[[1]], expected=1)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["best", "count"]),
    ]),
    reference="""class Solution {
public:
    int count = 0;
    void walk(TreeNode* node, int best) {
        if (!node) return;
        if (node->val >= best) count++;
        best = max(best, node->val);
        walk(node->left, best);
        walk(node->right, best);
    }
    int goodNodes(TreeNode* root) {
        walk(root, INT_MIN);
        return count;
    }
};""",
)

add(
    id=1642, slug="furthest-building-you-can-reach", title="Furthest Building You Can Reach", difficulty="Medium", world="heap",
    tags=["array", "greedy", "heap"],
    story=dict(
        title="Ladders for the Tallest Climbs",
        text="A rooftop runner has some bricks and a few ladders. Every climb takes a ladder for now; when ladders run "
             "out, the smallest climb in the ladder pyramid is paid for with bricks instead.",
        goal="Return the furthest building index reachable.",
    ),
    spec=dict(method="furthestBuilding", ret="int", params=[["vector<int>&", "heights"], ["int", "bricks"], ["int", "ladders"]]),
    tests=[dict(args=[[4, 2, 7, 6, 9, 14, 12], 5, 1], expected=4), dict(args=[[4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2], expected=7),
           dict(args=[[14, 3, 19, 3], 17, 0], expected=3)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="heights", label="rooftops", pointers=["i"]),
        dict(kind="heap", var="pq", label="climbs using ladders (smallest on top)"),
        dict(kind="values", vars=["climb", "bricks", "ladders"]),
    ]),
    reference="""class Solution {
public:
    int furthestBuilding(vector<int>& heights, int bricks, int ladders) {
        priority_queue<int, vector<int>, greater<int>> pq;
        for (int i = 0; i + 1 < (int)heights.size(); i++) {
            int climb = heights[i + 1] - heights[i];
            if (climb <= 0) continue;
            pq.push(climb);
            if ((int)pq.size() > ladders) {
                bricks -= pq.top();
                pq.pop();
                if (bricks < 0) return i;
            }
        }
        return heights.size() - 1;
    }
};""",
)

add(
    id=1091, slug="shortest-path-in-binary-matrix", title="Shortest Path in Binary Matrix", difficulty="Medium", world="graphs",
    tags=["array", "bfs", "matrix"],
    story=dict(
        title="The Flood of Footsteps",
        text="An explorer must cross a maze from the top-left to the bottom-right, moving in any of eight directions over "
             "open tiles. Footsteps spread outward like a flood, each tile marked with how many steps it took to reach.",
        goal="Return the length of the shortest clear path, or -1.",
    ),
    spec=dict(method="shortestPathBinaryMatrix", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[0, 1], [1, 0]]], expected=2), dict(args=[[[0, 0, 0], [1, 1, 0], [1, 1, 0]]], expected=4),
           dict(args=[[[1, 0, 0], [1, 1, 0], [1, 1, 0]]], expected=-1)],
    visualTest=1,
    scene=dict(theme="cave", layers=[
        dict(kind="row", children=[
            dict(kind="grid", var="grid", palette="maze", label="maze", pointers=[["r", "c"]]),
            dict(kind="grid", var="dist", palette="dp", label="steps to reach"),
        ]),
        dict(kind="queue", var="q", label="frontier (r,c)"),
    ]),
    reference="""class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        int n = grid.size();
        if (grid[0][0] || grid[n - 1][n - 1]) return -1;
        vector<vector<int>> dist(n, vector<int>(n, 0));
        queue<pair<int, int>> q;
        q.push({0, 0});
        dist[0][0] = 1;
        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();
            if (r == n - 1 && c == n - 1) return dist[r][c];
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr, nc = c + dc;
                    if (nr < 0 || nc < 0 || nr >= n || nc >= n || grid[nr][nc] || dist[nr][nc]) continue;
                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});
                }
            }
        }
        return -1;
    }
};""",
)

add(
    id=1971, slug="find-if-path-exists-in-graph", title="Find if Path Exists in Graph", difficulty="Easy", world="graphs",
    tags=["graph", "bfs", "dfs", "union-find"],
    story=dict(
        title="Can the Messenger Get Through?",
        text="Towns are joined by two-way roads. A messenger leaves the source town; every town they reach sends riders "
             "down each unvisited road, and green towns have been reached.",
        goal="Return true if the destination can be reached from the source.",
    ),
    spec=dict(method="validPath", ret="bool", params=[["int", "n"], ["vector<vector<int>>&", "edges"], ["int", "source"], ["int", "destination"]]),
    tests=[dict(args=[3, [[0, 1], [1, 2], [2, 0]], 0, 2], expected=True),
           dict(args=[6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5], expected=False),
           dict(args=[6, [[0, 1], [1, 2], [2, 5], [0, 3], [3, 4]], 0, 5], expected=True)],
    visualTest=2,
    scene=dict(theme="forest", layers=[
        dict(kind="graph", edges="edges", n="n", state="seen", pointers=["u"], label="towns"),
        dict(kind="queue", var="q", label="messengers"),
    ]),
    reference="""class Solution {
public:
    bool validPath(int n, vector<vector<int>>& edges, int source, int destination) {
        vector<vector<int>> adj(n);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }
        vector<int> seen(n, 0);
        queue<int> q;
        q.push(source);
        seen[source] = 2;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            if (u == destination) return true;
            for (int v : adj[u]) {
                if (!seen[v]) {
                    seen[v] = 2;
                    q.push(v);
                }
            }
        }
        return false;
    }
};""",
)

add(
    id=90, slug="subsets-ii", title="Subsets II", difficulty="Medium", world="backtracking",
    tags=["array", "backtracking", "bit-manipulation"],
    story=dict(
        title="Packing with Twins",
        text="Some items in the cupboard are identical twins. Sorted side by side, the packer only tries a twin at a door "
             "if the first copy was tried at that same door, so no bag is packed twice.",
        goal="Return every distinct subset (any order).",
    ),
    spec=dict(method="subsetsWithDup", ret="vector<vector<int>>", params=[["vector<int>&", "nums"]]),
    compare="unordered-deep",
    tests=[dict(args=[[1, 2, 2]], expected=[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]), dict(args=[[0]], expected=[[], [0]])],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="items (sorted)", pointers=["start", "i"]),
        dict(kind="array", var="path", label="bag", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void go(vector<int>& nums, int start) {
        res.push_back(path);
        for (int i = start; i < (int)nums.size(); i++) {
            if (i > start && nums[i] == nums[i - 1]) continue;
            path.push_back(nums[i]);
            go(nums, i + 1);
            path.pop_back();
        }
    }
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        go(nums, 0);
        return res;
    }
};""",
)

add(
    id=118, slug="pascals-triangle", title="Pascal's Triangle", difficulty="Easy", world="dp",
    tags=["array", "dynamic-programming"],
    story=dict(
        title="The Stacked Hay Bales",
        text="Hay bales are stacked in a triangle. Every bale's number is the sum of the two bales it rests on, and the "
             "edges are always 1.",
        goal="Return the first numRows rows of the triangle.",
    ),
    spec=dict(method="generate", ret="vector<vector<int>>", params=[["int", "numRows"]]),
    tests=[dict(args=[5], expected=[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]), dict(args=[1], expected=[[1]])],
    scene=dict(theme="farm", layers=[dict(kind="grid", var="res", palette="dp", label="hay stack", pointers=[["i", "j"]])]),
    reference="""class Solution {
public:
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> res;
        for (int i = 0; i < numRows; i++) {
            res.push_back(vector<int>(i + 1, 1));
            for (int j = 1; j < i; j++) res[i][j] = res[i - 1][j - 1] + res[i - 1][j];
        }
        return res;
    }
};""",
)

add(
    id=152, slug="maximum-product-subarray", title="Maximum Product Subarray", difficulty="Medium", world="dp",
    tags=["array", "dynamic-programming"],
    story=dict(
        title="The Multiplying Chests",
        text="Chests multiply your gold, and negative ones flip it to debt. The explorer tracks both the best and the "
             "worst running product, since a second negative chest can turn the worst into the best.",
        goal="Return the largest product of any contiguous run of chests.",
    ),
    spec=dict(method="maxProduct", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[2, 3, -2, 4]], expected=6), dict(args=[[-2, 0, -1]], expected=0), dict(args=[[-2, 3, -4]], expected=24)],
    visualTest=2,
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="chests", pointers=["i"]),
        dict(kind="values", vars=["hi", "lo", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int hi = nums[0], lo = nums[0], best = nums[0];
        for (int i = 1; i < (int)nums.size(); i++) {
            int x = nums[i];
            if (x < 0) swap(hi, lo);
            hi = max(x, hi * x);
            lo = min(x, lo * x);
            best = max(best, hi);
        }
        return best;
    }
};""",
)

add(
    id=228, slug="summary-ranges", title="Summary Ranges", difficulty="Easy", world="intervals", tags=["array"],
    story=dict(
        title="Booking Blocks",
        text="A diary lists booked days in order. A clerk groups consecutive days into blocks like \"2->4\" and writes "
             "single days on their own.",
        goal="Return the smallest list of ranges covering every number.",
    ),
    spec=dict(method="summaryRanges", ret="vector<string>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[0, 1, 2, 4, 5, 7]], expected=["0->2", "4->5", "7"]), dict(args=[[0, 2, 3, 4, 6, 8, 9]], expected=["0", "2->4", "6", "8->9"]),
           dict(args=[[]], expected=[])],
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="nums", label="booked days", pointers=["start", "i"], window=["start", "i"]),
        dict(kind="array", var="res", label="blocks", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> summaryRanges(vector<int>& nums) {
        vector<string> res;
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            int start = i;
            while (i + 1 < n && nums[i + 1] == nums[i] + 1) i++;
            if (start == i) res.push_back(to_string(nums[i]));
            else res.push_back(to_string(nums[start]) + "->" + to_string(nums[i]));
        }
        return res;
    }
};""",
)

add(
    id=763, slug="partition-labels", title="Partition Labels", difficulty="Medium", world="greedy",
    tags=["hash-table", "two-pointers", "string", "greedy"],
    story=dict(
        title="Cutting the Ribbon",
        text="A ribbon of letters must be cut so each letter appears in only one piece. Lockers remember where each "
             "letter last appears; a cutter walks along stretching the piece to the furthest last-appearance, and cuts "
             "when they reach it.",
        goal="Return the sizes of the pieces, left to right.",
    ),
    spec=dict(method="partitionLabels", ret="vector<int>", params=[["string", "s"]]),
    tests=[dict(args=["ababcbacadefegdehijhklij"], expected=[9, 7, 8]), dict(args=["eccbbbbdec"], expected=[10])],
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="ribbon", pointers=["start", "i", "end"], window=["start", "end"]),
        dict(kind="map", var="last", label="last seen at"),
        dict(kind="array", var="res", label="pieces", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> partitionLabels(string s) {
        map<char, int> last;
        for (int i = 0; i < (int)s.size(); i++) last[s[i]] = i;
        vector<int> res;
        int start = 0, end = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            end = max(end, last[s[i]]);
            if (i == end) {
                res.push_back(end - start + 1);
                start = i + 1;
            }
        }
        return res;
    }
};""",
)

add(
    id=461, slug="hamming-distance", title="Hamming Distance", difficulty="Easy", world="bits", tags=["bit-manipulation"],
    story=dict(
        title="Two Lamp Rows",
        text="Two rows of lamps show two numbers. XOR lights only the lamps where the rows disagree; then switch those "
             "off one at a time and count.",
        goal="Return how many bit positions differ between x and y.",
    ),
    spec=dict(method="hammingDistance", ret="int", params=[["int", "x"], ["int", "y"]]),
    tests=[dict(args=[1, 4], expected=2), dict(args=[3, 1], expected=1), dict(args=[93, 73], expected=2)],
    visualTest=2,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["x", "y", "diff", "count"])]),
    reference="""class Solution {
public:
    int hammingDistance(int x, int y) {
        int diff = x ^ y, count = 0;
        while (diff) {
            diff &= diff - 1;
            count++;
        }
        return count;
    }
};""",
)
