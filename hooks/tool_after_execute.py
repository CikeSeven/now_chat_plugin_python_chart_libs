"""图表插件工具执行后日志 Hook。"""

from __future__ import annotations

import json
from typing import Any, Dict


def _safe_to_text(value: Any, max_len: int = 500) -> str:
    """将任意值转为短文本，避免日志过长。"""
    try:
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    except Exception:
        text = str(value)
    if len(text) <= max_len:
        return text
    return text[:max_len] + "...(truncated)"


def main(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Hook 入口：打印工具执行结果摘要与返回值片段。"""
    data = payload.get("payload", {}) if isinstance(payload, dict) else {}
    tool_name = str(data.get("toolName", "unknown"))
    status = str(data.get("status", "unknown"))
    duration_ms = data.get("durationMs")
    error = data.get("error")
    summary = data.get("summary")
    tool_message_content = data.get("toolMessageContent")

    print(
        "[python_chart_libs] tool_after_execute"
        f" tool={tool_name}"
        f" status={status}"
        f" durationMs={duration_ms}"
        f" error={_safe_to_text(error, max_len=200)}"
    )
    print(
        "[python_chart_libs] tool_after_execute summary="
        f"{_safe_to_text(summary, max_len=300)}"
    )
    print(
        "[python_chart_libs] tool_after_execute return="
        f"{_safe_to_text(tool_message_content, max_len=1000)}"
    )
    return {"ok": True}

