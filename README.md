# 🤖 AI Code Humanizer

AI Code Humanizer is a powerful web application that detects and rewrites AI-generated source code into natural, human-like code using AST-based logic, variable renaming, comment generation, and documentation suggestions.

Supports the following languages:

- ✅ Python
- ✅ Java
- ✅ JavaScript
- ✅ C++

---

## 🚀 Features

- Detects AI-generated code
- Converts it into human-written style using AST
- Renames variables (e.g. `x` → `totalSum`)
- Adds meaningful inline comments
- Adds docstrings or JavaDoc-style method descriptions
- Monaco Editor for syntax highlighting and editing
- Copy-to-clipboard functionality
- Loading spinner for UX feedback

---

## 🧩 Project Structure

```
AI-CodeHumanizer/
├── Backend/
│   ├── main.py                # FastAPI entry point
│   ├── humanizer.py           # Multi-language AST humanization logic
│   ├── humanizer_ast/
│   │   ├── cpp_ast.py
│   │   ├── js_humanizer.js
│   │   ├── JavaHumanizer.java
│   │   └── python_ast/
│   │       └── __init__.py
│   ├── test.cpp, input.js, Test.java  # Temp files used during processing
│   └── requirements.txt
├── Frontend/
│   ├── App.jsx                # React App with Monaco editor and spinner
│   ├── index.css
│   └── package.json
```

---

## 🛠️ Setup Instructions

### 1. Backend Setup

1. Install Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install LLVM & Clang (for C++ parsing) and set path in `cpp_ast.py`:

```py
Config.set_library_file("path/to/libclang.dll")
```

4. Ensure Java is installed and `javaparser-core-3.23.1.jar` is present in `humanizer_ast/`

### 2. Frontend Setup

```bash
cd Frontend
npm install
npm run dev
```

### 3. Run FastAPI backend

```bash
cd Backend
uvicorn main:app --reload
```

---

## 🌐 Usage

1. Paste AI-generated code into the Monaco editor.
2. Select language from the dropdown.
3. Click “Humanize Code”.
4. View and copy the humanized output.

---

## 📦 Tech Stack

- 🐍 Python 3.10
- ⚡ FastAPI
- 🖥️ React + Vite + Monaco Editor
- ☕ Java + JavaParser
- 🧠 Clang libclang bindings
- 📜 Esprima + Escodegen (for JS AST rewriting)

---

## 🙌 Credits

Made with ❤️ by Yash=

---

## 📄 License

MIT License