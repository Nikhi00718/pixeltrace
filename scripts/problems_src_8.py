"""Eighth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=1365, slug="how-many-numbers-are-smaller-than-the-current-number", title="How Many Numbers Are Smaller Than the Current Number",
    difficulty="Easy", world="arrays", tags=["array", "hash-table", "sorting", "counting"],
    story=dict(
        title="Ranking the Runners",
        text="Runners' times are sorted in a copy of the list. The first place each time shows up in the sorted copy is "
             "how many runners were faster; lockers remember it for every time.",
        goal="For each number, return how many numbers are smaller than it.",
    ),
    spec=dict(method="smallerNumbersThanCurrent", ret="vector<int>", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[8, 1, 2, 2, 3]], expected=[4, 0, 1, 1, 3]), dict(args=[[6, 5, 4, 8]], expected=[2, 1, 0, 3]), dict(args=[[7, 7, 7, 7]], expected=[0, 0, 0, 0])],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="times", pointers=["i"]),
        dict(kind="array", var="sorted", label="sorted copy", style="tiles", pointers=["i"]),
        dict(kind="map", var="first", label="first seen at"),
    ]),
    reference="""class Solution {
public:
    vector<int> smallerNumbersThanCurrent(vector<int>& nums) {
        vector<int> sorted = nums;
        sort(sorted.begin(), sorted.end());
        map<int, int> first;
        for (int i = 0; i < (int)sorted.size(); i++) {
            if (!first.count(sorted[i])) first[sorted[i]] = i;
        }
        vector<int> res;
        for (int x : nums) res.push_back(first[x]);
        return res;
    }
};""",
)

add(
    id=1512, slug="number-of-good-pairs", title="Number of Good Pairs", difficulty="Easy", world="arrays",
    tags=["array", "hash-table", "math", "counting"],
    story=dict(
        title="Matching Socks",
        text="Socks come out of the dryer one by one. Each new sock pairs with every earlier sock of the same colour, so "
             "add the colour's count before bumping it.",
        goal="Return the number of pairs (i < j) with equal values.",
    ),
    spec=dict(method="numIdenticalPairs", ret="int", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 3, 1, 1, 3]], expected=4), dict(args=[[1, 1, 1, 1]], expected=6), dict(args=[[1, 2, 3]], expected=0)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="socks", pointers=["i"]),
        dict(kind="map", var="cnt", label="seen so far"),
        dict(kind="values", vars=["pairs"]),
    ]),
    reference="""class Solution {
public:
    int numIdenticalPairs(vector<int>& nums) {
        map<int, int> cnt;
        int pairs = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            pairs += cnt[nums[i]];
            cnt[nums[i]]++;
        }
        return pairs;
    }
};""",
)

add(
    id=1189, slug="maximum-number-of-balloons", title="Maximum Number of Balloons", difficulty="Easy", world="arrays",
    tags=["hash-table", "string", "counting"],
    story=dict(
        title="Spelling BALLOON",
        text="Letter tiles are counted into lockers. Each copy of the word needs one b, a and n, and two l and o; the "
             "scarcest letter decides how many words you can spell.",
        goal="Return how many times \"balloon\" can be formed.",
    ),
    spec=dict(method="maxNumberOfBalloons", ret="int", params=[["string", "text"]]),
    tests=[dict(args=["nlaebolko"], expected=1), dict(args=["loonbalxballpoon"], expected=2), dict(args=["leetcode"], expected=0)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="string", var="text", label="tiles"),
        dict(kind="map", var="cnt", label="letter counts"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int maxNumberOfBalloons(string text) {
        map<char, int> cnt;
        for (char c : text) cnt[c]++;
        int best = min({cnt['b'], cnt['a'], cnt['n']});
        best = min({best, cnt['l'] / 2, cnt['o'] / 2});
        return best;
    }
};""",
)

