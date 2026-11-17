from judge.specs import P, C

P(1, "two-sum", "两数之和", "简单", "twoSum", ["ints", "int"], "ints",
  [C([[2, 7, 11, 15], 9], [0, 1], "unordered"),
   C([[3, 2, 4], 6], [1, 2], "unordered"),
   C([[3, 3], 6], [0, 1], "unordered")])
P(2, "add-two-numbers", "两数相加", "中等", "addTwoNumbers", ["list", "list"], "list",
  [C([[2, 4, 3], [5, 6, 4]], [7, 0, 8]),
   C([[0], [0]], [0]),
   C([[9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]], [8, 9, 9, 9, 0, 0, 0, 1])])
P(3, "longest-substring-without-repeating-characters", "无重复字符的最长子串", "中等",
  "lengthOfLongestSubstring", ["string"], "int",
  [C(["abcabcbb"], 3), C(["bbbbb"], 1), C(["pwwkew"], 3), C([""], 0)])
P(4, "median-of-two-sorted-arrays", "寻找两个正序数组的中位数", "困难",
  "findMedianSortedArrays", ["ints", "ints"], "double",
  [C([[1, 3], [2]], 2.0), C([[1, 2], [3, 4]], 2.5)], compare="float")
P(5, "longest-palindromic-substring", "最长回文子串", "中等", "longestPalindrome", ["string"], "string",
  [C(["babad"], {"any": ["bab", "aba"]}), C(["cbbd"], "bb"), C(["a"], "a"),
   C(["ac"], {"any": ["a", "c"]})])
P(6, "zigzag-conversion", "Z 字形变换", "中等", "convert", ["string", "int"], "string",
  [C(["PAYPALISHIRING", 3], "PAHNAPLSIIGYIR"),
   C(["PAYPALISHIRING", 4], "PINALSIGYAHRPI"), C(["A", 1], "A")])
P(7, "reverse-integer", "整数反转", "中等", "reverse", ["int"], "int",
  [C([123], 321), C([-123], -321), C([120], 21), C([0], 0), C([1534236469], 0)])
P(8, "string-to-integer-atoi", "字符串转换整数 (atoi)", "中等", "myAtoi", ["string"], "int",
  [C(["42"], 42), C(["   -42"], -42), C(["4193 with words"], 4193),
   C(["words and 987"], 0), C(["-91283472332"], -2147483648)])
P(9, "palindrome-number", "回文数", "简单", "isPalindrome", ["int"], "bool",
  [C([121], True), C([-121], False), C([10], False)])
P(10, "regular-expression-matching", "正则表达式匹配", "困难", "isMatch", ["string", "string"], "bool",
  [C(["aa", "a"], False), C(["aa", "a*"], True), C(["ab", ".*"], True),
   C(["aab", "c*a*b"], True), C(["mississippi", "mis*is*p*."], False)])
P(11, "container-with-most-water", "盛最多水的容器", "中等", "maxArea", ["ints"], "int",
  [C([[1, 8, 6, 2, 5, 4, 8, 3, 7]], 49), C([[1, 1]], 1)])
P(12, "integer-to-roman", "整数转罗马数字", "中等", "intToRoman", ["int"], "string",
  [C([3], "III"), C([4], "IV"), C([9], "IX"), C([58], "LVIII"), C([1994], "MCMXCIV")])
P(13, "roman-to-integer", "罗马数字转整数", "简单", "romanToInt", ["string"], "int",
  [C(["III"], 3), C(["LVIII"], 58), C(["MCMXCIV"], 1994)])
P(14, "longest-common-prefix", "最长公共前缀", "简单", "longestCommonPrefix", ["strings"], "string",
  [C([["flower", "flow", "flight"]], "fl"), C([["dog", "racecar", "car"]], "")])
P(15, "3sum", "三数之和", "中等", "threeSum", ["ints"], "intss",
  [C([[-1, 0, 1, 2, -1, -4]], [[-1, -1, 2], [-1, 0, 1]]),
   C([[0, 1, 1]], []), C([[0, 0, 0]], [[0, 0, 0]])], compare="unordered_deep")
P(16, "3sum-closest", "最接近的三数之和", "中等", "threeSumClosest", ["ints", "int"], "int",
  [C([[-1, 2, 1, -4], 1], 2), C([[0, 0, 0], 1], 0)])
P(17, "letter-combinations-of-a-phone-number", "电话号码的字母组合", "中等",
  "letterCombinations", ["string"], "strings",
  [C(["23"], ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]),
   C([""], []), C(["2"], ["a", "b", "c"])], compare="unordered")
