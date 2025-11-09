# Excel MCP 服务器安装说明

## 已安装的MCP服务器

### 1. Filesystem MCP 服务器
- **包**: `@modelcontextprotocol/server-filesystem`
- **功能**: 读取和处理文件系统中的文件
- **配置路径**: `/Users/xuechenglong/Library/CloudStorage/GoogleDrive-alongor0512@gmail.com/我的云端硬盘/WPS+iMac/车险签单清单_2025年3月`

### 2. Excel MCP 服务器 (Node.js)
- **包**: `@negokaz/excel-mcp-server`
- **功能**: 专门处理Excel文件的MCP服务器
- **支持**: 读取、写入Excel文件

### 3. Excel MCP 服务器 (Python)
- **文件**: `excel_mcp_server.py`
- **功能**: 自定义Python实现的Excel处理服务器
- **支持**: 
  - 读取Excel文件 (`read_excel`)
  - 获取Excel文件信息 (`get_info`)
  - 列出Excel文件 (`list_excel_files`)

## 使用方法

### 读取Excel文件
```python
# 使用pandas直接读取（在Python环境中）
import pandas as pd
df = pd.read_excel('保批单业务报表-20250317.xlsx')
print(df.shape)
print(df.columns)
```

### 通过MCP服务器访问
MCP服务器现在可以通过Claude Desktop访问这些Excel文件。重启Claude Desktop后，您应该能够：

1. 读取Excel文件内容
2. 分析数据
3. 执行数据处理操作

## 测试验证

运行测试脚本验证安装：
```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行Excel测试
python test_excel.py
```

## 配置文件位置

Claude Desktop配置文件：`/Users/xuechenglong/Library/Application Support/Claude/claude_desktop_config.json`

## 注意事项

1. 确保Claude Desktop已重启以加载新的MCP服务器
2. 所有Excel文件都在允许访问的目录中
3. 虚拟环境已激活，所有依赖项已安装

## 故障排除

如果MCP服务器无法工作：
1. 检查配置文件语法
2. 验证Node.js模块是否正确安装
3. 查看Claude Desktop日志获取错误信息
4. 确保文件路径正确且有访问权限