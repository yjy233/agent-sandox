// Universal TS driver. Usage: node driver.ts problem.json solution.ts [case_idx]
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

class ListNode {
  val: number; next: ListNode | null;
  constructor(val = 0, next: ListNode | null = null) { this.val = val; this.next = next; }
}
class TreeNode {
  val: number; left: TreeNode | null; right: TreeNode | null;
  constructor(val = 0, left: TreeNode | null = null, right: TreeNode | null = null) {
    this.val = val; this.left = left; this.right = right;
  }
}
class Node {
  val: number; left: Node | null; right: Node | null; next: Node | null;
  constructor(val = 0, left: Node | null = null, right: Node | null = null, next: Node | null = null) {
    this.val = val; this.left = left; this.right = right; this.next = next;
  }
}
class GNode {
  val: number; neighbors: GNode[];
  constructor(val = 0, neighbors: GNode[] = []) { this.val = val; this.neighbors = neighbors; }
}
class RNode {
  val: number; next: RNode | null; random: RNode | null;
  constructor(val = 0, next: RNode | null = null, random: RNode | null = null) {
    this.val = val; this.next = next; this.random = random;
  }
}

function buildList(vals: number[]): ListNode | null {
  const dummy = new ListNode();
  let cur = dummy;
  for (const v of vals) { cur.next = new ListNode(v); cur = cur.next; }
  return dummy.next;
}
function listToSlice(head: ListNode | null): number[] {
  const out: number[] = [];
  while (head) { out.push(head.val); head = head.next; }
  return out;
}
function buildTree(vals: any[], cls: any = TreeNode): any {
  if (!vals.length || vals[0] === null) return null;
  const root = new cls(vals[0]);
  const queue = [root];
  let i = 1;
  while (queue.length && i < vals.length) {
    const n = queue.shift();
    if (i < vals.length) {
      const v = vals[i]; i++;
      if (v !== null && v !== undefined) { n.left = new cls(v); queue.push(n.left); }
    }
    if (i < vals.length) {
      const v = vals[i]; i++;
      if (v !== null && v !== undefined) { n.right = new cls(v); queue.push(n.right); }
    }
  }
  return root;
}
function treeToSlice(root: any): any[] {
  if (!root) return [];
  const out: any[] = [], queue = [root];
  while (queue.length) {
    const n = queue.shift();
    if (n === null) { out.push(null); continue; }
    out.push(n.val);
    queue.push(n.left ?? null);
    queue.push(n.right ?? null);
  }
  while (out.length && out[out.length - 1] === null) out.pop();
  return out;
}
function treesToSlices(roots: any[]): any[][] { return roots.map(treeToSlice); }
function nextLevels(root: any): number[][] {
  if (!root) return [];
  const out: number[][] = [];
  let leftmost = root;
  while (leftmost) {
    const level: number[] = [];
    let n = leftmost;
    while (n) { level.push(n.val); n = n.next; }
    out.push(level);
    let nxt = null;
    n = leftmost;
    while (n) {
      if (n.left) { nxt = n.left; break; }
      if (n.right) { nxt = n.right; break; }
      n = n.next;
    }
    leftmost = nxt;
  }
  return out;
}
function buildLists(arrs: number[][]): (ListNode | null)[] { return arrs.map(buildList); }
function buildCycleList(vals: number[], pos: number): [ListNode | null, ListNode[]] {
  const nodes = vals.map((v) => new ListNode(v));
  for (let i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
  if (nodes.length && pos >= 0 && pos < nodes.length) nodes[nodes.length - 1].next = nodes[pos];
  return [nodes[0] ?? null, nodes];
}
function cycleIndex(ret: ListNode | null, nodes: ListNode[]): number {
  for (let i = 0; i < nodes.length; i++) if (nodes[i] === ret) return i;
  return -1;
}
function buildIntersect(a: number[], b: number[], skipA: number, skipB: number): [ListNode | null, ListNode | null] {
  if (skipA >= a.length || skipB >= b.length) return [buildList(a), buildList(b)];
  const common = buildList(a.slice(skipA));
  let ha = buildList(a.slice(0, skipA));
  let hb = buildList(b.slice(0, skipB));
  if (!ha) ha = common;
  else { let t = ha; while (t.next) t = t.next; t.next = common; }
  if (!hb) hb = common;
  else { let t = hb; while (t.next) t = t.next; t.next = common; }
  return [ha, hb];
}
function valOrNull(n: ListNode | null): number | null { return n ? n.val : null; }
function buildRandomList(rows: number[][]): RNode | null {
  if (!rows.length) return null;
  const nodes = rows.map((r) => new RNode(r[0]));
  rows.forEach((r, i) => {
    nodes[i].next = r[1] >= 0 ? nodes[r[1]] : null;
    nodes[i].random = r[2] >= 0 ? nodes[r[2]] : null;
  });
  return nodes[0];
}
function dumpRandomList(head: RNode | null): number[][] {
  const nodes: RNode[] = [];
  let n = head;
  while (n) { nodes.push(n); n = n.next; }
  const idx = new Map<RNode, number>();
  nodes.forEach((x, i) => idx.set(x, i));
  return nodes.map((x) => [x.val, x.next ? idx.get(x.next)! : -1, x.random ? idx.get(x.random)! : -1]);
}
function buildGraph(adj: number[][]): GNode | null {
  if (!adj.length) return null;
  const nodes = adj.map((_, i) => new GNode(i + 1));
  adj.forEach((nb, i) => { nodes[i].neighbors = nb.map((j) => nodes[j - 1]); });
  return nodes[0];
}
function dumpGraph(node: GNode | null): number[][] {
  if (!node) return [];
  const seen = new Map<number, GNode>();
  const queue = [node];
  while (queue.length) {
    const n = queue.shift()!;
    if (seen.has(n.val)) continue;
    seen.set(n.val, n);
    queue.push(...n.neighbors);
  }
  return [...seen.keys()].sort((a, b) => a - b)
    .map((v) => seen.get(v)!.neighbors.map((x) => x.val).sort((a, b) => a - b));
}

function convertArg(t: string, v: any): any {
  switch (t) {
    case "list": return buildList(v);
    case "tree": return buildTree(v);
    case "nexttree": return buildTree(v, Node);
    case "lists": return buildLists(v);
    case "randomlist": return buildRandomList(v);
    case "graph": return buildGraph(v);
    default: return v;
  }
}
function serialize(t: string, v: any): any {
  switch (t) {
    case "list": return listToSlice(v);
    case "tree": return treeToSlice(v);
    case "trees": return treesToSlices(v);
    case "nexttree": return nextLevels(v);
    case "randomlist": return dumpRandomList(v);
    case "graph": return dumpGraph(v);
    default: return v;
  }
}

function runFunc(mod: any, spec: any, c: any): any {
  const args = c.args;
  const call: any[] = [];
  let i = 0, nodes: ListNode[] = [];
  for (const t of spec.params) {
    if (t === "cyclelist") {
      const [head, ns] = buildCycleList(args[i], args[i + 1]);
      call.push(head); nodes = ns; i += 2;
    } else if (t === "intersect") {
      const [ha, hb] = buildIntersect(args[i], args[i + 1], args[i + 2], args[i + 3]);
      call.push(ha, hb); i += 4;
    } else {
      call.push(convertArg(t, args[i])); i++;
    }
  }
  const ret = mod[spec.func](...call);
  const out = spec.out;
  if (out && out.arg !== undefined) return serialize(spec.params[out.arg], call[out.arg]);
  if (out && out.ret_prefix !== undefined) return [ret, call[out.ret_prefix].slice(0, ret)];
  if (spec.special_ret === "cycle_index") return cycleIndex(ret, nodes);
  if (spec.special_ret === "intersect_val") return valOrNull(ret);
  return serialize(spec.ret, ret);
}

function runDesign(mod: any, spec: any, c: any): any {
  const cls = mod[spec.class];
  let obj: any = null;
  const results: any[] = [];
  for (const op of c.ops) {
    const name = op[0];
    let args = op.slice(1);
    if (name === spec.class) {
      args = args.map((v: any, j: number) => convertArg(spec.ctor[j], v));
      obj = new cls(...args);
      results.push(null);
    } else {
      const ms = spec.methods[name];
      args = args.map((v: any, j: number) => convertArg(ms.params[j], v));
      const r = obj[name](...args);
      results.push(ms.ret === "void" ? null : serialize(ms.ret, r));
    }
  }
  return results;
}

function runRead4(mod: any, spec: any, c: any): any {
  const obj = new mod.Solution();
  const data: string = c.file;
  let pos = 0;
  obj.read4 = (buf4: string[]): number => {
    let cnt = 0;
    while (cnt < 4 && pos < data.length) { buf4[cnt] = data[pos]; pos++; cnt++; }
    return cnt;
  };
  const results: any[] = [];
  for (const n of c.ns) {
    const buf = new Array(Math.max(4, n)).fill("");
    const r = obj.read(buf, n);
    results.push([r, buf.slice(0, r).join("")]);
  }
  return results;
}

async function main() {
  const spec = JSON.parse(readFileSync(process.argv[2], "utf8"));
  const solPath = resolve(process.argv[3]);
  const only = process.argv.length > 4 ? parseInt(process.argv[4]) : -1;
  let mod: any;
  try {
    mod = await import(pathToFileURL(solPath).href);
  } catch (e: any) {
    for (const _ of spec.cases) console.log(JSON.stringify({ ok: false, error: String(e?.stack ?? e) }));
    return;
  }
  const runner = spec.kind === "design" ? runDesign : spec.kind === "read4" ? runRead4 : runFunc;
  for (let i = 0; i < spec.cases.length; i++) {
    if (only >= 0 && i !== only) continue;
    try {
      const out = runner(mod, spec, spec.cases[i]);
      console.log(JSON.stringify({ ok: true, output: out }));
    } catch (e: any) {
      console.log(JSON.stringify({ ok: false, error: String(e?.stack ?? e) }));
    }
  }
}

main();