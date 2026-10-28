"""Seventh batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=1929, slug="concatenation-of-array", title="Concatenation of Array", difficulty="Easy", world="arrays", tags=["array", "simulation"],
    story=dict(
        title="The Double Shipment",
        text="The warehouse ships every order twice. A clerk copies each crate into the first half of a new dock and "
             "again into the second half.",
        goal="Return the array followed by itself.",
    ),
    spec=dict(method="getConcatenation", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 1]], expected=[1, 2, 1, 1, 2, 1]), dict(args=[[1, 3, 2, 1]], expected=[1, 3, 2, 1, 1, 3, 2, 1])],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="order", pointers=["i"]),
        dict(kind="array", var="ans", label="double shipment", style="tiles", pointers=["i"]),
    ]),
    reference="""class Solution {
public:
    vector<int> getConcatenation(vector<int>& nums) {
        int n = nums.size();
        vector<int> ans(2 * n);
        for (int i = 0; i < n; i++) {
            ans[i] = nums[i];
            ans[i + n] = nums[i];
        }
        return ans;
    }
};""",
)

add(
    id=2215, slug="find-the-difference-of-two-arrays", title="Find the Difference of Two Arrays", difficulty="Easy", world="arrays",
    tags=["array", "hash-table"],
    story=dict(
        title="Two Collectors Compare",
        text="Two collectors put their stamps into locker walls. Then each walks their own wall listing every stamp the "
             "other one doesn't have.",
        goal="Return [stamps only in nums1, stamps only in nums2] (any order inside each list).",
    ),
    spec=dict(method="findDifference", ret="vector<vector<int>>", params=[["vector<int>&", "nums1"], ["vector<int>&", "nums2"]]),
    compare="unordered-deep",
    tests=[dict(args=[[1, 2, 3], [2, 4, 6]], expected=[[1, 3], [4, 6]]), dict(args=[[1, 2, 3, 3], [1, 1, 2, 2]], expected=[[3], []])],
    scene=dict(theme="market", layers=[
        dict(kind="row", children=[dict(kind="set", var="a", label="collector 1", lookup=["x"]), dict(kind="set", var="b", label="collector 2", lookup=["x"])]),
        dict(kind="row", children=[dict(kind="array", var="onlyA", label="only in 1", style="tiles"), dict(kind="array", var="onlyB", label="only in 2", style="tiles")]),
        dict(kind="values", vars=["x"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> findDifference(vector<int>& nums1, vector<int>& nums2) {
        set<int> a(nums1.begin(), nums1.end()), b(nums2.begin(), nums2.end());
        vector<int> onlyA, onlyB;
        for (int x : a) {
            if (!b.count(x)) onlyA.push_back(x);
        }
        for (int x : b) {
            if (!a.count(x)) onlyB.push_back(x);
        }
        return {onlyA, onlyB};
    }
};""",
)

add(
    id=1207, slug="unique-number-of-occurrences", title="Unique Number of Occurrences", difficulty="Easy", world="arrays",
    tags=["array", "hash-table"],
    story=dict(
        title="No Two Tallies Alike",
        text="A teacher tallies how often each sticker shows up, then checks the tallies themselves: if two stickers have "
             "the same count, the rule is broken.",
        goal="Return true if every value's count is different.",
    ),
    spec=dict(method="uniqueOccurrences", ret="bool", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[1, 2, 2, 1, 1, 3]], expected=True), dict(args=[[1, 2]], expected=False), dict(args=[[-3, 0, 1, -3, 1, 1, 1, -3, 10, 0]], expected=True)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="arr", label="stickers"),
        dict(kind="map", var="cnt", label="tallies"),
        dict(kind="set", var="seen", label="counts already used", lookup=["c"]),
    ]),
    reference="""class Solution {
public:
    bool uniqueOccurrences(vector<int>& arr) {
        map<int, int> cnt;
        for (int x : arr) cnt[x]++;
        set<int> seen;
        for (auto& [v, c] : cnt) {
            if (seen.count(c)) return false;
            seen.insert(c);
        }
        return true;
    }
};""",
)

