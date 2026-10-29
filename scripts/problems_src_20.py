"""Twentieth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=1122, slug="relative-sort-array", title="Relative Sort Array", difficulty="Easy", world="arrays", tags=["array", "hash-table", "sorting", "counting-sort"],
    story=dict(title="Sorting by the House Rules", text="Count every value. First pour out values in the order arr2 lists them, then everything else in ascending order.",
               goal="Return arr1 sorted relative to arr2."),
    spec=dict(method="relativeSortArray", ret="vector<int>", params=[["vector<int>&", "arr1"], ["vector<int>&", "arr2"]]),
    tests=[dict(args=[[2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]], expected=[2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19]), dict(args=[[28, 6, 22, 8, 44, 17], [22, 28, 8, 6]], expected=[22, 28, 8, 6, 17, 44])],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="map", var="cnt", label="counts"),
        dict(kind="array", var="res", label="sorted", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> relativeSortArray(vector<int>& arr1, vector<int>& arr2) {
        map<int, int> cnt;
        for (int x : arr1) cnt[x]++;
        vector<int> res;
        for (int x : arr2) {
            while (cnt[x]-- > 0) res.push_back(x);
            cnt.erase(x);
        }
        for (auto& [v, c] : cnt)
            while (c-- > 0) res.push_back(v);
        return res;
    }
};""",
)

add(
    id=1123, slug="lowest-common-ancestor-of-deepest-leaves", title="Lowest Common Ancestor of Deepest Leaves", difficulty="Medium", world="trees",
    tags=["hash-table", "tree", "dfs", "bfs"],
    story=dict(title="Where the Deepest Fruit Meet", text="Each fruit reports its subtree depth and the lowest fruit above all its deepest leaves. Equal depths on both sides mean this fruit is the meeting point.",
               goal="Return the subtree rooted at the LCA of the deepest leaves."),
    spec=dict(method="lcaDeepestLeaves", ret="TreeNode*", params=[["TreeNode*", "root"]]),
    tests=[dict(args=[[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]], expected=[2, 7, 4]), dict(args=[[1]], expected=[1]), dict(args=[[0, 1, 3, None, 2]], expected=[2])],
    scene=dict(theme="forest", layers=[
        dict(kind="tree", var="root", pointers=["node"], label="orchard"),
        dict(kind="values", vars=["dl", "dr"]),
    ]),
    reference="""class Solution {
public:
    pair<int, TreeNode*> deep(TreeNode* node) {
        if (!node) return {0, nullptr};
        auto l = deep(node->left);
        auto r = deep(node->right);
        int dl = l.first, dr = r.first;
        if (dl == dr) return {dl + 1, node};
        return dl > dr ? make_pair(dl + 1, l.second) : make_pair(dr + 1, r.second);
    }
    TreeNode* lcaDeepestLeaves(TreeNode* root) {
        return deep(root).second;
    }
};""",
)

add(
    id=1124, slug="longest-well-performing-interval", title="Longest Well-Performing Interval", difficulty="Medium", world="arrays", tags=["array", "hash-table", "stack", "monotonic-stack", "prefix-sum"],
    story=dict(title="More Tiring Days Than Easy Ones", text="Score +1 for a tiring day (>8 hours) and -1 otherwise. A positive running score covers everything so far; otherwise look up where the score was one lower.",
               goal="Return the longest interval with more tiring days than non-tiring days."),
    spec=dict(method="longestWPI", ret="int", params=[["vector<int>&", "hours"]]),
    tests=[dict(args=[[9, 9, 6, 0, 6, 6, 9]], expected=3), dict(args=[[6, 6, 6]], expected=0)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="hours", label="hours worked", pointers=["i"]),
        dict(kind="map", var="first", label="score first seen at"),
        dict(kind="values", vars=["score", "best"]),
    ]),
    reference="""class Solution {
public:
    int longestWPI(vector<int>& hours) {
        map<int, int> first;
        int score = 0, best = 0;
        for (int i = 0; i < (int)hours.size(); i++) {
            score += hours[i] > 8 ? 1 : -1;
            if (score > 0) best = i + 1;
            else {
                if (!first.count(score)) first[score] = i;
                if (first.count(score - 1)) best = max(best, i - first[score - 1]);
            }
        }
        return best;
    }
};""",
)

