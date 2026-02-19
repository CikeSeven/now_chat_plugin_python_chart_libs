"""图表插件工具执行后日志 Hook。"""

from __future__ import annotations

import json
from typing import Any, Dict


def _to_text(value: Any) -> str:
    """将任意值转为文本，保留完整内容用于调试。"""
    try:
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    except Exception:
        text = str(value)
    return text


def main(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Hook 入口：打印工具执行结果完整内容。"""
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
        f" error={_to_text(error)}"
    )
    print(
        "[python_chart_libs] tool_after_execute summary="
        f"{_to_text(summary)}"
    )
    print(
        "[python_chart_libs] tool_after_execute return="
        f"{_to_text(tool_message_content)}"
    )
    return {"ok": True}
