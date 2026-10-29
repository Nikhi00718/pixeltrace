"""Tenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=1748, slug="sum-of-unique-elements", title="Sum of Unique Elements", difficulty="Easy", world="arrays",
    tags=["array", "hash-table", "counting"],
    story=dict(
        title="One-of-a-Kind Coins",
        text="Coins go into lockers by value. Afterwards only the values that showed up exactly once are added to the "
             "collector's purse.",
        goal="Return the sum of the values that appear exactly once.",
    ),
    spec=dict(method="sumOfUnique", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 2]], expected=4), dict(args=[[1, 1, 1, 1, 1]], expected=0), dict(args=[[1, 2, 3, 4, 5]], expected=15)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="coins"),
        dict(kind="map", var="cnt", label="lockers"),
        dict(kind="values", vars=["sum"]),
    ]),
    reference="""class Solution {
public:
    int sumOfUnique(vector<int>& nums) {
        map<int, int> cnt;
        for (int x : nums) cnt[x]++;
        int sum = 0;
        for (auto& [v, c] : cnt) {
            if (c == 1) sum += v;
        }
        return sum;
    }
};""",
)

add(
    id=1295, slug="find-numbers-with-even-number-of-digits", title="Find Numbers with Even Number of Digits", difficulty="Easy",
    world="arrays", tags=["array", "math"],
    story=dict(
        title="Even-Length Tickets",
        text="A clerk counts the digits on each ticket by chopping off the last digit until nothing is left, and keeps "
             "the tickets with an even count.",
        goal="Return how many numbers have an even number of digits.",
    ),
    spec=dict(method="findNumbers", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[12, 345, 2, 6, 7896]], expected=2), dict(args=[[555, 901, 482, 1771]], expected=1)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="tickets", pointers=["i"]),
        dict(kind="values", vars=["x", "digits", "count"]),
    ]),
    reference="""class Solution {
public:
    int findNumbers(vector<int>& nums) {
        int count = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            int x = nums[i], digits = 0;
            while (x > 0) {
                x /= 10;
                digits++;
            }
            if (digits % 2 == 0) count++;
        }
        return count;
    }
};""",
)

add(
    id=1672, slug="richest-customer-wealth", title="Richest Customer Wealth", difficulty="Easy", world="arrays", tags=["array", "matrix"],
    story=dict(
        title="The Bank's Ledger",
        text="Each row of the ledger is one customer's bank accounts. A teller adds up each row and remembers the "
             "biggest total.",
        goal="Return the wealth of the richest customer.",
    ),
    spec=dict(method="maximumWealth", ret="int", params=[["vector<vector<int>>&", "accounts"]]),
    tests=[dict(args=[[[1, 2, 3], [3, 2, 1]]], expected=6), dict(args=[[[1, 5], [7, 3], [3, 5]]], expected=10), dict(args=[[[2, 8, 7], [7, 1, 3], [1, 9, 5]]], expected=17)],
    visualTest=2,
    scene=dict(theme="city", layers=[
        dict(kind="grid", var="accounts", palette="dp", label="ledger", pointers=[["i", "j"]]),
        dict(kind="values", vars=["sum", "best"]),
    ]),
    reference="""class Solution {
public:
    int maximumWealth(vector<vector<int>>& accounts) {
        int best = 0;
        for (int i = 0; i < (int)accounts.size(); i++) {
            int sum = 0;
            for (int j = 0; j < (int)accounts[i].size(); j++) sum += accounts[i][j];
            best = max(best, sum);
        }
        return best;
    }
};""",
)

add(
    id=2367, slug="number-of-arithmetic-triplets", title="Number of Arithmetic Triplets", difficulty="Easy", world="arrays",
    tags=["array", "hash-table", "two-pointers", "enumeration"],
    story=dict(
        title="Evenly Spaced Lanterns",
        text="Lanterns hang at increasing heights. For each lantern, check the lockers for lanterns exactly diff and 2·diff "
             "lower; if both exist, that's a triplet.",
        goal="Return how many triplets have equal spacing diff.",
    ),
    spec=dict(method="arithmeticTriplets", ret="int", params=[["vector<int>&", "nums"], ["int", "diff"]]),
    tests=[dict(args=[[0, 1, 4, 6, 7, 10], 3], expected=2), dict(args=[[4, 5, 6, 7, 8, 9], 2], expected=2)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="nums", label="lanterns", pointers=["i"]),
        dict(kind="set", var="seen", label="heights seen"),
        dict(kind="values", vars=["diff", "count"]),
    ]),
    reference="""class Solution {
public:
    int arithmeticTriplets(vector<int>& nums, int diff) {
        set<int> seen;
        int count = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (seen.count(nums[i] - diff) && seen.count(nums[i] - 2 * diff)) count++;
            seen.insert(nums[i]);
        }
        return count;
    }
};""",
)

add(
    id=2108, slug="find-first-palindromic-string-in-the-array", title="Find First Palindromic String in the Array", difficulty="Easy",
    world="two-pointers", tags=["array", "two-pointers", "string"],
    story=dict(
        title="The First Mirror Word",
        text="Scrolls are checked in order. On each, two readers walk in from both ends; the first scroll they agree on "
             "all the way through wins.",
        goal="Return the first palindrome, or an empty string.",
    ),
    spec=dict(method="firstPalindrome", ret="string", params=[["vector<string>&", "words"]]),
    tests=[dict(args=[["abc", "car", "ada", "racecar", "cool"]], expected="ada"), dict(args=[["notapalindrome", "racecar"]], expected="racecar"), dict(args=[["def", "ghi"]], expected="")],
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="words", label="scrolls", style="tiles", pointers=["k"]),
        dict(kind="string", var="w", label="checking", pointers=["l", "r"], window=["l", "r"]),
    ]),
    reference="""class Solution {
public:
    bool mirror(string& w) {
        int l = 0, r = w.size() - 1;
        while (l < r) {
            if (w[l] != w[r]) return false;
            l++;
            r--;
        }
        return true;
    }
    string firstPalindrome(vector<string>& words) {
        for (int k = 0; k < (int)words.size(); k++) {
            if (mirror(words[k])) return words[k];
        }
        return "";
    }
};""",
)

add(
    id=917, slug="reverse-only-letters", title="Reverse Only Letters", difficulty="Easy", world="two-pointers", tags=["two-pointers", "string"],
    story=dict(
        title="Leave the Punctuation Alone",
        text="Two painters walk in from both ends of a sign, skipping anything that isn't a letter, and swap the letters "
             "they stop on.",
        goal="Reverse only the letters, keeping other characters in place.",
    ),
    spec=dict(method="reverseOnlyLetters", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["ab-cd"], expected="dc-ba"), dict(args=["a-bC-dEf-ghIj"], expected="j-Ih-gfE-dCba"), dict(args=["Test1ng-Leet=code-Q!"], expected="Qedo1ct-eeLg=ntse-T!")],
    visualTest=1,
    scene=dict(theme="market", layers=[dict(kind="string", var="s", label="sign", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    string reverseOnlyLetters(string s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            if (!isalpha(s[l])) l++;
            else if (!isalpha(s[r])) r--;
            else {
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
    id=1876, slug="substrings-of-size-three-with-distinct-characters", title="Substrings of Size Three with Distinct Characters",
    difficulty="Easy", world="sliding-window", tags=["hash-table", "string", "sliding-window", "counting"],
    story=dict(
        title="Three Different Buoys",
        text="A beam exactly three buoys wide slides along the row. Every time the three buoys inside are all different "
             "colours, it counts one.",
        goal="Return how many length-3 substrings have no repeated letters.",
    ),
    spec=dict(method="countGoodSubstrings", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["xyzzaz"], expected=1), dict(args=["aababcabc"], expected=4)],
    visualTest=1,
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="buoys", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int countGoodSubstrings(string s) {
        int count = 0;
        for (int r = 2; r < (int)s.size(); r++) {
            int l = r - 2;
            if (s[l] != s[l + 1] && s[l] != s[r] && s[l + 1] != s[r]) count++;
        }
        return count;
    }
};""",
)