P(18, "4sum", "四数之和", "中等", "fourSum", ["ints", "int"], "intss",
  [C([[1, 0, -1, 0, -2, 2], 0], [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
   C([[2, 2, 2, 2, 2], 8], [[2, 2, 2, 2]])], compare="unordered_deep")
P(19, "remove-nth-node-from-end-of-list", "删除链表的倒数第 N 个结点", "中等",
  "removeNthFromEnd", ["list", "int"], "list",
  [C([[1, 2, 3, 4, 5], 2], [1, 2, 3, 5]), C([[1], 1], []), C([[1, 2], 1], [1])])
P(20, "valid-parentheses", "有效的括号", "简单", "isValid", ["string"], "bool",
  [C(["()"], True), C(["()[]{}"], True), C(["(]"], False), C(["([)]"], False), C(["{[]}"], True)])
P(21, "merge-two-sorted-lists", "合并两个有序链表", "简单", "mergeTwoLists", ["list", "list"], "list",
  [C([[1, 2, 4], [1, 3, 4]], [1, 1, 2, 3, 4, 4]), C([[], []], []), C([[], [0]], [0])])
P(22, "generate-parentheses", "括号生成", "中等", "generateParenthesis", ["int"], "strings",
  [C([3], ["((()))", "(()())", "(())()", "()(())", "()()()"]), C([1], ["()"])],
  compare="unordered")
P(23, "merge-k-sorted-lists", "合并 K 个升序链表", "困难", "mergeKLists", ["lists"], "list",
  [C([[[1, 4, 5], [1, 3, 4], [2, 6]]], [1, 1, 2, 3, 4, 4, 5, 6]),
   C([[]], []), C([[[]]], [])])
P(24, "swap-nodes-in-pairs", "两两交换链表中的节点", "中等", "swapPairs", ["list"], "list",
  [C([[1, 2, 3, 4]], [2, 1, 4, 3]), C([[]], []), C([[1]], [1])])
P(25, "reverse-nodes-in-k-group", "K 个一组翻转链表", "困难", "reverseKGroup", ["list", "int"], "list",
  [C([[1, 2, 3, 4, 5], 2], [2, 1, 4, 3, 5]), C([[1, 2, 3, 4, 5], 3], [3, 2, 1, 4, 5])])
P(26, "remove-duplicates-from-sorted-array", "删除有序数组中的重复项", "简单",
  "removeDuplicates", ["ints"], "int",
  [C([[1, 1, 2]], [2, [1, 2]]),
   C([[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]], [5, [0, 1, 2, 3, 4]])],
  out={"ret_prefix": 0}, note="原地修改，返回 k；判题比较 [k, nums 前 k 项]")
P(27, "remove-element", "移除元素", "简单", "removeElement", ["ints", "int"], "int",
  [C([[3, 2, 2, 3], 3], [2, [2, 2]], "prefix_set"),
   C([[0, 1, 2, 2, 3, 0, 4, 2], 2], [5, [0, 1, 3, 0, 4]], "prefix_set")],
  out={"ret_prefix": 0}, note="原地修改；前 k 项顺序任意（按多重集比较）")
P(28, "find-the-index-of-the-first-occurrence-in-a-string", "找出字符串中第一个匹配项的下标", "简单",
  "strStr", ["string", "string"], "int",
  [C(["sadbutsad", "sad"], 0), C(["leetcode", "leeto"], -1), C(["a", "a"], 0)])
P(29, "divide-two-integers", "两数相除", "中等", "divide", ["int", "int"], "int",
  [C([10, 3], 3), C([7, -3], -2), C([0, 1], 0), C([1, 1], 1), C([-2147483648, -1], 2147483647)])
P(30, "substring-with-concatenation-of-all-words", "串联所有单词的子串", "困难",
  "findSubstring", ["string", "strings"], "ints",
  [C(["barfoothefoobarman", ["foo", "bar"]], [0, 9]),
   C(["wordgoodgoodgoodbestword", ["word", "good", "best", "word"]], []),
   C(["barfoofoobarthefoobarman", ["bar", "foo", "the"]], [6, 9, 12])], compare="unordered")
P(31, "next-permutation", "下一个排列", "中等", "nextPermutation", ["ints"], "void",
  [C([[1, 2, 3]], [1, 3, 2]), C([[3, 2, 1]], [1, 2, 3]), C([[1, 1, 5]], [1, 5, 1])],
  out={"arg": 0})
P(32, "longest-valid-parentheses", "最长有效括号", "困难", "longestValidParentheses", ["string"], "int",
  [C(["(()"], 2), C([")()())"], 4), C([""], 0)])
P(33, "search-in-rotated-sorted-array", "搜索旋转排序数组", "中等", "search", ["ints", "int"], "int",
  [C([[4, 5, 6, 7, 0, 1, 2], 0], 4), C([[4, 5, 6, 7, 0, 1, 2], 3], -1), C([[1], 0], -1)])
P(34, "find-first-and-last-position-of-element-in-sorted-array",
  "在排序数组中查找元素的第一个和最后一个位置", "中等", "searchRange", ["ints", "int"], "ints",
  [C([[5, 7, 7, 8, 8, 10], 8], [3, 4]), C([[5, 7, 7, 8, 8, 10], 6], [-1, -1]), C([[], 0], [-1, -1])])
P(35, "search-insert-position", "搜索插入位置", "简单", "searchInsert", ["ints", "int"], "int",
  [C([[1, 3, 5, 6], 5], 2), C([[1, 3, 5, 6], 2], 1), C([[1, 3, 5, 6], 7], 4)])
P(36, "valid-sudoku", "有效的数独", "中等", "isValidSudoku", ["grid"], "bool",
  [C([["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
       "7...2...6", ".6....28.", "...419..5", "....8..79"]], True),
   C([["83..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
       "7...2...6", ".6....28.", "...419..5", "....8..79"]], False)],
  note="棋盘用字符串数组表示，每行一个字符串，'.' 表示空格")
P(37, "sudoku-solver", "解数独", "困难", "solveSudoku", ["grid"], "void",
  [C([["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
       "7...2...6", ".6....28.", "...419..5", "....8..79"]],
      ["534678912", "672195348", "198342567", "859761423", "426853791",
       "713924856", "961537284", "287419635", "345286179"])],
  out={"arg": 0}, note="原地修改棋盘；字符串数组表示，每行一个字符串")
P(38, "count-and-say", "外观数列", "中等", "countAndSay", ["int"], "string",
  [C([1], "1"), C([2], "11"), C([3], "21"), C([4], "1211")])
P(39, "combination-sum", "组合总和", "中等", "combinationSum", ["ints", "int"], "intss",
  [C([[2, 3, 6, 7], 7], [[2, 2, 3], [7]]),
   C([[2, 3, 5], 8], [[2, 2, 2, 2], [2, 3, 3], [3, 5]]), C([[2], 1], [])],
  compare="unordered_deep")
P(40, "combination-sum-ii", "组合总和 II", "中等", "combinationSum2", ["ints", "int"], "intss",
  [C([[10, 1, 2, 7, 6, 1, 5], 8], [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]),
   C([[2, 5, 2, 1, 2], 5], [[1, 2, 2], [5]])], compare="unordered_deep")
P(41, "first-missing-positive", "缺失的第一个正数", "困难", "firstMissingPositive", ["ints"], "int",
  [C([[1, 2, 0]], 3), C([[3, 4, -1, 1]], 2), C([[7, 8, 9, 11, 12]], 1)])
P(42, "trapping-rain-water", "接雨水", "困难", "trap", ["ints"], "int",
  [C([[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], 6), C([[4, 2, 0, 3, 2, 5]], 9)])
P(43, "multiply-strings", "字符串相乘", "中等", "multiply", ["string", "string"], "string",
  [C(["2", "3"], "6"), C(["123", "456"], "56088"), C(["0", "52"], "0")])
P(44, "wildcard-matching", "通配符匹配", "困难", "isMatch", ["string", "string"], "bool",
  [C(["aa", "a"], False), C(["aa", "*"], True), C(["cb", "?a"], False),
   C(["adceb", "*a*b"], True), C(["acdcb", "a*c?b"], False)])
P(45, "jump-game-ii", "跳跃游戏 II", "中等", "jump", ["ints"], "int",
  [C([[2, 3, 1, 1, 4]], 2), C([[2, 3, 0, 1, 4]], 2), C([[0]], 0)])
P(46, "permutations", "全排列", "中等", "permute", ["ints"], "intss",
  [C([[1, 2, 3]], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
   C([[0, 1]], [[0, 1], [1, 0]]), C([[1]], [[1]])], compare="unordered")
P(47, "permutations-ii", "全排列 II", "中等", "permuteUnique", ["ints"], "intss",
  [C([[1, 1, 2]], [[1, 1, 2], [1, 2, 1], [2, 1, 1]]), C([[1, 1]], [[1, 1]])],
  compare="unordered")
P(48, "rotate-image", "旋转图像", "中等", "rotate", ["intss"], "void",
  [C([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
   C([[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]],
     [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]])],
  out={"arg": 0})
P(49, "group-anagrams", "字母异位词分组", "中等", "groupAnagrams", ["strings"], "stringss",
  [C([["eat", "tea", "tan", "ate", "nat", "bat"]],
     [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
   C([[""]], [[""]]), C([["a"]], [["a"]])], compare="unordered_deep")
P(50, "powx-n", "Pow(x, n)", "中等", "myPow", ["double", "int"], "double",
  [C([2.0, 10], 1024.0), C([2.1, 3], 9.261), C([2.0, -2], 0.25)], compare="float")