add(
    id=1128, slug="number-of-equivalent-domino-pairs", title="Number of Equivalent Domino Pairs", difficulty="Easy", world="arrays", tags=["array", "hash-table", "counting"],
    story=dict(title="Matching Dominoes", text="A domino reads the same either way up, so file it under (small, big). Each new domino pairs with every earlier one in its locker.",
               goal="Return the number of equivalent domino pairs."),
    spec=dict(method="numEquivDominoPairs", ret="int", params=[["vector<vector<int>>&", "dominoes"]]),
    tests=[dict(args=[[[1, 2], [2, 1], [3, 4], [5, 6]]], expected=1), dict(args=[[[1, 2], [1, 2], [1, 1], [1, 2], [2, 2]]], expected=3)],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="dominoes", label="dominoes", style="tiles", pointers=["i"]),
        dict(kind="map", var="cnt", label="seen (as small*10+big)"),
        dict(kind="values", vars=["pairs"]),
    ]),
    reference="""class Solution {
public:
    int numEquivDominoPairs(vector<vector<int>>& dominoes) {
        map<int, int> cnt;
        int pairs = 0;
        for (int i = 0; i < (int)dominoes.size(); i++) {
            int a = dominoes[i][0], b = dominoes[i][1];
            int key = min(a, b) * 10 + max(a, b);
            pairs += cnt[key]++;
        }
        return pairs;
    }
};""",
)

add(
    id=1130, slug="minimum-cost-tree-from-leaf-values", title="Minimum Cost Tree From Leaf Values", difficulty="Medium", world="stack", tags=["array", "dynamic-programming", "stack", "greedy", "monotonic-stack"],
    story=dict(title="Pairing Leaves Cheaply", text="A small leaf should be merged with its smaller neighbour as soon as possible. A falling tower of leaves pops each small leaf, paying it times the smaller of its neighbours.",
               goal="Return the smallest possible sum of non-leaf node values."),
    spec=dict(method="mctFromLeafValues", ret="int", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[6, 2, 4]], expected=32), dict(args=[[4, 11]], expected=44), dict(args=[[15, 13, 5, 3, 15]], expected=500)],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="arr", label="leaves", pointers=["i"]),
        dict(kind="stack", var="st", label="falling tower"),
        dict(kind="values", vars=["cost"]),
    ]),
    reference="""class Solution {
public:
    int mctFromLeafValues(vector<int>& arr) {
        vector<int> st = {INT_MAX};
        int cost = 0;
        for (int i = 0; i < (int)arr.size(); i++) {
            while (st.back() <= arr[i]) {
                int mid = st.back();
                st.pop_back();
                cost += mid * min(st.back(), arr[i]);
            }
            st.push_back(arr[i]);
        }
        while (st.size() > 2) {
            int mid = st.back();
            st.pop_back();
            cost += mid * st.back();
        }
        return cost;
    }
};""",
)

add(
    id=1140, slug="stone-game-ii", title="Stone Game II", difficulty="Medium", world="dp", tags=["array", "math", "dynamic-programming", "prefix-sum", "game-theory"],
    story=dict(title="Grabbing Up to 2M Piles", text="A player may take the next x piles, 1 ≤ x ≤ 2M, and M grows to max(M, x). The table stores the most stones the mover can get from pile i with a given M.",
               goal="Return the most stones Alice can get."),
    spec=dict(method="stoneGameII", ret="int", params=[["vector<int>&", "piles"]]),
    tests=[dict(args=[[2, 7, 9, 4, 4]], expected=10), dict(args=[[1, 2, 3, 4, 5, 100]], expected=104)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="suffix", label="stones from pile i onward", style="tiles", pointers=["i"]),
        dict(kind="grid", var="dp", palette="dp", label="best by (pile, M)", pointers=[["i", "m"]]),
    ]),
    reference="""class Solution {
public:
    int stoneGameII(vector<int>& piles) {
        int n = piles.size();
        vector<int> suffix(n + 1, 0);
        for (int i = n - 1; i >= 0; i--) suffix[i] = suffix[i + 1] + piles[i];
        vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
        for (int i = n - 1; i >= 0; i--) {
            for (int m = 1; m <= n; m++) {
                if (i + 2 * m >= n) {
                    dp[i][m] = suffix[i];
                    continue;
                }
                for (int x = 1; x <= 2 * m; x++) dp[i][m] = max(dp[i][m], suffix[i] - dp[i + x][max(m, x)]);
            }
        }
        return dp[0][1];
    }
};""",
)

