# Python Chart Libs Plugin

> 这是一个“图表处理增强插件”示例，用于给 NowChat 扩展更多 Python 图表库执行能力。

## 插件功能说明

1. 工具：`python_chart_exec`
- 供大模型执行图表处理代码（如统计图、趋势图、分组可视化等）。
- 无需传入输出目录，工具会自动生成本次图表输出路径。

2. 插件配置页面
- 提供“检查图表环境”按钮（检查常见图表库是否可导入）。
- 提供代码输入框与执行按钮，方便手动验证图表代码。

## 目录结构
```text
python_chart_libs_plugin/
  plugin.json
  README.md
  assets/
    .gitkeep
  hooks/
    app_start.py
  libs/
    .gitkeep
  runtime/
    .gitkeep
  tools/
    python_chart_exec.py
  python_chart_ui/
    __init__.py
    base.py
    schema.py
```