add(
    id=383, slug="ransom-note", title="Ransom Note", difficulty="Easy", world="arrays", tags=["hash-table", "string", "counting"],
    story=dict(
        title="Cutting Letters from the Magazine",
        text="Every letter cut from the magazine goes into the lockers. Then each letter of the note takes one from its "
             "locker; an empty locker means the note can't be made.",
        goal="Return true if the note can be built from the magazine's letters.",
    ),
    spec=dict(method="canConstruct", ret="bool", params=[["string", "ransomNote"], ["string", "magazine"]]),
    tests=[dict(args=["a", "b"], expected=False), dict(args=["aa", "ab"], expected=False), dict(args=["aab", "baa"], expected=True)],
    visualTest=2,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="ransomNote", label="note", pointers=["i"]),
        dict(kind="map", var="cnt", label="letters available"),
    ]),
    reference="""class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        map<char, int> cnt;
        for (char c : magazine) cnt[c]++;
        for (int i = 0; i < (int)ransomNote.size(); i++) {
            if (--cnt[ransomNote[i]] < 0) return false;
        }
        return true;
    }
};""",
)

add(
    id=290, slug="word-pattern", title="Word Pattern", difficulty="Easy", world="arrays", tags=["hash-table", "string"],
    story=dict(
        title="The Secret Code Book",
        text="Each pattern letter must stand for exactly one word and each word for one letter. Two locker walls keep the "
             "code in both directions; any clash breaks it.",
        goal="Return true if s follows the same pattern.",
    ),
    spec=dict(method="wordPattern", ret="bool", params=[["string", "pattern"], ["string", "s"]]),
    tests=[dict(args=["abba", "dog cat cat dog"], expected=True), dict(args=["abba", "dog cat cat fish"], expected=False),
           dict(args=["aaaa", "dog cat cat dog"], expected=False)],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="pattern", label="pattern", pointers=["i"]),
        dict(kind="array", var="words", label="words", style="tiles", pointers=["i"]),
        dict(kind="row", children=[dict(kind="map", var="pw", label="letter → word"), dict(kind="map", var="wp", label="word → letter")]),
    ]),
    reference="""class Solution {
public:
    bool wordPattern(string pattern, string s) {
        vector<string> words;
        string cur;
        for (char c : s) {
            if (c == ' ') {
                words.push_back(cur);
                cur.clear();
            } else {
                cur.push_back(c);
            }
        }
        words.push_back(cur);
        if (words.size() != pattern.size()) return false;
        map<char, string> pw;
        map<string, char> wp;
        for (int i = 0; i < (int)pattern.size(); i++) {
            char p = pattern[i];
            string& w = words[i];
            if (pw.count(p) && pw[p] != w) return false;
            if (wp.count(w) && wp[w] != p) return false;
            pw[p] = w;
            wp[w] = p;
        }
        return true;
    }
};""",
)

add(
    id=2486, slug="append-characters-to-string-to-make-subsequence", title="Append Characters to String to Make Subsequence",
    difficulty="Medium", world="two-pointers", tags=["two-pointers", "string", "greedy"],
    story=dict(
        title="Finishing the Secret Word",
        text="Read along s, matching as much of t in order as possible. Whatever part of t is left unmatched has to be "
             "glued onto the end.",
        goal="Return how many characters must be appended to s so t is a subsequence.",
    ),
    spec=dict(method="appendCharacters", ret="int", params=[["string", "s"], ["string", "t"]]),
    tests=[dict(args=["coaching", "coding"], expected=4), dict(args=["abcde", "a"], expected=0), dict(args=["z", "abcde"], expected=5)],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="s", pointers=["i"]),
        dict(kind="string", var="t", label="t", pointers=["j"]),
    ]),
    reference="""class Solution {
public:
    int appendCharacters(string s, string t) {
        int j = 0;
        for (int i = 0; i < (int)s.size() && j < (int)t.size(); i++) {
            if (s[i] == t[j]) j++;
        }
        return t.size() - j;
    }
};""",
)

