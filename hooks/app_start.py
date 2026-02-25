"""插件启动 Hook 示例。"""


def main(payload):
    """应用启动时输出一条轻量调试信息。"""
    print("[now_chat_plugin_python_chart_libs] app_start hook triggered")
    return {
        "ok": True,
        "summary": "now_chat_plugin_python_chart_libs 已启动",
    }
