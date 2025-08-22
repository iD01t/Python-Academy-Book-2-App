
<img width="1024" height="1024" alt="icon" src="https://github.com/user-attachments/assets/7733b37a-d3f4-4ea7-b78e-d01a13ca583c" />

# iD01t Academy - Python Exercises Book 2, Edition #2

Premium 2025 Dark Suite, a single-file Python desktop application that bundles 12 polished mini apps with a modern GUI.  
The app auto-installs dependencies, uses `icon.ico` as the window icon, saves data locally in `./data`, and can export everything to a ZIP.

## Features
- 12 full apps in one, Expense Tracker, Adventure, Password Vault, To Do, Web Scraper, Unit Converter, Quiz, Weather, Plotter, Reminders, Text Tools, Timer
- Dark UI with ttkbootstrap when available, clean ttk fallback otherwise
- Auto dependency installation on first run
- Persistent JSON storage, per app
- Export all data to ZIP
- Cross platform, Windows, macOS, Linux
- One command build to EXE with PyInstaller

## Quick start
```bash
git clone https://github.com/your-username/id01t-academy-exercises-book2.git
cd id01t-academy-exercises-book2
python main.py
````

If Python asks for packages, the app installs them automatically on first run.
You can also install manually:

```bash
pip install -r requirements.txt
```

## Build Windows executable

```bash
pyinstaller --noconfirm --windowed --icon icon.ico main.py
```

The build creates `dist/main/main.exe`.
For reproducible builds in CI, use the included GitHub Actions workflow.

## Project structure

```
├── main.py                 # The all-in-one app
├── icon.ico                # App icon, drop your 256x256 ICO here
├── data/                   # Local storage created at runtime
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── pyinstaller.spec
└── .github/
    └── workflows/
        └── build.yml       # CI builds an .exe artifact on every push tag
```

## Screenshots

<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/1f142634-d8f4-4c1e-838e-08284a2b7f25" />


## About

Created by **Guillaume Lessard**, iD01t Productions.
Website: [https://id01t.store](https://id01t.store)
Contact: [admin@id01t.store](mailto:admin@id01t.store)

## License

MIT License, see `LICENSE`.

## Security notice

The Password Vault is for learning, not for real secrets. Use a professional password manager for sensitive credentials.

## Contributing

Issues and pull requests are welcome. See `CONTRIBUTING.md`.

## Changelog

See `CHANGELOG.md`.

````

---

### `LICENSE`
```text
MIT License

Copyright (c) 2025 Guillaume Lessard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
````

---

### `requirements.txt`

```text
ttkbootstrap>=1.10
requests>=2.31
beautifulsoup4>=4.12
matplotlib>=3.8
pillow>=10.3
```

---

### `pyproject.toml`

```toml
[project]
name = "id01t-academy-book2-suite"
version = "1.5.2.0"
description = "iD01t Academy - Python Exercises Book 2, Edition #2, Premium 2025 Dark Suite"
authors = [{ name = "Guillaume Lessard", email = "admin@id01t.store" }]
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
dependencies = [
  "ttkbootstrap>=1.10",
  "requests>=2.31",
  "beautifulsoup4>=4.12",
  "matplotlib>=3.8",
  "pillow>=10.3",
]

[project.urls]
Homepage = "https://id01t.store"
Repository = "https://github.com/your-username/id01t-academy-exercises-book2"

[tool.pyinstaller]
# Informational, the workflow uses the CLI command
entry = "main.py"
icon = "icon.ico"
windowed = true
```

---

### `.gitignore`

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.pdb
*.egg-info/
.venv/
venv/
.env
.DS_Store

# PyInstaller
build/
dist/
*.spec

# VS Code
.vscode/

# Runtime data
data/
*.log
```

---

### `pyinstaller.spec`

```python
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.' )],
    hiddenimports=[],
    hookspath=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='iD01t Academy - Book2 Edition2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='id01t_academy_book2_suite'
)
```

---

### `.github/workflows/build.yml`

```yaml
name: Build Windows EXE

on:
  push:
    tags:
      - "v*"
  workflow_dispatch: {}

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build
        run: |
          pyinstaller --noconfirm --windowed --icon icon.ico main.py

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: id01t-academy-book2-suite-windows
          path: dist/**
```

---

### `CONTRIBUTING.md`

```markdown
# Contributing

Thank you for your interest in improving this project.

## How to contribute
1. Fork the repo and create a new branch.
2. Keep changes focused and well documented.
3. Run a quick test, `python main.py`.
4. Submit a pull request with a clear description.

## Coding standards
- Python 3.9 or newer
- Keep the single-file architecture for the app
- Do not add paid or closed dependencies
- Follow clean, readable naming
```

---

### `SECURITY.md`

```markdown
# Security Policy

## Reporting a vulnerability
If you discover a security issue, email **admin@id01t.store**.  
Please do not open public issues with exploit details.

## Scope
The Password Vault is a demo, not a production password manager.  
Do not store real secrets in it.
```

---

### `CODE_OF_CONDUCT.md`

```markdown
# Code of Conduct

Be respectful, concise, and constructive.  
No harassment, spam, or hateful content will be tolerated.
```

---

### `CHANGELOG.md`

```markdown
# Changelog

## 1.5.2.0
- New dark 2025 UI
- Stable imports for ttk and ttkbootstrap
- 12 tabs, each with View Tab Code
- Data export to ZIP
- PyInstaller spec and CI workflow added
```

---

### `requirements-dev.txt`  *(optional)*

```text
pyinstaller>=6.6
ruff>=0.4
```