add(
    id=1838, slug="frequency-of-the-most-frequent-element", title="Frequency of the Most Frequent Element", difficulty="Medium",
    world="sliding-window", tags=["array", "binary-search", "greedy", "sliding-window", "sorting", "prefix-sum"],
    story=dict(
        title="Levelling Up the Towers",
        text="You may add at most k bricks in total. On the sorted towers, the beam tries to raise every tower in the "
             "window to the tallest one on its right edge; if that needs more than k bricks, the left edge moves up.",
        goal="Return the largest number of equal towers you can make.",
    ),
    spec=dict(method="maxFrequency", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[1, 2, 4], 5], expected=3), dict(args=[[1, 4, 8, 13], 5], expected=2), dict(args=[[3, 9, 6], 2], expected=1)],
    visualTest=1,
    scene=dict(theme="city", layers=[
        dict(kind="bars", var="nums", label="towers (sorted)", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="values", vars=["k", "sum", "best"]),
    ]),
    reference="""class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        long long sum = 0;
        int l = 0, best = 0;
        for (int r = 0; r < (int)nums.size(); r++) {
            sum += nums[r];
            while ((long long)nums[r] * (r - l + 1) - sum > k) {
                sum -= nums[l];
                l++;
            }
            best = max(best, r - l + 1);
        }
        return best;
    }
};""",
)

