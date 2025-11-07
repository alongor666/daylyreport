import argparse
import os
import sys

import pandas as pd


def find_first_xlsx(search_dirs: list[str]) -> str | None:
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            if name.lower().endswith(".xlsx"):
                path = os.path.join(d, name)
                if os.path.isfile(path):
                    return path
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview first rows of an Excel file (.xlsx)")
    parser.add_argument("file", nargs="?", help="Path to .xlsx file (optional)")
    parser.add_argument("--sheet", dest="sheet", default=0, help="Sheet name or index (default: 0)")
    parser.add_argument("--rows", dest="rows", type=int, default=5, help="Rows to preview (default: 5)")
    args = parser.parse_args()

    path = args.file
    if not path:
        path = find_first_xlsx([os.path.join(os.getcwd(), "data"), os.getcwd()])
        if not path:
            print("未在当前目录找到 .xlsx 文件，请指定路径：python scripts/read_excel_sample.py <文件路径>")
            sys.exit(2)

    try:
        df = pd.read_excel(path, sheet_name=args.sheet)
    except Exception as e:
        print(f"读取失败: {e}")
        sys.exit(1)

    print(f"文件: {path}")
    print(f"行列: {df.shape}")
    print(df.head(args.rows).to_string(index=False))


if __name__ == "__main__":
    main()
