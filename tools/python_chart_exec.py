"""图表代码执行工具。

用途：
1. 提供给大模型执行短时图表处理代码。
2. 返回标准输出、错误输出、执行结果与图表文件列表。

约定：
- 用户代码可通过 `_result` 返回结构化结果。
- 用户代码可通过 `_chart_files` 返回生成文件路径列表。
- 推荐用于图表专项处理任务，支持中等复杂度绘图脚本。
"""

from __future__ import annotations

import contextlib
import io
import os
import traceback
import uuid
from typing import Any, Dict, List


def _safe_import(module_name: str):
    """尝试导入模块，失败时返回 None，避免工具整体失败。"""
    try:
        module = __import__(module_name)
        return module
    except Exception:
        return None


def _detect_chart_libraries() -> Dict[str, str]:
    """检测常见图表库可用性并返回版本摘要。"""
    summary: Dict[str, str] = {}
    for name in ("numpy", "pandas", "matplotlib", "seaborn", "plotly"):
        module = _safe_import(name)
        if module is None:
            summary[name] = "missing"
            continue
        summary[name] = str(getattr(module, "__version__", "unknown"))
    return summary


def _normalize_chart_files(raw_files: Any) -> List[str]:
    """将 `_chart_files` 统一规范成字符串路径列表。"""
    if not isinstance(raw_files, list):
        return []
    result: List[str] = []
    for item in raw_files:
        path = str(item).strip()
        if not path:
            continue
        result.append(path)
    return result


def _build_output_dir() -> str:
    """为当前执行自动生成独立输出目录。"""
    run_id = uuid.uuid4().hex[:12]
    output_dir = os.path.join(os.getcwd(), "chart_outputs", f"run_{run_id}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def _collect_generated_files(
    output_dir: str,
    before_files: List[str],
    declared_files: List[str],
) -> List[str]:
    """汇总本次生成图表文件。

    优先使用用户声明的 `_chart_files`，并补充输出目录中新产生的文件。
    """
    result: List[str] = []
    seen = set()

    # 先收集脚本主动声明的图表路径。
    for path in declared_files:
        normalized = os.path.abspath(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)

    # 再补充输出目录中新增的文件，防止用户忘记写 `_chart_files`。
    current_files: List[str] = []
    try:
        for name in os.listdir(output_dir):
            full_path = os.path.abspath(os.path.join(output_dir, name))
            if os.path.isfile(full_path):
                current_files.append(full_path)
    except Exception:
        current_files = []
    before_set = {os.path.abspath(item) for item in before_files}
    for full_path in sorted(current_files):
        if full_path in before_set or full_path in seen:
            continue
        seen.add(full_path)
        result.append(full_path)
    return result


def main(payload: Dict[str, Any]) -> Dict[str, Any]:
    """工具入口。

    输入:
        payload["code"]: 要执行的 Python 代码（必填）
    """
    code = str(payload.get("code", "") or "")
    if not code.strip():
        return {
            "ok": False,
            "summary": "python_chart_exec 缺少 code 参数",
            "error": "missing code",
            "stdout": "",
            "stderr": "",
            "chartFiles": [],
            "libraries": _detect_chart_libraries(),
        }

    # 不从入参读取输出目录，始终由工具自动生成本次执行专属目录。
    output_dir = _build_output_dir()
    before_files: List[str] = []
    try:
        for name in os.listdir(output_dir):
            full_path = os.path.abspath(os.path.join(output_dir, name))
            if os.path.isfile(full_path):
                before_files.append(full_path)
    except Exception:
        before_files = []

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    # 默认注入常见图表变量，降低模型编写代码门槛。
    np = _safe_import("numpy")
    pd = _safe_import("pandas")
    sns = _safe_import("seaborn")
    plotly = _safe_import("plotly")

    plt = None
    matplotlib = _safe_import("matplotlib")
    if matplotlib is not None:
        try:
            matplotlib.use("Agg")
            plt = __import__("matplotlib.pyplot", fromlist=["pyplot"])
        except Exception:
            plt = None

    exec_scope: Dict[str, Any] = {
        "__name__": "__main__",
        "__builtins__": __builtins__,
        "np": np,
        "pd": pd,
        "plt": plt,
        "sns": sns,
        "plotly": plotly,
        "output_dir": output_dir,
        "_result": None,
        "_chart_files": [],
    }

    exit_code = 0
    try:
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(
            stderr_buffer
        ):
            exec(compile(code, "<python_chart_exec>", "exec"), exec_scope, exec_scope)
    except Exception:
        exit_code = 1
        traceback.print_exc(file=stderr_buffer)
    finally:
        # 避免 matplotlib 句柄持续堆积。
        if plt is not None:
            try:
                plt.close("all")
            except Exception:
                pass

    stdout_text = stdout_buffer.getvalue()
    stderr_text = stderr_buffer.getvalue()
    declared_chart_files = _normalize_chart_files(exec_scope.get("_chart_files"))
    chart_files = _collect_generated_files(
        output_dir=output_dir,
        before_files=before_files,
        declared_files=declared_chart_files,
    )
    result_value = exec_scope.get("_result")
    libraries = _detect_chart_libraries()

    ok = exit_code == 0
    summary = (
        f"python_chart_exec 执行成功，chart_files={len(chart_files)}"
        if ok
        else "python_chart_exec 执行失败"
    )
    return {
        "ok": ok,
        "summary": summary,
        "error": None if ok else (stderr_text.strip().splitlines()[0] if stderr_text.strip() else "execution_failed"),
        "stdout": stdout_text,
        "stderr": stderr_text,
        "result": result_value,
        "chartFiles": chart_files,
        "generatedChartFiles": chart_files,
        "libraries": libraries,
        "outputDir": output_dir,
    }