add(
    id=1155, slug="number-of-dice-rolls-with-target-sum", title="Number of Dice Rolls With Target Sum", difficulty="Medium", world="dp", tags=["dynamic-programming"],
    story=dict(title="Rolling Toward the Target", text="Each die adds a face 1..k. The ledger counts the ways to reach every total after each die.",
               goal="Return the number of ways to roll exactly target, mod 1e9+7."),
    spec=dict(method="numRollsToTarget", ret="int", params=[["int", "n"], ["int", "k"], ["int", "target"]]),
    tests=[dict(args=[1, 6, 3], expected=1), dict(args=[2, 6, 7], expected=6), dict(args=[30, 30, 500], expected=222616187)],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="ways", label="ways to reach total", style="tiles", pointers=["t"]),
        dict(kind="values", vars=["die", "face"]),
    ]),
    reference="""class Solution {
public:
    int numRollsToTarget(int n, int k, int target) {
        const long long MOD = 1000000007;
        vector<long long> ways(target + 1, 0);
        ways[0] = 1;
        for (int die = 1; die <= n; die++) {
            vector<long long> next(target + 1, 0);
            for (int t = 1; t <= target; t++)
                for (int face = 1; face <= k && face <= t; face++) next[t] = (next[t] + ways[t - face]) % MOD;
            ways = next;
        }
        return ways[target];
    }
};""",
)

