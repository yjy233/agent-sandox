from judge.specs import P, C

P(151, "reverse-words-in-a-string", "反转字符串中的单词", "中等", "reverseWords", ["string"], "string",
  [C(["the sky is blue"], "blue is sky the"), C(["  hello world  "], "world hello"),
   C(["a good   example"], "example good a")])
P(152, "maximum-product-subarray", "乘积最大子数组", "中等", "maxProduct", ["ints"], "int",
  [C([[2, 3, -2, 4]], 6), C([[-2, 0, -1]], 0)])
P(153, "find-minimum-in-rotated-sorted-array", "寻找旋转排序数组中的最小值", "中等",
  "findMin", ["ints"], "int",
  [C([[3, 4, 5, 1, 2]], 1), C([[4, 5, 6, 7, 0, 1, 2]], 0), C([[11, 13, 15, 17]], 11)])
P(154, "find-minimum-in-rotated-sorted-array-ii", "寻找旋转排序数组中的最小值 II", "困难",
  "findMin", ["ints"], "int",
  [C([[1, 3, 5]], 1), C([[2, 2, 2, 0, 1]], 0)])
P(155, "min-stack", "最小栈", "中等", None, [], "void", kind="design",
  **{"class": "MinStack", "ctor": [],
     "methods": {"push": {"params": ["int"], "ret": "void"},
                 "pop": {"params": [], "ret": "void"},
                 "top": {"params": [], "ret": "int"},
                 "getMin": {"params": [], "ret": "int"}}},
  cases=[{"ops": [["MinStack"], ["push", -2], ["push", 0], ["push", -3],
                  ["getMin"], ["pop"], ["top"], ["getMin"]],
          "expected": [None, None, None, None, -3, None, 0, -2]}],
  note="设计题：所有操作 O(1)")
P(156, "binary-tree-upside-down", "上下翻转二叉树", "中等", "upsideDownBinaryTree", ["tree"], "tree",
  [C([[1, 2, 3, 4, 5]], [4, 5, 2, None, None, 3, 1]), C([[]], []), C([[1]], [1])],
  note="原题锁定题；规则：最左节点成为新根，原父节点变为右子节点，原右兄弟变为左子节点")
P(157, "read-n-characters-given-read4", "用 Read4 读取 N 个字符", "简单", None, [], "void",
  kind="read4",
  cases=[{"file": "abc", "ns": [4], "expected": [[3, "abc"]]},
         {"file": "abcde", "ns": [3], "expected": [[3, "abc"]]}],
  note="判题器注入 read4；read(buf, n) 返回实际读取字符数，buf 前 r 项为读到的内容")
P(158, "read-n-characters-given-read4-ii-call-multiple-times",
  "用 Read4 读取 N 个字符 II - 多次调用", "困难", None, [], "void", kind="read4",
  cases=[{"file": "abc", "ns": [1, 2, 1], "expected": [[1, "a"], [2, "bc"], [0, ""]]},
         {"file": "abcde", "ns": [4, 4], "expected": [[4, "abcd"], [1, "e"]]}],
  note="read 会被多次调用，需跨调用保存 read4 的剩余缓冲")
P(159, "longest-substring-with-at-most-two-distinct-characters",
  "至多包含两个不同字符的最长子串", "中等", "lengthOfLongestSubstringTwoDistinct", ["string"], "int",
  [C(["eceba"], 3), C(["ccaabbb"], 5)], note="原题锁定题")
