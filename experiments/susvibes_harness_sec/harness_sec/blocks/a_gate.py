"""A 安全验收：有阻断级 Finding 就不放行（retry），否则 deliver。

负责人：P4
验收：tests/test_a_gate.py（有 high/medium → retry；只有 low/空 → deliver）
说明：本块只做"放不放行"；重做几次由 orchestrator + C 块的 policy 决定。
"""
from __future__ import annotations

from ..base import Action, BlockBase, Ctx, Finding, register


@register("a")
class AGate(BlockBase):
    owner = "P4"
    implemented = True

    def decide(self, findings: list[Finding], ctx: Ctx) -> Action:
        blocking = [f for f in findings if f.is_blocking()]
        if not blocking:
            return Action("deliver", "no blocking findings")
        return Action("retry", str(len(blocking)) + " blocking findings")