add(
    id=2269, slug="find-the-k-beauty-of-a-number", title="Find the K-Beauty of a Number", difficulty="Easy", world="sliding-window",
    tags=["math", "string", "sliding-window"],
    story=dict(
        title="Digit Windows",
        text="A window k digits wide slides along the number. Each window is read as a number; if it divides the "
             "original evenly (and isn't zero), it adds to the beauty.",
        goal="Return how many k-digit windows divide num.",
    ),
    spec=dict(method="divisorSubstrings", ret="int", params=[["int", "num"], ["int", "k"]]),
    tests=[dict(args=[240, 2], expected=2), dict(args=[430043, 2], expected=2)],
    visualTest=1,
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="digits", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["part", "beauty"]),
    ]),
    reference="""class Solution {
public:
    int divisorSubstrings(int num, int k) {
        string s = to_string(num);
        int beauty = 0;
        for (int r = k - 1; r < (int)s.size(); r++) {
            int l = r - k + 1;
            int part = stoi(s.substr(l, k));
            if (part != 0 && num % part == 0) beauty++;
        }
        return beauty;
    }
};""",
)

add(
    id=1544, slug="make-the-string-great", title="Make The String Great", difficulty="Easy", world="stack", tags=["string", "stack"],
    story=dict(
        title="Cancelling Opposite Cases",
        text="Letters stack up one by one. A letter that lands on the same letter in the opposite case (a on A, or A on "
             "a) cancels both out.",
        goal="Return the string after removing all such pairs.",
    ),
    spec=dict(method="makeGood", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["leEeetcode"], expected="leetcode"), dict(args=["abBAcC"], expected=""), dict(args=["s"], expected="s")],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="letters arriving", pointers=["i"]),
        dict(kind="stack", var="st", label="tower"),
    ]),
    reference="""class Solution {
public:
    string makeGood(string s) {
        string st;
        for (int i = 0; i < (int)s.size(); i++) {
            if (!st.empty() && st.back() != s[i] && tolower(st.back()) == tolower(s[i])) st.pop_back();
            else st.push_back(s[i]);
        }
        return st;
    }
};""",
)

