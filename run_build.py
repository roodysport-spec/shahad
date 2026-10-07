import sys
import os

base_dir = r"C:\Users\USER\.gemini\antigravity\scratch\volleyball-platform\frontend"
script_file = os.path.join(base_dir, "build_frontend.py")

with open(script_file, "r", encoding="utf-8") as f:
    code = f.read()

globs = {"__name__": "__main__", "__file__": script_file}
exec(code, globs)
print("SUCCESS: Executed build_frontend.py properly!")
