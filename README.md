# UniFetch V1

UniFetch V1 is a universal, cross-language fetcher and builder.  
It downloads code and packages from multiple ecosystems (GitHub, npm, PyPI, Chocolatey), extracts them, and can also build source files using a dynamic compiler-detection system.

Everything is local and portable — UniFetch does not modify the system PATH or install anything globally.

---

## Features

### 🔹 Universal Fetch System

Supports multiple ecosystems:

- **GitHub** — fetch repositories or documentation
- **npm** — download Node packages without installing globally
- **PyPI** — fetch Python packages
- **Chocolatey** — pull `.nupkg` packages

### 🔹 Smart Build System

UniFetch includes a universal builder that:

- Detects compilers dynamically
- Supports C, C++, Zig, Rust, Go, TypeScript, Python, Lua, and Java
- Runs the correct compiler automatically
- Builds outputs with simple one-line commands

### 🔹 Portable by Design

- Zero installation
- No PATH modification
- All fetched packages stay inside the project folder
- Works anywhere Python works

---

## Requirements

- Python 3.8+
- Internet connection (for fetch operations)

---

## Installation

No installation required — just place `ufetch.py` and `builder.py` in your project and run:

```bash
python ufetch.py <command>
```

---

## Commands

### 📥 Fetch From GitHub

Download a repo:

```bash
python ufetch.py gh user/repo
```

Download only README + `/docs`:

```bash
python ufetch.py ghdocs user/repo
```

---

### 📦 Fetch From npm

```bash
python ufetch.py npm <package>
```

---

### 🐍 Fetch From PyPI

```bash
python ufetch.py pypi <package>
```

---

### 🍫 Fetch From Chocolatey

```bash
python ufetch.py choco <package>
```

---

## 🛠️ Build Files

UniFetch auto-detects compilers based on file extension.

Example:

```bash
python ufetch.py build hello.c
python ufetch.py build test.cpp
python ufetch.py build prog.zig
python ufetch.py build main.rs
python ufetch.py build app.go
python ufetch.py build script.ts
python ufetch.py build code.py
```

UniFetch chooses the correct compiler automatically:

| Extension | Compiler(s) Checked |
| --------- | ------------------- |
| `.c`      | gcc, clang          |
| `.cpp`    | g++, clang++        |
| `.cc`     | g++, clang++        |
| `.zig`    | zig                 |
| `.rs`     | rustc               |
| `.go`     | go                  |
| `.ts`     | tsc                 |
| `.py`     | python, pyinstaller |
| `.lua`    | luac                |
| `.java`   | javac               |

---

## Examples

### Fetch + Build a GitHub Repo

```bash
python ufetch.py gh NightNovaNN/CryoCompiler
```

### Fetch an npm tarball

```bash
python ufetch.py npm express
```

### Build a Zig program

```bash
python ufetch.py build main.zig
```

---

## Project Structure Example

```
project/
│  ufetch.py
│  builder.py
│
├── myrepo/          <-- GitHub repo
├── express/         <-- npm package
├── somepkg/         <-- PyPI or Choco package
└── main.exe         <-- build output
```

---

## Version

Run:

```bash
python ufetch.py version
```

Outputs:

```
UniFetch version 2.0.0
```

---

## Planned Features

- GitHub Release auto-downloader
- Automatic tool installation
- Manifest-based version locking
- Linux/macOS support
- Self-updater using GitHub API
- Turn UniFetch into a standalone `.exe`

---

## License

MIT License
Copyright (c) 2025 ISD NightNova