add(
    id=904, slug="fruit-into-baskets", title="Fruit Into Baskets", difficulty="Medium", world="sliding-window",
    tags=["array", "hash-table", "sliding-window"],
    story=dict(
        title="Two Baskets Only",
        text="Walking along a row of trees you may carry only two kinds of fruit. The picking window grows to the right; "
             "a third kind makes the left edge drop trees until only two kinds remain.",
        goal="Return the most fruit you can pick.",
    ),
    spec=dict(method="totalFruit", ret="int", params=[["vector<int>&", "fruits"]]),
    tests=[dict(args=[[1, 2, 1]], expected=3), dict(args=[[0, 1, 2, 2]], expected=3), dict(args=[[1, 2, 3, 2, 2]], expected=4), dict(args=[[3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]], expected=5)],
    visualTest=3,
    scene=dict(theme="forest", layers=[
        dict(kind="array", var="fruits", label="trees", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="map", var="basket", label="baskets"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        map<int, int> basket;
        int l = 0, best = 0;
        for (int r = 0; r < (int)fruits.size(); r++) {
            basket[fruits[r]]++;
            while (basket.size() > 2) {
                if (--basket[fruits[l]] == 0) basket.erase(fruits[l]);
                l++;
            }
            best = max(best, r - l + 1);
        }
        return best;
    }
};""",
)

add(
    id=1700, slug="number-of-students-unable-to-eat-lunch", title="Number of Students Unable to Eat Lunch", difficulty="Easy",
    world="stack", tags=["array", "stack", "queue", "simulation"],
    story=dict(
        title="The Sandwich Line",
        text="Students queue for a stack of sandwiches (0 round, 1 square). The front student takes the top sandwich if "
             "they like it; otherwise they walk to the back. If a full trip round the line gets nobody fed, the rest "
             "go hungry.",
        goal="Return how many students cannot eat.",
    ),
    spec=dict(method="countStudents", ret="int", params=[["vector<int>&", "students"], ["vector<int>&", "sandwiches"]]),
    tests=[dict(args=[[1, 1, 0, 0], [0, 1, 0, 1]], expected=0), dict(args=[[1, 1, 1, 0, 0, 1], [1, 0, 0, 0, 1, 1]], expected=3)],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="queue", var="q", label="student line"),
        dict(kind="array", var="sandwiches", label="sandwich stack (top first)", style="tiles", pointers=["top"]),
        dict(kind="values", vars=["misses"]),
    ]),
    reference="""class Solution {
public:
    int countStudents(vector<int>& students, vector<int>& sandwiches) {
        queue<int> q;
        for (int s : students) q.push(s);
        int top = 0, misses = 0;
        while (!q.empty() && misses < (int)q.size()) {
            int s = q.front();
            q.pop();
            if (s == sandwiches[top]) {
                top++;
                misses = 0;
            } else {
                q.push(s);
                misses++;
            }
        }
        return q.size();
    }
};""",
)

add(
    id=1475, slug="final-prices-with-a-special-discount-in-a-shop", title="Final Prices With a Special Discount in a Shop",
    difficulty="Easy", world="stack", tags=["array", "stack", "monotonic-stack"],
    story=dict(
        title="The Next Cheaper Item",
        text="Each item is discounted by the price of the next item to its right that costs no more. Items still waiting "
             "for their discount sit on a tower until a cheap enough item arrives.",
        goal="Return the final prices after discounts.",
    ),
    spec=dict(method="finalPrices", ret="vector<int>", params=[["vector<int>&", "prices"]]),
    tests=[dict(args=[[8, 4, 6, 2, 3]], expected=[4, 2, 4, 2, 3]), dict(args=[[1, 2, 3, 4, 5]], expected=[1, 2, 3, 4, 5]), dict(args=[[10, 1, 1, 6]], expected=[9, 0, 1, 6])],
    scene=dict(theme="market", layers=[
        dict(kind="bars", var="prices", label="prices", pointers=["i"]),
        dict(kind="stack", var="st", label="waiting (index)"),
    ]),
    reference="""class Solution {
public:
    vector<int> finalPrices(vector<int>& prices) {
        stack<int> st;
        for (int i = 0; i < (int)prices.size(); i++) {
            while (!st.empty() && prices[st.top()] >= prices[i]) {
                prices[st.top()] -= prices[i];
                st.pop();
            }
            st.push(i);
        }
        return prices;
    }
};""",
)

add(
    id=852, slug="peak-index-in-a-mountain-array", title="Peak Index in a Mountain Array", difficulty="Medium", world="binary-search",
    tags=["array", "binary-search"],
    story=dict(
        title="Finding the Summit in Fog",
        text="The trail only climbs and then only descends. A hiker checks whether the ground still rises to the right of "
             "the middle point and halves the trail toward the summit.",
        goal="Return the index of the peak.",
    ),
    spec=dict(method="peakIndexInMountainArray", ret="int", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[0, 1, 0]], expected=1), dict(args=[[0, 2, 1, 0]], expected=1), dict(args=[[0, 10, 5, 2]], expected=1), dict(args=[[1, 3, 5, 8, 12, 9, 4, 2]], expected=4)],
    visualTest=3,
    scene=dict(theme="forest", layers=[dict(kind="bars", var="arr", label="trail", pointers=["lo", "mid", "hi"], window=["lo", "hi"])]),
    reference="""class Solution {
public:
    int peakIndexInMountainArray(vector<int>& arr) {
        int lo = 0, hi = arr.size() - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] < arr[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
};""",
)

add(
    id=1351, slug="count-negative-numbers-in-a-sorted-matrix", title="Count Negative Numbers in a Sorted Matrix", difficulty="Easy",
    world="binary-search", tags=["array", "binary-search", "matrix"],
    story=dict(
        title="The Staircase Walk",
        text="Rows and columns both decrease. Start in the bottom-left corner: a negative tile means the rest of that row "
             "is negative too, so count it and go up; otherwise step right.",
        goal="Return how many negative numbers the grid holds.",
    ),
    spec=dict(method="countNegatives", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]]], expected=8), dict(args=[[[3, 2], [1, 0]]], expected=0)],
    scene=dict(theme="cave", layers=[
        dict(kind="grid", var="grid", palette="dp", label="grid", pointers=[["r", "c"]]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int countNegatives(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        int r = m - 1, c = 0, count = 0;
        while (r >= 0 && c < n) {
            if (grid[r][c] < 0) {
                count += n - c;
                r--;
            } else {
                c++;
            }
        }
        return count;
    }
};""",
)

add(
    id=1290, slug="convert-binary-number-in-a-linked-list-to-integer", title="Convert Binary Number in a Linked List to Integer",
    difficulty="Easy", world="linked-list", tags=["linked-list", "math"],
    story=dict(
        title="Reading the Signal Train",
        text="Each car carries one bit, most significant first. A clerk walks the train, doubling the running number and "
             "adding each car's bit.",
        goal="Return the number the bits spell.",
    ),
    spec=dict(method="getDecimalValue", ret="int", params=[["ListNode*", "head"]]),
    tests=[dict(args=[[1, 0, 1]], expected=5), dict(args=[[0]], expected=0), dict(args=[[1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]], expected=18880)],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "cur"], heads=["head"], label="signal train"),
        dict(kind="values", vars=["value"]),
    ]),
    reference="""class Solution {
public:
    int getDecimalValue(ListNode* head) {
        int value = 0;
        for (ListNode* cur = head; cur; cur = cur->next) value = value * 2 + cur->val;
        return value;
    }
};""",
)

