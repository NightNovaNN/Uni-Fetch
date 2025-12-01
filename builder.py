import os
import shutil
import subprocess
import sys

def find_compiler(ext):
    compilers = {
        ".c": ["gcc", "clang"],
        ".cpp": ["g++", "clang++"],
        ".cc": ["g++", "clang++"],
        ".zig": ["zig"],
        ".rs": ["rustc"],
        ".go": ["go"],
        ".ts": ["tsc"],
        ".py": ["python", "pyinstaller"],
        ".lua": ["luac"],
        ".java": ["javac"]
    }

    if ext not in compilers:
        return None

    for c in compilers[ext]:
        if shutil.which(c):
            return c

    return None

def build(file):
    if not os.path.exists(file):
        print("File not found.")
        return

    ext = os.path.splitext(file)[1]
    compiler = find_compiler(ext)

    if compiler is None:
        print(f"No compiler found for {ext}")
        return

    out = os.path.splitext(file)[0]

    print(f"Using compiler: {compiler}")

    # Dynamic build logic
    if compiler in ["gcc", "clang", "g++", "clang++"]:
        cmd = [compiler, file, "-o", out]
    elif compiler == "zig":
        cmd = ["zig", "build-exe", file]
    elif compiler == "rustc":
        cmd = ["rustc", file, "-o", out]
    elif compiler == "go":
        cmd = ["go", "build", "-o", out, file]
    elif compiler == "tsc":
        cmd = ["tsc", file]
    elif compiler == "python":
        cmd = ["python", file]
    elif compiler == "pyinstaller":
        cmd = ["pyinstaller", "--onefile", file]
    elif compiler == "luac":
        cmd = ["luac", "-o", out + ".luac", file]
    elif compiler == "javac":
        cmd = ["javac", file]
    else:
        print("Unknown compiler mapping.")
        return

    print("Running:", " ".join(cmd))
    subprocess.run(cmd)
    print("Build complete\n")
