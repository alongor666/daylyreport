#!/usr/bin/env python3
"""
简单的Excel MCP服务器实现
可以读取和处理Excel文件
"""

import json
import sys
import pandas as pd
import os

def read_excel_file(file_path, sheet_name=None):
    """读取Excel文件"""
    try:
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
        
        return {
            "success": True,
            "data": df.to_dict('records'),
            "columns": list(df.columns),
            "shape": df.shape,
            "file": file_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file": file_path
        }

def get_excel_info(file_path):
    """获取Excel文件信息"""
    try:
        excel_file = pd.ExcelFile(file_path)
        return {
            "success": True,
            "sheet_names": excel_file.sheet_names,
            "file": file_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file": file_path
        }

def process_request(request):
    """处理MCP请求"""
    action = request.get('action')
    file_path = request.get('file_path')
    
    if action == 'read_excel':
        sheet_name = request.get('sheet_name')
        return read_excel_file(file_path, sheet_name)
    elif action == 'get_info':
        return get_excel_info(file_path)
    elif action == 'list_excel_files':
        directory = request.get('directory', '.')
        excel_files = [f for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
        return {
            "success": True,
            "excel_files": excel_files,
            "directory": directory
        }
    else:
        return {
            "success": False,
            "error": f"Unknown action: {action}"
        }

def main():
    """主函数 - MCP服务器循环"""
    print("Excel MCP Server started", file=sys.stderr)
    
    while True:
        try:
            # 读取标准输入
            line = sys.stdin.readline()
            if not line:
                break
            
            # 解析JSON请求
            request = json.loads(line.strip())
            
            # 处理请求
            response = process_request(request)
            
            # 发送响应
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError as e:
            error_response = {
                "success": False,
                "error": f"JSON解析错误: {str(e)}"
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {
                "success": False,
                "error": f"服务器错误: {str(e)}"
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == '__main__':
    main()