add(
    id=1441, slug="build-an-array-with-stack-operations", title="Build an Array With Stack Operations", difficulty="Medium",
    world="stack", tags=["array", "stack", "simulation"],
    story=dict(
        title="Stacking Only the Right Crates",
        text="Crates numbered 1, 2, 3… come down a chute. Each one is pushed onto the stack; if it isn't wanted, it is "
             "popped straight off again, until the stack matches the target.",
        goal="Return the list of Push / Pop operations.",
    ),
    spec=dict(method="buildArray", ret="vector<string>", params=[["vector<int>&", "target"], ["int", "n"]]),
    tests=[dict(args=[[1, 3], 3], expected=["Push", "Push", "Pop", "Push"]), dict(args=[[1, 2, 3], 3], expected=["Push", "Push", "Push"]),
           dict(args=[[1, 2], 4], expected=["Push", "Push"])],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="target", label="target", pointers=["t"]),
        dict(kind="array", var="ops", label="operations", style="tiles"),
        dict(kind="values", vars=["x"]),
    ]),
    reference="""class Solution {
public:
    vector<string> buildArray(vector<int>& target, int n) {
        vector<string> ops;
        int t = 0;
        for (int x = 1; x <= n && t < (int)target.size(); x++) {
            ops.push_back("Push");
            if (target[t] == x) t++;
            else ops.push_back("Pop");
        }
        return ops;
    }
};""",
)

add(
    id=2529, slug="maximum-count-of-positive-integer-and-negative-integer", title="Maximum Count of Positive Integer and Negative Integer",
    difficulty="Easy", world="binary-search", tags=["array", "binary-search", "counting"],
    story=dict(
        title="Above and Below Sea Level",
        text="Depths are sorted. One guard finds where the zeros start, another where they end; everything before is "
             "below sea level and everything after is above.",
        goal="Return the larger of the negative count and the positive count.",
    ),
    spec=dict(method="maximumCount", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[-2, -1, -1, 1, 2, 3]], expected=3), dict(args=[[-3, -2, -1, 0, 0, 1, 2]], expected=3), dict(args=[[5, 20, 66, 1314]], expected=4)],
    visualTest=1,
    scene=dict(theme="dock", layers=[dict(kind="array", var="nums", label="depths", pointers=["lo", "mid", "hi"], window=["lo", "hi"], windowExclusive=True)]),
    reference="""class Solution {
public:
    int firstAtLeast(vector<int>& nums, int x) {
        int lo = 0, hi = nums.size();
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
    int maximumCount(vector<int>& nums) {
        int neg = firstAtLeast(nums, 0);
        int pos = nums.size() - firstAtLeast(nums, 1);
        return max(neg, pos);
    }
};""",
)

