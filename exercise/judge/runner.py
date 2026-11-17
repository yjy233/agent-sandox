"""Build & run drivers for each language."""
import json
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANG_DIR = os.path.join(HERE, "lang")
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, ".build")

GO_SCALAR = {"int": "int", "long": "int64", "uint32": "uint32", "double": "float64",
             "bool": "bool", "string": "string", "ints": "[]int", "intss": "[][]int",
             "strings": "[]string", "stringss": "[][]string", "grid": "[]string"}


def _prep(key, lang, files):
    d = os.path.join(BUILD, key, lang)
    os.makedirs(d, exist_ok=True)
    for src, dst in files:
        shutil.copyfile(src, os.path.join(d, dst))
    return d


def _run(cmd, cwd, timeout=30):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p


def _parse_lines(stdout, stderr, n):
    outs = []
    for line in stdout.strip().splitlines():
        try:
            outs.append(json.loads(line))
        except ValueError:
            outs.append({"ok": False, "error": "bad driver output: " + line})
    while len(outs) < n:
        outs.append({"ok": False, "error": (stderr or "driver produced no output").strip()[:2000]})
    return outs[:n]


# ---------------- go codegen ----------------

def _go_expand(params):
    lines, call, arg = [], [], 0
    for i, t in enumerate(params):
        if t in GO_SCALAR:
            lines.append("var a%d %s" % (i, GO_SCALAR[t]))
            lines.append("mustUnmarshal(args[%d], &a%d)" % (arg, i))
            call.append("a%d" % i)
            arg += 1
        elif t in ("list", "tree", "nexttree", "lists", "randomlist", "graph"):
            raw = {"list": "[]int", "tree": "[]interface{}", "nexttree": "[]interface{}",
                   "lists": "[][]int", "randomlist": "[][]int", "graph": "[][]int"}[t]
            fn = {"list": "buildList", "tree": "buildTreeFromLevel", "nexttree": "buildNextTree",
                  "lists": "buildLists", "randomlist": "buildRandomList", "graph": "buildGraph"}[t]
            lines.append("var r%d %s" % (i, raw))
            lines.append("mustUnmarshal(args[%d], &r%d)" % (arg, i))
            lines.append("a%d := %s(r%d)" % (i, fn, i))
            call.append("a%d" % i)
            arg += 1
        elif t == "cyclelist":
            lines.append("var r%d []int" % i)
            lines.append("var p%d int" % i)
            lines.append("mustUnmarshal(args[%d], &r%d)" % (arg, i))
            lines.append("mustUnmarshal(args[%d], &p%d)" % (arg + 1, i))
            lines.append("a%d, nodes%d := buildCycleList(r%d, p%d)" % (i, i, i, i))
            lines.append("_ = nodes%d" % i)
            call.append("a%d" % i)
            arg += 2
        elif t == "intersect":
            lines.append("var ra%d, rb%d []int" % (i, i))
            lines.append("var sa%d, sb%d int" % (i, i))
            for j, v in enumerate(("ra%d" % i, "rb%d" % i, "sa%d" % i, "sb%d" % i)):
                lines.append("mustUnmarshal(args[%d], &%s)" % (arg + j, v))
            lines.append("a%d, b%d := buildIntersect(ra%d, rb%d, sa%d, sb%d)" % (i, i, i, i, i, i))
            call.extend(["a%d" % i, "b%d" % i])
            arg += 4
        else:
            raise ValueError("go: unknown param type " + t)
    return lines, call


def _go_ser(expr, t):
    if t in GO_SCALAR or t == "void":
        return expr if t != "void" else "nil"
    return {"list": "listToSlice", "tree": "treeToSlice", "trees": "treesToSlices",
            "nexttree": "nextLevels", "randomlist": "dumpRandomList",
            "graph": "dumpGraph"}[t] + "(%s)" % expr


def _go_out_expr(spec, call):
    out = spec.get("out")
    if out and "arg" in out:
        i = out["arg"]
        return _go_ser(call[i], spec["params"][i])
    if out and "ret_prefix" in out:
        i = out["ret_prefix"]
        return "[]interface{}{ret, %s[:ret]}" % call[i]
    sr = spec.get("special_ret")
    if sr == "cycle_index":
        return "cycleIndex(ret, nodes0)"
    if sr == "intersect_val":
        return "valOrNull(ret)"
    return _go_ser("ret", spec["ret"])


