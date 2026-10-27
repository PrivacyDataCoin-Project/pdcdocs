#!/usr/bin/env python3
"""Deprecated: site theme is now the default docs build.

Use:
  python3 tools/build.py
"""

from build import main

if __name__ == "__main__":
    print("site theme is production — running tools/build.py")
    main()