add(
    id=86, slug="partition-list", title="Partition List", difficulty="Medium", world="linked-list", tags=["linked-list", "two-pointers"],
    story=dict(
        title="Light Cars to the Front",
        text="Cars lighter than x go to a front train, the rest to a back train, each keeping its order. Two couplers "
             "build the trains, then the back train is hooked behind the front one.",
        goal="Return the partitioned train.",
    ),
    spec=dict(method="partition", ret="ListNode*", params=[["ListNode*", "head"], ["int", "x"]]),
    tests=[dict(args=[[1, 4, 3, 2, 5, 2], 3], expected=[1, 2, 2, 4, 3, 5]), dict(args=[[2, 1], 2], expected=[1, 2])],
    scene=dict(theme="farm", layers=[
        dict(kind="list", vars=["head", "lowTail", "highTail"], heads=["head"], label="yard"),
        dict(kind="values", vars=["x"]),
    ]),
    reference="""class Solution {
public:
    ListNode* partition(ListNode* head, int x) {
        ListNode* low = new ListNode(0);
        ListNode* high = new ListNode(0);
        ListNode* lowTail = low;
        ListNode* highTail = high;
        while (head) {
            if (head->val < x) {
                lowTail->next = head;
                lowTail = head;
            } else {
                highTail->next = head;
                highTail = head;
            }
            head = head->next;
        }
        highTail->next = nullptr;
        lowTail->next = high->next;
        return low->next;
    }
};""",
)

add(
    id=222, slug="count-complete-tree-nodes", title="Count Complete Tree Nodes", difficulty="Easy", world="trees",
    tags=["binary-search", "bit-manipulation", "tree", "dfs"],
    story=dict(
        title="Counting the Fruit",
        text="A squirrel visits every fruit: each fruit reports one for itself plus whatever its two branches report.",
        goal="Return the number of nodes.",
    ),
    spec=dict(method="countNodes", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5, 6]], expected=6), dict(args=[[]], expected=0), dict(args=[[1]], expected=1)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["root"], label="orchard"),
        dict(kind="values", vars=["l", "r"]),
    ]),
    reference="""class Solution {
public:
    int countNodes(TreeNode* root) {
        if (!root) return 0;
        int l = countNodes(root->left);
        int r = countNodes(root->right);
        return 1 + l + r;
    }
};""",
    hints=["There is an O(log² n) trick using the tree's completeness: compare the leftmost and rightmost depths."],
)

add(
    id=1302, slug="deepest-leaves-sum", title="Deepest Leaves Sum", difficulty="Medium", world="trees", tags=["tree", "bfs", "dfs"],
    story=dict(
        title="The Lowest Row's Harvest",
        text="Pickers harvest row by row, weighing each row's basket. Each new row's basket replaces the last one, so the "
             "final basket is the deepest row.",
        goal="Return the sum of the values on the deepest level.",
    ),
    spec=dict(method="deepestLeavesSum", ret="int", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5, None, 6, 7, None, None, None, None, 8]], expected=15), dict(args=[[6, 7, 8, 2, 7, 1, 3, 9, None, 1, 4, None, None, None, 5]], expected=19)],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="queue", var="q", label="pickers"),
        dict(kind="values", vars=["sum"]),
    ]),
    reference="""class Solution {
public:
    int deepestLeavesSum(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);
        int sum = 0;
        while (!q.empty()) {
            int sz = q.size();
            sum = 0;
            for (int k = 0; k < sz; k++) {
                TreeNode* node = q.front();
                q.pop();
                sum += node->val;
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
        }
        return sum;
    }
};""",
)

