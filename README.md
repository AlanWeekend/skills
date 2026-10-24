# 中文开发规范 Skills

面向需要阅读、审查和维护源码及数据库的中文开发者，提供可独立安装、按需组合的代码注释、业务对象身份设计、数据库命名与审计字段、数据库中文注释和 Git 提交规范。说明文字及提交描述使用简体中文，代码标识符、协议名和工具标签保留规范英文。

目标是让读者理解文件用途、接口约定、执行流程和设计原因。复杂语法及框架机制也应解释清楚；不靠重复翻译赋值、括号或标签增加注释数量。

## Skills 目录

| Skill | 负责什么 | 适用场景 |
| --- | --- | --- |
| [chinese-code-comments](chinese-code-comments/SKILL.md) | 函数内部、业务分支、异步流程及关键语句的详细中文注释 | 任意语言，需要看懂具体实现 |
| [file-purpose-comments](file-purpose-comments/SKILL.md) | 文件开头的用途、职责、入口及关键依赖说明 | 新建文件，或补齐存量文件的用途说明 |
| [js-ts-chinese-comments](js-ts-chinese-comments/SKILL.md) | JS / TS 的函数、类、类型和成员 JSDoc | JavaScript、TypeScript、JSX、TSX，以及 Vue 脚本 |
| [vue-chinese-comments](vue-chinese-comments/SKILL.md) | Vue 组件输入输出契约、响应式、生命周期及模板业务语义 | Vue 页面与组件的专项注释 |
| [python-chinese-docstrings](python-chinese-docstrings/SKILL.md) | Python Docstring 的合法形式及类、函数等接口契约 | 同步 / 异步 Python 代码；模块用途复用同一份 Docstring |
| [chinese-comment-review](chinese-comment-review/SKILL.md) | 只审查完整性、准确性、一致性及重复问题，默认报告而不补写 | 代码审查，或检查已有代码的可读性 |
| [git-chinese-commits](git-chinese-commits/SKILL.md) | 中文 Conventional Commits、commitlint 校验、暂存范围与提交结果核对 | 编写提交信息、创建提交及已授权的推送 |
| [business-object-identity](business-object-identity/SKILL.md) | 区分记录键、稳定业务对象 ID、外部标识与业务编码，定义唯一范围和生命周期 | 模型设计、版本发布、API 标识、复制和导入导出；不限定数据库、语言或 ID 算法 |
| [database-naming-conventions](database-naming-conventions/SKILL.md) | 单数业务域表名、snake_case 字段及创建更新的时间和操作者四个必备审计字段 | 自有业务表、字段、ORM 模型及迁移的设计与审查；这是用户约定，不宣称唯一行业标准 |
| [database-chinese-comments](database-chinese-comments/SKILL.md) | 为表和字段编写准确的中文业务注释，保持 DDL、ORM、迁移及数据库元数据一致 | 新建或修改数据库表、字段；含 PostgreSQL、MySQL、SQLite 限制及 SQLModel、SQLAlchemy 与 Alembic 参考 |

各 Skill 可独立安装，入口写明适用场景、产出和必要约束，示例位于自身的 `references/` 中。注释类 Skills 分别覆盖文件用途、普通接口、内部流程、Vue 专项、Python Docstring 和审查；组合后仍保持详细中文说明要求。

多个 Skill 涉及同一段说明时，直接维护已有准确内容，同一信息只写一次。Python 模块用途使用一份合法 Docstring。

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

# 独立安装数据库相关 Skills。
npx skills add D:/Code/skills --skill business-object-identity database-naming-conventions database-chinese-comments --agent codex --copy -y
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
| 业务对象身份、版本关系和导入迁移设计 | `business-object-identity`，按项目需要结合已有数据库设计 Skill |
| 单数业务域表名、字段命名与基础审计 | `database-naming-conventions` |
| 数据库表和字段中文注释 | `database-chinese-comments`；同时变更对象身份时再加 `business-object-identity` |

安装是提供可发现的指导，不是自动执行的 lint 保证。需要长期强制执行时，可把以下约定写入使用方仓库的 `AGENTS.md`，并结合项目已有检查：

```markdown
- 自有源码的文件用途说明、接口说明及业务逻辑注释使用简体中文。
- 每个 Vue 文件说明页面或组件用途；TS 函数和类型说明语义；Python 模块、类和函数使用中文 Docstring。
- 注释覆盖参数含义、返回结果、异常、业务分支、异步流程及关键副作用；复杂语法说明实际作用。
- 修改代码时同步维护注释；保留工具必需标签、许可声明和指令，不修改生成文件或第三方源码。
```

Python 的 `Args:`、`Returns:`、`Raises:` 和 JSDoc 的 `@param`、`@returns` 等是工具识别的标签，其后的解释使用中文。

业务对象身份 Skill 不要求所有表同时增加自增主键、UUID 和业务编码；实体主键可以兼任稳定对象 ID。数据库注释 Skill 要求在目标引擎支持时将说明写入实际表列元数据，不以代码注释代替落库。

采用 `database-naming-conventions` 时，自有业务表使用单数、所属业务域前缀和 snake_case，字段采用 snake_case，必备 `created_at`、`updated_at`、`created_by`、`updated_by`。该 Skill 单独维护命名与基础审计偏好，业务身份和中文注释仍由另外两项 Skill 负责；存量和第三方表按其适用边界处理。

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
├── business-object-identity/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/identity-lifecycle.md
├── database-chinese-comments/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── sql-dialects.md
│       ├── sqlmodel-alembic.md
│       └── sqlalchemy-alembic.md
├── database-naming-conventions/
│   ├── SKILL.md
│   └── agents/openai.yaml
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
