# Skills 仓库协作规则

- 本仓库维护可跨项目复用的 Agent Skills，不绑定某个应用的框架、路径、数据库或部署方式。
- 修改前检查 Git 状态和现有规范，保留与当前任务无关的改动。
- Skill 按实际职责拆分，名称和目录保持一致；保留已有名称的兼容性，不随意移动已发布入口。
- 每个 Skill 可独立安装；必需资源放在自身目录中，不依赖兄弟 Skill、个人路径或未声明的工具。
- Skill 优先写适用场景、产出和影响正确性的必要约束；`description` 用于准确触发，具体语言和复杂场景示例按需放入 `references/`。
- 中文说明、注释和文档应具体、准确；不要靠重复规则或逐行翻译代码扩充内容。
- 只补充注释时，不改变逻辑、接口、类型注解、导入顺序或外部操作范围。
- 修改后运行 `uv run scripts/validate_skills.py`，并按风险验证 Skills CLI 的发现和安装；不得把结构校验描述为行为效果保证。
- 第三方 CLI 维护自己的安装锁记录，不手工生成安装哈希，不为提供 Skills 强行创建 npm 项目。
- Git 提交任务读取并遵循 [git-chinese-commits/SKILL.md](git-chinese-commits/SKILL.md)，提交规范只在该 Skill 中维护。
