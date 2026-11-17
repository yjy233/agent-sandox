"""ex CLI: list / run / test / show."""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from judge import specs
from judge.compare import compare
from judge.runner import run_lang

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS = os.path.join(ROOT, "problems")
PROGRESS = os.path.join(ROOT, ".progress.json")

LANGS = ["py", "go", "cpp", "ts"]
LANG_FILE = {"py": "solution.py", "go": "solution.go", "cpp": "solution.cpp",
             "ts": "solution.ts", "sql": "solution.sql", "shell": "solution.sh"}
DIFF_MARK = {"简单": "🟢", "中等": "🟡", "困难": "🔴"}


def load_progress():
    if os.path.exists(PROGRESS):
        with open(PROGRESS) as f:
            return json.load(f)
    return {}


def save_progress(p):
    with open(PROGRESS, "w") as f:
        json.dump(p, f, ensure_ascii=False, indent=1)


def problem_dir(spec):
    pid = str(spec["id"])
    prefix = pid.lower().replace(" ", "-") if pid.lower().startswith("lcp") else "%04d" % int(pid)
    return os.path.join(PROBLEMS, "%s-%s" % (prefix, spec["slug"]))


def langs_for(spec):
    if spec["kind"] == "sql":
        return ["sql"]
    if spec["kind"] == "shell":
        return ["shell"]
    return LANGS


def cmd_list(args):
    prog = load_progress()
    rows = []
    for s in specs.all_specs():
        if args.difficulty and s["difficulty"] != args.difficulty:
            continue
        if args.keyword and args.keyword.lower() not in s["title"].lower() \
                and args.keyword.lower() not in s["slug"]:
            continue
        key = str(s["id"]).lower()
        done = prog.get(key, {})
        marks = "".join("✓" + l for l in langs_for(s) if done.get(l)) or "-"
        if args.unsolved and done:
            continue
        rows.append((str(s["id"]), DIFF_MARK.get(s["difficulty"], ""), s["title"], marks))
    for pid, mark, title, marks in rows:
        print("%-7s %s %-30s %s" % (pid, mark, title, marks))
    print("\n共 %d 题" % len(rows))


def _resolve(pid, lang):
    spec = specs.get(pid)
    avail = langs_for(spec)
    if lang is None:
        lang = avail[0]
    if lang == "all":
        return spec, avail
    if lang not in avail:
        sys.exit("题目 %s 仅支持: %s" % (pid, ", ".join(avail)))
    return spec, [lang]


def _solution_path(spec, lang, override):
    if override:
        return os.path.abspath(override)
    return os.path.join(problem_dir(spec), LANG_FILE[lang])


def cmd_run(args):
    spec, langs = _resolve(args.id, args.lang)
    if len(langs) > 1:
        sys.exit("run 需要指定单一语言: -l py|go|cpp|ts")
    lang = langs[0]
    sol = _solution_path(spec, lang, args.solution)
    if not os.path.exists(sol):
        sys.exit("找不到解答文件: " + sol)
    idx = args.case
    results = run_lang(spec, lang, sol, case_idx=idx)
    r = results[0]
    if not r["ok"]:
        print("运行失败:\n" + r["error"])
        sys.exit(1)
    print(json.dumps(r["output"], ensure_ascii=False, indent=1))


def cmd_test(args):
    spec, langs = _resolve(args.id, args.lang)
    prog = load_progress()
    key = str(spec["id"]).lower()
    all_pass = True
    for lang in langs:
        sol = _solution_path(spec, lang, args.solution)
        if not os.path.exists(sol):
            print("[%s] 缺少解答文件: %s" % (lang, sol))
            all_pass = False
            continue
        if not spec["cases"]:
            print("[%s] ⚠ 该题暂无测试用例，请自行在 problem.json 中补充" % lang)
            continue
        t0 = time.time()
        results = run_lang(spec, lang, sol)
        passed = 0
        for i, (c, r) in enumerate(zip(spec["cases"], results)):
            if not r["ok"]:
                print("[%s] ✗ case %d 运行错误: %s" % (lang, i, r["error"]))
                all_pass = False
                continue
            mode = c.get("compare", spec.get("compare", "exact"))
            if spec["kind"] == "shell":
                ok, reason = r["output"] == c["expected"], \
                    "expected %r, got %r" % (c["expected"], r["output"])
            elif spec["kind"] == "sql":
                from judge.compare import _norm, _key
                a, b = _norm(r["output"]), _norm(c["expected"])
                if not c.get("ordered"):
                    a, b = sorted(a, key=_key), sorted(b, key=_key)
                ok = a == b
                reason = "" if ok else "expected %s, got %s" % (
                    json.dumps(b, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
            else:
                ok, reason = compare(r["output"], c["expected"], mode, c)
            if ok:
                passed += 1
            else:
                all_pass = False
                print("[%s] ✗ case %d: %s" % (lang, i, reason))
                if args.verbose:
                    print("    输入: %s" % json.dumps(c.get("args", c.get("ops", "")), ensure_ascii=False))
        status = "✓ 通过" if passed == len(spec["cases"]) else "✗ 未通过"
        print("[%s] %s %d/%d (%.2fs)" % (lang, status, passed, len(spec["cases"]), time.time() - t0))
        if passed == len(spec["cases"]) and spec["cases"]:
            prog.setdefault(key, {})[lang] = True
            save_progress(prog)
    sys.exit(0 if all_pass else 1)


def cmd_show(args):
    spec = specs.get(args.id)
    print(json.dumps(spec, ensure_ascii=False, indent=1))
    print("\n目录: " + problem_dir(spec))


def main():
    ap = argparse.ArgumentParser(prog="ex", description="LeetCode 练习判题器")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="列出题目与完成状态")
    p.add_argument("-d", "--difficulty", choices=["简单", "中等", "困难"])
    p.add_argument("-k", "--keyword")
    p.add_argument("-u", "--unsolved", action="store_true", help="只看未通过的")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("run", help="运行某个用例并打印输出")
    p.add_argument("id")
    p.add_argument("-l", "--lang", choices=LANGS + ["sql", "shell"])
    p.add_argument("-c", "--case", type=int, default=0)
    p.add_argument("-s", "--solution", help="指定解答文件路径")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("test", help="判题：运行全部用例")
    p.add_argument("id")
    p.add_argument("-l", "--lang", choices=LANGS + ["sql", "shell", "all"])
    p.add_argument("-s", "--solution", help="指定解答文件路径")
    p.add_argument("-v", "--verbose", action="store_true")
    p.set_defaults(fn=cmd_test)

    p = sub.add_parser("show", help="查看题目 spec")
    p.add_argument("id")
    p.set_defaults(fn=cmd_show)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()