add(
    id=113, slug="path-sum-ii", title="Path Sum II", difficulty="Medium", world="trees", tags=["backtracking", "tree", "dfs"],
    story=dict(
        title="Every Exact-Weight Basket",
        text="This time the picker writes down every root-to-leaf path whose basket weighs exactly the target. They add "
             "each fruit to the basket going down and take it out coming back up.",
        goal="Return all root-to-leaf paths that sum to targetSum (any order).",
    ),
    spec=dict(method="pathSum", ret="vector<vector<int>>", params=[["TreeNode*", "root"], ["int", "targetSum"]]),
    compare="unordered",
    tests=[dict(args=[[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22], expected=[[5, 4, 11, 2], [5, 8, 4, 5]]), dict(args=[[1, 2, 3], 5], expected=[]),
           dict(args=[[1, 2], 0], expected=[])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="array", var="path", label="basket", style="tiles"),
        dict(kind="values", vars=["remain"]),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void walk(TreeNode* node, int remain) {
        if (!node) return;
        path.push_back(node->val);
        remain -= node->val;
        if (!node->left && !node->right && remain == 0) res.push_back(path);
        walk(node->left, remain);
        walk(node->right, remain);
        path.pop_back();
    }
    vector<vector<int>> pathSum(TreeNode* root, int targetSum) {
        walk(root, targetSum);
        return res;
    }
};""",
)

add(
    id=463, slug="island-perimeter", title="Island Perimeter", difficulty="Easy", world="graphs", tags=["array", "dfs", "bfs", "matrix"],
    story=dict(
        title="Fencing the Island",
        text="Every land tile has four sides of fence. Each time two land tiles touch, the fence between them comes down "
             "on both sides, so subtract two.",
        goal="Return the island's perimeter.",
    ),
    spec=dict(method="islandPerimeter", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]], expected=16), dict(args=[[[1]]], expected=4), dict(args=[[[1, 0]]], expected=4)],
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="grid", palette="islands", label="island", pointers=[["r", "c"]]),
        dict(kind="values", vars=["fence"]),
    ]),
    reference="""class Solution {
public:
    int islandPerimeter(vector<vector<int>>& grid) {
        int fence = 0;
        for (int r = 0; r < (int)grid.size(); r++) {
            for (int c = 0; c < (int)grid[0].size(); c++) {
                if (!grid[r][c]) continue;
                fence += 4;
                if (r > 0 && grid[r - 1][c]) fence -= 2;
                if (c > 0 && grid[r][c - 1]) fence -= 2;
            }
        }
        return fence;
    }
};""",
)

add(
    id=130, slug="surrounded-regions", title="Surrounded Regions", difficulty="Medium", world="graphs",
    tags=["array", "dfs", "bfs", "union-find", "matrix"],
    story=dict(
        title="Capturing the Trapped Camps",
        text="O camps touching the board's edge are safe, and so is anything connected to them. Scouts flood from every "
             "edge camp marking safe ones; every camp left unmarked is captured and turned to X.",
        goal="Capture every O region not connected to the border, in place.",
    ),
    spec=dict(method="solve", ret="void", params=[["vector<vector<char>>&", "board"]], output="param:0"),
    tests=[dict(args=[[["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]],
                expected=[["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]]),
           dict(args=[[["X"]]], expected=[["X"]])],
    scene=dict(theme="castle", layers=[dict(kind="grid", var="board", palette="board", label="board", pointers=[["r", "c"]])]),
    reference="""class Solution {
public:
    void mark(vector<vector<char>>& board, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)board.size() || c >= (int)board[0].size() || board[r][c] != 'O') return;
        board[r][c] = '#';
        mark(board, r + 1, c);
        mark(board, r - 1, c);
        mark(board, r, c + 1);
        mark(board, r, c - 1);
    }
    void solve(vector<vector<char>>& board) {
        int m = board.size(), n = board[0].size();
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                if (r == 0 || c == 0 || r == m - 1 || c == n - 1) mark(board, r, c);
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                board[r][c] = board[r][c] == '#' ? 'O' : 'X';
    }
};""",
)

add(
    id=131, slug="palindrome-partitioning", title="Palindrome Partitioning", difficulty="Medium", world="backtracking",
    tags=["string", "dynamic-programming", "backtracking"],
    story=dict(
        title="Cutting the Ribbon into Mirrors",
        text="A ribbon must be cut so every piece reads the same both ways. At each door the cutter tries every palindrome "
             "piece starting at the current position, goes deeper, then tapes it back.",
        goal="Return every way to cut s into palindromes (any order).",
    ),
    spec=dict(method="partition", ret="vector<vector<string>>", params=[["string", "s"]]),
    compare="unordered",
    tests=[dict(args=["aab"], expected=[["a", "a", "b"], ["aa", "b"]]), dict(args=["a"], expected=[["a"]])],
    scene=dict(theme="cave", layers=[
        dict(kind="string", var="s", label="ribbon", pointers=["start", "end"], window=["start", "end"]),
        dict(kind="array", var="path", label="pieces", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<string>> res;
    vector<string> path;
    bool mirror(string& s, int l, int r) {
        while (l < r) {
            if (s[l] != s[r]) return false;
            l++;
            r--;
        }
        return true;
    }
    void go(string& s, int start) {
        if (start == (int)s.size()) {
            res.push_back(path);
            return;
        }
        for (int end = start; end < (int)s.size(); end++) {
            if (!mirror(s, start, end)) continue;
            path.push_back(s.substr(start, end - start + 1));
            go(s, end + 1);
            path.pop_back();
        }
    }
    vector<vector<string>> partition(string s) {
        go(s, 0);
        return res;
    }
};""",
)

