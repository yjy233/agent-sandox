from judge.specs import P, C

P("LCP06", "na-ying-bi", "拿硬币", "简单", "minCount", ["ints"], "int",
  [C([[4, 2, 1]], 4), C([[2, 3, 10]], 8)],
  note="每堆每次可拿 1 或 2 枚，求拿完所有硬币的最少次数")
P("LCP12", "xiao-zhang-shua-ti-ji-hua", "小张刷题计划", "中等", "splitArray", ["ints", "int"], "int",
  [C([[1, 2, 3], 1], 3), C([[1, 2, 3], 2], 1), C([[1, 2, 3, 4, 5], 2], 4)],
  note="把数组分成 m 段连续子数组，每段代价为段内和减去段内最大值，最小化最大段代价")
P("LCP13", "xun-bao", "寻宝", "困难", "minimumSteps", ["grid"], "int",
  cases=[],
  note="maze 为字符串数组（S 起点 T 终点 O 空地 # 墙 M 机关）；官方用例较复杂，请自行补充到 problem.json")
P("LCP15", "you-le-yuan-de-mi-gong", "游乐园的迷宫", "困难", "visitOrder", ["int", "intss", "ints"], "ints",
  cases=[],
  note="visitOrder(N, roads, distanceLimit)；请核对力扣签名并自行补充用例")
P("LCP16", "you-le-yuan-de-you-lan-ji-hua", "游乐园的游览计划", "困难", "maxWeight", ["intss", "ints", "intss"], "int",
  cases=[],
  note="maxWeight(edges, values, nums)；请核对力扣签名并自行补充用例")