add(
    id=1385, slug="find-the-distance-value-between-two-arrays", title="Find the Distance Value Between Two Arrays", difficulty="Easy",
    world="binary-search", tags=["array", "two-pointers", "binary-search", "sorting"],
    story=dict(
        title="Keeping Your Distance",
        text="For each number in the first list, a guard binary-searches the sorted second list for its nearest "
             "neighbours. If none is within d, it counts.",
        goal="Return how many values in arr1 are farther than d from every value in arr2.",
    ),
    spec=dict(method="findTheDistanceValue", ret="int", params=[["vector<int>&", "arr1"], ["vector<int>&", "arr2"], ["int", "d"]]),
    tests=[dict(args=[[4, 5, 8], [10, 9, 1, 8], 2], expected=2), dict(args=[[1, 4, 2, 3], [-4, -3, 6, 10, 20, 30], 3], expected=2), dict(args=[[2, 1, 100, 3], [-5, -2, 10, -3, 7], 6], expected=1)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="arr1", label="first list", pointers=["i"]),
        dict(kind="array", var="arr2", label="second list (sorted)", pointers=["lo", "mid", "hi"], window=["lo", "hi"], windowExclusive=True),
        dict(kind="values", vars=["d", "count"]),
    ]),
    reference="""class Solution {
public:
    int findTheDistanceValue(vector<int>& arr1, vector<int>& arr2, int d) {
        sort(arr2.begin(), arr2.end());
        int count = 0, m = arr2.size();
        for (int i = 0; i < (int)arr1.size(); i++) {
            int lo = 0, hi = m;
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                if (arr2[mid] < arr1[i]) lo = mid + 1;
                else hi = mid;
            }
            bool far = true;
            if (lo < m && arr2[lo] - arr1[i] <= d) far = false;
            if (lo > 0 && arr1[i] - arr2[lo - 1] <= d) far = false;
            if (far) count++;
        }
        return count;
    }
};""",
)

add(
    id=2181, slug="merge-nodes-in-between-zeros", title="Merge Nodes in Between Zeros", difficulty="Medium", world="linked-list",
    tags=["linked-list", "simulation"],
    story=dict(
        title="Packing Cars Between Markers",
        text="Zero cars mark the edges of groups. A worker walks the train adding up each group's cargo, writing the "
             "total onto the next marker car and coupling the markers together.",
        goal="Return a train with one car per group holding the group's sum.",
    ),
    spec=dict(method="mergeNodes", ret="ListNode*", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[0, 3, 1, 0, 4, 5, 2, 0]], expected=[4, 11]), dict(args=[[0, 1, 0, 3, 0, 2, 2, 0]], expected=[1, 3, 4])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "tail", "cur"], heads=["head"], label="train"),
        dict(kind="values", vars=["sum"]),
    ]),
    reference="""class Solution {
public:
    ListNode* mergeNodes(ListNode* head) {
        ListNode* tail = head;
        ListNode* cur = head->next;
        int sum = 0;
        while (cur) {
            if (cur->val == 0) {
                tail->next = cur;
                tail = cur;
                tail->val = sum;
                sum = 0;
            } else {
                sum += cur->val;
            }
            cur = cur->next;
        }
        return head->next;
    }
};""",
)

add(
    id=725, slug="split-linked-list-in-parts", title="Split Linked List in Parts", difficulty="Medium", world="linked-list",
    tags=["linked-list"],
    story=dict(
        title="Dividing the Train",
        text="The train must be split into k shorter trains as evenly as possible, the first ones one car longer if "
             "needed. A worker counts the cars, then walks along uncoupling at each cut.",
        goal="Return the k parts (empty parts are null).",
    ),
    spec=dict(method="splitListToParts", ret="vector<ListNode*>", params=[["ListNode*", "head"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 3], 5], expected=[[1], [2], [3], [], []]), dict(args=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3], expected=[[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]])],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "cur"], heads=["head"], label="train"),
        dict(kind="values", vars=["n", "size", "part"]),
    ]),
    reference="""class Solution {
public:
    vector<ListNode*> splitListToParts(ListNode* head, int k) {
        int n = 0;
        for (ListNode* p = head; p; p = p->next) n++;
        vector<ListNode*> res(k, nullptr);
        ListNode* cur = head;
        for (int part = 0; part < k && cur; part++) {
            res[part] = cur;
            int size = n / k + (part < n % k ? 1 : 0);
            for (int s = 1; s < size; s++) cur = cur->next;
            ListNode* nxt = cur->next;
            cur->next = nullptr;
            cur = nxt;
        }
        return res;
    }
};""",
)