def _go_func_body(spec):
    lines, call = _go_expand(spec["params"])
    args = ", ".join(call)
    if spec["ret"] == "void":
        lines.append("%s(%s)" % (spec["func"], args))
    else:
        lines.append("ret := %s(%s)" % (spec["func"], args))
    lines.append("return %s, nil" % _go_out_expr(spec, call))
    return "\n".join("\t" + l for l in lines)


def _go_design_body(spec):
    cls = spec["class"]
    lines = ["var obj *%s" % cls, "var results []interface{}",
             "for _, op := range c.Ops {",
             "\tvar name string", "\tmustUnmarshal(op[0], &name)",
             "\targs := op[1:]", "\tswitch name {", '\tcase "%s":' % cls]
    ctor_lines, ctor_call = _go_expand(spec["ctor"])
    lines += ["\t\t" + l for l in ctor_lines]
    lines.append("\t\tobj = Constructor(%s)" % ", ".join(ctor_call))
    lines.append("\t\tresults = append(results, nil)")
    for m, ms in spec["methods"].items():
        lines.append('\tcase "%s":' % m)
        ml, mc = _go_expand(ms["params"])
        lines += ["\t\t" + l for l in ml]
        if ms["ret"] == "void":
            lines.append("\t\tobj.%s(%s)" % (m, ", ".join(mc)))
            lines.append("\t\tresults = append(results, nil)")
        else:
            lines.append("\t\tresults = append(results, %s)" % _go_ser("obj.%s(%s)" % (m, ", ".join(mc)), ms["ret"]))
    lines += ["\tdefault:", '\t\tpanic("unknown op: " + name)', "\t}", "}", "return results, nil"]
    return "\n".join("\t" + l for l in lines)


GO_READ4_BODY = """\tsrc := newRead4Source(c.File)
\tobj := &Solution{Read4Source: src}
\tvar results []interface{}
\tfor _, n := range c.Ns {
\t\tsize := n
\t\tif size < 4 { size = 4 }
\t\tbuf := make([]byte, size)
\t\tr := obj.read(buf, n)
\t\tresults = append(results, []interface{}{r, string(buf[:r])})
\t}
\treturn results, nil"""

GO_MAIN_TMPL = """package main

import (
\t"bufio"
\t"encoding/json"
\t"fmt"
\t"os"
\t"strconv"
)

type Case struct {
\tArgs []json.RawMessage   `json:"args"`
\tOps  [][]json.RawMessage `json:"ops"`
\tFile string              `json:"file"`
\tNs   []int               `json:"ns"`
}

type Problem struct {
\tCases []Case `json:"cases"`
}

func runCase(c Case) (interface{}, error) {
\targs := c.Args
\t_ = args
{BODY}
}

func safeRun(c Case) (out interface{}, ok bool, msg string) {
\tdefer func() {
\t\tif r := recover(); r != nil {
\t\t\tok = false
\t\t\tmsg = fmt.Sprint(r)
\t\t}
\t}()
\tout, err := runCase(c)
\tif err != nil {
\t\treturn nil, false, err.Error()
\t}
\treturn out, true, ""
}

func main() {
\tdata, err := os.ReadFile(os.Args[1])
\tif err != nil { panic(err) }
\tvar p Problem
\tif err := json.Unmarshal(data, &p); err != nil { panic(err) }
\tonly := -1
\tif len(os.Args) > 2 { only, _ = strconv.Atoi(os.Args[2]) }
\tw := bufio.NewWriter(os.Stdout)
\tdefer w.Flush()
\tfor i, c := range p.Cases {
\t\tif only >= 0 && i != only { continue }
\t\tout, ok, msg := safeRun(c)
\t\tline, _ := json.Marshal(map[string]interface{}{"ok": ok, "output": out, "error": msg})
\t\tw.Write(line)
\t\tw.WriteByte('\\n')
\t}
}
"""


def _gen_go(spec, d):
    kind = spec["kind"]
    if kind == "design":
        body = _go_design_body(spec)
    elif kind == "read4":
        body = GO_READ4_BODY
    else:
        body = _go_func_body(spec)
    with open(os.path.join(d, "main.go"), "w") as f:
        f.write(GO_MAIN_TMPL.replace("{BODY}", body))


# ---------------- c++ codegen ----------------