add(
    id=377, slug="combination-sum-iv", title="Combination Sum IV", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(
        title="Counting Every Order",
        text="Here different orders count as different ways. The ledger fills each amount by trying every coin as the "
             "last one dropped in, adding the ways to make the rest.",
        goal="Return the number of ordered combinations that add up to target.",
    ),
    spec=dict(method="combinationSum4", ret="int", params=[["vector<int>&", "nums"], ["int", "target"]]),
    tests=[dict(args=[[1, 2, 3], 4], expected=7), dict(args=[[9], 3], expected=0), dict(args=[[1, 2], 10], expected=89)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="nums", label="coins", pointers=["c"]),
        dict(kind="array", var="ways", label="ways per amount", style="tiles", pointers=["a"]),
    ]),
    reference="""class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        vector<unsigned long long> ways(target + 1, 0);
        ways[0] = 1;
        for (int a = 1; a <= target; a++) {
            for (int c = 0; c < (int)nums.size(); c++) {
                if (nums[c] <= a) ways[a] += ways[a - nums[c]];
            }
        }
        return ways[target];
    }
};""",
)

add(
    id=279, slug="perfect-squares", title="Perfect Squares", difficulty="Medium", world="dp", tags=["math", "dynamic-programming", "bfs"],
    story=dict(
        title="Square Paving Stones",
        text="A path is paved with square stones (1, 4, 9, …). The ledger records the fewest stones for every length, "
             "trying each square stone as the last one laid.",
        goal="Return the least number of perfect squares summing to n.",
    ),
    spec=dict(method="numSquares", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[12], expected=3), dict(args=[13], expected=2), dict(args=[1], expected=1)],
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="dp", label="fewest stones per length", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["s"]),
    ]),
    reference="""class Solution {
public:
    int numSquares(int n) {
        vector<int> dp(n + 1, INT_MAX);
        dp[0] = 0;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s * s <= i; s++) dp[i] = min(dp[i], dp[i - s * s] + 1);
        }
        return dp[n];
    }
};""",
)