add(
    id=1022, slug="sum-of-root-to-leaf-binary-numbers", title="Sum of Root To Leaf Binary Numbers", difficulty="Easy", world="trees",
    tags=["tree", "dfs"],
    story=dict(
        title="Binary Trails",
        text="Every fruit is a 0 or 1. Climbing down, the squirrel shifts its number left and adds the fruit's bit; at "
             "each leaf the number joins the total.",
        goal="Return the sum of all root-to-leaf binary numbers.",
    ),
    spec=dict(method="sumRootToLeaf", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 0, 1, 0, 1, 0, 1]], expected=22), dict(args=[[0]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["cur", "total"]),
    ]),
    reference="""class Solution {
public:
    int total = 0;
    void walk(TreeNode* node, int cur) {
        if (!node) return;
        cur = cur * 2 + node->val;
        if (!node->left && !node->right) total += cur;
        walk(node->left, cur);
        walk(node->right, cur);
    }
    int sumRootToLeaf(TreeNode* root) {
        walk(root, 0);
        return total;
    }
};""",
)

add(
    id=965, slug="univalued-binary-tree", title="Univalued Binary Tree", difficulty="Easy", world="trees", tags=["tree", "dfs", "bfs"],
    story=dict(
        title="All the Same Fruit?",
        text="An inspector climbs every branch checking that each fruit has the same label as the one at the top.",
        goal="Return true if every node has the same value.",
    ),
    spec=dict(method="isUnivalTree", ret="bool", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 1, 1, 1, 1, None, 1]], expected=True), dict(args=[[2, 2, 2, 5, 2]], expected=False)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["want"]),
    ]),
    reference="""class Solution {
public:
    bool same(TreeNode* node, int want) {
        if (!node) return true;
        if (node->val != want) return false;
        return same(node->left, want) && same(node->right, want);
    }
    bool isUnivalTree(TreeNode* root) {
        return same(root, root->val);
    }
};""",
)

add(
    id=2331, slug="evaluate-boolean-binary-tree", title="Evaluate Boolean Binary Tree", difficulty="Easy", world="trees",
    tags=["tree", "dfs"],
    story=dict(
        title="The Logic Orchard",
        text="Leaves hold 0 (false) or 1 (true). Branch fruits are gates: 2 means OR, 3 means AND. Each gate asks both "
             "branches for their answer and combines them.",
        goal="Return the value at the root.",
    ),
    spec=dict(method="evaluateTree", ret="bool", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[2, 1, 3, None, None, 0, 1]], expected=True), dict(args=[[0]], expected=False), dict(args=[[3, 2, 1, 0, 0]], expected=False)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="logic orchard"),
        dict(kind="values", vars=["l", "r"]),
    ]),
    reference="""class Solution {
public:
    bool eval(TreeNode* node) {
        if (!node->left) return node->val == 1;
        bool l = eval(node->left);
        bool r = eval(node->right);
        return node->val == 2 ? (l || r) : (l && r);
    }
    bool evaluateTree(TreeNode* root) {
        return eval(root);
    }
};""",
)