CPP_EXTRACT = {
    "int": "(int)%s.as_long()", "long": "%s.as_long()", "uint32": "(uint32_t)%s.as_long()",
    "double": "%s.as_double()", "bool": "%s.as_bool()", "string": "%s.as_string()",
    "ints": "jsonToInts(%s)", "intss": "jsonToIntss(%s)", "strings": "jsonToStrings(%s)",
    "stringss": "jsonToStringss(%s)", "grid": "jsonToStrings(%s)",
}
CPP_DECL = {
    "int": "int", "long": "long long", "uint32": "uint32_t", "double": "double",
    "bool": "bool", "string": "std::string", "ints": "std::vector<int>",
    "intss": "std::vector<std::vector<int>>", "strings": "std::vector<std::string>",
    "stringss": "std::vector<std::vector<std::string>>", "grid": "std::vector<std::string>",
}


def _cpp_expand(params):
    lines, call, arg = [], [], 0
    for i, t in enumerate(params):
        if t in CPP_EXTRACT:
            lines.append("%s a%d = %s;" % (CPP_DECL[t], i, CPP_EXTRACT[t] % ("args[%d]" % arg)))
            call.append("a%d" % i)
            arg += 1
        elif t in ("list", "tree", "nexttree", "lists", "randomlist", "graph"):
            fn = {"list": "buildList(jsonToInts(%s))", "tree": "buildTree(%s.as_array())",
                  "nexttree": "buildNextTree(%s.as_array())", "lists": "buildLists(jsonToIntss(%s))",
                  "randomlist": "buildRandomList(jsonToIntss(%s))", "graph": "buildGraph(jsonToIntss(%s))"}[t]
            decl = {"list": "ListNode*", "tree": "TreeNode*", "nexttree": "Node*",
                    "lists": "std::vector<ListNode*>", "randomlist": "RNode*", "graph": "GNode*"}[t]
            lines.append("%s a%d = %s;" % (decl, i, fn % ("args[%d]" % arg)))
            call.append("a%d" % i)
            arg += 1
        elif t == "cyclelist":
            lines.append("std::vector<ListNode*> nodes%d;" % i)
            lines.append("ListNode* a%d = buildCycleList(jsonToInts(args[%d]), (int)args[%d].as_long(), nodes%d);" % (i, arg, arg + 1, i))
            call.append("a%d" % i)
            arg += 2
        elif t == "intersect":
            lines.append("auto pr%d = buildIntersect(jsonToInts(args[%d]), jsonToInts(args[%d]), (int)args[%d].as_long(), (int)args[%d].as_long());" % (i, arg, arg + 1, arg + 2, arg + 3))
            lines.append("ListNode* a%d = pr%d.first;" % (i, i))
            lines.append("ListNode* b%d = pr%d.second;" % (i, i))
            call.extend(["a%d" % i, "b%d" % i])
            arg += 4
        else:
            raise ValueError("cpp: unknown param type " + t)
    return lines, call


def _cpp_ser(expr, t):
    if t == "void":
        return "Json::mk_null()"
    if t in ("int", "long", "uint32", "double"):
        return "Json::mk_num(%s)" % expr
    if t == "bool":
        return "Json::mk_bool(%s)" % expr
    if t == "string":
        return "Json::mk_str(%s)" % expr
    return {"ints": "intsToJson", "intss": "intssToJson", "strings": "stringsToJson",
            "stringss": "stringssToJson", "grid": "stringsToJson", "list": "listToJson",
            "tree": "treeToJson", "trees": "treesToJson", "nexttree": "nextLevelsJson",
            "randomlist": "dumpRandomListJson", "graph": "dumpGraphJson"}[t] + "(%s)" % expr


def _cpp_out_expr(spec, call):
    out = spec.get("out")
    if out and "arg" in out:
        i = out["arg"]
        return _cpp_ser(call[i], spec["params"][i])
    if out and "ret_prefix" in out:
        i = out["ret_prefix"]
        return ("Json::mk_arr({Json::mk_num(ret), intsToJson(std::vector<int>(%s.begin(), %s.begin()+ret))})" % (call[i], call[i]))
    sr = spec.get("special_ret")
    if sr == "cycle_index":
        return "Json::mk_num(cycleIndex(ret, nodes0))"
    if sr == "intersect_val":
        return "valOrNullJson(ret)"
    return _cpp_ser("ret", spec["ret"])


