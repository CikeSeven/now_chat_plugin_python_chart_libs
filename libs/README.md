# libs 准备说明

该目录用于放置图表处理相关 Python 库文件（解压后的包目录或纯 Python 文件）。

## 建议至少准备
- `matplotlib`
- `seaborn`
- `plotly`
- 以及它们的依赖（例如 `numpy`、`pandas`、`python-dateutil`、`pytz` 等）。

## 放置方式
将库文件直接解压到 `libs/` 下，例如：

```text
libs/
  matplotlib/
  seaborn/
  plotly/
  numpy/
  pandas/
  ...
```

## 注意
- 若包含原生扩展（`.so`），请确保与目标 ABI 匹配（当前主要为 Android arm64）。
- 建议优先使用可在 Android/Chaquopy 环境运行的包版本。
- 该插件定位为图表专项处理插件，建议优先准备图表生态完整依赖链。