add(
    id=1094, slug="car-pooling", title="Car Pooling", difficulty="Medium", world="intervals",
    tags=["array", "sorting", "heap", "simulation", "prefix-sum"],
    story=dict(
        title="The Shuttle Bus",
        text="Each trip boards some passengers at one stop and drops them at another. Lockers note how many get on or "
             "off at each stop; driving along, the bus adds them up and checks it never overflows.",
        goal="Return true if all trips fit within capacity.",
    ),
    spec=dict(method="carPooling", ret="bool", params=[["vector<vector<int>>&", "trips"], ["int", "capacity"]]),
    tests=[dict(args=[[[2, 1, 5], [3, 3, 7]], 4], expected=False), dict(args=[[[2, 1, 5], [3, 3, 7]], 5], expected=True), dict(args=[[[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11], expected=True)],
    visualTest=2,
    scene=dict(theme="city", layers=[
        dict(kind="array", var="trips", label="trips [people, from, to]", style="tiles"),
        dict(kind="map", var="change", label="change at stop"),
        dict(kind="values", vars=["onboard", "capacity"]),
    ]),
    reference="""class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        map<int, int> change;
        for (auto& t : trips) {
            change[t[1]] += t[0];
            change[t[2]] -= t[0];
        }
        int onboard = 0;
        for (auto& [stop, d] : change) {
            onboard += d;
            if (onboard > capacity) return false;
        }
        return true;
    }
};""",
)

add(
    id=1029, slug="two-city-scheduling", title="Two City Scheduling", difficulty="Medium", world="greedy", tags=["array", "greedy", "sorting"],
    story=dict(
        title="Splitting the Interviewers",
        text="Half the candidates must fly to city A and half to city B. Sort them by how much cheaper A is than B; the "
             "first half go to A and the rest to B.",
        goal="Return the minimum total flight cost.",
    ),
    spec=dict(method="twoCitySchedCost", ret="int", params=[["vector<vector<int>>&", "costs"]]),
    tests=[dict(args=[[[10, 20], [30, 200], [400, 50], [30, 20]]], expected=110), dict(args=[[[259, 770], [448, 54], [926, 667], [184, 139], [840, 118], [577, 469]]], expected=1859)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="costs", label="candidates [A, B] (sorted)", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int twoCitySchedCost(vector<vector<int>>& costs) {
        sort(costs.begin(), costs.end(), [](const vector<int>& a, const vector<int>& b) { return a[0] - a[1] < b[0] - b[1]; });
        int n = costs.size() / 2, total = 0;
        for (int i = 0; i < 2 * n; i++) total += i < n ? costs[i][0] : costs[i][1];
        return total;
    }
};""",
)

add(
    id=693, slug="binary-number-with-alternating-bits", title="Binary Number with Alternating Bits", difficulty="Easy",
    world="bits", tags=["bit-manipulation"],
    story=dict(
        title="The Blinking Lamp Row",
        text="Do the lamps alternate on, off, on…? Read the last lamp, shift right, and compare it with the next one; two "
             "neighbours the same breaks the pattern.",
        goal="Return true if n's bits alternate.",
    ),
    spec=dict(method="hasAlternatingBits", ret="bool", params=[["int", "n"]]),
    tests=[dict(args=[5], expected=True), dict(args=[7], expected=False), dict(args=[11], expected=False), dict(args=[170], expected=True)],
    visualTest=3,
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n", "last", "bit"])]),
    reference="""class Solution {
public:
    bool hasAlternatingBits(int n) {
        int last = n & 1;
        n >>= 1;
        while (n) {
            int bit = n & 1;
            if (bit == last) return false;
            last = bit;
            n >>= 1;
        }
        return true;
    }
};""",
)
