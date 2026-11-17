# LeetCode 练习场（exercise）

205 道题（1–200 + LCP 06/12/13/15/16），每题支持 **Python3 / Go / C++ / TypeScript** 四种语言，
自带测试用例与本地判题器。SQL 题（175–185、196、197）用 sqlite3 判题，Shell 题（192–195）用 bash 判题。

## 快速开始

```bash
cd exercise

./ex list                     # 全部题目 + 完成状态
./ex list -d 简单 -u          # 只看未通过的简单题
./ex list -k 链表             # 按关键词过滤

# 做题：编辑 problems/0001-two-sum/solution.py（或 .go / .cpp / .ts）

./ex run 1 -l py              # 运行用例 0，打印输出
./ex run 1 -l go -c 2         # 运行用例 2
./ex test 1 -l py             # 判题（全部用例）
./ex test 1 -l all            # 四语言全部判一遍
./ex test 1 -l cpp -v         # 失败时打印输入
./ex show 1                   # 查看题目 spec（签名/用例/比较方式）
```

判题全部通过后自动记录到 `.progress.json`，`./ex list` 中显示 `✓py` 等标记。

## 目录结构

```
exercise/
├── ex                    # CLI 入口
├── judge/                # 判题器（比较器/运行器/生成器/题目数据）
│   ├── specs/            # 205 题的签名 + 用例数据
│   └── lang/             # 四语言驱动器与数据结构 helpers
├── problems/             # 每题一个目录
│   └── 0001-two-sum/
│       ├── problem.json  # 题目 spec（可补充用例）
│       ├── README.md     # 题目说明 + 力扣链接
│       ├── solution.py / solution.go / solution.cpp / solution.ts
└── .build/               # 编译/运行临时产物（可删）
```

## 各语言约定

- **Python3**：直接写函数/类，签名见 stub。链表/树节点由判题器传入，按 `.val/.next/.left/.right` 使用即可。
- **Go**：`package main`，可直接使用 helpers 中的 `ListNode{Val,Next}`、`TreeNode{Val,Left,Right}`、
  `Node`（含 Next）、`GNode`（图）、`RNode`（random 链表）。设计题实现 `Constructor` 返回指针 + 小写方法名（`get/put`）。
- **C++**：solution.cpp 会被 `#include` 进驱动，可直接使用 `ListNode/TreeNode/Node/GNode/RNode`（成员小写 `val/next/left/right`）
  与 `std::vector` 等。数组参数为**非常量引用**（原地修改题直接改）。设计题方法名小写。
- **TypeScript**：Node ≥ 23.6 原生运行（type stripping）。**只用可擦除语法**：不要用 enum、namespace、
  构造函数参数属性（`constructor(private x)`）；类型名 `ListNode/TreeNode` 等可直接写在注解里（运行时擦除，无需定义）。
  函数/类需要 `export`。

## 特殊表示法

- **树**：层序数组，`null` 表示空节点，如 `[3,9,20,null,null,15,7]`。
- **grid 类题**（数独/单词搜索/岛屿等）：字符串数组，每行一个字符串；原地修改时整行替换（`board[i] = ...`）。
- **环链表**（141/142）：输入 `[值数组, pos]`；142 输出入环节点下标（无环 -1）。
- **相交链表**（160）：输入 `[listA, listB, skipA, skipB]`，输出相交节点值或 null。
- **随机链表**（138）：每节点 `[val, next下标, random下标]`，-1 表示 null。
- **图**（133）：邻接表，节点编号 1..n。
- **next 指针树**（116/117）：输出按层的 next 链 `[[1],[2,3],[4,5,6,7]]`。
- **设计题**（146/155/170/173）：按 `ops` 序列构造对象并调用方法，逐条比对返回值。
- **read4**（157/158）：判题器注入 `read4`，你实现 `read(buf, n)`。
- **原地坐标题**（26/27/80 等）：返回 k 并修改数组，判题比较 `[k, 前k项]`。
- **答案不唯一**：5/162 任一合法答案；15/18/39/40/46/47/49/77/78/90/95 等按集合比较；
  108/109 检查是否为高度平衡 BST；89 按标准反射格雷码顺序。

## 补充 / 修改用例

编辑 `problems/<题目>/problem.json` 的 `cases`：

```json
{"args": [[2,7,11,15], 9], "expected": [0,1], "compare": "unordered"}
```

`compare` 可选：`exact`（默认）/ `unordered` / `unordered_deep` / `float` / `prefix_set` / `bst`；
`expected` 可写 `{"any": [...]}` 接受多个答案。LCP13/15/16 暂无用例，请自行补充。

重新生成目录（**不会覆盖已有 solution 文件**）：

```bash
python3 -m judge.generate
```

## 依赖

python3、go、g++（C++17）、node（≥23.6，建议 24+）、sqlite3（python 内置模块）。