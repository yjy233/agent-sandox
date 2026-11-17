"""Output comparators for the exercise judge."""
import json
import math


def _norm(x):
    if isinstance(x, float) and x.is_integer():
        return int(x)
    if isinstance(x, list):
        return [_norm(v) for v in x]
    if isinstance(x, dict):
        return {k: _norm(v) for k, v in x.items()}
    return x


def _key(x):
    return json.dumps(_norm(x), sort_keys=True, ensure_ascii=False)


def _sort_deep(x):
    if isinstance(x, list):
        return sorted((_sort_deep(v) for v in x), key=_key)
    return x


def _float_eq(a, b, tol=1e-5):
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_float_eq(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=tol, abs_tol=tol)
    return a == b


def _tree_from_level(vals):
    if not vals or vals[0] is None:
        return None
    nodes = [None if v is None else {"v": v, "l": None, "r": None} for v in vals]
    kids = iter(nodes[1:])
    for n in nodes:
        if n is None:
            continue
        n["l"] = next(kids, None)
        n["r"] = next(kids, None)
    return nodes[0]


def _inorder(root):
    out, stack, cur = [], [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur["l"]
        cur = stack.pop()
        out.append(cur["v"])
        cur = cur["r"]
    return out


def _balanced(root):
    def height(n):
        if n is None:
            return 0
        lh, rh = height(n["l"]), height(n["r"])
        if lh < 0 or rh < 0 or abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)
    return height(root) >= 0


def compare(output, expected, mode, case=None):
    """Return (passed: bool, reason: str)."""
    output, expected = _norm(output), _norm(expected)
    if isinstance(expected, dict) and "any" in expected:
        results = [compare(output, opt, mode, case) for opt in expected["any"]]
        if any(p for p, _ in results):
            return True, ""
        return False, "output matches none of the accepted answers"
    if mode == "float":
        ok = _float_eq(output, expected)
    elif mode == "unordered":
        ok = isinstance(output, list) and isinstance(expected, list) and \
            sorted(output, key=_key) == sorted(expected, key=_key)
    elif mode == "unordered_deep":
        ok = _key(_sort_deep(output)) == _key(_sort_deep(expected))
    elif mode == "prefix_set":
        # [k, prefix]: k equal, prefix equal as multiset
        ok = (isinstance(output, list) and len(output) == 2 and
              output[0] == expected[0] and
              isinstance(output[1], list) and
              sorted(output[1], key=_key) == sorted(expected[1], key=_key))
    elif mode == "bst":
        nums = case["args"][0] if case else []
        root = _tree_from_level(output) if isinstance(output, list) else None
        ok = root is not None or not nums
        if ok and nums:
            ok = _inorder(root) == sorted(nums) and _balanced(root)
        if not ok:
            return False, "output is not a height-balanced BST of the input values"
    else:
        ok = output == expected
    if ok:
        return True, ""
    return False, "expected %s, got %s" % (
        json.dumps(expected, ensure_ascii=False), json.dumps(output, ensure_ascii=False))