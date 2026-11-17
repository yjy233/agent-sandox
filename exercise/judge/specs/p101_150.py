from judge.specs import P, C

P(101, "symmetric-tree", "对称二叉树", "简单", "isSymmetric", ["tree"], "bool",
  [C([[1, 2, 2, 3, 4, 4, 3]], True), C([[1, 2, 2, None, 3, None, 3]], False)])
P(102, "binary-tree-level-order-traversal", "二叉树的层序遍历", "中等", "levelOrder", ["tree"], "intss",
  [C([[3, 9, 20, None, None, 15, 7]], [[3], [9, 20], [15, 7]]), C([[1]], [[1]]), C([[]], [])])
P(103, "binary-tree-zigzag-level-order-traversal", "二叉树的锯齿形层序遍历", "中等",
  "zigzagLevelOrder", ["tree"], "intss",
  [C([[3, 9, 20, None, None, 15, 7]], [[3], [20, 9], [15, 7]]), C([[1]], [[1]]), C([[]], [])])
P(104, "maximum-depth-of-binary-tree", "二叉树的最大深度", "简单", "maxDepth", ["tree"], "int",
  [C([[3, 9, 20, None, None, 15, 7]], 3), C([[1, None, 2]], 2), C([[]], 0)])
P(105, "construct-binary-tree-from-preorder-and-inorder-traversal",
  "从前序与中序遍历序列构造二叉树", "中等", "buildTree", ["ints", "ints"], "tree",
  [C([[3, 9, 20, 15, 7], [9, 3, 15, 20, 7]], [3, 9, 20, None, None, 15, 7]),
   C([[-1], [-1]], [-1])])
P(106, "construct-binary-tree-from-inorder-and-postorder-traversal",
  "从中序与后序遍历序列构造二叉树", "中等", "buildTree", ["ints", "ints"], "tree",
  [C([[9, 3, 15, 20, 7], [9, 15, 7, 20, 3]], [3, 9, 20, None, None, 15, 7]),
   C([[-1], [-1]], [-1])])
P(107, "binary-tree-level-order-traversal-ii", "二叉树的层序遍历 II", "中等",
  "levelOrderBottom", ["tree"], "intss",
  [C([[3, 9, 20, None, None, 15, 7]], [[15, 7], [9, 20], [3]]), C([[1]], [[1]]), C([[]], [])])
P(108, "convert-sorted-array-to-binary-search-tree", "将有序数组转换为二叉搜索树", "简单",
  "sortedArrayToBST", ["ints"], "tree",
  [C([[-10, -3, 0, 5, 9]], None), C([[1, 3]], None)], compare="bst",
  note="答案不唯一：判题检查输出是输入值构成的高度平衡 BST")
P(109, "convert-sorted-list-to-binary-search-tree", "有序链表转换二叉搜索树", "中等",
  "sortedListToBST", ["list"], "tree",
  [C([[-10, -3, 0, 5, 9]], None), C([[]], None)], compare="bst",
  note="答案不唯一：判题检查输出是输入值构成的高度平衡 BST")
P(110, "balanced-binary-tree", "平衡二叉树", "简单", "isBalanced", ["tree"], "bool",
  [C([[3, 9, 20, None, None, 15, 7]], True),
   C([[1, 2, 2, 3, 3, None, None, 4, 4]], False)])
P(111, "minimum-depth-of-binary-tree", "二叉树的最小深度", "简单", "minDepth", ["tree"], "int",
  [C([[3, 9, 20, None, None, 15, 7]], 2),
   C([[2, None, 3, None, 4, None, 5, None, 6]], 5)])
