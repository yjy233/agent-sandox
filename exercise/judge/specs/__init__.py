"""Problem spec registry.

Types:
  int long uint32 double bool string void
  ints([]int) intss([][]int) strings([]string) stringss([][]string) grid([]string rows)
  list(ListNode) tree(TreeNode) trees([]TreeNode) lists([]ListNode)
  nexttree(Node with next) randomlist graph cyclelist intersect
Kinds: func(default) design read4 sql shell
"""
import importlib
import os

REGISTRY = {}


def C(args, expected, compare=None, **extra):
    d = {"args": args, "expected": expected}
    if compare:
        d["compare"] = compare
    d.update(extra)
    return d


def P(pid, slug, title, difficulty, func, params, ret, cases=None,
      compare="exact", kind="func", out=None, **extra):
    spec = {
        "id": pid, "slug": slug, "title": title, "difficulty": difficulty,
        "kind": kind, "func": func, "params": params, "ret": ret,
        "compare": compare, "cases": cases or [],
    }
    if out:
        spec["out"] = out
    spec.update(extra)
    key = str(pid).lower().replace(" ", "")
    REGISTRY[key] = spec
    return spec


def _load():
    here = os.path.dirname(__file__)
    for name in sorted(os.listdir(here)):
        if name.startswith("p") and name.endswith(".py"):
            importlib.import_module("judge.specs." + name[:-3])


_load()


def get(pid):
    key = str(pid).lower().replace(" ", "").lstrip("0") or "0"
    if key in REGISTRY:
        return REGISTRY[key]
    key2 = str(pid).lower().replace(" ", "")
    if key2 in REGISTRY:
        return REGISTRY[key2]
    # numeric ids stored zero-stripped; lcp ids stored as 'lcp06'
    for k, v in REGISTRY.items():
        if k.lstrip("0") == key or k == key2:
            return v
    raise KeyError("unknown problem id: %s" % pid)


def all_specs():
    def sort_key(s):
        pid = str(s["id"])
        if pid.lower().startswith("lcp"):
            return (1, int(pid[3:]))
        return (0, int(pid))
    return sorted(REGISTRY.values(), key=sort_key)