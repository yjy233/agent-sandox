"""Generate problem directories (stubs + problem.json + README) from specs.

Existing solution files are never overwritten.
Usage: python3 -m judge.generate
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from judge import specs
from judge.cli import problem_dir, LANG_FILE

PY_T = {"int": "int", "long": "int", "uint32": "int", "double": "float", "bool": "bool",
        "string": "str", "ints": "List[int]", "intss": "List[List[int]]", "strings": "List[str]",
        "stringss": "List[List[str]]", "grid": "List[str]", "list": "Optional[ListNode]",
        "tree": "Optional[TreeNode]", "trees": "List[TreeNode]", "lists": "List[Optional[ListNode]]",
        "nexttree": "Optional[Node]", "randomlist": "Optional[RNode]", "graph": "Optional[GNode]",
        "void": "None"}
GO_T = {"int": "int", "long": "int64", "uint32": "uint32", "double": "float64", "bool": "bool",
        "string": "string", "ints": "[]int", "intss": "[][]int", "strings": "[]string",
        "stringss": "[][]string", "grid": "[]string", "list": "*ListNode", "tree": "*TreeNode",
        "trees": "[]*TreeNode", "lists": "[]*ListNode", "nexttree": "*Node",
        "randomlist": "*RNode", "graph": "*GNode", "void": ""}
CPP_T = {"int": "int", "long": "long long", "uint32": "uint32_t", "double": "double",
         "bool": "bool", "string": "std::string", "ints": "std::vector<int>&",
         "intss": "std::vector<std::vector<int>>&", "strings": "std::vector<std::string>&",
         "stringss": "std::vector<std::vector<std::string>>&", "grid": "std::vector<std::string>&",
         "list": "ListNode*", "tree": "TreeNode*", "trees": "std::vector<TreeNode*>",
         "lists": "std::vector<ListNode*>", "nexttree": "Node*", "randomlist": "RNode*",
         "graph": "GNode*", "void": "void"}
TS_T = {"int": "number", "long": "number", "uint32": "number", "double": "number",
        "bool": "boolean", "string": "string", "ints": "number[]", "intss": "number[][]",
        "strings": "string[]", "stringss": "string[][]", "grid": "string[]",
        "list": "ListNode | null", "tree": "TreeNode | null", "trees": "(TreeNode | null)[]",
        "lists": "(ListNode | null)[]", "nexttree": "Node | null", "randomlist": "RNode | null",
        "graph": "GNode | null", "void": "void"}

PARAM_NAMES = {
    "twoSum": ["nums", "target"], "addTwoNumbers": ["l1", "l2"],
}


def _names(spec):
    if spec["params"] == ["intersect"]:
        return ["headA", "headB"]
    if spec["params"] == ["cyclelist"]:
        return ["head"]
    n = len(_stub_params(spec))
    base = ["nums", "target", "s", "t", "p", "q", "root", "head", "grid", "matrix",
            "words", "k", "n", "m", "x", "y"]
    return [base[i] if i < len(base) else "arg%d" % i for i in range(n)]


def _stub_params(spec):
    out = []
    for t in spec["params"]:
        if t == "cyclelist":
            out.append("list")
        elif t == "intersect":
            out.extend(["list", "list"])
        else:
            out.append(t)
    return out


def _default_ret(lang, t):
    if t == "void":
        return ""
    if lang == "py":
        if t in ("int", "long", "uint32", "double"):
            return "return 0"
        if t == "bool":
            return "return False"
        if t == "string":
            return 'return ""'
        if t in ("ints", "intss", "strings", "stringss", "grid", "trees", "lists"):
            return "return []"
        return "pass"
    if lang == "go":
        return 'panic("TODO")'
    if lang == "cpp":
        return 'throw std::runtime_error("TODO");'
    if lang == "ts":
        if t in ("int", "long", "uint32", "double"):
            return "return 0;"
        if t == "bool":
            return "return false;"
        if t == "string":
            return 'return "";'
        if t in ("ints", "intss", "strings", "stringss", "grid", "trees", "lists"):
            return "return [];"
        return "return null;"
    return ""


def _sig_types(spec):
    return _stub_params(spec)


def gen_py(spec):
    lines = ["from __future__ import annotations", "from typing import List, Optional", ""]
    names = _names(spec)
    if spec["kind"] == "design":
        cls = spec["class"]
        lines.append("class %s:" % cls)
        ctor = spec["ctor"]
        cn = ["capacity" if t == "int" else "root" for t in ctor]
        args = ", ".join("%s: %s" % (cn[i], PY_T[t]) for i, t in enumerate(ctor))
        lines.append("    def __init__(self%s):" % (", " + args if args else ""))
        lines.append("        # TODO")
        lines.append("        pass")
        for m, ms in spec["methods"].items():
            ma = ", ".join("p%d: %s" % (i, PY_T[t]) for i, t in enumerate(ms["params"]))
            lines.append("")
            lines.append("    def %s(self%s) -> %s:" % (m, ", " + ma if ma else "", PY_T[ms["ret"]]))
            lines.append("        " + (_default_ret("py", ms["ret"]) or "pass"))
        return "\n".join(lines) + "\n"
    if spec["kind"] == "read4":
        return ("from __future__ import annotations\nfrom typing import List\n\n\n"
                "class Solution:\n"
                "    def read(self, buf: List[str], n: int) -> int:\n"
                "        # 判题器已注入 self.read4(buf4) -> int，每次最多读 4 个字符\n"
                "        pass\n")
    args = ", ".join("%s: %s" % (names[i], PY_T[t]) for i, t in enumerate(_sig_types(spec)))
    lines.append("def %s(%s) -> %s:" % (spec["func"], args, PY_T[spec["ret"]]))
    lines.append("    " + (_default_ret("py", spec["ret"]) or "pass"))
    return "\n".join(lines) + "\n"


def gen_go(spec):
    names = _names(spec)
    if spec["kind"] == "design":
        cls = spec["class"]
        lines = ["package main", "", "type %s struct {" % cls, "\t// TODO", "}", ""]
        cn = ["capacity" if t == "int" else "root" for t in spec["ctor"]]
        args = ", ".join("%s %s" % (cn[i], GO_T[t]) for i, t in enumerate(spec["ctor"]))
        lines.append("func Constructor(%s) *%s {" % (args, cls))
        lines.append("\treturn &%s{}" % cls)
        lines.append("}")
        for m, ms in spec["methods"].items():
            ma = ", ".join("p%d %s" % (i, GO_T[t]) for i, t in enumerate(ms["params"]))
            rt = GO_T[ms["ret"]]
            lines.append("")
            lines.append("func (o *%s) %s(%s)%s {" % (cls, m, ma, " " + rt if rt else ""))
            lines.append("\t" + (_default_ret("go", ms["ret"]) or "// TODO"))
            lines.append("}")
        return "\n".join(lines) + "\n"
    if spec["kind"] == "read4":
        return ("package main\n\n"
                "type Solution struct {\n\t*Read4Source\n}\n\n"
                "func (s *Solution) read(buf []byte, n int) int {\n"
                "\t// 调用 s.Read4(buf4) 每次最多读 4 字节\n"
                '\tpanic("TODO")\n}\n')
    args = ", ".join("%s %s" % (names[i], GO_T[t]) for i, t in enumerate(_sig_types(spec)))
    rt = GO_T[spec["ret"]]
    lines = ["package main", "", "func %s(%s)%s {" % (spec["func"], args, " " + rt if rt else "")]
    lines.append("\t" + (_default_ret("go", spec["ret"]) or "// TODO"))
    lines.append("}")
    return "\n".join(lines) + "\n"


def gen_cpp(spec):
    names = _names(spec)
    head = '#include "helpers.hpp"\n\n'
    if spec["kind"] == "design":
        cls = spec["class"]
        lines = ["class %s {" % cls, "public:"]
        cn = ["capacity" if t == "int" else "root" for t in spec["ctor"]]
        args = ", ".join("%s %s" % (CPP_T[t], cn[i]) for i, t in enumerate(spec["ctor"]))
        lines.append("    %s(%s) {" % (cls, args))
        lines.append("        // TODO")
        lines.append("    }")
        for m, ms in spec["methods"].items():
            ma = ", ".join("%s p%d" % (CPP_T[t], i) for i, t in enumerate(ms["params"]))
            lines.append("    %s %s(%s) {" % (CPP_T[ms["ret"]], m, ma))
            lines.append("        " + (_default_ret("cpp", ms["ret"]) or "// TODO"))
            lines.append("    }")
        lines.append("};")
        return head + "\n".join(lines) + "\n"
    if spec["kind"] == "read4":
        return (head + "class Solution : public SolutionBase {\n"
                "public:\n"
                "    using SolutionBase::SolutionBase;\n"
                "    int read(char* buf, int n) {\n"
                "        // 调用 read4(buf4) 每次最多读 4 个字符\n"
                '        throw std::runtime_error("TODO");\n'
                "    }\n};\n")
    args = ", ".join("%s %s" % (CPP_T[t], names[i]) for i, t in enumerate(_sig_types(spec)))
    lines = ["%s %s(%s) {" % (CPP_T[spec["ret"]], spec["func"], args)]
    lines.append("    " + (_default_ret("cpp", spec["ret"]) or "// TODO"))
    lines.append("}")
    return head + "\n".join(lines) + "\n"


def gen_ts(spec):
    names = _names(spec)
    if spec["kind"] == "design":
        cls = spec["class"]
        lines = ["export class %s {" % cls]
        cn = ["capacity" if t == "int" else "root" for t in spec["ctor"]]
        args = ", ".join("%s: %s" % (cn[i], TS_T[t]) for i, t in enumerate(spec["ctor"]))
        lines.append("  constructor(%s) {" % args)
        lines.append("    // TODO")
        lines.append("  }")
        for m, ms in spec["methods"].items():
            ma = ", ".join("p%d: %s" % (i, TS_T[t]) for i, t in enumerate(ms["params"]))
            lines.append("  %s(%s): %s {" % (m, ma, TS_T[ms["ret"]]))
            lines.append("    " + (_default_ret("ts", ms["ret"]) or "// TODO"))
            lines.append("  }")
        lines.append("}")
        return "\n".join(lines) + "\n"
    if spec["kind"] == "read4":
        return ("export class Solution {\n"
                "  // 判题器已注入 this.read4(buf4: string[]): number\n"
                "  read4!: (buf4: string[]) => number;\n"
                "  read(buf: string[], n: number): number {\n"
                "    // TODO\n"
                "    return 0;\n"
                "  }\n}\n")
    args = ", ".join("%s: %s" % (names[i], TS_T[t]) for i, t in enumerate(_sig_types(spec)))
    lines = ["export function %s(%s): %s {" % (spec["func"], args, TS_T[spec["ret"]])]
    lines.append("  " + (_default_ret("ts", spec["ret"]) or "// TODO"))
    lines.append("}")
    return "\n".join(lines) + "\n"


def gen_readme(spec):
    pid = str(spec["id"])
    url = "https://leetcode.cn/problems/%s/" % spec["slug"]
    lines = ["# %s. %s" % (pid, spec["title"]), "",
             "- 难度: %s" % spec["difficulty"],
             "- 链接: %s" % url, ""]
    if spec["kind"] == "sql":
        lines += ["本题为 SQL 题，编辑 `solution.sql`，判题: `../../ex test %s`" % pid,
                  "judge 使用 sqlite3 内存库执行 setup 后运行你的 SQL。", ""]
    elif spec["kind"] == "shell":
        lines += ["本题为 Shell 题，编辑 `solution.sh`，判题: `../../ex test %s`" % pid, ""]
    else:
        lines += ["编辑对应语言的 solution 文件，然后:", "",
                  "```bash", "../../ex run %s -l py      # 运行样例 0" % pid,
                  "../../ex test %s -l py     # 判题 (py/go/cpp/ts)" % pid,
                  "../../ex test %s -l all    # 四语言全测" % pid, "```", ""]
    if spec.get("note"):
        lines += ["> " + spec["note"], ""]
    if not spec["cases"]:
        lines += ["⚠ 暂无测试用例，请自行在 problem.json 的 cases 中补充后再判题。", ""]
    lines += ["用例数: %d" % len(spec["cases"]), ""]
    return "\n".join(lines)


def main():
    count = 0
    for spec in specs.all_specs():
        d = problem_dir(spec)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "problem.json"), "w") as f:
            json.dump(spec, f, ensure_ascii=False, indent=1)
        with open(os.path.join(d, "README.md"), "w") as f:
            f.write(gen_readme(spec))
        kind = spec["kind"]
        if kind == "sql":
            targets = [("sql", "-- TODO: 写出 SQL\nSELECT 1;\n")]
        elif kind == "shell":
            targets = [("shell", "#!/usr/bin/env bash\n# TODO\n")]
        else:
            targets = [("py", gen_py(spec)), ("go", gen_go(spec)),
                       ("cpp", gen_cpp(spec)), ("ts", gen_ts(spec))]
        for lang, content in targets:
            path = os.path.join(d, LANG_FILE[lang])
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)
        count += 1
    print("generated/updated %d problems" % count)


if __name__ == "__main__":
    main()