add(
    id=1732, slug="find-the-highest-altitude", title="Find the Highest Altitude", difficulty="Easy", world="arrays", tags=["array", "prefix-sum"],
    story=dict(
        title="The Cyclist's Altimeter",
        text="A cyclist starts at sea level. Each leg of the ride changes the height by some gain; the altimeter keeps "
             "the running height and the highest point reached.",
        goal="Return the highest altitude reached.",
    ),
    spec=dict(method="largestAltitude", ret="int", params=[["vector<int>&", "gain"]]),
    tests=[dict(args=[[-5, 1, 5, 0, -7]], expected=1), dict(args=[[-4, -3, -2, -1, 4, 3, 2]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="gain", label="legs", pointers=["i"]),
        dict(kind="values", vars=["alt", "best"]),
    ]),
    reference="""class Solution {
public:
    int largestAltitude(vector<int>& gain) {
        int alt = 0, best = 0;
        for (int i = 0; i < (int)gain.size(); i++) {
            alt += gain[i];
            best = max(best, alt);
        }
        return best;
    }
};""",
)

add(
    id=1431, slug="kids-with-the-greatest-number-of-candies", title="Kids With the Greatest Number of Candies", difficulty="Easy",
    world="arrays", tags=["array"],
    story=dict(
        title="The Candy Bonus",
        text="Each kid holds some candies. For every kid, imagine giving them all the extra candies: would they then "
             "have at least as many as the richest kid?",
        goal="Return a true/false for each kid.",
    ),
    spec=dict(method="kidsWithCandies", ret="vector<bool>", params=[["vector<int>&", "candies"], ["int", "extraCandies"]]),
    tests=[dict(args=[[2, 3, 5, 1, 3], 3], expected=[True, True, True, False, True]), dict(args=[[4, 2, 1, 1, 2], 1], expected=[True, False, False, False, False])],
    scene=dict(theme="market", layers=[
        dict(kind="bars", var="candies", label="candies", pointers=["i"]),
        dict(kind="array", var="res", label="could be richest?", style="tiles"),
        dict(kind="values", vars=["most", "extraCandies"]),
    ]),
    reference="""class Solution {
public:
    vector<bool> kidsWithCandies(vector<int>& candies, int extraCandies) {
        int most = *max_element(candies.begin(), candies.end());
        vector<bool> res;
        for (int i = 0; i < (int)candies.size(); i++) res.push_back(candies[i] + extraCandies >= most);
        return res;
    }
};""",
)

add(
    id=1657, slug="determine-if-two-strings-are-close", title="Determine if Two Strings Are Close", difficulty="Medium",
    world="arrays", tags=["hash-table", "string", "sorting", "counting"],
    story=dict(
        title="Swap and Relabel",
        text="You may swap letters around, or swap two letters' identities everywhere. So two words are close if they "
             "use the same set of letters, and the lists of letter counts match once sorted.",
        goal="Return true if word1 can become word2.",
    ),
    spec=dict(method="closeStrings", ret="bool", params=[["string", "word1"], ["string", "word2"]]),
    tests=[dict(args=["abc", "bca"], expected=True), dict(args=["a", "aa"], expected=False), dict(args=["cabbba", "abbccc"], expected=True)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[dict(kind="map", var="a", label="word1 counts"), dict(kind="map", var="b", label="word2 counts")]),
        dict(kind="row", children=[dict(kind="array", var="ca", label="counts 1 (sorted)", style="tiles"), dict(kind="array", var="cb", label="counts 2 (sorted)", style="tiles")]),
    ]),
    reference="""class Solution {
public:
    bool closeStrings(string word1, string word2) {
        map<char, int> a, b;
        for (char c : word1) a[c]++;
        for (char c : word2) b[c]++;
        vector<int> ca, cb;
        for (auto& [c, n] : a) {
            if (!b.count(c)) return false;
            ca.push_back(n);
        }
        for (auto& [c, n] : b) {
            if (!a.count(c)) return false;
            cb.push_back(n);
        }
        sort(ca.begin(), ca.end());
        sort(cb.begin(), cb.end());
        return ca == cb;
    }
};""",
)

