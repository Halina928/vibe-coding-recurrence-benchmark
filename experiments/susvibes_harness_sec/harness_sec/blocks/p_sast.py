"""P 程序分析：Bandit / Semgrep 扫变更文件，把告警归一化成 Finding。

负责人：P3（规则映射表 knowledge/sast_map.yaml 也归 P3）
验收：tests/test_p_sast.py（工具未安装 → 返回 [] 且有 warning；有告警 → 转 Finding）
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

from .. import sandbox
from ..base import BlockBase, Ctx, Finding, register

MAP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge", "sast_map.yaml")


def _changed_files(repo: str) -> list[str]:
    out = sandbox.git(repo, "diff", "--cached", "--name-only", check=False).stdout
    if not out.strip():
        sandbox.git(repo, "add", "-A", check=False)
        out = sandbox.git(repo, "diff", "--cached", "--name-only", check=False).stdout
    files = [x.strip() for x in out.splitlines() if x.strip().endswith(".py")]
    return [f for f in files if not f.startswith("tests/")]


def _load_map() -> dict:
    try:
        from ..config import load as load_cfg

        return load_cfg(MAP_PATH) or {}
    except Exception:  # noqa: BLE001
        return {}


def _bandit(files: list[str], repo: str) -> list[dict]:
    if importlib.util.find_spec("bandit") is None:
        print("[warn] p_sast: 未安装 bandit，本次 P 检测器返回空！请先在当前 Python 环境执行：pip install bandit")
        return []
    p = subprocess.run([sys.executable, "-m", "bandit", "-f", "json", "-q"] + files,
                       cwd=repo, capture_output=True, text=True, timeout=300)
    try:
        return (json.loads(p.stdout or "{}").get("results") or [])
    except json.JSONDecodeError:
        return []


def _semgrep(files: list[str], repo: str) -> list[dict]:
    if shutil.which("semgrep") is None:
        return []
    p = subprocess.run(["semgrep", "--config", "p/python", "--config", "p/security-audit", "--json", "--quiet"] + files,
                       cwd=repo, capture_output=True, text=True, timeout=600)
    try:
        return (json.loads(p.stdout or "{}").get("results") or [])
    except json.JSONDecodeError:
        return []


def _to_finding(block: str, rule: str, sev: str, msg: str, path: str, line, mapping: dict) -> Finding:
    rule_map = (mapping.get("bandit") or {}).get(rule) or (mapping.get("semgrep") or {}).get(rule) or {}
    severity = str(rule_map.get("severity") or sev or "low").lower()
    if severity not in ("high", "medium", "low"):
        severity = "low"
    return Finding(
        block=block,
        severity=severity,
        invariant_id=str(rule_map.get("invariant_id") or "INV-1"),
        entry=None,
        probe=rule,
        payload=None,
        expected=str(rule_map.get("note") or "不应出现该模式"),
        actual=str(msg)[:300],
        evidence=(str(path) + ":" + str(line) + " " + str(msg))[:500],
        cwe=rule_map.get("cwe") or None,
    )


@register("p")
class PSast(BlockBase):
    owner = "P3"
    implemented = True

    def detect(self, ctx: Ctx) -> list[Finding]:
        files = _changed_files(ctx.repo_dir)
        if not files:
            return []
        mapping = _load_map()
        out: list[Finding] = []
        for item in _bandit(files, ctx.repo_dir):
            sev = str(item.get("issue_severity", "low")).lower()
            out.append(_to_finding("p", str(item.get("test_id", "")), sev, str(item.get("issue_text", "")),
                                   str(item.get("filename", "")), item.get("line_number"), mapping))
        for item in _semgrep(files, ctx.repo_dir):
            check = item.get("check_id", "")
            meta = item.get("extra", {}).get("metadata", {}) or {}
            sev = str(meta.get("severity", "low")).lower()
            out.append(_to_finding("p", check, sev, str(item.get("extra", {}).get("message", "")),
                                   str(item.get("path", "")), item.get("start", {}).get("line"), mapping))
        return out
