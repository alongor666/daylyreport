import sys
import importlib


def main() -> None:
    mods = [
        ("numpy", "__version__"),
        ("pandas", "__version__"),
        ("flask", "__version__"),
        ("flask_cors", None),
        ("openpyxl", "__version__"),
    ]
    print(f"Python: {sys.version.split()[0]}")
    for name, attr in mods:
        try:
            m = importlib.import_module(name)
            ver = getattr(m, attr) if attr else "OK"
            print(f"{name}: {ver}")
        except Exception as e:
            print(f"{name}: MISSING ({e})")


if __name__ == "__main__":
    main()

