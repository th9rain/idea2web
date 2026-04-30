"""
idea2web - 全栈网页应用生成器

用法:
  python -m scripts quick --user-input "我想做一个记账软件" --output-dir ./my-app
  python -m scripts --help

依赖安装:
  pip install -r requirements.txt
"""
import sys
from pathlib import Path

# Ensure the scripts directory is on sys.path for absolute imports
_scripts_dir = str(Path(__file__).resolve().parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

try:
    from generator import main
    main()
except ImportError as e:
    print(f"错误: 缺少依赖 — {e}", file=sys.stderr)
    print("请运行: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)
except SystemExit:
    raise
except Exception as e:
    print(f"执行失败: {e}", file=sys.stderr)
    sys.exit(1)