P(112, "path-sum", "路径总和", "简单", "hasPathSum", ["tree", "int"], "bool",
  [C([[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22], True),
   C([[1, 2, 3], 5], False), C([[], 0], False)])
P(113, "path-sum-ii", "路径总和 II", "中等", "pathSum", ["tree", "int"], "intss",
  [C([[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22],
     [[5, 4, 11, 2], [5, 8, 4, 5]]),
   C([[1, 2, 3], 5], []), C([[1, 2], 0], [])], compare="unordered")
P(114, "flatten-binary-tree-to-linked-list", "二叉树展开为链表", "中等", "flatten", ["tree"], "void",
  [C([[1, 2, 5, 3, 4, None, 6]], [1, None, 2, None, 3, None, 4, None, 5, None, 6]),
   C([[]], []), C([[0]], [0])],
  out={"arg": 0}, note="原地展开：所有节点的 left 置空，right 指向先序遍历的下一个节点")
P(115, "distinct-subsequences", "不同的子序列", "困难", "numDistinct", ["string", "string"], "int",
  [C(["rabbbit", "rabbit"], 3), C(["babgbag", "bag"], 5)])
P(116, "populating-next-right-pointers-in-each-node", "填充每个节点的下一个右侧节点指针", "中等",
  "connect", ["nexttree"], "nexttree",
  [C([[1, 2, 3, 4, 5, 6, 7]], [[1], [2, 3], [4, 5, 6, 7]]), C([[]], [])],
  note="Node 含 val/left/right/next；输出按层序列化 next 链：[[1],[2,3],[4,5,6,7]]")
P(117, "populating-next-right-pointers-in-each-node-ii", "填充每个节点的下一个右侧节点指针 II", "中等",
  "connect", ["nexttree"], "nexttree",
  [C([[1, 2, 3, 4, 5, None, 7]], [[1], [2, 3], [4, 5, 7]]), C([[]], [])],
  note="Node 含 val/left/right/next；输出按层序列化 next 链")
P(118, "pascals-triangle", "杨辉三角", "简单", "generate", ["int"], "intss",
  [C([5], [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]), C([1], [[1]])])
P(119, "pascals-triangle-ii", "杨辉三角 II", "简单", "getRow", ["int"], "ints",
  [C([3], [1, 3, 3, 1]), C([0], [1]), C([1], [1, 1])])
P(120, "triangle", "三角形最小路径和", "中等", "minimumTotal", ["intss"], "int",
  [C([[[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]], 11), C([[[-10]]], -10)])
P(121, "best-time-to-buy-and-sell-stock", "买卖股票的最佳时机", "简单", "maxProfit", ["ints"], "int",
  [C([[7, 1, 5, 3, 6, 4]], 5), C([[7, 6, 4, 3, 1]], 0)])
P(122, "best-time-to-buy-and-sell-stock-ii", "买卖股票的最佳时机 II", "中等", "maxProfit", ["ints"], "int",
  [C([[7, 1, 5, 3, 6, 4]], 7), C([[1, 2, 3, 4, 5]], 4), C([[7, 6, 4, 3, 1]], 0)])
P(123, "best-time-to-buy-and-sell-stock-iii", "买卖股票的最佳时机 III", "困难", "maxProfit", ["ints"], "int",
  [C([[3, 3, 5, 0, 0, 3, 1, 4]], 6), C([[1, 2, 3, 4, 5]], 4), C([[7, 6, 4, 3, 1]], 0)])
P(124, "binary-tree-maximum-path-sum", "二叉树中的最大路径和", "困难", "maxPathSum", ["tree"], "int",
  [C([[1, 2, 3]], 6), C([[-10, 9, 20, None, None, 15, 7]], 42)])
P(125, "valid-palindrome", "验证回文串", "简单", "isPalindrome", ["string"], "bool",
  [C(["A man, a plan, a canal: Panama"], True), C(["race a car"], False), C([" "], True)])
P(126, "word-ladder-ii", "单词接龙 II", "困难", "findLadders", ["string", "string", "strings"], "stringss",
  [C(["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]],
     [["hit", "hot", "dot", "dog", "cog"], ["hit", "hot", "lot", "log", "cog"]]),
   C(["hit", "cog", ["hot", "dot", "dog", "lot", "log"]], [])], compare="unordered")
P(127, "word-ladder", "单词接龙", "困难", "ladderLength", ["string", "string", "strings"], "int",
  [C(["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]], 5),
   C(["hit", "cog", ["hot", "dot", "dog", "lot", "log"]], 0)])
P(128, "longest-consecutive-sequence", "最长连续序列", "中等", "longestConsecutive", ["ints"], "int",
  [C([[100, 4, 200, 1, 3, 2]], 4), C([[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], 9)])
P(129, "sum-root-to-leaf-numbers", "求根节点到叶节点数字之和", "中等", "sumNumbers", ["tree"], "int",
  [C([[1, 2, 3]], 25), C([[4, 9, 0, 5, 1]], 1026)])
P(130, "surrounded-regions", "被围绕的区域", "中等", "solve", ["grid"], "void",
  [C([["XXXX", "XOOX", "XXOX", "XOXX"]], ["XXXX", "XXXX", "XXXX", "XOXX"]),
   C([["X"]], ["X"])],
  out={"arg": 0}, note="原地修改；字符串数组表示棋盘，修改时整行替换")
P(131, "palindrome-partitioning", "分割回文串", "中等", "partition", ["string"], "stringss",
  [C(["aab"], [["a", "a", "b"], ["aa", "b"]]), C(["a"], [["a"]])], compare="unordered")
P(132, "palindrome-partitioning-ii", "分割回文串 II", "困难", "minCut", ["string"], "int",
  [C(["aab"], 1), C(["a"], 0), C(["ab"], 1)])
P(133, "clone-graph", "克隆图", "中等", "cloneGraph", ["graph"], "graph",
  [C([[[2, 4], [1, 3], [2, 4], [1, 3]]], [[2, 4], [1, 3], [2, 4], [1, 3]]),
   C([[[]]], [[]]), C([[]], [])],
  note="图用邻接表表示（节点编号 1..n）；GNode 含 val 与 neighbors；需深拷贝")
P(134, "gas-station", "加油站", "中等", "canCompleteCircuit", ["ints", "ints"], "int",
  [C([[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], 3), C([[2, 3, 4], [3, 4, 3]], -1)])
P(135, "candy", "分发糖果", "困难", "candy", ["ints"], "int",
  [C([[1, 0, 2]], 5), C([[1, 2, 2]], 4)])
P(136, "single-number", "只出现一次的数字", "简单", "singleNumber", ["ints"], "int",
  [C([[2, 2, 1]], 1), C([[4, 1, 2, 1, 2]], 4), C([[1]], 1)])
P(137, "single-number-ii", "只出现一次的数字 II", "中等", "singleNumber", ["ints"], "int",
  [C([[2, 2, 3, 2]], 3), C([[0, 1, 0, 1, 0, 1, 99]], 99)])
P(138, "copy-list-with-random-pointer", "随机链表的复制", "中等", "copyRandomList",
  ["randomlist"], "randomlist",
  [C([[[7, 1, -1], [13, 2, 0], [11, 3, 4], [10, 4, 2], [1, -1, 0]]],
     [[7, 1, -1], [13, 2, 0], [11, 3, 4], [10, 4, 2], [1, -1, 0]]),
   C([[]], [])],
  note="输入/输出格式: 每个节点 [val, next下标, random下标]，-1 表示 null；需深拷贝")
P(139, "word-break", "单词拆分", "中等", "wordBreak", ["string", "strings"], "bool",
  [C(["leetcode", ["leet", "code"]], True),
   C(["applepenapple", ["apple", "pen"]], True),
   C(["catsandog", ["cats", "dog", "sand", "and", "cat"]], False)])
P(140, "word-break-ii", "单词拆分 II", "困难", "wordBreak", ["string", "strings"], "strings",
  [C(["catsanddog", ["cat", "cats", "and", "sand", "dog"]],
     ["cats and dog", "cat sand dog"]),
   C(["pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]],
     ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]),
   C(["catsandog", ["cats", "dog", "sand", "and", "cat"]], [])], compare="unordered")
P(141, "linked-list-cycle", "环形链表", "简单", "hasCycle", ["cyclelist"], "bool",
  [C([[3, 2, 0, -4], 1], True), C([[1, 2], 0], True), C([[1], -1], False)],
  note="输入 [节点值数组, pos]：pos 为尾节点指向的下标，-1 表示无环")
P(142, "linked-list-cycle-ii", "环形链表 II", "中等", "detectCycle", ["cyclelist"], "list",
  [C([[3, 2, 0, -4], 1], 1), C([[1, 2], 0], 0), C([[1], -1], -1)],
  special_ret="cycle_index",
  note="返回入环节点；判题输出该节点在原链表中的下标，无环输出 -1")
P(143, "reorder-list", "重排链表", "中等", "reorderList", ["list"], "void",
  [C([[1, 2, 3, 4]], [1, 4, 2, 3]), C([[1, 2, 3, 4, 5]], [1, 5, 2, 4, 3])],
  out={"arg": 0}, note="原地重排 L0→Ln→L1→Ln-1→…")
P(144, "binary-tree-preorder-traversal", "二叉树的前序遍历", "简单", "preorderTraversal", ["tree"], "ints",
  [C([[1, None, 2, 3]], [1, 2, 3]), C([[]], []), C([[1]], [1])])
P(145, "binary-tree-postorder-traversal", "二叉树的后序遍历", "简单", "postorderTraversal", ["tree"], "ints",
  [C([[1, None, 2, 3]], [3, 2, 1]), C([[]], []), C([[1]], [1])])
P(146, "lru-cache", "LRU 缓存", "中等", None, [], "void", kind="design",
  **{"class": "LRUCache", "ctor": ["int"],
     "methods": {"get": {"params": ["int"], "ret": "int"},
                 "put": {"params": ["int", "int"], "ret": "void"}}},
  cases=[{"ops": [["LRUCache", 2], ["put", 1, 1], ["put", 2, 2], ["get", 1],
                  ["put", 3, 3], ["get", 2], ["put", 4, 4], ["get", 1],
                  ["get", 3], ["get", 4]],
          "expected": [None, None, None, 1, None, -1, None, -1, 3, 4]}],
  note="设计题：实现 LRUCache 类（get/put 均 O(1)）；ops 首项为构造")
P(147, "insertion-sort-list", "对链表进行插入排序", "中等", "insertionSortList", ["list"], "list",
  [C([[4, 2, 1, 3]], [1, 2, 3, 4]), C([[-1, 5, 3, 4, 0]], [-1, 0, 3, 4, 5])])
P(148, "sort-list", "排序链表", "中等", "sortList", ["list"], "list",
  [C([[4, 2, 1, 3]], [1, 2, 3, 4]), C([[-1, 5, 3, 4, 0]], [-1, 0, 3, 4, 5]), C([[]], [])])
P(149, "max-points-on-a-line", "直线上最多的点数", "困难", "maxPoints", ["intss"], "int",
  [C([[[1, 1], [2, 2], [3, 3]]], 3),
   C([[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]], 4)])
P(150, "evaluate-reverse-polish-notation", "逆波兰表达式求值", "中等", "evalRPN", ["strings"], "int",
  [C([["2", "1", "+", "3", "*"]], 9), C([["4", "13", "5", "/", "+"]], 6),
   C([["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]], 22)])