# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""校验 Skill 入口、展示元数据及本地文档引用，只读取文件，不执行安装。

通过结构检查不能证明注释准确，行为效果仍需实际任务或隔离样例验证。
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def local_link_paths(markdown: str) -> list[str]:
    """提取非代码块中的本地 Markdown 链接，忽略远程地址和页内锚点。

    Args:
        markdown: 已按 UTF-8 解码的 Markdown 全文。

    Returns:
        去除查询串和锚点、完成 URL 解码的本地路径。
    """
    # 示例命令和源码内的链接不属于文档导航，先移除围栏代码块。
    prose: list[str] = []
    marker = ""
    marker_length = 0
    for line in markdown.splitlines():
        fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            opening, suffix = fence.groups()
            if not marker:
                marker, marker_length = opening[0], len(opening)
            elif (
                opening[0] == marker
                and len(opening) >= marker_length
                and not suffix.strip()
            ):
                marker, marker_length = "", 0
            continue
        if not marker:
            prose.append(line)

    # 当前仓库使用行内 Markdown 链接；带空格路径可使用尖括号包裹。
    paths: list[str] = []
    pattern = r"\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)"
    for match in re.finditer(pattern, "\n".join(prose)):
        target = match.group(1) or match.group(2)
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        paths.append(unquote(parsed.path))
    return paths


def check_links(document: Path, boundary: Path) -> list[str]:
    """检查本地文档链接存在，并且不超出允许的独立安装边界。

    Args:
        document: 要检查的 Markdown 文件。
        boundary: 允许引用的根目录；Skill 内部限制在自己的目录中。

    Returns:
        包含文件名和原因的错误列表；没有错误时为空列表。
    """
    try:
        content = document.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [f"{document}: 无法按 UTF-8 读取：{error}"]

    issues: list[str] = []
    allowed_root = boundary.resolve()
    for target in local_link_paths(content):
        resolved = (document.parent / target).resolve()
        # 单独安装只复制自身目录，兄弟 Skill 不能成为隐式依赖。
        if not resolved.is_relative_to(allowed_root):
            issues.append(f"{document}: 引用超出独立安装边界：{target}")
        elif not resolved.exists():
            issues.append(f"{document}: 本地链接不存在：{target}")
    return issues


def check_interface(skill: Path, skill_name: str) -> list[str]:
    """检查可选的 Codex 展示元数据，不要求其他 Agent 使用该文件。

    Args:
        skill: 单个 Skill 的目录。
        skill_name: frontmatter 中声明的安装名称。

    Returns:
        中文展示字段或默认调用提示存在问题时的错误列表。
    """
    metadata_path = skill / "agents" / "openai.yaml"
    if not metadata_path.exists():
        return []
    try:
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return [f"{metadata_path}: 无法读取展示元数据：{error}"]
    if not isinstance(metadata, dict) or not isinstance(
        metadata.get("interface"), dict
    ):
        return [f"{metadata_path}: 缺少 interface 映射"]

    interface = metadata["interface"]
    issues: list[str] = []
    for key in ("display_name", "short_description", "default_prompt"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            issues.append(f"{metadata_path}: {key} 必须是非空字符串")
    short_description = interface.get("short_description")
    if isinstance(short_description, str) and not 25 <= len(short_description) <= 64:
        issues.append(f"{metadata_path}: short_description 长度须为 25 至 64 个字符")
    prompt = interface.get("default_prompt")
    if isinstance(prompt, str) and ("$" + skill_name) not in prompt:
        issues.append(f"{metadata_path}: default_prompt 必须引用 $" + skill_name)
    return issues


def check_skill(skill: Path) -> list[str]:
    """校验一个 Skill 的入口和随安装复制的资源引用。

    Args:
        skill: 包含 SKILL.md 的独立 Skill 目录。

    Returns:
        入口格式、命名或引用存在问题时的错误列表。
    """
    entry = skill / "SKILL.md"
    try:
        content = entry.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [f"{entry}: 无法按 UTF-8 读取：{error}"]

    # 入口必须从 YAML 开始，避免 BOM 或普通标题干扰安装器发现元数据。
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if not match:
        return [f"{entry}: 缺少合法的 YAML frontmatter"]
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        return [f"{entry}: YAML 格式错误：{error}"]
    if not isinstance(frontmatter, dict):
        return [f"{entry}: frontmatter 必须是映射"]

    issues: list[str] = []
    name = frontmatter.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        issues.append(f"{entry}: name 必须是小写字母、数字及单个连字符组成的名称")
    elif len(name) > 64 or name != skill.name:
        issues.append(f"{entry}: name 须与目录同名，且不超过 64 个字符")
    description = frontmatter.get("description")
    if (
        not isinstance(description, str)
        or not description.strip()
        or len(description) > 1024
    ):
        issues.append(f"{entry}: description 须为 1 至 1024 个字符的非空字符串")
    allowed_keys = {
        "name",
        "description",
        "license",
        "compatibility",
        "metadata",
        "allowed-tools",
    }
    unknown = set(frontmatter) - allowed_keys
    if unknown:
        issues.append(f"{entry}: 不支持的 frontmatter 字段：{sorted(unknown)}")

    # 必需资料只能指向同一 Skill，单独安装后才不会丢失参考文件。
    for document in sorted(skill.rglob("*.md")):
        issues.extend(check_links(document, skill))
    if isinstance(name, str):
        issues.extend(check_interface(skill, name))
    return issues


def main(argv: Sequence[str] | None = None) -> int:
    """执行只读检查，输出汇总并以退出码区分成功和失败。

    Args:
        argv: 可选命令行参数；None 表示读取实际进程参数。

    Returns:
        所有检查通过时为 0，发现入口、引用或目录问题时为 1。
    """
    parser = argparse.ArgumentParser(description="检查 Skills 结构、元数据和本地引用。")
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    root = parser.parse_args(argv).root.resolve()
    if not root.is_dir():
        print(f"校验失败：目录不存在：{root}")
        return 1

    # 保持一层目录布局，不扫描依赖、试装副本或本机工具缓存。
    skills = sorted(
        child
        for child in root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    )
    issues: list[str] = []
    if not skills:
        issues.append("没有找到包含 SKILL.md 的 Skill 目录")
    if (root / "SKILL.md").exists():
        issues.append("根目录不放置 SKILL.md，避免常规发现过程遗漏独立目录")
    for skill in skills:
        issues.extend(check_skill(skill))

    # README 既是目录入口也是安装说明，必须覆盖当前所有可安装 Skill。
    readme = root / "README.md"
    if not readme.is_file():
        issues.append("缺少 README.md")
    else:
        issues.extend(check_links(readme, root))
        try:
            linked = set(local_link_paths(readme.read_text(encoding="utf-8")))
            for skill in skills:
                if f"{skill.name}/SKILL.md" not in linked:
                    issues.append(f"README.md 未链接到 {skill.name}/SKILL.md")
        except (OSError, UnicodeError):
            # 链接检查已报告读取失败，避免重复输出同一问题。
            pass

    if issues:
        for issue in issues:
            print(f"失败：{issue}")
        print(f"校验失败：{len(issues)} 个问题，检查 {len(skills)} 个 Skill。")
        return 1
    print(
        f"校验通过：{len(skills)} 个 Skill，入口、展示元数据、自包含引用和 README 目录均有效。"
    )
    return 0


if __name__ == "__main__":
    # 命令行统一输出 UTF-8，避免 Windows 默认编码导致中文校验结果乱码。
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
