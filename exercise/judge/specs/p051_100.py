from judge.specs import P, C

P(51, "n-queens", "N 皇后", "困难", "solveNQueens", ["int"], "stringss",
  [C([4], [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]),
   C([1], [["Q"]])], compare="unordered")
P(52, "n-queens-ii", "N 皇后 II", "困难", "totalNQueens", ["int"], "int",
  [C([4], 2), C([1], 1), C([8], 92)])
P(53, "maximum-subarray", "最大子数组和", "中等", "maxSubArray", ["ints"], "int",
  [C([[-2, 1, -3, 4, -1, 2, 1, -5, 4]], 6), C([[1]], 1), C([[5, 4, -1, 7, 8]], 23)])
P(54, "spiral-matrix", "螺旋矩阵", "中等", "spiralOrder", ["intss"], "ints",
  [C([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
   C([[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])])
P(55, "jump-game", "跳跃游戏", "中等", "canJump", ["ints"], "bool",
  [C([[2, 3, 1, 1, 4]], True), C([[3, 2, 1, 0, 4]], False)])
P(56, "merge-intervals", "合并区间", "中等", "merge", ["intss"], "intss",
  [C([[[1, 3], [2, 6], [8, 10], [15, 18]]], [[1, 6], [8, 10], [15, 18]]),
   C([[[1, 4], [4, 5]]], [[1, 5]])])
P(57, "insert-interval", "插入区间", "中等", "insert", ["intss", "ints"], "intss",
  [C([[[1, 3], [6, 9]], [2, 5]], [[1, 5], [6, 9]]),
   C([[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]], [[1, 2], [3, 10], [12, 16]])])
P(58, "length-of-last-word", "最后一个单词的长度", "简单", "lengthOfLastWord", ["string"], "int",
  [C(["Hello World"], 5), C(["   fly me   to   the moon  "], 4), C(["luffy is still joyboy"], 6)])
P(59, "spiral-matrix-ii", "螺旋矩阵 II", "中等", "generateMatrix", ["int"], "intss",
  [C([3], [[1, 2, 3], [8, 9, 4], [7, 6, 5]]), C([1], [[1]])])
P(60, "permutation-sequence", "排列序列", "困难", "getPermutation", ["int", "int"], "string",
  [C([3, 3], "213"), C([4, 9], "2314"), C([3, 1], "123")])
P(61, "rotate-list", "旋转链表", "中等", "rotateRight", ["list", "int"], "list",
  [C([[1, 2, 3, 4, 5], 2], [4, 5, 1, 2, 3]), C([[0, 1, 2], 4], [2, 0, 1])])
P(62, "unique-paths", "不同路径", "中等", "uniquePaths", ["int", "int"], "int",
  [C([3, 7], 28), C([3, 2], 3), C([7, 3], 28), C([3, 3], 6)])
P(63, "unique-paths-ii", "不同路径 II", "中等", "uniquePathsWithObstacles", ["intss"], "int",
  [C([[[0, 0, 0], [0, 1, 0], [0, 0, 0]]], 2), C([[[0, 1], [0, 0]]], 1)])
P(64, "minimum-path-sum", "最小路径和", "中等", "minPathSum", ["intss"], "int",
  [C([[[1, 3, 1], [1, 5, 1], [4, 2, 1]]], 7), C([[[1, 2, 3], [4, 5, 6]]], 12)])
P(65, "valid-number", "有效数字", "困难", "isNumber", ["string"], "bool",
  [C(["0"], True), C([" 0.1 "], True), C(["abc"], False), C(["1 a"], False),
   C(["2e10"], True), C([" -90e3   "], True), C(["1e"], False), C(["e3"], False),
   C([" 6e-1"], True), C([" 99e2.5 "], False), C(["53.5e93"], True),
   C([" --6 "], False), C(["-+3"], False), C(["95a54e53"], False)])
P(66, "plus-one", "加一", "简单", "plusOne", ["ints"], "ints",
  [C([[1, 2, 3]], [1, 2, 4]), C([[4, 3, 2, 1]], [4, 3, 2, 2]), C([[9]], [1, 0])])
P(67, "add-binary", "二进制求和", "简单", "addBinary", ["string", "string"], "string",
  [C(["11", "1"], "100"), C(["1010", "1011"], "10101")])
P(68, "text-justification", "文本左右对齐", "困难", "fullJustify", ["strings", "int"], "strings",
  [C([["This", "is", "an", "example", "of", "text", "justification."], 16],
     ["This    is    an", "example  of text", "justification.  "]),
   C([["What", "must", "be", "acknowledgment", "shall", "be"], 16],
     ["What   must   be", "acknowledgment  ", "shall be        "])])
P(69, "sqrtx", "x 的平方根", "简单", "mySqrt", ["int"], "int",
  [C([4], 2), C([8], 2), C([0], 0), C([1], 1)])
P(70, "climbing-stairs", "爬楼梯", "简单", "climbStairs", ["int"], "int",
  [C([2], 2), C([3], 3), C([1], 1)])
P(71, "simplify-path", "简化路径", "中等", "simplifyPath", ["string"], "string",
  [C(["/home/"], "/home"), C(["/../"], "/"), C(["/home//foo/"], "/home/foo"),
   C(["/a/./b/../../c/"], "/c")])
P(72, "edit-distance", "编辑距离", "中等", "minDistance", ["string", "string"], "int",
  [C(["horse", "ros"], 3), C(["intention", "execution"], 5)])
P(73, "set-matrix-zeroes", "矩阵置零", "中等", "setZeroes", ["intss"], "void",
  [C([[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
   C([[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])],
  out={"arg": 0})
P(74, "search-a-2d-matrix", "搜索二维矩阵", "中等", "searchMatrix", ["intss", "int"], "bool",
  [C([[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3], True),
   C([[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13], False)])
P(75, "sort-colors", "颜色分类", "中等", "sortColors", ["ints"], "void",
  [C([[2, 0, 2, 1, 1, 0]], [0, 0, 1, 1, 2, 2]), C([[2, 0, 1]], [0, 1, 2])],
  out={"arg": 0})
P(76, "minimum-window-substring", "最小覆盖子串", "困难", "minWindow", ["string", "string"], "string",
  [C(["ADOBECODEBANC", "ABC"], "BANC"), C(["a", "a"], "a"), C(["a", "aa"], "")])
P(77, "combinations", "组合", "中等", "combine", ["int", "int"], "intss",
  [C([4, 2], [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]), C([1, 1], [[1]])],
  compare="unordered_deep")
P(78, "subsets", "子集", "中等", "subsets", ["ints"], "intss",
  [C([[1, 2, 3]], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]),
   C([[0]], [[], [0]])], compare="unordered_deep")
P(79, "word-search", "单词搜索", "中等", "exist", ["grid", "string"], "bool",
  [C([["ABCE", "SFCS", "ADEE"], "ABCCED"], True),
   C([["ABCE", "SFCS", "ADEE"], "SEE"], True),
   C([["ABCE", "SFCS", "ADEE"], "ABCB"], False)],
  note="棋盘用字符串数组表示，每行一个字符串")
P(80, "remove-duplicates-from-sorted-array-ii", "删除有序数组中的重复项 II", "中等",
  "removeDuplicates", ["ints"], "int",
  [C([[1, 1, 1, 2, 2, 3]], [5, [1, 1, 2, 2, 3]]),
   C([[0, 0, 1, 1, 1, 1, 2, 3, 3]], [7, [0, 0, 1, 1, 2, 3, 3]])],
  out={"ret_prefix": 0})
P(81, "search-in-rotated-sorted-array-ii", "搜索旋转排序数组 II", "中等", "search", ["ints", "int"], "bool",
  [C([[2, 5, 6, 0, 0, 1, 2], 0], True), C([[2, 5, 6, 0, 0, 1, 2], 3], False)])
P(82, "remove-duplicates-from-sorted-list-ii", "删除排序链表中的重复元素 II", "中等",
  "deleteDuplicates", ["list"], "list",
  [C([[1, 2, 3, 3, 4, 4, 5]], [1, 2, 5]), C([[1, 1, 1, 2, 3]], [2, 3])])
P(83, "remove-duplicates-from-sorted-list", "删除排序链表中的重复元素", "简单",
  "deleteDuplicates", ["list"], "list",
  [C([[1, 1, 2]], [1, 2]), C([[1, 1, 2, 3, 3]], [1, 2, 3])])
P(84, "largest-rectangle-in-histogram", "柱状图中最大的矩形", "困难",
  "largestRectangleArea", ["ints"], "int",
  [C([[2, 1, 5, 6, 2, 3]], 10), C([[2, 4]], 4)])
P(85, "maximal-rectangle", "最大矩形", "困难", "maximalRectangle", ["grid"], "int",
  [C([["10100", "10111", "11111", "10010"]], 6), C([["0"]], 0), C([["1"]], 1)],
  note="矩阵用字符串数组表示，每行一个 '0'/'1' 字符串")
P(86, "partition-list", "分隔链表", "中等", "partition", ["list", "int"], "list",
  [C([[1, 4, 3, 2, 5, 2], 3], [1, 2, 2, 4, 3, 5]), C([[2, 1], 2], [1, 2])])
P(87, "scramble-string", "扰乱字符串", "困难", "isScramble", ["string", "string"], "bool",
  [C(["great", "rgeat"], True), C(["abcde", "caebd"], False), C(["a", "a"], True)])
P(88, "merge-sorted-array", "合并两个有序数组", "简单", "merge", ["ints", "int", "ints", "int"], "void",
  [C([[1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3], [1, 2, 2, 3, 5, 6]),
   C([[1], 1, [], 0], [1]), C([[0], 0, [1], 1], [1])],
  out={"arg": 0}, note="原地合并到 nums1")
P(89, "gray-code", "格雷编码", "中等", "grayCode", ["int"], "ints",
  [C([2], [0, 1, 3, 2]), C([1], [0, 1]), C([0], [0])],
  note="判题按标准反射格雷码顺序比较：n 位结果 = [0] + [x | 1<<(n-1) for x in 反序(n-1位结果)]")
P(90, "subsets-ii", "子集 II", "中等", "subsetsWithDup", ["ints"], "intss",
  [C([[1, 2, 2]], [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]), C([[0]], [[], [0]])],
  compare="unordered_deep")
P(91, "decode-ways", "解码方法", "中等", "numDecodings", ["string"], "int",
  [C(["12"], 2), C(["226"], 3), C(["06"], 0), C(["0"], 0), C(["10"], 1)])
P(92, "reverse-linked-list-ii", "反转链表 II", "中等", "reverseBetween", ["list", "int", "int"], "list",
  [C([[1, 2, 3, 4, 5], 2, 4], [1, 4, 3, 2, 5]), C([[5], 1, 1], [5])])
P(93, "restore-ip-addresses", "复原 IP 地址", "中等", "restoreIpAddresses", ["string"], "strings",
  [C(["25525511135"], ["255.255.11.135", "255.255.111.35"]),
   C(["0000"], ["0.0.0.0"]), C(["1111"], ["1.1.1.1"])], compare="unordered")
P(94, "binary-tree-inorder-traversal", "二叉树的中序遍历", "简单", "inorderTraversal", ["tree"], "ints",
  [C([[1, None, 2, 3]], [1, 3, 2]), C([[]], []), C([[1]], [1])],
  note="树用层序数组表示，null 表示空节点")
P(95, "unique-binary-search-trees-ii", "不同的二叉搜索树 II", "中等", "generateTrees", ["int"], "trees",
  [C([3], [[1, None, 2, None, 3], [1, None, 3, 2], [2, 1, 3],
           [3, 1, None, None, 2], [3, 2, None, 1]]),
   C([2], [[1, None, 2], [2, 1]]), C([1], [[1]])], compare="unordered_deep",
  note="返回所有 BST 根节点；每棵树序列化为层序数组（去掉末尾 null）")
P(96, "unique-binary-search-trees", "不同的二叉搜索树", "中等", "numTrees", ["int"], "int",
  [C([3], 5), C([1], 1), C([4], 14)])
P(97, "interleaving-string", "交错字符串", "中等", "isInterleave", ["string", "string", "string"], "bool",
  [C(["aabcc", "dbbca", "aadbbcbcac"], True),
   C(["aabcc", "dbbca", "aadbbbaccc"], False), C(["", "", ""], True)])
P(98, "validate-binary-search-tree", "验证二叉搜索树", "中等", "isValidBST", ["tree"], "bool",
  [C([[2, 1, 3]], True), C([[5, 1, 4, None, None, 3, 6]], False)])
P(99, "recover-binary-search-tree", "恢复二叉搜索树", "中等", "recoverTree", ["tree"], "void",
  [C([[1, 3, None, None, 2]], [3, 1, None, None, 2]),
   C([[3, 1, 4, None, None, 2]], [2, 1, 4, None, None, 3])],
  out={"arg": 0}, note="原地交换两个被错误放置的节点值")
P(100, "same-tree", "相同的树", "简单", "isSameTree", ["tree", "tree"], "bool",
  [C([[1, 2, 3], [1, 2, 3]], True), C([[1, 2], [1, None, 2]], False),
   C([[1, 2, 1], [1, 1, 2]], False)])