# 89. 格雷编码

- 难度: 中等
- 链接: https://leetcode.cn/problems/gray-code/

编辑对应语言的 solution 文件，然后:

```bash
../../ex run 89 -l py      # 运行样例 0
../../ex test 89 -l py     # 判题 (py/go/cpp/ts)
../../ex test 89 -l all    # 四语言全测
```

> 判题按标准反射格雷码顺序比较：n 位结果 = [0] + [x | 1<<(n-1) for x in 反序(n-1位结果)]

用例数: 3
