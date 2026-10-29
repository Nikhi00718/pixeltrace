"""Seventeenth batch of hand-crafted situation files (registered into problems_src.P)."""

from problems_src import add

add(
    id=796, slug="rotate-string", title="Rotate String", difficulty="Easy", world="arrays", tags=["string", "string-matching"],
    story=dict(title="The Spinning Banner", text="A banner spun around keeps its letters in a loop. Every rotation of s is hidden inside s written twice.",
               goal="Return true if s can become goal by rotation."),
    spec=dict(method="rotateString", ret="bool", params=[["string", "s"], ["string", "goal"]]),
    tests=[dict(args=["abcde", "cdeab"], expected=True), dict(args=["abcde", "abced"], expected=False)],
    scene=dict(theme="market", layers=[dict(kind="string", var="twice", label="banner twice", pointers=["i"])]),
    reference="""class Solution {
public:
    bool rotateString(string s, string goal) {
        if (s.size() != goal.size()) return false;
        string twice = s + s;
        for (int i = 0; i < (int)s.size(); i++) {
            if (twice.compare(i, goal.size(), goal) == 0) return true;
        }
        return false;
    }
};""",
)

add(
    id=797, slug="all-paths-from-source-to-target", title="All Paths From Source to Target", difficulty="Medium", world="graphs", tags=["backtracking", "dfs", "bfs", "graph"],
    story=dict(title="Every Road Out of the Valley", text="One-way roads never loop. A traveller tries every road from town 0, writing the route down when they reach the last town, then backs up to try the next road.",
               goal="Return every path from 0 to n-1 (any order)."),
    spec=dict(method="allPathsSourceTarget", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "graph"]]),
    compare="unordered",
    tests=[dict(args=[[[1, 2], [3], [3], []]], expected=[[0, 1, 3], [0, 2, 3]]), dict(args=[[[4, 3, 1], [3, 2, 4], [3], [4], []]], expected=[[0, 4], [0, 3, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4], [0, 1, 4]])],
    scene=dict(theme="forest", layers=[
        dict(kind="graph", adj="graph", directed=True, pointers=["u"], label="valley"),
        dict(kind="array", var="path", label="route", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void go(vector<vector<int>>& graph, int u) {
        path.push_back(u);
        if (u == (int)graph.size() - 1) res.push_back(path);
        else
            for (int v : graph[u]) go(graph, v);
        path.pop_back();
    }
    vector<vector<int>> allPathsSourceTarget(vector<vector<int>>& graph) {
        go(graph, 0);
        return res;
    }
};""",
)

add(
    id=799, slug="champagne-tower", title="Champagne Tower", difficulty="Medium", world="dp", tags=["dynamic-programming"],
    story=dict(title="Pouring the Glass Pyramid", text="Pour everything into the top glass. Any glass holding more than one cup splits the overflow evenly into the two glasses below it.",
               goal="Return how full the glass at (query_row, query_glass) is."),
    spec=dict(method="champagneTower", ret="double", params=[["int", "poured"], ["int", "query_row"], ["int", "query_glass"]]),
    compare="float",
    tests=[dict(args=[1, 1, 1], expected=0.0), dict(args=[2, 1, 1], expected=0.5), dict(args=[100000009, 33, 17], expected=1.0)],
    visualTest=1,
    scene=dict(theme="market", layers=[dict(kind="grid", var="t", palette="dp", label="glasses", pointers=[["r", "c"]])]),
    reference="""class Solution {
public:
    double champagneTower(int poured, int query_row, int query_glass) {
        vector<vector<double>> t(query_row + 2, vector<double>(query_row + 2, 0.0));
        t[0][0] = poured;
        for (int r = 0; r <= query_row; r++) {
            for (int c = 0; c <= r; c++) {
                double extra = (t[r][c] - 1.0) / 2.0;
                if (extra > 0) {
                    t[r + 1][c] += extra;
                    t[r + 1][c + 1] += extra;
                }
            }
        }
        return min(1.0, t[query_row][query_glass]);
    }
};""",
)

add(
    id=802, slug="find-eventual-safe-states", title="Find Eventual Safe States", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "graph", "topological-sort"],
    story=dict(title="Towns You Can't Get Stuck In", text="A town is safe if every road out of it leads to safety. Paint towns yellow while exploring, green once proven safe; reaching a yellow town means a loop.",
               goal="Return every safe node in ascending order."),
    spec=dict(method="eventualSafeNodes", ret="vector<int>", params=[["vector<vector<int>>&", "graph"]]),
    tests=[dict(args=[[[1, 2], [2, 3], [5], [0], [5], [], []]], expected=[2, 4, 5, 6]), dict(args=[[[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]], expected=[4])],
    scene=dict(theme="forest", layers=[dict(kind="graph", adj="graph", directed=True, state="state", pointers=["u"], label="towns")]),
    reference="""class Solution {
public:
    vector<int> state;
    bool safe(vector<vector<int>>& graph, int u) {
        if (state[u]) return state[u] == 2;
        state[u] = 1;
        for (int v : graph[u]) {
            if (!safe(graph, v)) return false;
        }
        state[u] = 2;
        return true;
    }
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        state.assign(graph.size(), 0);
        vector<int> res;
        for (int u = 0; u < (int)graph.size(); u++) {
            if (safe(graph, u)) res.push_back(u);
        }
        return res;
    }
};""",
)

add(
    id=804, slug="unique-morse-code-words", title="Unique Morse Code Words", difficulty="Easy", world="arrays", tags=["array", "hash-table", "string"],
    story=dict(title="The Telegraph Office", text="Every word is tapped out in Morse and the tapped codes go into the lockers; count the distinct codes.",
               goal="Return the number of different transformations."),
    spec=dict(method="uniqueMorseRepresentations", ret="int", params=[["vector<string>&", "words"]]),
    tests=[dict(args=[["gin", "zen", "gig", "msg"]], expected=2), dict(args=[["a"]], expected=1)],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="words", label="words", style="tiles", pointers=["k"]),
        dict(kind="set", var="codes", label="codes seen"),
    ]),
    reference="""class Solution {
public:
    int uniqueMorseRepresentations(vector<string>& words) {
        vector<string> morse = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--",
                                "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};
        set<string> codes;
        for (int k = 0; k < (int)words.size(); k++) {
            string code;
            for (char c : words[k]) code += morse[c - 'a'];
            codes.insert(code);
        }
        return codes.size();
    }
};""",
)

add(
    id=807, slug="max-increase-to-keep-city-skyline", title="Max Increase to Keep City Skyline", difficulty="Medium", world="greedy", tags=["array", "greedy", "matrix"],
    story=dict(title="Building Up Without Changing the View", text="Each building may grow up to the lower of its row's and column's tallest building, so neither skyline changes.",
               goal="Return the total height that can be added."),
    spec=dict(method="maxIncreaseKeepingSkyline", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[3, 0, 8, 4], [2, 4, 5, 7], [9, 2, 6, 3], [0, 3, 1, 0]]], expected=35), dict(args=[[[0, 0, 0], [0, 0, 0], [0, 0, 0]]], expected=0)],
    scene=dict(theme="city", layers=[
        dict(kind="grid", var="grid", palette="dp", label="city blocks", pointers=[["r", "c"]]),
        dict(kind="row", children=[dict(kind="array", var="rowMax", label="row skyline", style="tiles"), dict(kind="array", var="colMax", label="column skyline", style="tiles")]),
        dict(kind="values", vars=["total"]),
    ]),
    reference="""class Solution {
public:
    int maxIncreaseKeepingSkyline(vector<vector<int>>& grid) {
        int n = grid.size(), total = 0;
        vector<int> rowMax(n, 0), colMax(n, 0);
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) {
                rowMax[r] = max(rowMax[r], grid[r][c]);
                colMax[c] = max(colMax[c], grid[r][c]);
            }
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) total += min(rowMax[r], colMax[c]) - grid[r][c];
        return total;
    }
};""",
)

add(
    id=821, slug="shortest-distance-to-a-character", title="Shortest Distance to a Character", difficulty="Easy", world="two-pointers", tags=["array", "two-pointers", "string"],
    story=dict(title="Distance to the Nearest Lamp Post", text="Sweep left to right remembering the last post, then right to left remembering the next one; each tile keeps the closer distance.",
               goal="Return the distance from every index to the nearest c."),
    spec=dict(method="shortestToChar", ret="vector<int>", params=[["string", "s"], ["char", "c"]]),
    tests=[dict(args=["loveleetcode", "e"], expected=[3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]), dict(args=["aaab", "b"], expected=[3, 2, 1, 0])],
    visualTest=1,
    scene=dict(theme="city", layers=[
        dict(kind="string", var="s", label="street", pointers=["i"]),
        dict(kind="array", var="res", label="distance", style="tiles", pointers=["i"]),
        dict(kind="values", vars=["last"]),
    ]),
    reference="""class Solution {
public:
    vector<int> shortestToChar(string s, char c) {
        int n = s.size(), last = -100000;
        vector<int> res(n);
        for (int i = 0; i < n; i++) {
            if (s[i] == c) last = i;
            res[i] = i - last;
        }
        last = 200000;
        for (int i = n - 1; i >= 0; i--) {
            if (s[i] == c) last = i;
            res[i] = min(res[i], last - i);
        }
        return res;
    }
};""",
)

add(
    id=827, slug="making-a-large-island", title="Making A Large Island", difficulty="Hard", world="graphs", tags=["array", "dfs", "bfs", "union-find", "matrix"],
    story=dict(title="One Bag of Sand", text="Label every island with its own number and record its size. Then for each sea tile, add up the distinct islands touching it plus the tile itself.",
               goal="Return the largest island possible after turning at most one 0 into 1."),
    spec=dict(method="largestIsland", ret="int", params=[["vector<vector<int>>&", "grid"]]),
    tests=[dict(args=[[[1, 0], [0, 1]]], expected=3), dict(args=[[[1, 1], [1, 0]]], expected=4), dict(args=[[[1, 1], [1, 1]]], expected=4)],
    scene=dict(theme="forest", layers=[
        dict(kind="grid", var="grid", palette="dp", label="island labels", pointers=[["r", "c"]]),
        dict(kind="map", var="size", label="size by label"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    map<int, int> size;
    int paint(vector<vector<int>>& grid, int r, int c, int label) {
        int n = grid.size();
        if (r < 0 || c < 0 || r >= n || c >= n || grid[r][c] != 1) return 0;
        grid[r][c] = label;
        return 1 + paint(grid, r + 1, c, label) + paint(grid, r - 1, c, label) + paint(grid, r, c + 1, label) + paint(grid, r, c - 1, label);
    }
    int largestIsland(vector<vector<int>>& grid) {
        int n = grid.size(), label = 2, best = 0;
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
                if (grid[r][c] == 1) {
                    size[label] = paint(grid, r, c, label);
                    best = max(best, size[label]);
                    label++;
                }
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) {
                if (grid[r][c] != 0) continue;
                set<int> near;
                for (int d = 0; d < 4; d++) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr >= 0 && nc >= 0 && nr < n && nc < n && grid[nr][nc] > 1) near.insert(grid[nr][nc]);
                }
                int total = 1;
                for (int l : near) total += size[l];
                best = max(best, total);
            }
        return best;
    }
};""",
)

