# FORTIFY_SOURCE 速查

## 1) 级别含义

- `_FORTIFY_SOURCE=0`：关闭 Fortify。
- `_FORTIFY_SOURCE=1`：基础检查（编译期+运行期）。
- `_FORTIFY_SOURCE=2`：更严格检查（常见发行版强化选项）。
- `_FORTIFY_SOURCE=3`：新版本 glibc/GCC 才支持，检查更激进（不是所有环境都有）。

注意：Fortify 依赖优化选项，通常至少需要 `-O1`，实践中一般配合 `-O2`。

## 2) 在哪里确认 FORTIFY_SOURCE 级别

### A. 看编译命令（最直接）

如果你能看到构建命令，直接找：

```bash
-D_FORTIFY_SOURCE=0
-D_FORTIFY_SOURCE=1
-D_FORTIFY_SOURCE=2
```

例如：

```bash
gcc -O2 -D_FORTIFY_SOURCE=2 demo.c -o demo
```

### B. 看源码/头文件宏定义

代码里也可能显式写了：

```c
#define _FORTIFY_SOURCE 2
```

或在编译日志里用 `-Wp,-dM` 导出的宏中确认。

### C. 看二进制符号（逆向场景常用）

如果看不到编译命令，可检查是否出现 Fortify 包装函数：

```bash
readelf -s ./pwn | grep -E "__.*_chk|__fortify_fail"
objdump -T ./pwn | grep -E "__.*_chk|__fortify_fail"
strings ./pwn | grep -E "__.*_chk|__fortify_fail"
```

常见符号：`__strcpy_chk`、`__memcpy_chk`、`__printf_chk`、`__fortify_fail`。

有这些符号通常说明 Fortify 开启了，但仅凭符号不一定精确区分 1 和 2。

### D. checksec 辅助判断

`checksec` 可能给出 `FORTIFY` 相关字段（fortified/fortifiable），可做快速参考。
但它不是“级别读取器”，要精确到 0/1/2，优先看编译参数。