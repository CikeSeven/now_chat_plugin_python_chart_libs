"""插件启动 Hook 示例。"""


def main(payload):
    """应用启动时输出一条轻量调试信息。"""
    print("[python_chart_libs] app_start hook triggered")
    return {
        "ok": True,
        "summary": "python_chart_libs 已启动",
    }
