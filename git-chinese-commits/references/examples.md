# 提交格式与执行注意事项

## 中文 Conventional Commits

```text
feat(conversations): 支持按用户查询会话列表
fix(runtime): 修复取消执行后订阅未释放的问题
docs(skills): 补充独立安装与组合使用说明
chore(scaffold): 初始化项目目录与开发规范
```

type 和 scope 只是规范标签，冒号后的变更描述使用中文。默认类型的选择：功能用 feat，缺陷用 fix，纯文档用 docs，代码结构调整用 refactor，测试用 test，构建与依赖用 build，流水线用 ci；其他维护工作按仓库约定使用 chore。

破坏性变更示例：

```text
feat(api)!: 统一分页响应字段

将列表响应统一为 items 和 nextCursor，便于客户端复用分页逻辑。

BREAKING CHANGE: 原 records 字段已移除，调用方需要改用 items。
```

例子只解释格式，不能据此编造当前项目的功能、字段、测试结果或破坏性变更。

## commitlint 校验

- 有配置时，先看仓库已有配置、依赖和脚本，不假定所有项目都使用 npm。
- 没有配置时，可以使用临时执行环境中的 `@commitlint/cli` 和 `@commitlint/config-conventional` 校验本次消息。
- 临时 npm 包的安装位置与仓库根目录不同；`npx --package` 不意味着任意目录中的配置都能解析这些包。应让临时配置可解析实际 preset，必要时使用在该环境中解析得到的绝对路径，不硬编码机器路径。
- 临时配置和校验消息不提交到业务仓库。实际校验失败时修正问题，不禁用规则、设置跳过 hooks 的变量或使用跳过检查的提交参数绕过。

## Windows 的 UTF-8 消息文件

仅在已经审查暂存内容、完成适用校验且任务授权提交时，使用以下方式传入已校验的中文信息；实际标题根据本次变更选择：

```powershell
$commitMessagePath = [IO.Path]::GetTempFileName()
try {
    $commitMessage = 'docs(skills): 补充安装说明'
    [IO.File]::WriteAllText(
        $commitMessagePath,
        $commitMessage + [Environment]::NewLine,
        [Text.UTF8Encoding]::new($false)
    )
    git -c i18n.commitEncoding=UTF-8 commit --file $commitMessagePath
    if ($LASTEXITCODE -ne 0) {
        throw 'Git 提交失败，需要根据错误继续检查。'
    }
} finally {
    Remove-Item -LiteralPath $commitMessagePath
}
```

临时文件是本次创建的消息文件；清理范围不能扩大到用户文件。类 Unix shell 也可使用 UTF-8 消息文件，避免把含反引号或 `$()` 的文本作为可执行 shell 代码拼接。

## 最终核对

- 提交标题、实际提交文件及暂存树与审查结果一致。
- 原有无关工作和剩余未提交内容没有被覆盖或意外纳入。
- 获得推送授权且执行 push 时，远程分支实际包含本次提交。
- 清楚区分“已本地提交”“已推送”和“验证未能运行”。