add(
    id=1160, slug="find-words-that-can-be-formed-by-characters", title="Find Words That Can Be Formed by Characters", difficulty="Easy", world="arrays", tags=["array", "hash-table", "string", "counting"],
    story=dict(title="Spelling from a Tile Rack", text="Count the rack's tiles. A word is spellable if no letter needs more tiles than the rack has; add up the spellable words' lengths.",
               goal="Return the sum of lengths of the good words."),
    spec=dict(method="countCharacters", ret="int", params=[["vector<string>&", "words"], ["string", "chars"]]),
    tests=[dict(args=[["cat", "bt", "hat", "tree"], "atach"], expected=6), dict(args=[["hello", "world", "leetcode"], "welldonehoneyr"], expected=10)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="words", label="words", style="tiles", pointers=["k"]),
        dict(kind="array", var="rack", label="rack counts a..z", style="tiles"),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int countCharacters(vector<string>& words, string chars) {
        vector<int> rack(26, 0);
        for (char c : chars) rack[c - 'a']++;
        int total = 0;
        for (int k = 0; k < (int)words.size(); k++) {
            vector<int> need(26, 0);
            bool ok = true;
            for (char c : words[k]) {
                if (++need[c - 'a'] > rack[c - 'a']) ok = false;
            }
            if (ok) total += words[k].size();
        }
        return total;
    }
};""",
)

add(
    id=1184, slug="distance-between-bus-stops", title="Distance Between Bus Stops", difficulty="Easy", world="arrays", tags=["array"],
    story=dict(title="Clockwise or the Other Way?", text="Add the distances going clockwise from start to destination; the other way round is the total minus that.",
               goal="Return the shorter distance between the two stops."),
    spec=dict(method="distanceBetweenBusStops", ret="int", params=[["vector<int>&", "distance"], ["int", "start"], ["int", "destination"]]),
    tests=[dict(args=[[1, 2, 3, 4], 0, 1], expected=1), dict(args=[[1, 2, 3, 4], 0, 2], expected=3), dict(args=[[1, 2, 3, 4], 0, 3], expected=4)],
    visualTest=2,
    scene=dict(theme="city", layers=[
        dict(kind="array", var="distance", label="road segments", pointers=["i"]),
        dict(kind="values", vars=["clockwise", "total"]),
    ]),
    reference="""class Solution {
public:
    int distanceBetweenBusStops(vector<int>& distance, int start, int destination) {
        if (start > destination) swap(start, destination);
        int clockwise = 0, total = 0;
        for (int i = 0; i < (int)distance.size(); i++) {
            total += distance[i];
            if (i >= start && i < destination) clockwise += distance[i];
        }
        return min(clockwise, total - clockwise);
    }
};""",
)

add(
    id=1186, slug="maximum-subarray-sum-with-one-deletion", title="Maximum Subarray Sum with One Deletion", difficulty="Medium", world="dp", tags=["array", "dynamic-programming"],
    story=dict(title="Treasure Walk with One Skip", text="Track two purses: the best run ending here with no chest skipped, and with one chest skipped (either this one, or an earlier one).",
               goal="Return the max subarray sum with at most one deletion (non-empty)."),
    spec=dict(method="maximumSum", ret="int", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[1, -2, 0, 3]], expected=4), dict(args=[[1, -2, -2, 3]], expected=3), dict(args=[[-1, -1, -1, -1]], expected=-1)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="arr", label="chests", pointers=["i"]),
        dict(kind="values", vars=["keep", "skipped", "best"]),
    ]),
    reference="""class Solution {
public:
    int maximumSum(vector<int>& arr) {
        int keep = arr[0], skipped = 0, best = arr[0];
        for (int i = 1; i < (int)arr.size(); i++) {
            skipped = max(skipped + arr[i], keep);
            keep = max(keep + arr[i], arr[i]);
            best = max({best, keep, skipped});
        }
        return best;
    }
};""",
)

add(
    id=1190, slug="reverse-substrings-between-each-pair-of-parentheses", title="Reverse Substrings Between Each Pair of Parentheses", difficulty="Medium",
    world="stack", tags=["string", "stack"],
    story=dict(title="Unfolding Nested Mirrors", text="On ( the text so far is stacked and a fresh piece starts. On ), the piece is reversed and appended to what was stacked.",
               goal="Return the string with every bracketed part reversed, innermost first, brackets removed."),
    spec=dict(method="reverseParentheses", ret="string", params=[["string", "s"]]),
    tests=[dict(args=["(abcd)"], expected="dcba"), dict(args=["(u(love)i)"], expected="iloveu"), dict(args=["(ed(et(oc))el)"], expected="leetcode")],
    visualTest=2,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="text", pointers=["i"]),
        dict(kind="stack", var="st", label="saved text"),
        dict(kind="values", vars=["cur"]),
    ]),
    reference="""class Solution {
public:
    string reverseParentheses(string s) {
        stack<string> st;
        string cur;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') {
                st.push(cur);
                cur = "";
            } else if (s[i] == ')') {
                reverse(cur.begin(), cur.end());
                cur = st.top() + cur;
                st.pop();
            } else {
                cur.push_back(s[i]);
            }
        }
        return cur;
    }
};""",
)

add(
    id=1200, slug="minimum-absolute-difference", title="Minimum Absolute Difference", difficulty="Easy", world="arrays", tags=["array", "sorting"],
    story=dict(title="The Closest Neighbours", text="After sorting, the closest pairs are always neighbours. Find the smallest gap, then list every neighbouring pair with that gap.",
               goal="Return all pairs with the minimum absolute difference, in ascending order."),
    spec=dict(method="minimumAbsDifference", ret="vector<vector<int>>", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[4, 2, 1, 3]], expected=[[1, 2], [2, 3], [3, 4]]), dict(args=[[1, 3, 6, 10, 15]], expected=[[1, 3]]), dict(args=[[3, 8, -10, 23, 19, -4, -14, 27]], expected=[[-14, -10], [19, 23], [23, 27]])],
    visualTest=2,
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="arr", label="values (sorted)", pointers=["i"]),
        dict(kind="values", vars=["gap"]),
        dict(kind="array", var="res", label="closest pairs", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> minimumAbsDifference(vector<int>& arr) {
        sort(arr.begin(), arr.end());
        int gap = INT_MAX;
        for (int i = 1; i < (int)arr.size(); i++) gap = min(gap, arr[i] - arr[i - 1]);
        vector<vector<int>> res;
        for (int i = 1; i < (int)arr.size(); i++)
            if (arr[i] - arr[i - 1] == gap) res.push_back({arr[i - 1], arr[i]});
        return res;
    }
};""",
)

