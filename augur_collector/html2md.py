import subprocess
import sys

# 强制使用 UTF-8
print(sys.argv)
result = subprocess.run(
    "agent-browserxxx get html " + sys.argv[1],
    capture_output=True,
    # shell=True,
    encoding='utf-8',
    errors='raise',
    check=True
)
print(result.stdout)