add(
    id=2352, slug="equal-row-and-column-pairs", title="Equal Row and Column Pairs", difficulty="Medium", world="arrays",
    tags=["array", "hash-table", "matrix", "simulation"],
    story=dict(
        title="Matching Rows and Columns",
        text="A tile mosaic is checked for rows that read exactly like some column. Every row is filed in the lockers; "
             "then each column is read top to bottom and looked up.",
        goal="Return how many (row, column) pairs are equal.",
    ),
    spec=dict(method="equalPairs", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[3, 2, 1], [1, 7, 6], [2, 7, 7]]], expected=1), dict(args=[[[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]], expected=3)],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="grid", var="grid", palette="dp", label="mosaic", pointers=[["r", "c"]]),
        dict(kind="array", var="col", label="column being read", style="tiles"),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int equalPairs(vector<vector<int>>& grid) {
        int n = grid.size(), count = 0;
        map<vector<int>, int> rows;
        for (int r = 0; r < n; r++) rows[grid[r]]++;
        for (int c = 0; c < n; c++) {
            vector<int> col;
            for (int r = 0; r < n; r++) col.push_back(grid[r][c]);
            if (rows.count(col)) count += rows[col];
        }
        return count;
    }
};""",
)

add(
    id=345, slug="reverse-vowels-of-a-string", title="Reverse Vowels of a String", difficulty="Easy", world="two-pointers",
    tags=["two-pointers", "string"],
    story=dict(
        title="The Vowel Swap",
        text="Two painters walk in from both ends of a sign, skipping consonants. Whenever both stand on a vowel, they "
             "swap tiles and step inward.",
        goal="Reverse only the vowels of s.",
    ),
    spec=dict(method="reverseVowels", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["IceCreAm"], expected="AceCreIm"), dict(args=["leetcode"], expected="leotcede")],
    visualTest=1,
    scene=dict(theme="market", layers=[dict(kind="string", var="s", label="sign", pointers=["l", "r"], window=["l", "r"])]),
    reference="""class Solution {
public:
    bool vowel(char c) {
        c = tolower(c);
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }
    string reverseVowels(string s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            if (!vowel(s[l])) l++;
            else if (!vowel(s[r])) r--;
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
    id=151, slug="reverse-words-in-a-string", title="Reverse Words in a String", difficulty="Medium", world="two-pointers",
    tags=["two-pointers", "string"],
    story=dict(
        title="Reading the Sign Backwards",
        text="A messy sign has words with extra spaces between them. A reader picks out each word, files it on a shelf, "
             "then reads the shelf from the end, with single spaces between.",
        goal="Return the words in reverse order, separated by single spaces.",
    ),
    spec=dict(method="reverseWords", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["the sky is blue"], expected="blue is sky the"), dict(args=["  hello world  "], expected="world hello"),
           dict(args=["a good   example"], expected="example good a")],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="sign", pointers=["i", "j"], window=["i", "j"], windowExclusive=True),
        dict(kind="array", var="words", label="words found", style="tiles"),
        dict(kind="values", vars=["res"]),
    ]),
    reference="""class Solution {
public:
    string reverseWords(string s) {
        vector<string> words;
        int n = s.size(), i = 0;
        while (i < n) {
            while (i < n && s[i] == ' ') i++;
            if (i >= n) break;
            int j = i;
            while (j < n && s[j] != ' ') j++;
            words.push_back(s.substr(i, j - i));
            i = j;
        }
        string res;
        for (int k = words.size() - 1; k >= 0; k--) {
            res += words[k];
            if (k) res += ' ';
        }
        return res;
    }
};""",
)

