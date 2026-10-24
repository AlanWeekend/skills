# 中文代码注释与 Git 提交 Skills

面向需要阅读、审查和维护源码的中文开发者，提供可独立安装、按需组合的代码注释和 Git 提交规范。说明文字及提交描述使用简体中文，代码标识符、协议名和工具标签保留规范英文。

目标是让读者理解文件用途、接口约定、执行流程和设计原因。复杂语法及框架机制也应解释清楚；不靠重复翻译赋值、括号或标签增加注释数量。

## Skills 目录

| Skill | 负责什么 | 适用场景 |
| --- | --- | --- |
| [chinese-code-comments](chinese-code-comments/SKILL.md) | 函数内部、业务分支、异步流程及关键语句的详细中文注释 | 任意语言，需要看懂具体实现 |
| [file-purpose-comments](file-purpose-comments/SKILL.md) | 文件开头的用途、职责、入口及关键依赖说明 | 新建文件，或补齐存量文件的用途说明 |
| [js-ts-chinese-comments](js-ts-chinese-comments/SKILL.md) | JS / TS 的函数、类、类型和成员 JSDoc | JavaScript、TypeScript、JSX、TSX，以及 Vue 脚本 |
| [vue-chinese-comments](vue-chinese-comments/SKILL.md) | Vue SFC 文件头、组件契约、响应式逻辑、模板区块和生命周期说明 | Vue 页面与组件；支持 Options API 和 Composition API |
| [python-chinese-docstrings](python-chinese-docstrings/SKILL.md) | Python 模块、类、函数及方法的中文 Docstring | 同步 / 异步 Python 代码，不绑定后端框架 |
| [chinese-comment-review](chinese-comment-review/SKILL.md) | 审查注释的完整性、准确性及与代码的一致性 | 代码审查，或检查已有代码的可读性 |
| [git-chinese-commits](git-chinese-commits/SKILL.md) | 中文 Conventional Commits、commitlint 校验、暂存范围与提交结果核对 | 编写提交信息、创建提交及已授权的推送 |

`js-ts-chinese-comments` 保留原来的名称和目录，旧安装命令仍然可用。Vue 文件仍有基本兼容说明；需要完整的模板和响应式规则时，按需组合 `vue-chinese-comments`。

每个 Skill 都能独立使用，不要求同时安装其他 Skill。基础规则允许必要的少量重复，详细示例放在各自的 `references/` 中，避免安装后依赖仓库中的兄弟目录。

## 使用 npx 安装

命令中的工具名称是 **`skills`（复数）**。消费本仓库不需要安装 uv，也不需要本仓库提供 `package.json` 或发布 npm 包。

在目标项目目录运行：

```bash
# 查看 GitHub 仓库中可以安装的 Skills，不执行安装。
npx skills add AlanWeekend/skills --list

# 按名称安装一个 Skill；示例安装给 Codex。
npx skills add AlanWeekend/skills --skill vue-chinese-comments --agent codex --copy -y

# 一次安装多个 Skill。
npx skills add AlanWeekend/skills --skill file-purpose-comments js-ts-chinese-comments vue-chinese-comments --agent codex --copy -y

# 安装本仓库的全部 Skills，只面向指定 Agent。
npx skills add AlanWeekend/skills --skill '*' --agent codex --copy -y
```

`--copy` 使用复制方式安装，避免依赖符号链接；省略 `--agent codex` 可按 CLI 提示选择其他支持的 Agent。希望跨项目使用时，可以在安装命令中增加 `--global`。

远程安装读取 GitHub 上的内容。未推送的修改应通过本地路径安装验证；在目标项目目录运行：

```powershell
npx skills add D:/Code/skills --list
npx skills add D:/Code/skills --skill python-chinese-docstrings --agent codex --copy -y
```

`skills-lock.json` 等安装记录由 Skills CLI 维护，不手写或复制伪造。具体锁记录以安装来源和 CLI 当前支持的行为为准。

## 如何组合

| 项目或任务 | 建议选择 |
| --- | --- |
| Vue + TypeScript 前端 | `file-purpose-comments` + `js-ts-chinese-comments` + `vue-chinese-comments` + `chinese-code-comments` |
| Python 后端或脚本 | `python-chinese-docstrings` + `chinese-code-comments`；需要统一文件职责字段时再加 `file-purpose-comments` |
| 其他语言，只需要中文流程说明 | `file-purpose-comments` + `chinese-code-comments` |
| 只检查现有注释 | `chinese-comment-review` |
| 中文规范提交，不需要注释规则 | `git-chinese-commits` |

安装是提供可发现的指导，不是自动执行的 lint 保证。需要长期强制执行时，可把以下约定写入使用方仓库的 `AGENTS.md`，并结合项目已有检查：

```markdown
- 自有源码的文件用途说明、接口说明及业务逻辑注释使用简体中文。
- 每个 Vue 文件说明页面或组件用途；TS 函数和类型说明语义；Python 模块、类和函数使用中文 Docstring。
- 注释覆盖参数含义、返回结果、异常、业务分支、异步流程及关键副作用；复杂语法说明实际作用。
- 修改代码时同步维护注释；保留工具必需标签、许可声明和指令，不修改生成文件或第三方源码。
```

Python 的 `Args:`、`Returns:`、`Raises:` 和 JSDoc 的 `@param`、`@returns` 等是工具识别的标签，其后的解释使用中文。

## 仓库结构

```text
.
├── AGENTS.md
├── README.md
├── chinese-code-comments/
├── file-purpose-comments/
├── js-ts-chinese-comments/
├── vue-chinese-comments/
├── python-chinese-docstrings/
├── chinese-comment-review/
├── git-chinese-commits/
└── scripts/
    └── validate_skills.py
```

各 Skill 的入口为 `SKILL.md`，`agents/openai.yaml` 提供 Codex 的中文展示信息；有实际需要时才添加 `references/`。

## 维护与验证

新增 Skill 时，新建一个与 `name` 同名的目录及 `SKILL.md`，在 YAML frontmatter 中填写 `name` 和有明确触发范围的 `description`，再更新本页目录与组合建议。

维护者可以使用 uv 运行仓库校验器；依赖由脚本元数据声明，不需要创建 Python 项目或虚拟环境：

```bash
uv run scripts/validate_skills.py
npx skills add . --list
```

校验器检查元数据、名称、内部文档链接、引用的自包含性和 README 目录覆盖。它不能证明业务注释内容准确；更新 Skill 后，还应使用真实文件或隔离样例检查输出，并在临时目录试装。不要通过注释宣称代码不存在的权限检查、事务、重试或性能保证。