add(
    id=2530, slug="maximal-score-after-applying-k-operations", title="Maximal Score After Applying K Operations", difficulty="Medium",
    world="heap", tags=["array", "greedy", "heap"],
    story=dict(
        title="Draining the Richest Wells",
        text="Each turn you draw all the water from the fullest well and it refills to a third of that (rounded up). The "
             "pyramid always keeps the fullest well on top.",
        goal="Return the most water collected in k turns.",
    ),
    spec=dict(method="maxKelements", ret="long long", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[10, 10, 10, 10, 10], 5], expected=50), dict(args=[[1, 10, 3, 3, 3], 3], expected=17)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="heap", var="pq", label="wells (fullest on top)", color="#5ad1ff"),
        dict(kind="values", vars=["k", "top", "score"]),
    ]),
    reference="""class Solution {
public:
    long long maxKelements(vector<int>& nums, int k) {
        priority_queue<int> pq(nums.begin(), nums.end());
        long long score = 0;
        while (k-- > 0) {
            int top = pq.top();
            pq.pop();
            score += top;
            pq.push((top + 2) / 3);
        }
        return score;
    }
};""",
)

add(
    id=1791, slug="find-center-of-star-graph", title="Find Center of Star Graph", difficulty="Easy", world="graphs", tags=["graph"],
    story=dict(
        title="The Hub Town",
        text="Every road touches the hub. So the hub is simply whichever town appears in both of the first two roads.",
        goal="Return the center of the star graph.",
    ),
    spec=dict(method="findCenter", ret="int", params=[["vector<vector<int>>&", "edges"]]),
    tests=[dict(args=[[[1, 2], [2, 3], [4, 2]]], expected=2), dict(args=[[[1, 2], [5, 1], [1, 3], [1, 4]]], expected=1)],
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="edges", label="roads", style="tiles"),
        dict(kind="values", vars=["a", "b"]),
    ]),
    reference="""class Solution {
public:
    int findCenter(vector<vector<int>>& edges) {
        int a = edges[0][0], b = edges[0][1];
        return (a == edges[1][0] || a == edges[1][1]) ? a : b;
    }
};""",
)

add(
    id=1254, slug="number-of-closed-islands", title="Number of Closed Islands", difficulty="Medium", world="graphs",
    tags=["array", "dfs", "bfs", "union-find", "matrix"],
    story=dict(
        title="Islands Surrounded by Sea",
        text="Here 0 is land and 1 is water. A surveyor floods every land patch; if the flood ever reaches the map's edge, "
             "that patch isn't closed. Patches that stay inside count.",
        goal="Return the number of closed islands.",
    ),
    spec=dict(method="closedIsland", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 0]]], expected=2),
           dict(args=[[[0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0]]], expected=1)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="grid", palette="dp", label="map (0 land, 1 sea, 2 explored)", pointers=[["r", "c"]]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    bool closed(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size()) return false;
        if (grid[r][c] != 0) return true;
        grid[r][c] = 2;
        bool a = closed(grid, r + 1, c);
        bool b = closed(grid, r - 1, c);
        bool d = closed(grid, r, c + 1);
        bool e = closed(grid, r, c - 1);
        return a && b && d && e;
    }
    int closedIsland(vector<vector<int>>& grid) {
        int count = 0;
        for (int r = 0; r < (int)grid.size(); r++)
            for (int c = 0; c < (int)grid[0].size(); c++)
                if (grid[r][c] == 0 && closed(grid, r, c)) count++;
        return count;
    }
};""",
)

add(
    id=1863, slug="sum-of-all-subset-xor-totals", title="Sum of All Subset XOR Totals", difficulty="Easy", world="backtracking",
    tags=["array", "math", "backtracking", "bit-manipulation", "combinatorics", "enumeration"],
    story=dict(
        title="Every Bag's Lamp Pattern",
        text="Behind each door you decide whether the next item goes in the bag; the bag's value is the XOR of what's "
             "inside. Every complete bag adds its value to the total.",
        goal="Return the sum of XOR totals over every subset.",
    ),
    spec=dict(method="subsetXORSum", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 3]], expected=6), dict(args=[[5, 1, 6]], expected=28), dict(args=[[3, 4, 5, 6, 7, 8]], expected=480)],
    visualTest=1,
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="nums", label="items", pointers=["i"]),
        dict(kind="values", vars=["cur", "total"]),
    ]),
    reference="""class Solution {
public:
    int total = 0;
    void go(vector<int>& nums, int i, int cur) {
        if (i == (int)nums.size()) {
            total += cur;
            return;
        }
        go(nums, i + 1, cur ^ nums[i]);
        go(nums, i + 1, cur);
    }
    int subsetXORSum(vector<int>& nums) {
        go(nums, 0, 0);
        return total;
    }
};""",
)

add(
    id=1025, slug="divisor-game", title="Divisor Game", difficulty="Easy", world="dp", tags=["math", "dynamic-programming", "brainteaser", "game-theory"],
    story=dict(
        title="The Shrinking Pile",
        text="Two players take turns picking a divisor x of the pile size and removing x stones. The ledger marks each "
             "pile size as a win if some move leaves the opponent on a losing size.",
        goal="Return true if the first player wins with n stones.",
    ),
    spec=dict(method="divisorGame", ret="bool", params=[["int", "n"]]),
    tests=[dict(args=[2], expected=True), dict(args=[3], expected=False), dict(args=[8], expected=True)],
    visualTest=2,
    scene=dict(theme="farm", layers=[dict(kind="array", var="win", label="winning pile sizes", style="tiles", pointers=["i", "x"])]),
    reference="""class Solution {
public:
    bool divisorGame(int n) {
        vector<bool> win(n + 1, false);
        for (int i = 2; i <= n; i++) {
            for (int x = 1; x < i; x++) {
                if (i % x == 0 && !win[i - x]) {
                    win[i] = true;
                    break;
                }
            }
        }
        return win[n];
    }
};""",
)

add(
    id=1646, slug="get-maximum-in-generated-array", title="Get Maximum in Generated Array", difficulty="Easy", world="dp",
    tags=["array", "simulation"],
    story=dict(
        title="The Growing Ledger",
        text="Each even slot copies the slot at half its index; each odd slot adds the two slots around its half. The "
             "farmer fills the ledger and keeps the biggest number.",
        goal="Return the maximum value of the generated array.",
    ),
    spec=dict(method="getMaximumGenerated", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[7], expected=3), dict(args=[2], expected=1), dict(args=[3], expected=2), dict(args=[15], expected=5)],
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="a", label="generated", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int getMaximumGenerated(int n) {
        if (n == 0) return 0;
        vector<int> a(n + 1, 0);
        a[1] = 1;
        int best = 1;
        for (int i = 2; i <= n; i++) {
            a[i] = i % 2 == 0 ? a[i / 2] : a[i / 2] + a[i / 2 + 1];
            best = max(best, a[i]);
        }
        return best;
    }
};""",
)