add(
    id=443, slug="string-compression", title="String Compression", difficulty="Medium", world="two-pointers",
    tags=["two-pointers", "string"],
    story=dict(
        title="Packing the Letter Tiles",
        text="Runs of the same letter are packed as the letter followed by its count. A reader walks each run, and a "
             "writer packs the result into the front of the same row of tiles.",
        goal="Compress in place and return the new length.",
    ),
    spec=dict(method="compress", ret="int", params=[["vector<char>&", "chars"]]),
    tests=[dict(args=[["a", "a", "b", "b", "c", "c", "c"]], expected=6), dict(args=[["a"]], expected=1),
           dict(args=[["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]], expected=4)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="chars", label="tiles", style="letters", pointers=["w", "i", "j"]),
        dict(kind="values", vars=["run"]),
    ]),
    reference="""class Solution {
public:
    int compress(vector<char>& chars) {
        int n = chars.size(), w = 0, i = 0;
        while (i < n) {
            int j = i;
            while (j < n && chars[j] == chars[i]) j++;
            chars[w++] = chars[i];
            int run = j - i;
            if (run > 1) {
                string digits = to_string(run);
                for (char d : digits) chars[w++] = d;
            }
            i = j;
        }
        return w;
    }
};""",
)

add(
    id=2130, slug="maximum-twin-sum-of-a-linked-list", title="Maximum Twin Sum of a Linked List", difficulty="Medium",
    world="linked-list", tags=["linked-list", "two-pointers", "stack"],
    story=dict(
        title="Twin Cars",
        text="Car i and car n-1-i are twins. Find the middle with a tortoise and hare, turn the back half around, then "
             "walk both halves together adding twins.",
        goal="Return the largest twin sum.",
    ),
    spec=dict(method="pairSum", ret="int", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[5, 4, 2, 1]], expected=6), dict(args=[[4, 2, 2, 3]], expected=7), dict(args=[[1, 100000]], expected=100001)],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "slow", "fast", "prev", "a", "b"], heads=["head"], label="train"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int pairSum(ListNode* head) {
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
        int best = 0;
        ListNode* a = head;
        ListNode* b = prev;
        while (b) {
            best = max(best, a->val + b->val);
            a = a->next;
            b = b->next;
        }
        return best;
    }
};""",
)

add(
    id=605, slug="can-place-flowers", title="Can Place Flowers", difficulty="Easy", world="greedy", tags=["array", "greedy"],
    story=dict(
        title="Planting Without Crowding",
        text="Flowers can't be planted next to each other. A gardener walks the bed and plants in every empty plot whose "
             "neighbours are both empty, as early as possible.",
        goal="Return true if n new flowers fit.",
    ),
    spec=dict(method="canPlaceFlowers", ret="bool", params=[["vector<int>&", "flowerbed"], ["int", "n"]]),
    tests=[dict(args=[[1, 0, 0, 0, 1], 1], expected=True), dict(args=[[1, 0, 0, 0, 1], 2], expected=False), dict(args=[[0, 0, 1, 0, 0, 0, 0], 3], expected=True)],
    visualTest=2,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="flowerbed", label="flower bed", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["n"]),
    ]),
    reference="""class Solution {
public:
    bool canPlaceFlowers(vector<int>& flowerbed, int n) {
        int m = flowerbed.size();
        for (int i = 0; i < m && n > 0; i++) {
            bool leftFree = i == 0 || flowerbed[i - 1] == 0;
            bool rightFree = i == m - 1 || flowerbed[i + 1] == 0;
            if (flowerbed[i] == 0 && leftFree && rightFree) {
                flowerbed[i] = 1;
                n--;
            }
        }
        return n == 0;
    }
};""",
)

add(
    id=649, slug="dota2-senate", title="Dota2 Senate", difficulty="Medium", world="greedy", tags=["string", "greedy", "queue"],
    story=dict(
        title="The Senate Round Table",
        text="Two parties wait in queues by seat number. Whoever sits earlier bans the other party's next senator and "
             "rejoins the back of the line for the next round; the party that runs out loses.",
        goal="Return the winning party, \"Radiant\" or \"Dire\".",
    ),
    spec=dict(method="predictPartyVictory", ret="string", params=[["string", "senate"]]),
    tests=[dict(args=["RD"], expected="Radiant"), dict(args=["RDD"], expected="Dire"), dict(args=["DRRDRDRDRDDRDRDR"])],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="senate", label="seats"),
        dict(kind="queue", var="r", label="Radiant queue"),
        dict(kind="queue", var="d", label="Dire queue"),
    ]),
    reference="""class Solution {
public:
    string predictPartyVictory(string senate) {
        int n = senate.size();
        queue<int> r, d;
        for (int i = 0; i < n; i++) {
            if (senate[i] == 'R') r.push(i);
            else d.push(i);
        }
        while (!r.empty() && !d.empty()) {
            int a = r.front(), b = d.front();
            r.pop();
            d.pop();
            if (a < b) r.push(a + n);
            else d.push(b + n);
        }
        return r.empty() ? "Dire" : "Radiant";
    }
};""",
)

add(
    id=2462, slug="total-cost-to-hire-k-workers", title="Total Cost to Hire K Workers", difficulty="Medium", world="heap",
    tags=["array", "two-pointers", "heap", "simulation"],
    story=dict(
        title="Hiring from Both Ends of the Line",
        text="Workers stand in a line. Each round, the cheapest of the first few and last few candidates is hired "
             "(ties go to the lower index), and the next person from that end joins their pyramid.",
        goal="Return the total cost of hiring k workers.",
    ),
    spec=dict(method="totalCost", ret="long long", params=[["vector<int>&", "costs"], ["int", "k"], ["int", "candidates"]]),
    tests=[dict(args=[[17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4], expected=11), dict(args=[[1, 2, 4, 1], 3, 3], expected=4)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="costs", label="line of workers", pointers=["i", "j"]),
        dict(kind="row", children=[
            dict(kind="heap", var="left", label="front pyramid"),
            dict(kind="heap", var="right", label="back pyramid"),
        ]),
        dict(kind="values", vars=["k", "total"]),
    ]),
    reference="""class Solution {
public:
    long long totalCost(vector<int>& costs, int k, int candidates) {
        priority_queue<int, vector<int>, greater<int>> left, right;
        int i = 0, j = costs.size() - 1;
        long long total = 0;
        while (k-- > 0) {
            while ((int)left.size() < candidates && i <= j) left.push(costs[i++]);
            while ((int)right.size() < candidates && i <= j) right.push(costs[j--]);
            int a = left.empty() ? INT_MAX : left.top();
            int b = right.empty() ? INT_MAX : right.top();
            if (a <= b) {
                total += a;
                left.pop();
            } else {
                total += b;
                right.pop();
            }
        }
        return total;
    }
};""",
)

add(
    id=1268, slug="search-suggestions-system", title="Search Suggestions System", difficulty="Medium", world="binary-search",
    tags=["array", "string", "binary-search", "trie", "sorting"],
    story=dict(
        title="The Autocomplete Shelf",
        text="Products are sorted on a shelf. As each letter is typed, a guard binary-searches for the first product "
             "starting with what has been typed so far and suggests up to three that match.",
        goal="Return the suggestions after each typed letter.",
    ),
    spec=dict(method="suggestedProducts", ret="vector<vector<string>>", params=[["vector<string>&", "products"], ["string", "searchWord"]]),
    tests=[dict(args=[["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"],
                expected=[["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"], ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]),
           dict(args=[["havana"], "tatiana"], expected=[[], [], [], [], [], [], []])],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="products", label="shelf (sorted)", style="tiles", pointers=["lo", "k"]),
        dict(kind="values", vars=["prefix"]),
        dict(kind="array", var="pick", label="suggestions", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        sort(products.begin(), products.end());
        vector<vector<string>> res;
        string prefix;
        for (char c : searchWord) {
            prefix += c;
            int lo = lower_bound(products.begin(), products.end(), prefix) - products.begin();
            vector<string> pick;
            for (int k = lo; k < (int)products.size() && (int)pick.size() < 3; k++) {
                if (products[k].compare(0, prefix.size(), prefix) != 0) break;
                pick.push_back(products[k]);
            }
            res.push_back(pick);
        }
        return res;
    }
};""",
)