def _cpp_func_body(spec):
    lines, call = _cpp_expand(spec["params"])
    args = ", ".join(call)
    if spec["ret"] == "void":
        lines.append("%s(%s);" % (spec["func"], args))
    else:
        if spec["ret"] in CPP_DECL:
            rt = CPP_DECL[spec["ret"]]
        else:
            rt = {"list": "ListNode*", "tree": "TreeNode*",
                  "trees": "std::vector<TreeNode*>", "nexttree": "Node*",
                  "randomlist": "RNode*", "graph": "GNode*"}[spec["ret"]]
        lines.append("%s ret = %s(%s);" % (rt, spec["func"], args))
    lines.append("return %s;" % _cpp_out_expr(spec, call))
    return "\n".join("\t" + l for l in lines)


def _cpp_design_body(spec):
    cls = spec["class"]
    lines = ["%s* obj = nullptr;" % cls, "std::vector<Json> results;",
             "for (const auto& op : c.at(\"ops\").as_array()) {",
             "\tconst auto& opa = op.as_array();",
             "\tstd::string name = opa[0].as_string();",
             "\tauto args = std::vector<Json>(opa.begin()+1, opa.end());",
             '\tif (name == "%s") {' % cls]
    cl, cc = _cpp_expand(spec["ctor"])
    lines += ["\t\t" + l for l in cl]
    lines.append("\t\tobj = new %s(%s);" % (cls, ", ".join(cc)))
    lines.append("\t\tresults.push_back(Json::mk_null());")
    for m, ms in spec["methods"].items():
        lines.append('\t} else if (name == "%s") {' % m)
        ml, mc = _cpp_expand(ms["params"])
        lines += ["\t\t" + l for l in ml]
        if ms["ret"] == "void":
            lines.append("\t\tobj->%s(%s);" % (m, ", ".join(mc)))
            lines.append("\t\tresults.push_back(Json::mk_null());")
        else:
            lines.append("\t\tresults.push_back(%s);" % _cpp_ser("obj->%s(%s)" % (m, ", ".join(mc)), ms["ret"]))
    lines += ["\t} else {", '\t\tthrow std::runtime_error("unknown op: " + name);',
              "\t}", "}", "return Json::mk_arr(results);"]
    return "\n".join("\t" + l for l in lines)


CPP_READ4_BODY = """\tSolution obj(c.at("file").as_string());
\tstd::vector<Json> results;
\tfor (const auto& nj : c.at("ns").as_array()) {
\t\tint n = (int)nj.as_long();
\t\tstd::vector<char> buf(std::max(4, n), 0);
\t\tint r = obj.read(buf.data(), n);
\t\tresults.push_back(Json::mk_arr({Json::mk_num(r), Json::mk_str(std::string(buf.data(), r))}));
\t}
\treturn Json::mk_arr(results);"""

CPP_MAIN_TMPL = """#include "json.hpp"
#include "helpers.hpp"
#include "solution.cpp"
#include <fstream>
#include <sstream>
#include <iostream>

static Json runCase(const Json& c) {
\tconst std::vector<Json> args = c.has("args") ? c.at("args").as_array() : std::vector<Json>{};
\t(void)args;
{BODY}
}

int main(int argc, char** argv) {
\tstd::ifstream f(argv[1]);
\tstd::stringstream ss; ss << f.rdbuf();
\tJson p = Json::parse(ss.str());
\tint only = argc > 2 ? atoi(argv[2]) : -1;
\tconst auto& cases = p.at("cases").as_array();
\tfor (size_t i = 0; i < cases.size(); i++) {
\t\tif (only >= 0 && (int)i != only) continue;
\t\tJson line = Json::mk_obj();
\t\ttry {
\t\t\tJson out = runCase(cases[i]);
\t\t\tline.set("ok", Json::mk_bool(true));
\t\t\tline.set("output", out);
\t\t\tline.set("error", Json::mk_str(""));
\t\t} catch (const std::exception& e) {
\t\t\tline.set("ok", Json::mk_bool(false));
\t\t\tline.set("output", Json::mk_null());
\t\t\tline.set("error", Json::mk_str(e.what()));
\t\t}
\t\tstd::cout << line.dump() << "\\n";
\t}
\treturn 0;
}
"""


def _gen_cpp(spec, d):
    kind = spec["kind"]
    if kind == "design":
        body = _cpp_design_body(spec)
    elif kind == "read4":
        body = CPP_READ4_BODY
    else:
        body = _cpp_func_body(spec)
    with open(os.path.join(d, "main.cpp"), "w") as f:
        f.write(CPP_MAIN_TMPL.replace("{BODY}", body))


# ---------------- runners ----------------