P(160, "intersection-of-two-linked-lists", "相交链表", "简单", "getIntersectionNode",
  ["intersect"], "list",
  [C([[4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3], 8),
   C([[1, 9, 1, 2, 4], [3, 2, 4], 3, 1], 2),
   C([[2, 6, 4], [1, 5], 3, 2], None)],
  special_ret="intersect_val",
  note="输入 [listA, listB, skipA, skipB]：判题器构造相交链表；输出相交节点值，不相交输出 null")
P(161, "one-edit-distance", "相隔为 1 的编辑距离", "中等", "isOneEditDistance", ["string", "string"], "bool",
  [C(["ab", "acb"], True), C(["cab", "ad"], False), C(["1203", "1213"], True),
   C(["a", "a"], False)], note="原题锁定题；恰好一次编辑（增/删/改一个字符）")
P(162, "find-peak-element", "寻找峰值", "中等", "findPeakElement", ["ints"], "int",
  [C([[1, 2, 3, 1]], 2), C([[1, 2, 1, 3, 5, 6, 4]], {"any": [1, 5]})],
  note="峰值不唯一，任一峰值下标均可")
P(163, "missing-ranges", "缺失的区间", "简单", "findMissingRanges", ["ints", "int", "int"], "intss",
  [C([[0, 1, 3, 50, 75], 0, 99], [[2, 2], [4, 49], [51, 74], [76, 99]]),
   C([[], 1, 1], [[1, 1]]), C([[], -3, -1], [[-3, -1]])],
  note="原题锁定题；采用新版返回格式 [[lo,hi],...]")
P(164, "maximum-gap", "最大间距", "中等", "maximumGap", ["ints"], "int",
  [C([[3, 6, 9, 1]], 3), C([[10]], 0), C([[1, 3, 100]], 97)])
P(165, "compare-version-numbers", "比较版本号", "中等", "compareVersion", ["string", "string"], "int",
  [C(["1.01", "1.001"], 0), C(["1.0", "1.0.0"], 0), C(["0.1", "1.1"], -1),
   C(["1.2", "1.10"], -1)])
P(166, "fraction-to-recurring-decimal", "分数到小数", "中等", "fractionToDecimal", ["long", "long"], "string",
  [C([1, 2], "0.5"), C([2, 1], "2"), C([2, 3], "0.(6)"), C([4, 333], "0.(012)"),
   C([-50, 8], "-6.25"), C([7, -12], "-0.58(3)")])
P(167, "two-sum-ii-input-array-is-sorted", "两数之和 II - 输入有序数组", "中等",
  "twoSum", ["ints", "int"], "ints",
  [C([[2, 7, 11, 15], 9], [1, 2]), C([[2, 3, 4], 6], [1, 3]), C([[-1, 0], -1], [1, 2])],
  note="返回 1-based 下标")
P(168, "excel-sheet-column-title", "Excel 表列名称", "简单", "convertToTitle", ["int"], "string",
  [C([1], "A"), C([28], "AB"), C([701], "ZY"), C([2147483647], "FXSHRXW")])
P(169, "majority-element", "多数元素", "简单", "majorityElement", ["ints"], "int",
  [C([[3, 2, 3]], 3), C([[2, 2, 1, 1, 1, 2, 2]], 2)])
P(170, "two-sum-iii-data-structure-design", "两数之和 III - 数据结构设计", "简单",
  None, [], "void", kind="design",
  **{"class": "TwoSum", "ctor": [],
     "methods": {"add": {"params": ["int"], "ret": "void"},
                 "find": {"params": ["int"], "ret": "bool"}}},
  cases=[{"ops": [["TwoSum"], ["add", 1], ["add", 3], ["add", 5], ["find", 4], ["find", 7]],
          "expected": [None, None, None, None, True, False]}],
  note="原题锁定题；find 判断是否存在两数之和等于目标（同一数可用两次当且仅当加入过两次）")
P(171, "excel-sheet-column-number", "Excel 表列序号", "简单", "titleToNumber", ["string"], "int",
  [C(["A"], 1), C(["AB"], 28), C(["ZY"], 701)])
P(172, "factorial-trailing-zeroes", "阶乘后的零", "中等", "trailingZeroes", ["int"], "int",
  [C([3], 0), C([5], 1), C([0], 0), C([25], 6)])
P(173, "binary-search-tree-iterator", "二叉搜索树迭代器", "中等", None, [], "void", kind="design",
  **{"class": "BSTIterator", "ctor": ["tree"],
     "methods": {"next": {"params": [], "ret": "int"},
                 "hasNext": {"params": [], "ret": "bool"}}},
  cases=[{"ops": [["BSTIterator", [7, 3, 15, None, None, 9, 20]],
                  ["next"], ["next"], ["hasNext"], ["next"], ["hasNext"],
                  ["next"], ["hasNext"], ["next"], ["hasNext"]],
          "expected": [None, 3, 7, True, 9, True, 15, True, 20, False]}],
  note="设计题：next/hasNext 均摊 O(1)，空间 O(h)")
P(174, "dungeon-game", "地下城游戏", "困难", "calculateMinimumHP", ["intss"], "int",
  [C([[[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]], 7), C([[[0]]], 1), C([[[-3]]], 4)])

P(175, "combine-two-tables", "组合两个表", "简单", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Person (personId INT, firstName VARCHAR(50), lastName VARCHAR(50));"
                   "CREATE TABLE Address (addressId INT, personId INT, city VARCHAR(50), state VARCHAR(50));"
                   "INSERT INTO Person VALUES (1,'Allen','Wang'),(2,'Bob','Alice');"
                   "INSERT INTO Address VALUES (1,2,'New York','NY');",
          "expected": [["Allen", "Wang", None, None], ["Bob", "Alice", "New York", "NY"]]}],
  note="输出列: firstName, lastName, city, state（无地址则为 NULL）")