add(
    id=872, slug="leaf-similar-trees", title="Leaf-Similar Trees", difficulty="Easy", world="trees", tags=["tree", "dfs"],
    story=dict(
        title="Comparing the Bottom Fruit",
        text="Two orchards are leaf-similar if their bottom fruits, read left to right, are the same. A squirrel climbs "
             "each tree collecting its leaves into a basket, then the baskets are compared.",
        goal="Return true if both trees have the same leaf sequence.",
    ),
    spec=dict(method="leafSimilar", ret="bool", params=[["TreeNode*", "root1"], ["TreeNode*", "root2"]]),
    tests=[dict(args=[[3, 5, 1, 6, 2, 9, 8, None, None, 7, 4], [3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8]], expected=True),
           dict(args=[[1, 2, 3], [1, 3, 2]], expected=False)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="row", children=[
            dict(kind="tree", var="root1", pointers=["node"], label="orchard 1"),
            dict(kind="tree", var="root2", pointers=["node"], label="orchard 2"),
        ]),
        dict(kind="row", children=[dict(kind="array", var="a", label="leaves 1", style="tiles"), dict(kind="array", var="b", label="leaves 2", style="tiles")]),
    ]),
    reference="""class Solution {
public:
    void leaves(TreeNode* node, vector<int>& out) {
        if (!node) return;
        if (!node->left && !node->right) out.push_back(node->val);
        leaves(node->left, out);
        leaves(node->right, out);
    }
    bool leafSimilar(TreeNode* root1, TreeNode* root2) {
        vector<int> a, b;
        leaves(root1, a);
        leaves(root2, b);
        return a == b;
    }
};""",
)