add(
    id=830, slug="positions-of-large-groups", title="Positions of Large Groups", difficulty="Easy", world="two-pointers", tags=["string"],
    story=dict(title="Long Runs of the Same Letter", text="Walk the banner run by run; any run of three or more letters is written down by its start and end.",
               goal="Return [start, end] of every group of length ≥ 3."),
    spec=dict(method="largeGroupPositions", ret="vector<vector<int>>", params=[["string", "s"]]),
    tests=[dict(args=["abbxxxxzzy"], expected=[[3, 6]]), dict(args=["abc"], expected=[]), dict(args=["abcdddeeeeaabbbcd"], expected=[[3, 5], [6, 9], [12, 14]])],
    visualTest=2,
    scene=dict(theme="market", layers=[
        dict(kind="string", var="s", label="banner", pointers=["i", "j"], window=["i", "j"], windowExclusive=True),
        dict(kind="array", var="res", label="large groups", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<vector<int>> largeGroupPositions(string s) {
        vector<vector<int>> res;
        int i = 0, n = s.size();
        while (i < n) {
            int j = i;
            while (j < n && s[j] == s[i]) j++;
            if (j - i >= 3) res.push_back({i, j - 1});
            i = j;
        }
        return res;
    }
};""",
)

add(
    id=832, slug="flipping-an-image", title="Flipping an Image", difficulty="Easy", world="two-pointers", tags=["array", "two-pointers", "bit-manipulation", "matrix", "simulation"],
    story=dict(title="Mirror and Negative", text="Each row is mirrored by two painters swapping from both ends, and every pixel they touch is inverted.",
               goal="Flip every row horizontally, then invert it."),
    spec=dict(method="flipAndInvertImage", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "image"]]),
    tests=[dict(args=[[[1, 1, 0], [1, 0, 1], [0, 0, 0]]], expected=[[1, 0, 0], [0, 1, 0], [1, 1, 1]]), dict(args=[[[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]]], expected=[[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [1, 0, 1, 0]])],
    scene=dict(theme="lab", layers=[dict(kind="grid", var="image", palette="bool", label="image", pointers=[["r", "l"], ["r", "rr"]])]),
    reference="""class Solution {
public:
    vector<vector<int>> flipAndInvertImage(vector<vector<int>>& image) {
        for (int r = 0; r < (int)image.size(); r++) {
            int l = 0, rr = image[r].size() - 1;
            while (l <= rr) {
                int a = image[r][l] ^ 1, b = image[r][rr] ^ 1;
                image[r][l] = b;
                image[r][rr] = a;
                l++;
                rr--;
            }
        }
        return image;
    }
};""",
)

add(
    id=836, slug="rectangle-overlap", title="Rectangle Overlap", difficulty="Easy", world="intervals", tags=["math", "geometry"],
    story=dict(title="Do the Rugs Overlap?", text="Two rugs overlap only if their x-ranges overlap and their y-ranges overlap, each by more than a touching edge.",
               goal="Return true if the rectangles overlap with positive area."),
    spec=dict(method="isRectangleOverlap", ret="bool", params=[["vector<int>&", "rec1"], ["vector<int>&", "rec2"]]),
    tests=[dict(args=[[0, 0, 2, 2], [1, 1, 3, 3]], expected=True), dict(args=[[0, 0, 1, 1], [1, 0, 2, 1]], expected=False), dict(args=[[0, 0, 1, 1], [2, 2, 3, 3]], expected=False)],
    scene=dict(theme="lab", layers=[dict(kind="values", vars=["xs", "ys"])]),
    reference="""class Solution {
public:
    bool isRectangleOverlap(vector<int>& rec1, vector<int>& rec2) {
        bool xs = min(rec1[2], rec2[2]) > max(rec1[0], rec2[0]);
        bool ys = min(rec1[3], rec2[3]) > max(rec1[1], rec2[1]);
        return xs && ys;
    }
};""",
)

add(
    id=838, slug="push-dominoes", title="Push Dominoes", difficulty="Medium", world="two-pointers", tags=["two-pointers", "string", "dynamic-programming"],
    story=dict(title="The Falling Domino Row", text="Every domino records how strongly it is pushed: a right-push that fades with distance from the left, minus a left-push that fades from the right. The sign decides how it falls.",
               goal="Return the final state of the dominoes."),
    spec=dict(method="pushDominoes", ret="string", params=[["string", "dominoes"]]),
    tests=[dict(args=["RR.L"], expected="RR.L"), dict(args=[".L.R...LR..L.."], expected="LL.RR.LLRRLL..")],
    visualTest=1,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="dominoes", label="dominoes", pointers=["i"]),
        dict(kind="array", var="force", label="net push", style="tiles", pointers=["i"]),
    ]),
    reference="""class Solution {
public:
    string pushDominoes(string dominoes) {
        int n = dominoes.size();
        vector<int> force(n, 0);
        int f = 0;
        for (int i = 0; i < n; i++) {
            if (dominoes[i] == 'R') f = n;
            else if (dominoes[i] == 'L') f = 0;
            else f = max(f - 1, 0);
            force[i] += f;
        }
        f = 0;
        for (int i = n - 1; i >= 0; i--) {
            if (dominoes[i] == 'L') f = n;
            else if (dominoes[i] == 'R') f = 0;
            else f = max(f - 1, 0);
            force[i] -= f;
        }
        for (int i = 0; i < n; i++) dominoes[i] = force[i] > 0 ? 'R' : force[i] < 0 ? 'L' : '.';
        return dominoes;
    }
};""",
)

add(
    id=845, slug="longest-mountain-in-array", title="Longest Mountain in Array", difficulty="Medium", world="two-pointers", tags=["array", "two-pointers", "dynamic-programming", "enumeration"],
    story=dict(title="The Tallest Hike", text="From each valley, a hiker climbs as long as the trail rises, then descends as long as it falls. A real mountain needs both a climb and a descent.",
               goal="Return the length of the longest mountain subarray."),
    spec=dict(method="longestMountain", ret="int", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[2, 1, 4, 7, 3, 2, 5]], expected=5), dict(args=[[2, 2, 2]], expected=0)],
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="arr", label="trail", pointers=["start", "end"], window=["start", "end"]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int longestMountain(vector<int>& arr) {
        int n = arr.size(), best = 0, start = 0;
        while (start < n) {
            int end = start;
            if (end + 1 < n && arr[end] < arr[end + 1]) {
                while (end + 1 < n && arr[end] < arr[end + 1]) end++;
                if (end + 1 < n && arr[end] > arr[end + 1]) {
                    while (end + 1 < n && arr[end] > arr[end + 1]) end++;
                    best = max(best, end - start + 1);
                }
            }
            start = max(end, start + 1);
        }
        return best;
    }
};""",
)

add(
    id=846, slug="hand-of-straights", title="Hand of Straights", difficulty="Medium", world="greedy", tags=["array", "hash-table", "greedy", "sorting"],
    story=dict(title="Dealing Runs of Cards", text="Card counts sit in sorted lockers. The smallest card left must start a run, so take groupSize consecutive cards from it, or fail.",
               goal="Return true if the hand can be split into consecutive groups."),
    spec=dict(method="isNStraightHand", ret="bool", params=[["vector<int>&", "hand"], ["int", "groupSize"]]),
    tests=[dict(args=[[1, 2, 3, 6, 2, 3, 4, 7, 8], 3], expected=True), dict(args=[[1, 2, 3, 4, 5], 4], expected=False)],
    scene=dict(theme="market", layers=[
        dict(kind="map", var="cnt", label="cards left", lookup=["start"]),
        dict(kind="values", vars=["start", "take"]),
    ]),
    reference="""class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        map<int, int> cnt;
        for (int x : hand) cnt[x]++;
        while (!cnt.empty()) {
            int start = cnt.begin()->first;
            int take = cnt.begin()->second;
            for (int v = start; v < start + groupSize; v++) {
                if (cnt[v] < take) return false;
                cnt[v] -= take;
                if (cnt[v] == 0) cnt.erase(v);
            }
        }
        return true;
    }
};""",
)

add(
    id=849, slug="maximize-distance-to-closest-person", title="Maximize Distance to Closest Person", difficulty="Medium", world="two-pointers", tags=["array"],
    story=dict(title="The Quietest Seat", text="Walk the row remembering the last occupied seat. Gaps in the middle give half their width; empty runs at either end give their full width.",
               goal="Return the maximum distance to the closest person."),
    spec=dict(method="maxDistToClosest", ret="int", params=[["vector<int>&", "seats"]]),
    tests=[dict(args=[[1, 0, 0, 0, 1, 0, 1]], expected=2), dict(args=[[1, 0, 0, 0]], expected=3), dict(args=[[0, 1]], expected=1)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="seats", label="seats", style="tiles", pointers=["last", "i"]),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int maxDistToClosest(vector<int>& seats) {
        int n = seats.size(), last = -1, best = 0;
        for (int i = 0; i < n; i++) {
            if (!seats[i]) continue;
            best = last < 0 ? i : max(best, (i - last) / 2);
            last = i;
        }
        return max(best, n - 1 - last);
    }
};""",
)

add(
    id=853, slug="car-fleet", title="Car Fleet", difficulty="Medium", world="stack", tags=["array", "stack", "sorting", "monotonic-stack"],
    story=dict(title="Convoys on the Highway", text="Cars closest to the target go first. Each car's arrival time is stacked; a car that would arrive no later than the fleet ahead of it just joins that fleet.",
               goal="Return how many fleets reach the target."),
    spec=dict(method="carFleet", ret="int", params=[["int", "target"], ["vector<int>&", "position"], ["vector<int>&", "speed"]]),
    tests=[dict(args=[12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]], expected=3), dict(args=[10, [3], [3]], expected=1), dict(args=[100, [0, 2, 4], [4, 2, 1]], expected=1)],
    scene=dict(theme="city", layers=[
        dict(kind="array", var="order", label="cars by position (closest first)", style="tiles", pointers=["k"]),
        dict(kind="stack", var="fleets", label="fleet arrival times"),
    ]),
    reference="""class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        vector<int> order(n);
        for (int i = 0; i < n; i++) order[i] = i;
        sort(order.begin(), order.end(), [&](int a, int b) { return position[a] > position[b]; });
        vector<double> fleets;
        for (int k = 0; k < n; k++) {
            int car = order[k];
            double t = (double)(target - position[car]) / speed[car];
            if (fleets.empty() || t > fleets.back()) fleets.push_back(t);
        }
        return fleets.size();
    }
};""",
)

add(
    id=856, slug="score-of-parentheses", title="Score of Parentheses", difficulty="Medium", world="stack", tags=["string", "stack"],
    story=dict(title="Scoring Nested Brackets", text="Every ( stacks a fresh score of 0. On ), the inner score is popped: an empty pair is worth 1, otherwise it doubles, and it's added to the level below.",
               goal="Return the score of the balanced string."),
    spec=dict(method="scoreOfParentheses", ret="int", params=[["string", "s"]]),
    tests=[dict(args=["()"], expected=1), dict(args=["(())"], expected=2), dict(args=["()()"], expected=2), dict(args=["(()(()))"], expected=6)],
    visualTest=3,
    scene=dict(theme="castle", layers=[
        dict(kind="string", var="s", label="brackets", pointers=["i"]),
        dict(kind="stack", var="st", label="score per level"),
    ]),
    reference="""class Solution {
public:
    int scoreOfParentheses(string s) {
        vector<int> st(1, 0);
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(') {
                st.push_back(0);
            } else {
                int inner = st.back();
                st.pop_back();
                st.back() += max(2 * inner, 1);
            }
        }
        return st[0];
    }
};""",
)

add(
    id=859, slug="buddy-strings", title="Buddy Strings", difficulty="Easy", world="arrays", tags=["hash-table", "string"],
    story=dict(title="One Swap Away", text="Collect the positions where the words differ. Exactly two crossed-over differences make a swap; equal words need a repeated letter to swap with itself.",
               goal="Return true if one swap in s makes it equal goal."),
    spec=dict(method="buddyStrings", ret="bool", params=[["string", "s"], ["string", "goal"]]),
    tests=[dict(args=["ab", "ba"], expected=True), dict(args=["ab", "ab"], expected=False), dict(args=["aa", "aa"], expected=True), dict(args=["abcd", "cbad"], expected=True)],
    visualTest=3,
    scene=dict(theme="lab", layers=[
        dict(kind="string", var="s", label="s", pointers=["i"]),
        dict(kind="string", var="goal", label="goal", pointers=["i"]),
        dict(kind="array", var="diff", label="differences at", style="tiles"),
    ]),
    reference="""class Solution {
public:
    bool buddyStrings(string s, string goal) {
        if (s.size() != goal.size()) return false;
        if (s == goal) {
            set<char> seen(s.begin(), s.end());
            return seen.size() < s.size();
        }
        vector<int> diff;
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] != goal[i]) diff.push_back(i);
        }
        return diff.size() == 2 && s[diff[0]] == goal[diff[1]] && s[diff[1]] == goal[diff[0]];
    }
};""",
)

add(
    id=867, slug="transpose-matrix", title="Transpose Matrix", difficulty="Easy", world="arrays", tags=["array", "matrix", "simulation"],
    story=dict(title="Turning the Ledger Sideways", text="Every row becomes a column: the tile at (r, c) moves to (c, r).",
               goal="Return the transpose of the matrix."),
    spec=dict(method="transpose", ret="vector<vector<int>>", params=[["vector<vector<int>>&", "matrix"]]),
    tests=[dict(args=[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], expected=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]), dict(args=[[[1, 2, 3], [4, 5, 6]]], expected=[[1, 4], [2, 5], [3, 6]])],
    visualTest=1,
    scene=dict(theme="lab", layers=[dict(kind="row", children=[
        dict(kind="grid", var="matrix", palette="dp", label="ledger", pointers=[["r", "c"]]),
        dict(kind="grid", var="res", palette="dp", label="turned", pointers=[["c", "r"]]),
    ])]),
    reference="""class Solution {
public:
    vector<vector<int>> transpose(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<vector<int>> res(n, vector<int>(m));
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++) res[c][r] = matrix[r][c];
        return res;
    }
};""",
)

add(
    id=868, slug="binary-gap", title="Binary Gap", difficulty="Easy", world="bits", tags=["bit-manipulation"],
    story=dict(title="The Widest Dark Stretch", text="Scan the lamps from the right, remembering where the last lit lamp was. The distance between two lit lamps is a gap.",
               goal="Return the longest distance between adjacent 1 bits."),
    spec=dict(method="binaryGap", ret="int", params=[["int", "n"]]),
    tests=[dict(args=[22], expected=2), dict(args=[8], expected=0), dict(args=[5], expected=2)],
    scene=dict(theme="space", layers=[dict(kind="values", vars=["n", "pos", "last", "best"])]),
    reference="""class Solution {
public:
    int binaryGap(int n) {
        int last = -1, best = 0;
        for (int pos = 0; n > 0; pos++, n >>= 1) {
            if (n & 1) {
                if (last >= 0) best = max(best, pos - last);
                last = pos;
            }
        }
        return best;
    }
};""",
)

add(
    id=873, slug="length-of-longest-fibonacci-subsequence", title="Length of Longest Fibonacci Subsequence", difficulty="Medium", world="dp",
    tags=["array", "hash-table", "dynamic-programming"],
    story=dict(title="Hidden Fibonacci Chains", text="For each pair (j, k), look up the earlier value arr[k] - arr[j]; if it exists, the chain ending in that pair extends the chain ending at (i, j).",
               goal="Return the length of the longest Fibonacci-like subsequence (0 if none)."),
    spec=dict(method="lenLongestFibSubseq", ret="int", params=[["vector<int>&", "arr"]]),
    tests=[dict(args=[[1, 2, 3, 4, 5, 6, 7, 8]], expected=5), dict(args=[[1, 3, 7, 11, 12, 14, 18]], expected=3)],
    visualTest=1,
    scene=dict(theme="farm", layers=[
        dict(kind="array", var="arr", label="values", pointers=["j", "k"]),
        dict(kind="map", var="where", label="index of value"),
        dict(kind="values", vars=["best"]),
    ]),
    reference="""class Solution {
public:
    int lenLongestFibSubseq(vector<int>& arr) {
        int n = arr.size(), best = 0;
        map<int, int> where;
        for (int i = 0; i < n; i++) where[arr[i]] = i;
        vector<vector<int>> dp(n, vector<int>(n, 2));
        for (int k = 0; k < n; k++)
            for (int j = 0; j < k; j++) {
                int need = arr[k] - arr[j];
                if (need < arr[j] && where.count(need)) {
                    dp[j][k] = dp[where[need]][j] + 1;
                    best = max(best, dp[j][k]);
                }
            }
        return best;
    }
};""",
)

add(
    id=877, slug="stone-game", title="Stone Game", difficulty="Medium", world="dp", tags=["array", "math", "dynamic-programming", "game-theory"],
    story=dict(title="Alice and Bob's Stone Piles", text="Players take a pile from either end. The table stores how far ahead the player to move ends up on every stretch of piles.",
               goal="Return true if Alice wins with optimal play."),
    spec=dict(method="stoneGame", ret="bool", params=[["vector<int>&", "piles"]]),
    tests=[dict(args=[[5, 3, 4, 5]], expected=True), dict(args=[[3, 7, 2, 3]], expected=True)],
    scene=dict(theme="market", layers=[
        dict(kind="array", var="piles", label="piles", pointers=["i", "j"], window=["i", "j"]),
        dict(kind="grid", var="dp", palette="dp", label="lead for stretch", pointers=[["i", "j"]]),
    ]),
    reference="""class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        int n = piles.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int i = 0; i < n; i++) dp[i][i] = piles[i];
        for (int len = 2; len <= n; len++)
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                dp[i][j] = max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1]);
            }
        return dp[0][n - 1] > 0;
    }
};""",
    hints=["With an even number of piles and an odd total, the first player can always win; the table shows why."],
)

add(
    id=886, slug="possible-bipartition", title="Possible Bipartition", difficulty="Medium", world="graphs", tags=["dfs", "bfs", "union-find", "graph"],
    story=dict(title="Splitting Rivals into Two Teams", text="Each dislike is a road between two people who can't share a team. Paint the graph in two colours; a road between same colours makes it impossible.",
               goal="Return true if everyone can be split into two groups."),
    spec=dict(method="possibleBipartition", ret="bool", params=[["int", "n"], ["vector<vector<int>>&", "dislikes"]]),
    tests=[dict(args=[4, [[1, 2], [1, 3], [2, 4]]], expected=True), dict(args=[3, [[1, 2], [1, 3], [2, 3]]], expected=False)],
    scene=dict(theme="castle", layers=[
        dict(kind="array", var="color", label="team by person", style="tiles", pointers=["u"]),
        dict(kind="queue", var="q", label="to assign"),
    ]),
    reference="""class Solution {
public:
    bool possibleBipartition(int n, vector<vector<int>>& dislikes) {
        vector<vector<int>> adj(n + 1);
        for (auto& d : dislikes) {
            adj[d[0]].push_back(d[1]);
            adj[d[1]].push_back(d[0]);
        }
        vector<int> color(n + 1, 0);
        for (int s = 1; s <= n; s++) {
            if (color[s]) continue;
            queue<int> q;
            q.push(s);
            color[s] = 1;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                for (int v : adj[u]) {
                    if (color[v] == color[u]) return false;
                    if (!color[v]) {
                        color[v] = 3 - color[u];
                        q.push(v);
                    }
                }
            }
        }
        return true;
    }
};""",
)

add(
    id=890, slug="find-and-replace-pattern", title="Find and Replace Pattern", difficulty="Medium", world="arrays", tags=["array", "hash-table", "string"],
    story=dict(title="Words That Fit the Stencil", text="A word fits if its letters map one-to-one onto the pattern's letters. Two locker walls check the mapping both ways.",
               goal="Return the words matching the pattern."),
    spec=dict(method="findAndReplacePattern", ret="vector<string>", params=[["vector<string>&", "words"], ["string", "pattern"]]),
    tests=[dict(args=[["abc", "deq", "mee", "aqq", "dkd", "ccc"], "abb"], expected=["mee", "aqq"]), dict(args=[["a", "b", "c"], "a"], expected=["a", "b", "c"])],
    scene=dict(theme="lab", layers=[
        dict(kind="array", var="words", label="words", style="tiles", pointers=["k"]),
        dict(kind="row", children=[dict(kind="map", var="wp", label="word → pattern"), dict(kind="map", var="pw", label="pattern → word")]),
        dict(kind="array", var="res", label="fits", style="tiles"),
    ]),
    reference="""class Solution {
public:
    vector<string> findAndReplacePattern(vector<string>& words, string pattern) {
        vector<string> res;
        for (int k = 0; k < (int)words.size(); k++) {
            map<char, char> wp, pw;
            bool ok = true;
            for (int i = 0; i < (int)pattern.size() && ok; i++) {
                char a = words[k][i], b = pattern[i];
                if ((wp.count(a) && wp[a] != b) || (pw.count(b) && pw[b] != a)) ok = false;
                wp[a] = b;
                pw[b] = a;
            }
            if (ok) res.push_back(words[k]);
        }
        return res;
    }
};""",
)

add(
    id=896, slug="monotonic-array", title="Monotonic Array", difficulty="Easy", world="arrays", tags=["array"],
    story=dict(title="Always Uphill or Always Downhill", text="Walk the trail noting whether it ever rises and whether it ever falls; it's monotonic unless it does both.",
               goal="Return true if the array is monotone increasing or decreasing."),
    spec=dict(method="isMonotonic", ret="bool", params=[["vector<int>&", "nums"]]),
    tests=[dict(args=[[1, 2, 2, 3]], expected=True), dict(args=[[6, 5, 4, 4]], expected=True), dict(args=[[1, 3, 2]], expected=False)],
    scene=dict(theme="forest", layers=[
        dict(kind="bars", var="nums", label="trail", pointers=["i"]),
        dict(kind="values", vars=["up", "down"]),
    ]),
    reference="""class Solution {
public:
    bool isMonotonic(vector<int>& nums) {
        bool up = false, down = false;
        for (int i = 1; i < (int)nums.size(); i++) {
            if (nums[i] > nums[i - 1]) up = true;
            if (nums[i] < nums[i - 1]) down = true;
        }
        return !(up && down);
    }
};""",
)