add(
    id=2144, slug="minimum-cost-of-buying-candies-with-discount", title="Minimum Cost of Buying Candies With Discount",
    difficulty="Easy", world="greedy", tags=["array", "greedy", "sorting"],
    story=dict(
        title="Buy Two, Get One Free",
        text="For every two candies bought, a third one no pricier is free. Sorted from most expensive, the shopper pays "
             "for two and takes the third free, over and over.",
        goal="Return the minimum total cost.",
    ),
    spec=dict(method="minimumCost", ret="int", params=[["vector<int>&", "cost"]]),
    tests=[dict(args=[[1, 2, 3]], expected=5), dict(args=[[6, 5, 7, 9, 2, 2]], expected=23), dict(args=[[5, 5]], expected=10)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="cost", label="candies (priciest first)", pointers=["i"]),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int minimumCost(vector<int>& cost) {
        sort(cost.rbegin(), cost.rend());
        int total = 0;
        for (int i = 0; i < (int)cost.size(); i++) {
            if (i % 3 != 2) total += cost[i];
        }
        return total;
    }
};""",
)

add(
    id=2220, slug="minimum-bit-flips-to-convert-number", title="Minimum Bit Flips to Convert Number", difficulty="Easy", world="bits",
    tags=["bit-manipulation"],
    story=dict(
        title="Rewiring the Lamp Row",
        text="XOR lights up exactly the lamps that differ between start and goal; switching them off one by one counts "
             "the flips needed.",
        goal="Return the number of bit flips to turn start into goal.",
    ),
    spec=dict(method="minBitFlips", ret="int", params=[["int", "start"], ["int", "goal"]]),
    tests=[dict(args=[10, 7], expected=3), dict(args=[3, 4], expected=3)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["start", "goal", "diff", "flips"])]),
    reference="""class Solution {
public:
    int minBitFlips(int start, int goal) {
        int diff = start ^ goal, flips = 0;
        while (diff) {
            diff &= diff - 1;
            flips++;
        }
        return flips;
    }
};""",
)