add(
    id=1372, slug="longest-zigzag-path-in-a-binary-tree", title="Longest ZigZag Path in a Binary Tree", difficulty="Medium",
    world="trees", tags=["tree", "dfs", "dynamic-programming"],
    story=dict(
        title="The Zigzagging Squirrel",
        text="A squirrel likes to alternate: left, right, left… Going the same way twice resets the count. Every branch "
             "is told which way the squirrel arrived and how long its zigzag is so far.",
        goal="Return the length of the longest zigzag path.",
    ),
    spec=dict(method="longestZigZag", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1]], expected=3), dict(args=[[1, 1, 1, None, 1, None, None, 1, 1, None, 1]], expected=4),
           dict(args=[[1]], expected=0)],
    visualTest=1,
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["wentLeft", "len", "best"]),
    ]),
    reference="""class Solution {
public:
    int best = 0;
    void walk(TreeNode* node, bool wentLeft, int len) {
        if (!node) return;
        best = max(best, len);
        if (wentLeft) {
            walk(node->right, false, len + 1);
            walk(node->left, true, 1);
        } else {
            walk(node->left, true, len + 1);
            walk(node->right, false, 1);
        }
    }
    int longestZigZag(TreeNode* root) {
        walk(root->left, true, 1);
        walk(root->right, false, 1);
        return best;
    }
};""",
)

add(
    id=1161, slug="maximum-level-sum-of-a-binary-tree", title="Maximum Level Sum of a Binary Tree", difficulty="Medium",
    world="trees", tags=["tree", "bfs"],
    story=dict(
        title="The Heaviest Row",
        text="Pickers harvest the orchard row by row and weigh each row's basket. The first row with the heaviest basket "
             "wins.",
        goal="Return the smallest level number with the maximum sum.",
    ),
    spec=dict(method="maxLevelSum", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 7, 0, 7, -8, None, None]], expected=2), dict(args=[[989, None, 10250, 98693, -89388, None, None, None, -32127]], expected=2)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="pickers"),
        dict(kind="values", vars=["level", "sum", "bestSum", "bestLevel"]),
    ]),
    reference="""class Solution {
public:
    int maxLevelSum(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);
        int level = 0, bestLevel = 1;
        long long bestSum = LLONG_MIN;
        while (!q.empty()) {
            level++;
            int sz = q.size();
            long long sum = 0;
            for (int k = 0; k < sz; k++) {
                TreeNode* node = q.front();
                q.pop();
                sum += node->val;
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            if (sum > bestSum) {
                bestSum = sum;
                bestLevel = level;
            }
        }
        return bestLevel;
    }
};""",
)

add(
    id=450, slug="delete-node-in-a-bst", title="Delete Node in a BST", difficulty="Medium", world="trees", tags=["tree", "bst"],
    story=dict(
        title="Removing a Fruit Carefully",
        text="The gardener walks down to the fruit to remove. A leaf just drops off; a fruit with one branch is replaced "
             "by that branch; with two branches, it takes the value of the smallest fruit on its right and that one is "
             "removed instead.",
        goal="Delete key from the BST and return the root.",
    ),
    spec=dict(method="deleteNode", ret="TreeNode*", params=[["TreeNode*", "root"], ["int", "key"]]),
    tests=[dict(args=[[5, 3, 6, 2, 4, None, 7], 3], expected=[5, 4, 6, 2, None, None, 7]), dict(args=[[5, 3, 6, 2, 4, None, 7], 0], expected=[5, 3, 6, 2, 4, None, 7]),
           dict(args=[[], 0], expected=[])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["root", "succ"], label="orchard"),
        dict(kind="values", vars=["key"]),
    ]),
    reference="""class Solution {
public:
    TreeNode* deleteNode(TreeNode* root, int key) {
        if (!root) return nullptr;
        if (key < root->val) {
            root->left = deleteNode(root->left, key);
        } else if (key > root->val) {
            root->right = deleteNode(root->right, key);
        } else {
            if (!root->left) return root->right;
            if (!root->right) return root->left;
            TreeNode* succ = root->right;
            while (succ->left) succ = succ->left;
            root->val = succ->val;
            root->right = deleteNode(root->right, succ->val);
        }
        return root;
    }
};""",
    hints=["LeetCode accepts any valid BST after deletion; these tests expect the in-order-successor approach."],
)

