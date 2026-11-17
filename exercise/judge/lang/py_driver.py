"""Universal python driver. Usage: python3 driver.py problem.json solution.py [case_idx]"""
import importlib.util
import json
import sys
import traceback


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class Node:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val, self.left, self.right, self.next = val, left, right, next


class GNode:
    def __init__(self, val=0, neighbors=None):
        self.val, self.neighbors = val, neighbors or []


class RNode:
    def __init__(self, val=0, next=None, random=None):
        self.val, self.next, self.random = val, next, random


def build_list(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_slice(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(vals, cls=TreeNode):
    if not vals or vals[0] is None:
        return None
    root = cls(vals[0])
    queue, i = [root], 1
    while queue and i < len(vals):
        n = queue.pop(0)
        if i < len(vals):
            v = vals[i]; i += 1
            if v is not None:
                n.left = cls(v)
                queue.append(n.left)
        if i < len(vals):
            v = vals[i]; i += 1
            if v is not None:
                n.right = cls(v)
                queue.append(n.right)
    return root


def tree_to_slice(root):
    if not root:
        return []
    out, queue = [], [root]
    while queue:
        n = queue.pop(0)
        if n is None:
            out.append(None)
            continue
        out.append(n.val)
        queue.append(n.left)
        queue.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


def trees_to_slices(roots):
    return [tree_to_slice(r) for r in roots]


def build_next_tree(vals):
    return build_tree(vals, Node)


def next_levels(root):
    if not root:
        return []
    out, leftmost = [], root
    while leftmost:
        level, n = [], leftmost
        while n:
            level.append(n.val)
            n = n.next
        out.append(level)
        nxt = None
        n = leftmost
        while n:
            if n.left:
                nxt = n.left
                break
            if n.right:
                nxt = n.right
                break
            n = n.next
        leftmost = nxt
    return out


def build_lists(arrs):
    return [build_list(a) for a in arrs]


def build_cycle_list(vals, pos):
    nodes = [ListNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if nodes and 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return (nodes[0] if nodes else None), nodes


def cycle_index(ret, nodes):
    for i, n in enumerate(nodes):
        if n is ret:
            return i
    return -1


def build_intersect(a, b, skip_a, skip_b):
    if skip_a >= len(a) or skip_b >= len(b):
        return build_list(a), build_list(b)
    common = build_list(a[skip_a:])
    ha = build_list(a[:skip_a])
    hb = build_list(b[:skip_b])
    if ha is None:
        ha = common
    else:
        t = ha
        while t.next:
            t = t.next
        t.next = common
    if hb is None:
        hb = common
    else:
        t = hb
        while t.next:
            t = t.next
        t.next = common
    return ha, hb


def val_or_null(node):
    return node.val if node else None


def build_random_list(rows):
    if not rows:
        return None
    nodes = [RNode(r[0]) for r in rows]
    for i, r in enumerate(rows):
        nodes[i].next = nodes[r[1]] if r[1] >= 0 else None
        nodes[i].random = nodes[r[2]] if r[2] >= 0 else None
    return nodes[0]


def dump_random_list(head):
    nodes, n = [], head
    while n:
        nodes.append(n)
        n = n.next
    idx = {id(n): i for i, n in enumerate(nodes)}
    out = []
    for n in nodes:
        out.append([n.val,
                    idx[id(n.next)] if n.next else -1,
                    idx[id(n.random)] if n.random else -1])
    return out


def build_graph(adj):
    if not adj:
        return None
    nodes = [GNode(i + 1) for i in range(len(adj))]
    for i, nb in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nb]
    return nodes[0]


def dump_graph(node):
    if not node:
        return []
    seen, queue = {}, [node]
    while queue:
        n = queue.pop(0)
        if n.val in seen:
            continue
        seen[n.val] = n
        queue.extend(n.neighbors)
    return [sorted(x.val for x in seen[v].neighbors) for v in sorted(seen)]


def convert_arg(t, v):
    if t == "list":
        return build_list(v)
    if t == "tree":
        return build_tree(v)
    if t == "nexttree":
        return build_next_tree(v)
    if t == "lists":
        return build_lists(v)
    if t == "randomlist":
        return build_random_list(v)
    if t == "graph":
        return build_graph(v)
    return v


def serialize(t, v):
    if t == "list":
        return list_to_slice(v)
    if t == "tree":
        return tree_to_slice(v)
    if t == "trees":
        return trees_to_slices(v)
    if t == "nexttree":
        return next_levels(v)
    if t == "randomlist":
        return dump_random_list(v)
    if t == "graph":
        return dump_graph(v)
    return v


def run_func(mod, spec, case):
    args = list(case["args"])
    call, i = [], 0
    for t in spec["params"]:
        if t == "cyclelist":
            head, nodes = build_cycle_list(args[i], args[i + 1])
            call.append(head)
            i += 2
        elif t == "intersect":
            ha, hb = build_intersect(args[i], args[i + 1], args[i + 2], args[i + 3])
            call.extend([ha, hb])
            i += 4
        else:
            call.append(convert_arg(t, args[i]))
            i += 1
    fn = getattr(mod, spec["func"])
    ret = fn(*call)
    out = spec.get("out")
    if out and "arg" in out:
        j = out["arg"]
        return serialize(spec["params"][j], call[j])
    if out and "ret_prefix" in out:
        j = out["ret_prefix"]
        return [ret, call[j][:ret]]
    if spec.get("special_ret") == "cycle_index":
        return cycle_index(ret, nodes)
    if spec.get("special_ret") == "intersect_val":
        return val_or_null(ret)
    return serialize(spec["ret"], ret)


def run_design(mod, spec, case):
    cls = getattr(mod, spec["class"])
    obj, results = None, []
    for op in case["ops"]:
        name, args = op[0], op[1:]
        if name == spec["class"]:
            args = [convert_arg(t, v) for t, v in zip(spec["ctor"], args)]
            obj = cls(*args)
            results.append(None)
        else:
            ms = spec["methods"][name]
            args = [convert_arg(t, v) for t, v in zip(ms["params"], args)]
            r = getattr(obj, name)(*args)
            results.append(None if ms["ret"] == "void" else serialize(ms["ret"], r))
    return results


def run_read4(mod, spec, case):
    obj = mod.Solution()
    data, pos = case["file"], [0]

    def read4(buf4):
        cnt = 0
        while cnt < 4 and pos[0] < len(data):
            buf4[cnt] = data[pos[0]]
            pos[0] += 1
            cnt += 1
        return cnt

    obj.read4 = read4
    results = []
    for n in case["ns"]:
        buf = [""] * max(4, n)
        r = obj.read(buf, n)
        results.append([r, "".join(buf[:r])])
    return results


def main():
    with open(sys.argv[1]) as f:
        spec = json.load(f)
    sol_path = sys.argv[2]
    only = int(sys.argv[3]) if len(sys.argv) > 3 else -1
    s = importlib.util.spec_from_file_location("solution", sol_path)
    mod = importlib.util.module_from_spec(s)
    try:
        s.loader.exec_module(mod)
    except Exception:
        for _ in spec["cases"]:
            print(json.dumps({"ok": False, "error": traceback.format_exc()[-2000:]}))
        return
    kind = spec.get("kind", "func")
    runner = {"func": run_func, "design": run_design, "read4": run_read4}[kind]
    for i, case in enumerate(spec["cases"]):
        if only >= 0 and i != only:
            continue
        try:
            out = runner(mod, spec, case)
            print(json.dumps({"ok": True, "output": out}, ensure_ascii=False))
        except Exception:
            print(json.dumps({"ok": False, "error": traceback.format_exc()[-2000:]}))


if __name__ == "__main__":
    main()