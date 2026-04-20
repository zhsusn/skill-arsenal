#!/usr/bin/env python3
"""跨平台 Skill 格式转换工具。

支持将标准 SKILL.md 转换为：
- Cursor .mdc 规则文件
- Aider CONVENTIONS.md 格式
- VS Code Snippets（JSON）

Usage:
    python3 convert.py --tool cursor --input skills/development/code-review --output .cursor/rules
    python3 convert.py --tool cursor --all --output .cursor/rules
    python3 convert.py --tool aider --all --output .
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """解析 YAML frontmatter，支持单层 metadata 嵌套，返回 (字段字典, 正文内容)。"""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}, content

    fm_text = match.group(1)
    body = content[match.end() :]

    fields = {}
    lines = fm_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        if key == "metadata" and not value:
            metadata = {}
            i += 1
            while i < len(lines):
                subline = lines[i]
                if not subline.startswith(" ") and not subline.startswith("\t"):
                    break
                subline_stripped = subline.lstrip()
                if subline_stripped.startswith("#") or ":" not in subline_stripped:
                    i += 1
                    continue
                k, _, v = subline_stripped.partition(":")
                metadata[k.strip()] = v.strip().strip('"').strip("'")
                i += 1
            fields["metadata"] = metadata
        else:
            fields[key] = value
            i += 1

    return fields, body


def convert_to_cursor(skill_path: Path, output_dir: Path, quiet: bool = False):
    """转换为 Cursor .mdc 格式。"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False

    content = skill_md.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(content)

    description = fields.get("description", f"Rule for {skill_path.name}")
    name = fields.get("name", skill_path.name)

    # .mdc frontmatter
    mdc_content = f"""---
description: {description}
globs: 
alwaysApply: false
---

# {name.replace("-", " ").title()}

{body}
"""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{name}.mdc"
    output_file.write_text(mdc_content, encoding="utf-8")

    if not quiet:
        print(f"  Generated: {output_file}")
    return True


def convert_to_aider(skill_path: Path, output_dir: Path, quiet: bool = False):
    """转换为 Aider CONVENTIONS.md 片段。"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False

    content = skill_md.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(content)

    name = fields.get("name", skill_path.name)
    description = fields.get("description", "")

    section = f"""## {name.replace("-", " ").title()}

> {description}

{body}

---

"""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "CONVENTIONS.md"

    # 追加模式
    if output_file.exists():
        existing = output_file.read_text(encoding="utf-8")
        if name in existing:
            if not quiet:
                print(f"  Skipped (exists): {output_file}#{name}")
            return True
        section = existing + "\n" + section

    output_file.write_text(section, encoding="utf-8")
    if not quiet:
        print(f"  Updated: {output_file}")
    return True


def convert_to_vscode(skill_path: Path, output_dir: Path, quiet: bool = False):
    """转换为 VS Code Snippets JSON。"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False

    content = skill_md.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(content)

    name = fields.get("name", skill_path.name)
    description = fields.get("description", "")

    # 将 body 转义为 snippet 字符串
    lines = body.strip().splitlines()
    snippet_body = lines if lines else [""]

    snippet = {
        name: {
            "prefix": name,
            "description": description,
            "body": snippet_body,
        }
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{name}.code-snippets"
    output_file.write_text(json.dumps(snippet, indent=2, ensure_ascii=False), encoding="utf-8")

    if not quiet:
        print(f"  Generated: {output_file}")
    return True


CONVERTERS = {
    "cursor": convert_to_cursor,
    "aider": convert_to_aider,
    "vscode": convert_to_vscode,
}


def main():
    parser = argparse.ArgumentParser(description="Convert skills to other tool formats")
    parser.add_argument("--tool", required=True, choices=list(CONVERTERS.keys()), help="Target tool format")
    parser.add_argument("--input", help="Specific skill directory to convert")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--all", action="store_true", help="Convert all skills")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")
    args = parser.parse_args()

    converter = CONVERTERS[args.tool]
    output_dir = Path(args.output)

    count = 0

    if args.all:
        if not SKILLS_DIR.exists():
            print(f"Skills directory not found: {SKILLS_DIR}", file=sys.stderr)
            return 1

        for category_dir in sorted(SKILLS_DIR.iterdir()):
            if not category_dir.is_dir():
                continue
            for skill_dir in sorted(category_dir.iterdir()):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    if converter(skill_dir, output_dir, quiet=args.quiet):
                        count += 1
    else:
        if not args.input:
            print("Error: specify --input or --all", file=sys.stderr)
            return 1

        skill_path = PROJECT_ROOT / args.input
        if not skill_path.exists():
            print(f"Input path not found: {skill_path}", file=sys.stderr)
            return 1

        if converter(skill_path, output_dir, quiet=args.quiet):
            count = 1

    print(f"\nDone. {count} skill(s) converted to {args.tool} format.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