P(176, "second-highest-salary", "第二高的薪水", "中等", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Employee (id INT, salary INT);"
                   "INSERT INTO Employee VALUES (1,100),(2,200),(3,300);",
          "expected": [[200]]},
         {"setup": "CREATE TABLE Employee (id INT, salary INT);"
                   "INSERT INTO Employee VALUES (1,100);",
          "expected": [[None]]}],
  note="输出列: SecondHighestSalary；不存在时为 NULL")
P(177, "nth-highest-salary", "第N高的薪水", "中等", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Employee (id INT, salary INT);"
                   "INSERT INTO Employee VALUES (1,100),(2,200),(3,300);",
          "params": {"N": 2}, "expected": [[200]]},
         {"setup": "CREATE TABLE Employee (id INT, salary INT);"
                   "INSERT INTO Employee VALUES (1,100),(2,200),(3,300);",
          "params": {"N": 1}, "expected": [[300]]},
         {"setup": "CREATE TABLE Employee (id INT, salary INT);"
                   "INSERT INTO Employee VALUES (1,100),(2,200),(3,300);",
          "params": {"N": 4}, "expected": [[None]]}],
  note="solution.sql 中用 {{N}} 占位，判题时替换为用例的 N；输出第 N 高薪水（去重），不存在为 NULL")
P(178, "rank-scores", "分数排名", "中等", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Scores (id INT, score DECIMAL(4,2));"
                   "INSERT INTO Scores VALUES (1,3.50),(2,3.65),(3,4.00),(4,3.85),(5,4.00),(6,3.65);",
          "expected": [[4.0, 1], [4.0, 1], [3.85, 2], [3.65, 3], [3.65, 3], [3.5, 4]],
          "ordered": True}],
  note="输出列: score, rank；按分数降序，dense rank（并列不跳号）")
P(179, "largest-number", "最大数", "中等", "largestNumber", ["ints"], "string",
  [C([[10, 2]], "210"), C([[3, 30, 34, 5, 9]], "9534330"), C([[0, 0]], "0")])
P(180, "consecutive-numbers", "连续出现的数字", "中等", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Logs (id INT, num INT);"
                   "INSERT INTO Logs VALUES (1,1),(2,1),(3,1),(4,2),(5,1),(6,2),(7,2);",
          "expected": [[1]]}],
  note="输出列: ConsecutiveNums；至少连续出现三次的数字（去重）")
P(181, "employees-earning-more-than-their-managers", "超过经理收入的员工", "简单",
  None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Employee (id INT, name VARCHAR(50), salary INT, managerId INT);"
                   "INSERT INTO Employee VALUES (1,'Joe',70000,3),(2,'Henry',80000,4),"
                   "(3,'Sam',60000,NULL),(4,'Max',90000,NULL);",
          "expected": [["Joe"]]}],
  note="输出列: Employee（员工姓名）")