add(
    id=1466, slug="reorder-routes-to-make-all-paths-lead-to-the-city-zero", title="Reorder Routes to Make All Paths Lead to the City Zero",
    difficulty="Medium", world="graphs", tags=["dfs", "bfs", "graph"],
    story=dict(
        title="Every Road to the Capital",
        text="One-way roads connect the towns as a tree. A surveyor walks out from the capital along every road; any "
             "road pointing away from the capital has to be flipped.",
        goal="Return the fewest roads to reverse so every town can reach town 0.",
    ),
    spec=dict(method="minReorder", ret="int", params=[["int", "n"], ["vector<vector<int>>&", "connections"]]),
    tests=[dict(args=[6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]], expected=3), dict(args=[5, [[1, 0], [1, 2], [3, 2], [3, 4]]], expected=2),
           dict(args=[3, [[1, 0], [2, 0]]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="graph", edges="connections", n="n", directed=True, state="seen", pointers=["u"], label="towns"),
        dict(kind="values", vars=["flips"]),
    ]),
    reference="""class Solution {
public:
    int minReorder(int n, vector<vector<int>>& connections) {
        vector<vector<pair<int, int>>> adj(n);
        for (auto& c : connections) {
            adj[c[0]].push_back({c[1], 1});
            adj[c[1]].push_back({c[0], 0});
        }
        vector<int> seen(n, 0);
        stack<int> st;
        st.push(0);
        seen[0] = 2;
        int flips = 0;
        while (!st.empty()) {
            int u = st.top();
            st.pop();
            for (auto& [v, away] : adj[u]) {
                if (seen[v]) continue;
                seen[v] = 2;
                flips += away;
                st.push(v);
            }
        }
        return flips;
    }
};""",
)