add(
    id=1202, slug="smallest-string-with-swaps", title="Smallest String With Swaps", difficulty="Medium", world="graphs", tags=["array", "hash-table", "string", "depth-first-search", "union-find", "sorting"],
    story=dict(title="Freely Shuffled Families", text="Swappable positions join into families; within a family any order is reachable. Sort each family's letters and hand them back to its positions in order.",
               goal="Return the lexicographically smallest string reachable."),
    spec=dict(method="smallestStringWithSwaps", ret="string", params=[["string", "s"], ["vector<vector<int>>&", "pairs"]]),
    tests=[dict(args=["dcab", [[0, 3], [1, 2]]], expected="bacd"), dict(args=["dcab", [[0, 3], [1, 2], [0, 2]]], expected="abcd"), dict(args=["cba", [[0, 1], [1, 2]]], expected="abc")],
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="letters", pointers=["i"]),
        dict(kind="array", var="parent", label="family leader by position", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<int> parent;
    int leader(int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];
        return x;
    }
    string smallestStringWithSwaps(string s, vector<vector<int>>& pairs) {
        int n = s.size();
        parent.resize(n);
        for (int i = 0; i < n; i++) parent[i] = i;
        for (auto& p : pairs) parent[leader(p[0])] = leader(p[1]);
        map<int, vector<int>> groups;
        for (int i = 0; i < n; i++) groups[leader(i)].push_back(i);
        for (auto& [root, idx] : groups) {
            string letters;
            for (int i : idx) letters.push_back(s[i]);
            sort(letters.begin(), letters.end());
            for (int k = 0; k < (int)idx.size(); k++) s[idx[k]] = letters[k];
        }
        return s;
    }
};""",
)

add(
    id=1208, slug="get-equal-substrings-within-budget", title="Get Equal Substrings Within Budget", difficulty="Medium", world="sliding-window", tags=["string", "binary-search", "sliding-window", "prefix-sum"],
    story=dict(title="Repainting on a Budget", text="Changing a letter costs its alphabet distance. The window stretches right; while its total cost exceeds the budget, the left edge moves up.",
               goal="Return the longest substring of s you can turn into the matching part of t within maxCost."),
    spec=dict(method="equalSubstring", ret="int", params=[["string", "s"], ["string", "t"], ["int", "maxCost"]]),
    tests=[dict(args=["abcd", "bcdf", 3], expected=3), dict(args=["abcd", "cdef", 3], expected=1), dict(args=["abcd", "acde", 0], expected=1)],
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="s", pointers=["l", "r"], window=["l", "r"]),
        dict(kind="string", var="t", label="t", pointers=["l", "r"]),
        dict(kind="values", vars=["cost", "best"]),
    ]),
    reference="""class Solution {
public:
    int equalSubstring(string s, string t, int maxCost) {
        int l = 0, cost = 0, best = 0;
        for (int r = 0; r < (int)s.size(); r++) {
            cost += abs(s[r] - t[r]);
            while (cost > maxCost) {
                cost -= abs(s[l] - t[l]);
                l++;
            }
            best = max(best, r - l + 1);
        }
        return best;
    }
};""",
)

add(
    id=1209, slug="remove-all-adjacent-duplicates-in-string-ii", title="Remove All Adjacent Duplicates in String II", difficulty="Medium", world="stack", tags=["string", "stack"],
    story=dict(title="Popping Runs of k", text="The tower stores letter blocks with run counts. A letter matching the top bumps the count; when a run reaches k, the whole run vanishes.",
               goal="Return the string after removing every run of k equal letters."),
    spec=dict(method="removeDuplicates", ret="string", params=[["string", "s"], ["int", "k"]]),
    tests=[dict(args=["abcd", 2], expected="abcd"), dict(args=["deeedbbcccbdaa", 3], expected="aa"), dict(args=["pbbcggttciiippooaais", 2], expected="ps")],
    visualTest=1,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="letters", pointers=["i"]),
        dict(kind="stack", var="st", label="tower [letter, run]"),
    ]),
    reference="""class Solution {
public:
    string removeDuplicates(string s, int k) {
        vector<pair<char, int>> st;
        for (int i = 0; i < (int)s.size(); i++) {
            if (!st.empty() && st.back().first == s[i]) {
                if (++st.back().second == k) st.pop_back();
            } else {
                st.push_back({s[i], 1});
            }
        }
        string res;
        for (auto& [c, n] : st) res += string(n, c);
        return res;
    }
};""",
)

add(
    id=1217, slug="minimum-cost-to-move-chips-to-the-same-position", title="Minimum Cost to Move Chips to The Same Position", difficulty="Easy", world="greedy", tags=["array", "math", "greedy"],
    story=dict(title="Two-Step Hops Are Free", text="Moving two spaces costs nothing, so every chip can reach any spot of its parity free. Only the smaller parity group has to pay one each.",
               goal="Return the minimum cost to gather all chips."),
    spec=dict(method="minCostToMoveChips", ret="int", params=[["vector<int>&", "position"]]),
    tests=[dict(args=[[1, 2, 3]], expected=1), dict(args=[[2, 2, 2, 3, 3]], expected=2), dict(args=[[1, 1000000000]], expected=1)],
    visualTest=1,
    scene=dict(theme="market", layers=[
        dict(kind="array", var="position", label="chips", pointers=["i"]),
        dict(kind="values", vars=["odd", "even"]),
    ]),
    reference="""class Solution {
public:
    int minCostToMoveChips(vector<int>& position) {
        int odd = 0, even = 0;
        for (int i = 0; i < (int)position.size(); i++) {
            if (position[i] % 2) odd++;
            else even++;
        }
        return min(odd, even);
    }
};""",
)

add(
    id=1218, slug="longest-arithmetic-subsequence-of-given-difference", title="Longest Arithmetic Subsequence of Given Difference", difficulty="Medium",
    world="dp", tags=["array", "hash-table", "dynamic-programming"],
    story=dict(title="Evenly Stepping Stones", text="For each value, the longest chain ending here is one more than the chain ending at value - difference, looked up in the lockers.",
               goal="Return the longest subsequence with constant difference."),
    spec=dict(method="longestSubsequence", ret="int", params=[["vector<int>&", "arr"], ["int", "difference"]]),
    tests=[dict(args=[[1, 2, 3, 4], 1], expected=4), dict(args=[[1, 3, 5, 7], 1], expected=1), dict(args=[[1, 5, 7, 8, 5, 3, 4, 2, 1], -2], expected=4)],
    visualTest=2,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="arr", label="stones", pointers=["i"]),
        dict(kind="map", var="chain", label="longest chain ending at value"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int longestSubsequence(vector<int>& arr, int difference) {
        map<int, int> chain;
        int best = 0;
        for (int i = 0; i < (int)arr.size(); i++) {
            int prev = chain.count(arr[i] - difference) ? chain[arr[i] - difference] : 0;
            chain[arr[i]] = prev + 1;
            best = max(best, chain[arr[i]]);
        }
        return best;
    }
};""",
)

