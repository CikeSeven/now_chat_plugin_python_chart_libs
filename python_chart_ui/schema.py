"""图表增强插件配置页面。"""

from __future__ import annotations

import contextlib
import io
import os
import traceback
from typing import Any, Dict

from python_chart_ui import UiButton
from python_chart_ui import UiPage
from python_chart_ui import UiTextInput


class PythonChartLibsConfigPage(UiPage):
    """图表增强插件配置页实现。"""

    def _default_state(self) -> Dict[str, Any]:
        """默认页面状态。"""
        return {
            "python_code": (
                "import matplotlib\n"
                "matplotlib.use('Agg')\n"
                "import matplotlib.pyplot as plt\n"
                "x = [1, 2, 3, 4]\n"
                "y = [3, 1, 4, 2]\n"
                "plt.figure(figsize=(4, 3))\n"
                "plt.plot(x, y)\n"
                "plt.title('NowChat Demo Chart')\n"
                "path = os.path.join(output_dir, 'demo_chart.png')\n"
                "plt.savefig(path)\n"
                "plt.close()\n"
                "_chart_files = [path]\n"
                "_result = {'saved': path}\n"
                "print('chart saved:', path)"
            ),
            "exec_output": "",
        }

    def _check_environment(self) -> str:
        """检查常见图表处理库是否可导入。"""
        libs = ("numpy", "pandas", "matplotlib", "seaborn", "plotly")
        lines = []
        for name in libs:
            try:
                module = __import__(name)
                version = getattr(module, "__version__", "unknown")
                lines.append(f"{name}: OK ({version})")
            except Exception as error:
                lines.append(f"{name}: FAIL ({error})")
        return "\n".join(lines)

    def _execute_python_code(self, code: str) -> str:
        """在页面内执行图表处理代码并输出结果。"""
        text = (code or "").strip()
        if not text:
            return "请输入 Python 图表代码。"

        output_dir = os.path.join(os.getcwd(), "chart_outputs")
        os.makedirs(output_dir, exist_ok=True)
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        local_scope: Dict[str, Any] = {
            "os": os,
            "output_dir": output_dir,
            "_result": None,
            "_chart_files": [],
        }

        try:
            with contextlib.redirect_stdout(stdout_buffer):
                with contextlib.redirect_stderr(stderr_buffer):
                    exec(text, {}, local_scope)
        except Exception:
            traceback.print_exc(file=stderr_buffer)

        sections = []
        stdout_text = stdout_buffer.getvalue().strip()
        stderr_text = stderr_buffer.getvalue().strip()
        result_data = local_scope.get("_result")
        chart_files = local_scope.get("_chart_files")

        if stdout_text:
            sections.append(f"[stdout]\n{stdout_text}")
        if result_data is not None:
            sections.append(f"[result]\n{result_data}")
        if isinstance(chart_files, list) and chart_files:
            sections.append(f"[chart_files]\n{chart_files}")
        if stderr_text:
            sections.append(f"[stderr]\n{stderr_text}")
        if not sections:
            sections.append("执行完成，无输出。")
        return "\n\n".join(sections)

    def _components(self, state: Dict[str, Any]):
        """生成当前页面组件。"""
        return [
            UiButton(
                component_id="check_environment",
                label="检查图表环境",
                description="检查 numpy/pandas/matplotlib/seaborn/plotly 可用性。",
            ),
            UiTextInput(
                component_id="python_code",
                label="图表 Python 代码",
                description="用于执行图表处理代码；可用 `_result` 与 `_chart_files` 回传结果。",
                placeholder="请输入图表代码",
                value=str(state.get("python_code", "")),
                multiline=True,
            ),
            UiButton(
                component_id="execute_code",
                label="执行图表代码",
                description="执行代码并返回 stdout/stderr 与图表文件信息。",
            ),
            UiTextInput(
                component_id="exec_output",
                label="执行输出",
                description="显示环境检查结果或图表代码执行输出。",
                value=str(state.get("exec_output", "")),
                multiline=True,
                enabled=False,
            ),
        ]

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """首屏渲染。"""
        state = self._default_state()
        return self.to_page(
            title="Python 图表增强插件配置",
            subtitle="检查图表库并执行图表处理代码",
            components=self._components(state),
            state=state,
        )

    def on_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """处理页面交互。"""
        event = event or {}
        state = dict(event.get("state") or {})
        event_type = str(event.get("type", "")).strip()
        component_id = str(event.get("componentId", "")).strip()
        value = event.get("value")

        message = ""
        if event_type == "input_submit" and component_id == "python_code":
            state["python_code"] = "" if value is None else str(value)
            message = "代码已更新"
        elif event_type == "button_click" and component_id == "check_environment":
            state["exec_output"] = self._check_environment()
            message = "环境检查已完成"
        elif event_type == "button_click" and component_id == "execute_code":
            code = str(state.get("python_code", ""))
            state["exec_output"] = self._execute_python_code(code)
            message = "代码执行完成"

        return self.to_page(
            title="Python 图表增强插件配置",
            subtitle="检查图表库并执行图表处理代码",
            components=self._components(state),
            state=state,
            message=message,
        )


def create_page() -> UiPage:
    """插件 UI 工厂入口。"""
    return PythonChartLibsConfigPage()