add(
    id=1557, slug="minimum-number-of-vertices-to-reach-all-nodes", title="Minimum Number of Vertices to Reach All Nodes",
    difficulty="Medium", world="graphs", tags=["graph"],
    story=dict(
        title="Where to Post the Heralds",
        text="Roads are one-way. A town that no road leads into can only be reached by starting there, and those towns "
             "are enough to reach everything else.",
        goal="Return every town with no incoming road.",
    ),
    spec=dict(method="findSmallestSetOfVertices", ret="vector<int>", params=[["int", "n"], ["vector<vector<int>>&", "edges"]]),
    compare="unordered",
    tests=[dict(args=[6, [[0, 1], [0, 2], [2, 5], [3, 4], [4, 2]]], expected=[0, 3]), dict(args=[5, [[0, 1], [2, 1], [3, 1], [1, 4], [2, 4]]], expected=[0, 2, 3])],
    scene=dict(theme="forest", layers=[
        dict(kind="graph", edges="edges", n="n", directed=True, state="indeg", label="towns"),
        dict(kind="array", var="res", label="post heralds at", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        vector<int> indeg(n, 0);
        for (auto& e : edges) indeg[e[1]]++;
        vector<int> res;
        for (int v = 0; v < n; v++) {
            if (indeg[v] == 0) res.push_back(v);
        }
        return res;
    }
};""",
)

add(
    id=790, slug="domino-and-tromino-tiling", title="Domino and Tromino Tiling", difficulty="Medium", world="dp",
    tags=["dynamic-programming"],
    story=dict(
        title="Tiling the Barn Floor",
        text="A 2-wide barn floor is tiled with dominoes and L-shaped trominoes. The farmer chalks how many ways each "
             "length can be tiled: dp[i] = 2·dp[i-1] + dp[i-3].",
        goal="Return the number of tilings of a 2 x n floor, modulo 1e9+7.",
    ),
    spec=dict(method="numTilings", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[3], expected=5), dict(args=[1], expected=1), dict(args=[30], expected=312342182), dict(args=[6], expected=53)],
    visualTest=3,
    scene=dict(theme="farm", layers=[dict(kind="array", var="dp", label="ways per length", style="tiles", pointers=["i"])]),
    reference="""class Solution {
public:
    int numTilings(int n) {
        const long long MOD = 1000000007;
        vector<long long> dp(max(n + 1, 4), 0);
        dp[0] = 1;
        dp[1] = 1;
        dp[2] = 2;
        for (int i = 3; i <= n; i++) dp[i] = (2 * dp[i - 1] + dp[i - 3]) % MOD;
        return dp[n];
    }
};""",
)

add(
    id=72, slug="edit-distance", title="Edit Distance", difficulty="Medium", world="dp", tags=["string", "dynamic-programming"],
    story=dict(
        title="Fixing the Copied Scroll",
        text="A scribe turns one word into another with inserts, deletes and replacements. Each cell of the grid holds "
             "the fewest edits between two prefixes: free if the letters match, otherwise one more than the cheapest "
             "neighbour.",
        goal="Return the minimum number of edits.",
    ),
    spec=dict(method="minDistance", ret="int", params=[["string", "word1"], ["string", "word2"]]),
    tests=[dict(args=["horse", "ros"], expected=3), dict(args=["intention", "execution"], expected=5), dict(args=["", "a"], expected=1)],
    scene=dict(theme="lab", layers=[
        dict(kind="row", children=[dict(kind="string", var="word1", label="word 1"), dict(kind="string", var="word2", label="word 2")]),
        dict(kind="grid", var="dp", palette="dp", label="edits table", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    int minDistance(string word1, string word2) {
        int n = word1.size(), m = word2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        for (int i = 0; i <= n; i++) dp[i][0] = i;
        for (int j = 0; j <= m; j++) dp[0][j] = j;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                if (word1[i - 1] == word2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
                else dp[i][j] = 1 + min({dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]});
            }
        }
        return dp[n][m];
    }
};""",
)

add(
    id=714, slug="best-time-to-buy-and-sell-stock-with-transaction-fee", title="Best Time to Buy and Sell Stock with Transaction Fee",
    difficulty="Medium", world="dp", tags=["array", "dynamic-programming", "greedy"],
    story=dict(
        title="Trading with a Toll",
        text="Every sale costs a fee. Each day the trader tracks two purses: the best cash if not holding a share, and "
             "the best value if holding one, switching only when it pays.",
        goal="Return the maximum profit.",
    ),
    spec=dict(method="maxProfit", ret="int", params=[["vector<int>&", "prices"], ["int", "fee"]]),
    tests=[dict(args=[[1, 3, 2, 8, 4, 9], 2], expected=8), dict(args=[[1, 3, 7, 5, 10, 3], 3], expected=6)],
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="prices", label="price towers", pointers=["i"]),
        dict(kind="values", vars=["cash", "hold", "fee"]),
    ]),
    reference="""class Solution {
public:
    int maxProfit(vector<int>& prices, int fee) {
        int cash = 0, hold = -prices[0];
        for (int i = 1; i < (int)prices.size(); i++) {
            cash = max(cash, hold + prices[i] - fee);
            hold = max(hold, cash - prices[i]);
        }
        return cash;
    }
};""",
)

add(
    id=1318, slug="minimum-flips-to-make-a-or-b-equal-to-c", title="Minimum Flips to Make a OR b Equal to c", difficulty="Medium",
    world="bits", tags=["bit-manipulation"],
    story=dict(
        title="Three Lamp Rows",
        text="Lamp rows a and b are OR-ed to light row c. Going lamp by lamp from the right: if c wants it off, every lit "
             "lamp in a and b must flip; if c wants it on and both are off, flip one.",
        goal="Return the fewest bit flips in a and b so that a OR b == c.",
    ),
    spec=dict(method="minFlips", ret="int", params=[["int", "a"], ["int", "b"], ["int", "c"]]),
    tests=[dict(args=[2, 6, 5], expected=3), dict(args=[4, 2, 7], expected=1), dict(args=[1, 2, 3], expected=0)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["a", "b", "c", "x", "y", "z", "flips"])]),
    reference="""class Solution {
public:
    int minFlips(int a, int b, int c) {
        int flips = 0;
        while (a || b || c) {
            int x = a & 1, y = b & 1, z = c & 1;
            if (z == 0) flips += x + y;
            else if (x == 0 && y == 0) flips += 1;
            a >>= 1;
            b >>= 1;
            c >>= 1;
        }
        return flips;
    }
};""",
)