P(182, "duplicate-emails", "查找重复的电子邮箱", "简单", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Person (id INT, email VARCHAR(100));"
                   "INSERT INTO Person VALUES (1,'a@b.com'),(2,'c@d.com'),(3,'a@b.com');",
          "expected": [["a@b.com"]]}],
  note="输出列: Email（去重）")
P(183, "customers-who-never-order", "从不订购的客户", "简单", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Customers (id INT, name VARCHAR(50));"
                   "CREATE TABLE Orders (id INT, customerId INT);"
                   "INSERT INTO Customers VALUES (1,'Joe'),(2,'Henry'),(3,'Sam'),(4,'Max');"
                   "INSERT INTO Orders VALUES (1,3),(2,1);",
          "expected": [["Henry"], ["Max"]]}],
  note="输出列: Customers（客户姓名）")
P(184, "department-highest-salary", "部门工资最高的员工", "中等", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Employee (id INT, name VARCHAR(50), salary INT, departmentId INT);"
                   "CREATE TABLE Department (id INT, name VARCHAR(50));"
                   "INSERT INTO Employee VALUES (1,'Joe',70000,1),(2,'Jim',90000,1),"
                   "(3,'Henry',80000,2),(4,'Sam',60000,2),(5,'Max',90000,1);"
                   "INSERT INTO Department VALUES (1,'IT'),(2,'Sales');",
          "expected": [["IT", "Joe", 70000], ["IT", "Max", 90000], ["Sales", "Henry", 80000]]}],
  note="输出列: Department, Employee, Salary（并列最高都输出）")
P(185, "department-top-three-salaries", "部门工资前三高的所有员工", "困难",
  None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Employee (id INT, name VARCHAR(50), salary INT, departmentId INT);"
                   "CREATE TABLE Department (id INT, name VARCHAR(50));"
                   "INSERT INTO Employee VALUES (1,'Joe',85000,1),(2,'Henry',80000,2),"
                   "(3,'Sam',60000,2),(4,'Max',90000,1),(5,'Janet',69000,1),"
                   "(6,'Randy',85000,1),(7,'Will',70000,1);"
                   "INSERT INTO Department VALUES (1,'IT'),(2,'Sales');",
          "expected": [["IT", "Max", 90000], ["IT", "Joe", 85000], ["IT", "Randy", 85000],
                       ["IT", "Will", 70000], ["Sales", "Henry", 80000], ["Sales", "Sam", 60000]]}],
  note="输出列: Department, Employee, Salary；部门内前三个不同最高薪水的所有员工")
P(186, "reverse-words-in-a-string-ii", "反转字符串中的单词 II", "中等", "reverseWords", ["strings"], "void",
  [C([["t", "h", "e", " ", "s", "k", "y", " ", "i", "s", " ", "b", "l", "u", "e"]],
     ["b", "l", "u", "e", " ", "i", "s", " ", "t", "h", "e", " ", "s", "k", "y"]),
   C([["a"]], ["a"])],
  out={"arg": 0}, note="原题锁定题；字符数组原地反转单词顺序，单词内字符顺序不变，O(1) 额外空间")
P(187, "repeated-dna-sequences", "重复的DNA序列", "中等", "findRepeatedDnaSequences", ["string"], "strings",
  [C(["AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"], ["AAAAACCCCC", "CCCCCAAAAA"]),
   C(["AAAAAAAAAAAAA"], ["AAAAAAAAAA"])], compare="unordered")
P(188, "best-time-to-buy-and-sell-stock-iv", "买卖股票的最佳时机 IV", "困难",
  "maxProfit", ["int", "ints"], "int",
  [C([2, [2, 4, 1]], 2), C([2, [3, 2, 6, 5, 0, 3]], 7)])
