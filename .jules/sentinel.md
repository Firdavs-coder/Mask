## 2025-05-14 - [Path Traversal and Input Validation Fixes]
**Vulnerability:** Input paths were not validated, potentially allowing access to arbitrary files through symlinks or unsupported file types. Also, constant-value images could cause division by zero.
**Learning:** `os.path.abspath` is not enough to prevent path traversal if symlinks are involved; `os.path.realpath` is necessary.
**Prevention:** Always validate input file extensions and use `realpath` for sensitive path operations. Ensure mathematical operations (like normalization) handle edge cases like zero variance.