add(
    id=1221, slug="split-a-string-in-balanced-strings", title="Split a String in Balanced Strings", difficulty="Easy", world="greedy", tags=["string", "greedy", "counting"],
    story=dict(title="Cutting When It Balances", text="Count +1 for L and -1 for R. Every time the running balance returns to zero, cut there: that's one more balanced piece.",
               goal="Return the maximum number of balanced substrings."),
    spec=dict(method="balancedStringSplit", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["RLRRLLRLRL"], expected=4), dict(args=["RLRRRLLRLL"], expected=2), dict(args=["LLLLRRRR"], expected=1)],
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="string", pointers=["i"]),
        dict(kind="values", vars=["bal", "pieces"]),
    ]),
    reference="""class Solution {
public:
    int balancedStringSplit(string s) {
        int bal = 0, pieces = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            bal += s[i] == 'L' ? 1 : -1;
            if (bal == 0) pieces++;
        }
        return pieces;
    }
};""",
)

add(
    id=1232, slug="check-if-it-is-a-straight-line", title="Check If It Is a Straight Line", difficulty="Easy", world="arrays", tags=["array", "math", "geometry"],
    story=dict(title="Are the Lanterns in a Line?", text="Compare every point's direction from the first point with the first two points' direction using cross products, avoiding division.",
               goal="Return true if all points lie on one straight line."),
    spec=dict(method="checkStraightLine", ret="bool", params=[["vector<vector<int>>&", "coordinates"]]),
    tests=[dict(args=[[[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]], expected=True), dict(args=[[[1, 1], [2, 2], [3, 4], [4, 5], [5, 6], [7, 7]]], expected=False)],
    visualTest=1,
    scene=dict(theme="city", layers=[
        dict(kind="array", var="coordinates", label="lanterns", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["dx", "dy"]),
    ]),
    reference="""class Solution {
public:
    bool checkStraightLine(vector<vector<int>>& coordinates) {
        int dx = coordinates[1][0] - coordinates[0][0];
        int dy = coordinates[1][1] - coordinates[0][1];
        for (int i = 2; i < (int)coordinates.size(); i++) {
            int x = coordinates[i][0] - coordinates[0][0], y = coordinates[i][1] - coordinates[0][1];
            if (dx * y != dy * x) return false;
        }
        return true;
    }
};""",
)

add(
    id=1233, slug="remove-sub-folders-from-the-filesystem", title="Remove Sub-Folders from the Filesystem", difficulty="Medium", world="arrays", tags=["array", "string", "depth-first-search", "trie"],
    story=dict(title="Tidying the Folder Tree", text="Sorted paths put every folder just before its sub-folders. Keep a folder unless it starts with the last kept folder followed by a slash.",
               goal="Return the folders after removing every sub-folder (any order)."),
    spec=dict(method="removeSubfolders", ret="vector<string>", params=[["vector<string>&", "folder"]]),
    compare="unordered",
    tests=[dict(args=[["/a", "/a/b", "/c/d", "/c/d/e", "/c/f"]], expected=["/a", "/c/d", "/c/f"]), dict(args=[["/a", "/a/b/c", "/a/b/d"]], expected=["/a"]),
           dict(args=[["/a/b/c", "/a/b/ca", "/a/b/d"]], expected=["/a/b/c", "/a/b/ca", "/a/b/d"])],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="folder", label="paths (sorted)", style="tiles", pointers=["k"]),
        dict(kind="array", var="res", label="kept", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> removeSubfolders(vector<string>& folder) {
        sort(folder.begin(), folder.end());
        vector<string> res;
        for (int k = 0; k < (int)folder.size(); k++) {
            string& f = folder[k];
            if (!res.empty()) {
                string prefix = res.back() + "/";
                if (f.compare(0, prefix.size(), prefix) == 0) continue;
            }
            res.push_back(f);
        }
        return res;
    }
};""",
)

add(
    id=1235, slug="maximum-profit-in-job-scheduling", title="Maximum Profit in Job Scheduling", difficulty="Hard", world="dp", tags=["array", "binary-search", "dynamic-programming", "sorting"],
    story=dict(title="Picking Paid Jobs That Don't Clash", text="Jobs are sorted by end time. For each job, binary-search the last job that ends by its start; the best total is either skipping it or taking it on top of that earlier best.",
               goal="Return the maximum profit from non-overlapping jobs."),
    spec=dict(method="jobScheduling", ret="int", params=[["vector<int>&", "startTime"], ["vector<int>&", "endTime"], ["vector<int>&", "profit"]]),
    tests=[dict(args=[[1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]], expected=120), dict(args=[[1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]], expected=150), dict(args=[[1, 1, 1], [2, 3, 4], [5, 6, 4]], expected=6)],
    scene=dict(theme="lab", layers=[
        dict(kind="intervals", vars=["jobs"], pointers=["i"], label="jobs (by end time)"),
        dict(kind="array", var="dp", label="best profit after job", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["lo", "hi"]),
    ]),
    reference="""class Solution {
public:
    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        vector<vector<int>> jobs;
        for (int i = 0; i < n; i++) jobs.push_back({startTime[i], endTime[i], profit[i]});
        sort(jobs.begin(), jobs.end(), [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
        vector<int> dp(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            int lo = 0, hi = i - 1;
            while (lo < hi) {
                int mid = (lo + hi + 1) / 2;
                if (jobs[mid - 1][1] <= jobs[i - 1][0]) lo = mid;
                else hi = mid - 1;
            }
            dp[i] = max(dp[i - 1], dp[lo] + jobs[i - 1][2]);
        }
        return dp[n];
    }
};""",
)

add(
    id=1239, slug="maximum-length-of-a-concatenated-string-with-unique-characters", title="Maximum Length of a Concatenated String with Unique Characters",
    difficulty="Medium", world="backtracking", tags=["array", "string", "backtracking", "bit-manipulation"],
    story=dict(title="Stacking Words Without Repeats", text="Each word lights a letter mask. Behind each door, add the next word if its mask doesn't clash with the bag's mask, then try skipping it too.",
               goal="Return the longest concatenation with all unique characters."),
    spec=dict(method="maxLength", ret="int", params=[["vector<string>&", "arr"]]),
    tests=[dict(args=[["un", "iq", "ue"]], expected=4), dict(args=[["cha", "r", "act", "ers"]], expected=6), dict(args=[["abcdefghijklmnopqrstuvwxyz"]], expected=26)],
    scene=dict(theme="cave", layers=[
        dict(kind="array", var="arr", label="words", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["mask", "len", "best"]),
    ]),
    reference="""class Solution {
public:
    int best = 0;
    vector<int> masks;
    void go(vector<string>& arr, int i, int mask, int len) {
        best = max(best, len);
        if (i == (int)arr.size()) return;
        if (masks[i] >= 0 && (mask & masks[i]) == 0) go(arr, i + 1, mask | masks[i], len + arr[i].size());
        go(arr, i + 1, mask, len);
    }
    int maxLength(vector<string>& arr) {
        for (auto& w : arr) {
            int m = 0;
            for (char c : w) {
                if (m & (1 << (c - 'a'))) {
                    m = -1;
                    break;
                }
                m |= 1 << (c - 'a');
            }
            masks.push_back(m);
        }
        go(arr, 0, 0, 0);
        return best;
    }
};""",
)

add(
    id=1248, slug="count-number-of-nice-subarrays", title="Count Number of Nice Subarrays", difficulty="Medium", world="sliding-window", tags=["array", "hash-table", "math", "sliding-window", "prefix-sum"],
    story=dict(title="Exactly k Odd Crates", text="Count odd crates so far. The logbook says how many earlier positions had exactly k fewer odd crates.",
               goal="Return how many subarrays contain exactly k odd numbers."),
    spec=dict(method="numberOfSubarrays", ret="int", params=[["vector<int>&", "nums"], ["int", "k"]]),
    tests=[dict(args=[[1, 1, 2, 1, 1], 3], expected=2), dict(args=[[2, 4, 6], 1], expected=0), dict(args=[[2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2], expected=16)],
    scene=dict(theme="dock", layers=[
        dict(kind="array", var="nums", label="crates", pointers=["i"]),
        dict(kind="array", var="seen", label="positions by odd-count", style="tiles", pointers=["odd"]),
        dict(kind="values", vars=["count"]),
    ]),
    reference="""class Solution {
public:
    int numberOfSubarrays(vector<int>& nums, int k) {
        vector<int> seen(nums.size() + 1, 0);
        seen[0] = 1;
        int odd = 0, count = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            odd += nums[i] % 2;
            if (odd >= k) count += seen[odd - k];
            seen[odd]++;
        }
        return count;
    }
};""",
)

add(
    id=1260, slug="shift-2d-grid", title="Shift 2D Grid", difficulty="Easy", world="arrays", tags=["array", "matrix", "simulation"],
    story=dict(title="Sliding the Tile Wall", text="Read the wall as one long ribbon. Shifting k times moves every tile k places along the ribbon, wrapping around.",
               goal="Return the grid after k shifts."),
    spec=dict(method="shiftGrid", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "grid"], ["int", "k"]]),
    tests=[dict(args=[[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1], expected=[[9, 1, 2], [3, 4, 5], [6, 7, 8]]), dict(args=[[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9], expected=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])],
    scene=dict(theme="lab", layers=[dict(kind="row", children=[
        dict(kind="grid", var="grid", palette="dp", label="old wall"),
        dict(kind="grid", var="res", palette="dp", label="shifted"),
    ])]),
    reference="""class Solution {
public:
    vector<vector<int>> shiftGrid(vector<vector<int>>& grid, int k) {
        int m = grid.size(), n = grid[0].size(), total = m * n;
        vector<vector<int>> res(m, vector<int>(n));
        for (int p = 0; p < total; p++) {
            int q = (p + k) % total;
            res[q / n][q % n] = grid[p / n][p % n];
        }
        return res;
    }
};""",
)

add(
    id=1266, slug="minimum-time-visiting-all-points", title="Minimum Time Visiting All Points", difficulty="Easy", world="greedy", tags=["array", "math", "geometry"],
    story=dict(title="The Diagonal Courier", text="A courier can step diagonally, so getting between two points takes the larger of the x and y distances.",
               goal="Return the minimum time to visit all points in order."),
    spec=dict(method="minTimeToVisitAllPoints", ret="int", params=[["vector<vector<int>>&", "points"]]),
    tests=[dict(args=[[[1, 1], [3, 4], [-1, 0]]], expected=7), dict(args=[[[3, 2], [-2, 2]]], expected=5)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="points", label="stops", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["time"]),
    ]),
    reference="""class Solution {
public:
    int minTimeToVisitAllPoints(vector<vector<int>>& points) {
        int time = 0;
        for (int i = 1; i < (int)points.size(); i++) {
            time += max(abs(points[i][0] - points[i - 1][0]), abs(points[i][1] - points[i - 1][1]));
        }
        return time;
    }
};""",
)
