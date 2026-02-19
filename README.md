# Python Chart Libs Plugin

> 这是一个“图表处理增强插件”示例，用于给 NowChat 扩展更多 Python 图表库执行能力。

## 插件功能说明
该插件当前提供以下能力：

1. 图表相关基础库路径占位
- 约定将图表相关 Python 库放入 `libs/` 目录。
- 插件安装后会把 `libs/` 加入 Python 运行路径。
- 该插件默认 `providesGlobalPythonPaths=true`，可为其他插件共享图表库路径。
- `requiredPluginIds=["python_base_libs"]`，安装本插件前需先安装 Python 基础库插件。
- 中文字体可放在 `assets/fonts/` 或 `libs/fonts/`，插件会在执行前自动尝试加载（matplotlib）。

2. 工具：`python_chart_exec`
- 供大模型执行图表处理代码（如统计图、趋势图、分组可视化等）。
- 无需传入输出目录，工具会自动生成本次图表输出路径。
- 返回 `stdout`、`stderr`、`_result`、`generatedChartFiles` 与 `outputDir`。
- 默认超时已提升，适合中等复杂度图表任务；极长任务建议拆分执行。

3. 插件配置页面
- 提供“检查图表环境”按钮（检查常见图表库是否可导入）。
- 提供代码输入框与执行按钮，方便手动验证图表代码。

## 需要准备哪些文件
必备文件：
- `plugin.json`：插件定义，包含工具、Hook、UI 命名空间等。
- `README.md`：插件说明文档。
- `tools/python_chart_exec.py`：图表执行工具脚本。
- `hooks/app_start.py`：启动 Hook（可用于启动日志/自检）。
- `python_chart_ui/schema.py`：插件配置页入口（必须有 `create_page()`）。
- `python_chart_ui/base.py` 与 `python_chart_ui/__init__.py`：UI DSL 基类与导出入口。

推荐目录：
- `libs/`：放图表库文件（如 matplotlib/seaborn/plotly 等）。
- `assets/`：静态资源占位。
- `runtime/`：运行时临时文件占位。

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

## 使用方式
1. 将 `python_chart_libs_plugin` 目录打包为 zip（zip 根目录必须直接包含 `plugin.json`）。
2. 在 NowChat 插件中心导入并安装该 zip。
3. 进入插件配置页先检查环境，再执行图表代码验证能力。