P(189, "rotate-array", "轮转数组", "中等", "rotate", ["ints", "int"], "void",
  [C([[1, 2, 3, 4, 5, 6, 7], 3], [5, 6, 7, 1, 2, 3, 4]),
   C([[-1, -100, 3, 99], 2], [3, 99, -1, -100])],
  out={"arg": 0}, note="原地轮转")
P(190, "reverse-bits", "颠倒二进制位", "简单", "reverseBits", ["uint32"], "uint32",
  [C([43261596], 964176192), C([4294967293], 3221225471)],
  note="输入为 32 位无符号整数")
P(191, "number-of-1-bits", "位1的个数", "简单", "hammingWeight", ["uint32"], "int",
  [C([11], 3), C([128], 1), C([4294967293], 31)])
P(192, "word-frequency", "统计词频", "中等", None, [], "void", kind="shell",
  cases=[{"files": {"words.txt": "the day is sunny the the\nthe sunny is is\n"},
          "expected": "the 4\nis 3\nsunny 2\nday 1\n"}],
  note="读取 words.txt，按词频降序输出 '单词 次数'")
P(193, "valid-phone-numbers", "有效电话号码", "简单", None, [], "void", kind="shell",
  cases=[{"files": {"file.txt": "987-123-4567\n123 456 7890\n(123) 456-7890\n"},
          "expected": "987-123-4567\n(123) 456-7890\n"}],
  note="读取 file.txt，输出格式为 (xxx) xxx-xxxx 或 xxx-xxx-xxxx 的行")
P(194, "transpose-file", "转置文件", "中等", None, [], "void", kind="shell",
  cases=[{"files": {"file.txt": "name age\nalice 21\nryan 30\n"},
          "expected": "name alice ryan\nage 21 30\n"}],
  note="读取 file.txt，转置行列（每行列数相同）")
P(195, "tenth-line", "第十行", "简单", None, [], "void", kind="shell",
  cases=[{"files": {"file.txt": "".join("Line %d\n" % i for i in range(1, 11))},
          "expected": "Line 10\n"},
         {"files": {"file.txt": "".join("Line %d\n" % i for i in range(1, 6))},
          "expected": ""}],
  note="输出 file.txt 第十行；不足十行输出空")
P(196, "delete-duplicate-emails", "删除重复的电子邮箱", "简单", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Person (id INT, email VARCHAR(100));"
                   "INSERT INTO Person VALUES (1,'john@example.com'),(2,'bob@example.com'),"
                   "(3,'john@example.com');",
          "verify": "SELECT id, email FROM Person ORDER BY id;",
          "expected": [[1, "john@example.com"], [2, "bob@example.com"]], "ordered": True}],
  note="写 DELETE 语句：删除重复邮箱，仅保留 id 最小的一行；判题执行后查询验证")
P(197, "rising-temperature", "上升的温度", "简单", None, [], "void", kind="sql",
  cases=[{"setup": "CREATE TABLE Weather (id INT, recordDate DATE, temperature INT);"
                   "INSERT INTO Weather VALUES (1,'2015-01-01',10),(2,'2015-01-02',25),"
                   "(3,'2015-01-03',20),(4,'2015-01-04',30);",
          "expected": [[2], [4]]}],
  note="输出列: id；温度比前一天高的日期 id")
P(198, "house-robber", "打家劫舍", "中等", "rob", ["ints"], "int",
  [C([[1, 2, 3, 1]], 4), C([[2, 7, 9, 3, 1]], 12)])
P(199, "binary-tree-right-side-view", "二叉树的右视图", "中等", "rightSideView", ["tree"], "ints",
  [C([[1, 2, 3, None, 5, None, 4]], [1, 3, 4]), C([[1, None, 3]], [1, 3]), C([[]], [])])
P(200, "number-of-islands", "岛屿数量", "中等", "numIslands", ["grid"], "int",
  [C([["11110", "11010", "11000", "00000"]], 1),
   C([["11000", "11000", "00100", "00011"]], 3)],
  note="网格用字符串数组表示，每行一个 '0'/'1' 字符串")