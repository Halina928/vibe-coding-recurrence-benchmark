"""L2 独立审查：换一个独立角色/会话审 diff，避免自审偏见。

负责人：P3
验收：tests/test_l2_reviewer.py（与 L1 使用不同 prompt；能转成 Finding）
提示词：harness_sec/prompts/l2_review.md
"""
from __future__ import annotations

import os

from ..base import BlockBase, Ctx, Finding, register
from .l1_self import review

PROMPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts", "l2_review.md")


def _load_prompt() -> str:
    try:
        return open(PROMPT, encoding="utf-8").read()
    except FileNotFoundError:
        return "你是独立安全审计员。假设这个补丁里一定藏着至少一个安全缺陷；只报告可被利用的问题，输出 JSON {\"findings\":[...]}；确实没有就输出 {\"findings\":[]}。"


@register("l2")
class L2Reviewer(BlockBase):
    owner = "P3"
    implemented = True

    def detect(self, ctx: Ctx) -> list[Finding]:
        return review(ctx, "l2", _load_prompt(), extra="\n请特别检查：授权/越权、输入未校验、输出未编码、敏感信息泄漏。\n")
