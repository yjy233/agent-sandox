package main

import (
	"encoding/json"
	"sort"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

type Node struct {
	Val   int
	Left  *Node
	Right *Node
	Next  *Node
}

type GNode struct {
	Val       int
	Neighbors []*GNode
}

type RNode struct {
	Val    int
	Next   *RNode
	Random *RNode
}

func mustUnmarshal(raw json.RawMessage, v interface{}) {
	if err := json.Unmarshal(raw, v); err != nil {
		panic(err)
	}
}

func buildList(vals []int) *ListNode {
	dummy := &ListNode{}
	cur := dummy
	for _, v := range vals {
		cur.Next = &ListNode{Val: v}
		cur = cur.Next
	}
	return dummy.Next
}

func listToSlice(head *ListNode) []int {
	out := []int{}
	for head != nil {
		out = append(out, head.Val)
		head = head.Next
	}
	return out
}

func buildTreeFromLevel(vals []interface{}) *TreeNode {
	if len(vals) == 0 || vals[0] == nil {
		return nil
	}
	root := &TreeNode{Val: int(vals[0].(float64))}
	queue := []*TreeNode{root}
	i := 1
	for len(queue) > 0 && i < len(vals) {
		n := queue[0]
		queue = queue[1:]
		if i < len(vals) {
			v := vals[i]
			i++
			if v != nil {
				n.Left = &TreeNode{Val: int(v.(float64))}
				queue = append(queue, n.Left)
			}
		}
		if i < len(vals) {
			v := vals[i]
			i++
			if v != nil {
				n.Right = &TreeNode{Val: int(v.(float64))}
				queue = append(queue, n.Right)
			}
		}
	}
	return root
}

func treeToSlice(root *TreeNode) []interface{} {
	if root == nil {
		return []interface{}{}
	}
	out := []interface{}{}
	queue := []*TreeNode{root}
	for len(queue) > 0 {
		n := queue[0]
		queue = queue[1:]
		if n == nil {
			out = append(out, nil)
			continue
		}
		out = append(out, n.Val)
		queue = append(queue, n.Left)
		queue = append(queue, n.Right)
	}
	for len(out) > 0 && out[len(out)-1] == nil {
		out = out[:len(out)-1]
	}
	return out
}

func treesToSlices(roots []*TreeNode) [][]interface{} {
	out := [][]interface{}{}
	for _, r := range roots {
		out = append(out, treeToSlice(r))
	}
	return out
}

func buildNextTree(vals []interface{}) *Node {
	if len(vals) == 0 || vals[0] == nil {
		return nil
	}
	root := &Node{Val: int(vals[0].(float64))}
	queue := []*Node{root}
	i := 1
	for len(queue) > 0 && i < len(vals) {
		n := queue[0]
		queue = queue[1:]
		if i < len(vals) {
			v := vals[i]
			i++
			if v != nil {
				n.Left = &Node{Val: int(v.(float64))}
				queue = append(queue, n.Left)
			}
		}
		if i < len(vals) {
			v := vals[i]
			i++
			if v != nil {
				n.Right = &Node{Val: int(v.(float64))}
				queue = append(queue, n.Right)
			}
		}
	}
	return root
}

func nextLevels(root *Node) [][]int {
	if root == nil {
		return [][]int{}
	}
	out := [][]int{}
	leftmost := root
	for leftmost != nil {
		level := []int{}
		for n := leftmost; n != nil; n = n.Next {
			level = append(level, n.Val)
		}
		out = append(out, level)
		var nxt *Node
		for n := leftmost; n != nil; n = n.Next {
			if n.Left != nil {
				nxt = n.Left
				break
			}
			if n.Right != nil {
				nxt = n.Right
				break
			}
		}
		leftmost = nxt
	}
	return out
}

func buildLists(arrs [][]int) []*ListNode {
	out := []*ListNode{}
	for _, a := range arrs {
		out = append(out, buildList(a))
	}
	return out
}

func buildCycleList(vals []int, pos int) (*ListNode, []*ListNode) {
	nodes := []*ListNode{}
	for _, v := range vals {
		nodes = append(nodes, &ListNode{Val: v})
	}
	for i := 0; i+1 < len(nodes); i++ {
		nodes[i].Next = nodes[i+1]
	}
	if len(nodes) > 0 && pos >= 0 && pos < len(nodes) {
		nodes[len(nodes)-1].Next = nodes[pos]
	}
	if len(nodes) == 0 {
		return nil, nodes
	}
	return nodes[0], nodes
}

func cycleIndex(ret *ListNode, nodes []*ListNode) int {
	for i, n := range nodes {
		if n == ret {
			return i
		}
	}
	return -1
}

func buildIntersect(a, b []int, skipA, skipB int) (*ListNode, *ListNode) {
	if skipA >= len(a) || skipB >= len(b) {
		return buildList(a), buildList(b)
	}
	common := buildList(a[skipA:])
	ha := buildList(a[:skipA])
	hb := buildList(b[:skipB])
	if ha == nil {
		ha = common
	} else {
		t := ha
		for t.Next != nil {
			t = t.Next
		}
		t.Next = common
	}
	if hb == nil {
		hb = common
	} else {
		t := hb
		for t.Next != nil {
			t = t.Next
		}
		t.Next = common
	}
	return ha, hb
}

func valOrNull(n *ListNode) interface{} {
	if n == nil {
		return nil
	}
	return n.Val
}

func buildRandomList(rows [][]int) *RNode {
	if len(rows) == 0 {
		return nil
	}
	nodes := []*RNode{}
	for _, r := range rows {
		nodes = append(nodes, &RNode{Val: r[0]})
	}
	for i, r := range rows {
		if r[1] >= 0 {
			nodes[i].Next = nodes[r[1]]
		}
		if r[2] >= 0 {
			nodes[i].Random = nodes[r[2]]
		}
	}
	return nodes[0]
}

func dumpRandomList(head *RNode) [][]int {
	nodes := []*RNode{}
	for n := head; n != nil; n = n.Next {
		nodes = append(nodes, n)
	}
	idx := map[*RNode]int{}
	for i, n := range nodes {
		idx[n] = i
	}
	out := [][]int{}
	for _, n := range nodes {
		ni, ri := -1, -1
		if n.Next != nil {
			ni = idx[n.Next]
		}
		if n.Random != nil {
			ri = idx[n.Random]
		}
		out = append(out, []int{n.Val, ni, ri})
	}
	return out
}

func buildGraph(adj [][]int) *GNode {
	if len(adj) == 0 {
		return nil
	}
	nodes := []*GNode{}
	for i := range adj {
		nodes = append(nodes, &GNode{Val: i + 1})
	}
	for i, nb := range adj {
		for _, j := range nb {
			nodes[i].Neighbors = append(nodes[i].Neighbors, nodes[j-1])
		}
	}
	return nodes[0]
}

func dumpGraph(node *GNode) [][]int {
	if node == nil {
		return [][]int{}
	}
	seen := map[int]*GNode{}
	queue := []*GNode{node}
	for len(queue) > 0 {
		n := queue[0]
		queue = queue[1:]
		if _, ok := seen[n.Val]; ok {
			continue
		}
		seen[n.Val] = n
		queue = append(queue, n.Neighbors...)
	}
	vals := []int{}
	for v := range seen {
		vals = append(vals, v)
	}
	sort.Ints(vals)
	out := [][]int{}
	for _, v := range vals {
		nb := []int{}
		for _, x := range seen[v].Neighbors {
			nb = append(nb, x.Val)
		}
		sort.Ints(nb)
		out = append(out, nb)
	}
	return out
}

type Read4Source struct {
	data []byte
	pos  int
}

func newRead4Source(s string) *Read4Source {
	return &Read4Source{data: []byte(s)}
}

func (s *Read4Source) Read4(buf []byte) int {
	cnt := 0
	for cnt < 4 && s.pos < len(s.data) {
		buf[cnt] = s.data[s.pos]
		s.pos++
		cnt++
	}
	return cnt
}