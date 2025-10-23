# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is CPython, the reference implementation of the Python programming language. Version 3.15.0 alpha 1. This is a large C codebase (~2.5M lines) implementing the Python interpreter, standard library C extensions, and extensive test suite.

## Building and Testing

### Unix/Linux/macOS Build

Standard build process:
```bash
./configure
make
make test
```

Debug build (recommended for development):
```bash
./configure --with-pydebug
make
```

Optimized build with PGO:
```bash
./configure --enable-optimizations
make
```

### Windows Build

```bash
PCbuild\build.bat
PCbuild\rt.bat -q  # Run tests
```

See `PCbuild/readme.txt` for detailed Windows build instructions.

### Running Tests

Run all tests:
```bash
make test
```

Run tests with resource-intensive tests enabled:
```bash
make buildbottest
```

Run specific tests:
```bash
make test TESTOPTS="-v test_os test_gdb"
```

Run a single test file directly:
```bash
./python -m test test_os
./python -m test.test_os  # Alternative syntax
```

Fast subset of tests:
```bash
make quicktest
```

## Repository Structure

### Core Interpreter Components

- **Include/** - C API headers (public and internal)
  - Public API: function declarations, type definitions, macros
  - Internal API (Internal/): interpreter internals not for external use

- **Python/** - Core interpreter implementation
  - `ceval.c` - Bytecode evaluation loop (VM heart)
  - `compile.c` - AST to bytecode compiler
  - `codegen.c` - Code generation from AST
  - `flowgraph.c` - Control flow graph and optimizations
  - `assemble.c` - Final bytecode assembly
  - `import.c` - Module import system
  - `initconfig.c` - Runtime configuration
  - `symtable.c` - Symbol table for variable scopes

- **Parser/** - Lexer, tokenizer, and PEG parser
  - `parser.c` - Auto-generated PEG parser (1.4MB, largest file)
  - `tokenizer/` - Lexical analysis
  - `Python.asdl` - Abstract Syntax Description Language grammar

- **Objects/** - Built-in type implementations (68 files)
  - `dictobject.c` - dict implementation (233KB)
  - `longobject.c` - Arbitrary precision integers (223KB)
  - `unicodeobject.c` - str implementation
  - `listobject.c` - list implementation (128KB)
  - `typeobject.c` - Type system and metaclasses (12,711 lines)
  - Plus: tuple, set, float, bytes, code objects, functions, etc.

- **Modules/** - C extension modules for standard library (150 files)
  - `_asyncio`, `_json`, `_sqlite3`, `_ssl`, `_testcapi`, etc.
  - Pattern: `PyInit_<modulename>()` entry point returns `PyModuleDef`

- **Programs/** - Entry points and utilities
  - `python.c` - Main executable entry point
  - `_freeze_module.c` - Freezes Python modules into C code
  - `_testembed.c` - Embedding API tests

- **Lib/** - Pure Python standard library (191 directories)
  - Standard library implemented in Python (when C not required)
  - `importlib/` - Import system (bootstrap frozen into interpreter)

- **Grammar/** - Language definition
  - `python.gram` - PEG grammar specification
  - `Tokens` - Token definitions

### Documentation and Internals

- **InternalDocs/** - Architecture documentation
  - `compiler.md` - Compilation pipeline (5 phases)
  - `interpreter.md` - VM and frame system
  - `parser.md` - PEG parser design
  - `garbage_collector.md` - GC implementation
  - `frames.md` - Frame objects and execution
  - `exception_handling.md` - Exception handling
  - `jit.md` - JIT compilation (experimental)

- **Doc/** - User-facing documentation (reStructuredText)
  - Build docs: `cd Doc && make venv && make html`

- **Misc/** - Miscellaneous files
  - `NEWS.d/` - Changelog entries
  - Various helper scripts

### Platform-Specific

- **PC/** - Windows-specific headers and utilities
- **PCbuild/** - Windows Visual Studio build files (140 files)
- **Mac/** - macOS-specific build instructions
- **Android/** - Android platform support
- **iOS/** - iOS platform support

### Tools

- **Tools/** - Development utilities
  - `msi/` - Windows installer creation
  - Various code generation and analysis tools

## Architecture Overview

### Execution Pipeline (6 stages)

```
Source Code → Lexer → Tokens → PEG Parser → AST →
Compiler (5 phases) → Bytecode → Stack VM → Execution
```

1. **Lexer/Tokenizer** (`Parser/tokenizer/`): Characters → Tokens
2. **PEG Parser** (`Parser/parser.c`): Tokens → AST
3. **Symbol Analysis** (`Python/symtable.c`): Determine variable scopes
4. **Code Generation** (`Python/codegen.c`): AST → Instruction sequences
5. **Flow Graph** (`Python/flowgraph.c`): Instructions → CFG + optimizations
6. **Assembly** (`Python/assemble.c`): CFG → Final bytecode
7. **Execution** (`Python/ceval.c`): Stack-based VM executes bytecode

### Key Architectural Concepts

**Stack-Based VM:**
- Evaluation stack pre-allocated as `PyObject*` array
- Stack size determined at compile time (`co_stacksize`)
- Instruction format: 8-bit opcode + 8-bit argument
- Extended arguments via `EXTENDED_ARG` opcode
- ~100+ opcodes defined in `Python/bytecodes.c`

**Adaptive Specialization (PEP 659):**
- Generic instructions → specialized variants at runtime
- Inline caches store type information
- Guards check assumptions, deoptimize if violated
- Significant performance improvements for hot paths

**Frame System:**
- Internal `_PyInterpreterFrame` for execution
- Public `PyFrameObject` exposed on demand (debuggers, `sys._getframe`)
- 3.11+ optimization: inlined Python→Python calls skip C dispatch
- Call stack uses pointer-bump allocator for locality

**Object System:**
- Everything is `PyObject*` (refcounted pointer)
- Type objects are `PyTypeObject` (40+ function pointer slots)
- C3 linearization for MRO (Method Resolution Order)
- Descriptor protocol for attribute access
- Type versioning for cache invalidation

**Module Loading:**
- Unified interface for `.py`, `.pyc`, `.so` files
- Bootstrap `importlib` frozen into interpreter
- `sys.modules` caches loaded modules
- C extensions integrate seamlessly via `PyModuleDef`

**Memory Management:**
- Reference counting (`Py_INCREF`/`Py_DECREF`) for deterministic cleanup
- Cycle-detecting GC for circular references
- Memory arenas for object allocation
- Small object allocator (pymalloc) for performance

## Common Development Workflows

### Modifying the Language Grammar

1. Edit `Grammar/python.gram`
2. Regenerate parser: `make regen-pegen`
3. Update AST definition if needed: `Parser/Python.asdl`
4. Implement in compiler: `Python/compile.c`, `Python/codegen.c`
5. Add bytecode instruction if needed: `Python/bytecodes.c`
6. Run `make regen-cases` to regenerate VM cases
7. Build and test

See `InternalDocs/changing_grammar.md` for detailed instructions.

### Adding a New Built-in Type

1. Create implementation in `Objects/yourtypeobject.c`
2. Define `PyTypeObject` structure with slots
3. Add header to `Include/`
4. Register type in appropriate module (often `builtins`)
5. Add tests in `Lib/test/test_yourtype.py`
6. Update documentation

### Adding a C Extension Module

1. Create module file in `Modules/yourmodule.c`
2. Define `PyModuleDef` structure
3. Implement `PyInit_yourmodule()` entry point
4. Add to `Modules/Setup` or configure build system
5. Build and test
6. Add tests in `Lib/test/test_yourmodule.py`

See detailed example in `PCbuild/readme.txt` (section "Add a new project").

### Debugging the Interpreter

Debug build is essential:
```bash
./configure --with-pydebug
make
```

This enables:
- Extra assertions
- Debug symbols
- Memory debugging
- `_d` suffix on binaries (e.g., `python_d`)

Use gdb/lldb:
```bash
gdb ./python
(gdb) run script.py
(gdb) bt  # Backtrace on crash
```

### Performance Profiling

Build with PGO for production:
```bash
./configure --enable-optimizations
make profile-opt
```

Profile compilation phases: Set `PYTHONDUMPREFS`, `PYTHONVERBOSE`

## Important Files for Reference

- **configure.ac** - Autoconf configuration
- **Makefile.pre.in** - Make template (generated → Makefile)
- **pyconfig.h.in** - Configuration header template
- **LICENSE** - Python Software Foundation license

## Code Style and Conventions

- Follow PEP 7 for C code style
- Follow PEP 8 for Python code style
- Use `.pre-commit-config.yaml` hooks (run `pre-commit install`)
- Ruff configured in `.ruff.toml` for Python linting
- See Developer's Guide: https://devguide.python.org/

## Testing Considerations

- Tests are in `Lib/test/`
- Test files named `test_*.py`
- Use unittest framework
- C API tests use `Modules/_testcapi`
- Some tests are resource-intensive and skipped by default (use `make buildbottest`)
- Tests must not modify system state
- Use `@unittest.skipIf` for platform-specific tests

## Build System Notes

- Generated files committed to repo (for bootstrapping)
- Regenerate parser: `make regen-pegen`
- Regenerate VM cases: `make regen-cases`
- Regenerate all: `make regen-all`
- Don't manually edit generated files (will be overwritten)

## Platform-Specific Notes

**Windows:**
- Use Visual Studio 2017 or later with Python workload
- Build script: `PCbuild\build.bat`
- Solution file: `PCbuild\pcbuild.sln`
- See `PCbuild/readme.txt` for complete instructions

**macOS:**
- Framework builds supported (see `Mac/README.rst`)
- Universal binary builds available
- May need to install dependencies via Homebrew

**Unix/Linux:**
- Install build dependencies per distribution
- See https://devguide.python.org/getting-started/setup-building.html#build-dependencies
- Configure detects available libraries (SSL, readline, etc.)

## External Resources

- Developer Guide: https://devguide.python.org/
- Issue Tracker: https://github.com/python/cpython/issues
- Documentation: https://docs.python.org
- Discourse: https://discuss.python.org/