def run_lang(spec, lang, solution_path, case_idx=None):
    """Return list of {"ok","output","error"} per case (or single case)."""
    key = str(spec["id"]).lower()
    n = 1 if case_idx is not None else len(spec["cases"])
    if not spec["cases"]:
        return [{"ok": False, "error": "no test cases defined; add cases to problem.json"}]
    pj = os.path.join(BUILD, key, lang, "problem.json")
    os.makedirs(os.path.dirname(pj), exist_ok=True)
    with open(pj, "w") as f:
        json.dump(spec, f, ensure_ascii=False)
    idx_arg = [str(case_idx)] if case_idx is not None else []

    if lang == "py":
        d = _prep(key, lang, [(os.path.join(LANG_DIR, "py_driver.py"), "driver.py"),
                              (solution_path, "solution.py")])
        p = _run(["python3", "driver.py", "problem.json", "solution.py"] + idx_arg, d)
        return _parse_lines(p.stdout, p.stderr, n)
    if lang == "ts":
        d = _prep(key, lang, [(os.path.join(LANG_DIR, "ts_driver.ts"), "driver.ts"),
                              (solution_path, "solution.ts")])
        p = _run(["node", "driver.ts", "problem.json", "solution.ts"] + idx_arg, d)
        return _parse_lines(p.stdout, p.stderr, n)
    if lang == "go":
        d = _prep(key, lang, [(os.path.join(LANG_DIR, "go_helpers.go"), "helpers.go"),
                              (solution_path, "solution.go")])
        _gen_go(spec, d)
        env = dict(os.environ, GO111MODULE="off", GOPROXY="off")
        b = subprocess.run(["go", "build", "-o", "prog", "main.go", "helpers.go", "solution.go"],
                           cwd=d, capture_output=True, text=True, env=env, timeout=180)
        if b.returncode != 0:
            return [{"ok": False, "error": "compile error:\n" + b.stderr[:3000]}] * n
        p = _run(["./prog", "problem.json"] + idx_arg, d)
        return _parse_lines(p.stdout, p.stderr, n)
    if lang == "cpp":
        d = _prep(key, lang, [(os.path.join(LANG_DIR, "cpp_json.hpp"), "json.hpp"),
                              (os.path.join(LANG_DIR, "cpp_helpers.hpp"), "helpers.hpp"),
                              (solution_path, "solution.cpp")])
        _gen_cpp(spec, d)
        b = _run(["g++", "-std=c++17", "-O2", "-o", "prog", "main.cpp"], d, timeout=180)
        if b.returncode != 0:
            return [{"ok": False, "error": "compile error:\n" + b.stderr[:3000]}] * n
        p = _run(["./prog", "problem.json"] + idx_arg, d)
        return _parse_lines(p.stdout, p.stderr, n)
    if lang == "sql":
        return run_sql(spec, solution_path, case_idx)
    if lang == "shell":
        return run_shell(spec, solution_path, case_idx)
    raise ValueError("unknown lang " + lang)


def run_sql(spec, solution_path, case_idx=None):
    import sqlite3
    with open(solution_path) as f:
        sql = f.read()
    results = []
    cases = spec["cases"]
    sel = range(len(cases)) if case_idx is None else [case_idx]
    for i in sel:
        c = cases[i]
        try:
            conn = sqlite3.connect(":memory:")
            conn.executescript(c["setup"])
            script = sql
            for k, v in c.get("params", {}).items():
                script = script.replace("{{%s}}" % k, str(v))
            if c.get("verify"):
                conn.executescript(script)
                rows = [list(r) for r in conn.execute(c["verify"])]
            else:
                rows = [list(r) for r in conn.execute(script)]
            conn.close()
            results.append({"ok": True, "output": rows})
        except Exception as e:
            results.append({"ok": False, "error": str(e)})
    return results


def run_shell(spec, solution_path, case_idx=None):
    results = []
    cases = spec["cases"]
    sel = range(len(cases)) if case_idx is None else [case_idx]
    for i in sel:
        c = cases[i]
        with tempfile.TemporaryDirectory() as td:
            for name, content in c.get("files", {}).items():
                with open(os.path.join(td, name), "w") as f:
                    f.write(content)
            shutil.copyfile(solution_path, os.path.join(td, "solution.sh"))
            try:
                p = subprocess.run(["bash", "solution.sh"], cwd=td, capture_output=True,
                                   text=True, timeout=15)
                if p.returncode != 0:
                    results.append({"ok": False, "error": p.stderr[:2000]})
                else:
                    results.append({"ok": True, "output": p.stdout})
            except Exception as e:
                results.append({"ok": False, "error": str(e)})
    return results