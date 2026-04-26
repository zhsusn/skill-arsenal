#!/usr/bin/env python3
"""SKILL.md 格式合规性校验工具。

Usage:
    python3 validate.py
    python3 validate.py --skill skills/development/code-review
    python3 validate.py --index
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
INDEX_FILE = PROJECT_ROOT / "index.json"

# 正则表达式：提取 YAML frontmatter
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# 合法的分类目录
VALID_CATEGORIES = {
    "core-deliverables",
    "development",
    "data-engineering",
    "architecture",
    "Reverse-Engineering",
    "writing",
    "analysis",
    "tools",
}

# kebab-case 校验（同时禁止连续连字符）
KEBAB_CASE_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def parse_frontmatter(fm: str) -> dict:
    """解析 YAML frontmatter，支持单层 metadata 嵌套。"""
    fields = {}
    lines = fm.splitlines()
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
    return fields


class Validator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checked = 0

    def error(self, path: str, msg: str):
        self.errors.append(f"[ERROR] {path}: {msg}")

    def warn(self, path: str, msg: str):
        self.warnings.append(f"[WARN]  {path}: {msg}")

    def validate_skill(self, skill_path: Path) -> bool:
        """校验单个 skill 目录。"""
        self.checked += 1
        rel_path = skill_path.relative_to(PROJECT_ROOT)
        ok = True

        # 1. 目录名 kebab-case
        name = skill_path.name
        if not KEBAB_CASE_RE.match(name):
            self.error(str(rel_path), f"directory name '{name}' must be kebab-case without consecutive hyphens")
            ok = False

        # 2. 必须存在 SKILL.md
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            self.error(str(rel_path), "missing required file SKILL.md")
            return False

        # 3. SKILL.md 内容校验
        content = skill_md.read_text(encoding="utf-8")
        lines = content.splitlines()

        # 3.1 行数检查
        if len(lines) > 500:
            self.warn(str(rel_path / "SKILL.md"), f"exceeds 500 lines ({len(lines)})")

        # 3.2 Frontmatter 检查
        match = FRONTMATTER_RE.match(content)
        if not match:
            self.error(str(rel_path / "SKILL.md"), "missing YAML frontmatter")
            ok = False
        else:
            frontmatter = match.group(1)
            fm_ok = self._validate_frontmatter(rel_path / "SKILL.md", frontmatter, name)
            ok = ok and fm_ok

        # 3.3 文件引用深度检查（正文部分）
        body = content[match.end():] if match else content
        self._check_file_references(rel_path / "SKILL.md", body)

        # 4. 分类目录校验
        category = skill_path.parent.name
        if category not in VALID_CATEGORIES:
            self.error(str(rel_path), f"unknown category '{category}'")
            ok = False

        # 5. references/ 推荐文件检查
        refs_dir = skill_path / "references"
        if refs_dir.exists() and refs_dir.is_dir():
            has_standard_ref = any(
                (refs_dir / f).exists() for f in ("REFERENCE.md", "FORMS.md")
            )
            if not has_standard_ref:
                self.warn(
                    str(rel_path / "references"),
                    "no REFERENCE.md or FORMS.md found (recommended by spec)",
                )

        # 6. meta.json 校验（如果存在）
        meta_file = skill_path / "meta.json"
        if meta_file.exists():
            self._validate_meta_json(rel_path / "meta.json", meta_file)

        return ok

    def _validate_frontmatter(self, path: Path, fm: str, expected_name: str) -> bool:
        ok = True
        fields = parse_frontmatter(fm)

        # name (required)
        if "name" not in fields:
            self.error(str(path), "frontmatter missing required field 'name'")
            ok = False
        else:
            name = fields["name"]
            if len(name) < 1 or len(name) > 64:
                self.error(str(path), f"name '{name}' length must be 1-64 characters")
                ok = False
            if not KEBAB_CASE_RE.match(name):
                self.error(str(path), f"name '{name}' must be lowercase kebab-case without consecutive hyphens")
                ok = False
            if name != expected_name:
                self.warn(
                    str(path),
                    f"name '{name}' does not match directory '{expected_name}'",
                )

        # description (required)
        if "description" not in fields:
            self.error(str(path), "frontmatter missing required field 'description'")
            ok = False
        else:
            desc = fields["description"]
            if not desc:
                self.error(str(path), "description must not be empty")
                ok = False
            elif len(desc) > 1024:
                self.error(str(path), f"description exceeds 1024 characters ({len(desc)})")
                ok = False

        # license (optional)
        if "license" in fields:
            if not fields["license"]:
                self.warn(str(path), "license is empty")

        # compatibility (optional)
        if "compatibility" in fields:
            comp = fields["compatibility"]
            if len(comp) > 500:
                self.error(str(path), f"compatibility exceeds 500 characters ({len(comp)})")
                ok = False

        # 检查 Kimi 兼容性：Frontmatter 仅限 name + description
        allowed_fields = {"name", "description"}
        for key in fields:
            if key not in allowed_fields:
                self.warn(
                    str(path),
                    f"extra frontmatter field '{key}' may cause Kimi Code to reject this skill; consider moving it to meta.json",
                )

        return ok

    def _validate_meta_json(self, rel_path: Path, meta_file: Path):
        """校验 meta.json 格式。"""
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            self.error(str(rel_path), f"invalid JSON: {e}")
            return

        if not isinstance(meta, dict):
            self.error(str(rel_path), "meta.json must be a JSON object")
            return

        if "name" in meta:
            if not isinstance(meta["name"], str):
                self.error(str(rel_path), "meta.json 'name' must be a string")

        if "tags" in meta:
            if not isinstance(meta["tags"], list) or not all(isinstance(t, str) for t in meta["tags"]):
                self.error(str(rel_path), "meta.json 'tags' must be an array of strings")

        if "platforms" in meta:
            if not isinstance(meta["platforms"], list) or not all(isinstance(p, str) for p in meta["platforms"]):
                self.error(str(rel_path), "meta.json 'platforms' must be an array of strings")

    def _check_file_references(self, path: Path, body: str):
        """检查文件引用是否保持一级深度。"""
        # 匹配 markdown 链接和直接路径引用
        # 简单检测 ../ 或深层路径如 a/b/c/
        deep_ref_patterns = [
            r"\]\(\.\./",       # markdown 链接中的 ../
            r"\]\([\w-]+/[\w-]+/[\w-]+",  # markdown 链接中深度 >=2
        ]
        for pattern in deep_ref_patterns:
            if re.search(pattern, body):
                self.warn(
                    str(path),
                    "detected potentially deep file references (spec recommends one level deep)",
                )
                break

    def validate_index(self) -> bool:
        """校验 index.json 与目录一致性。"""
        if not INDEX_FILE.exists():
            self.error("index.json", "missing")
            return False

        try:
            index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            self.error("index.json", f"invalid JSON: {e}")
            return False

        skills_in_index = {s["name"]: s for s in index.get("skills", [])}
        skills_on_disk = set()

        for category_dir in SKILLS_DIR.iterdir():
            if not category_dir.is_dir():
                continue
            for skill_dir in category_dir.iterdir():
                if not skill_dir.is_dir():
                    continue
                if not (skill_dir / "SKILL.md").exists():
                    continue
                skills_on_disk.add(skill_dir.name)

        ok = True
        # index 中有但磁盘上没有
        for name in skills_in_index:
            if name not in skills_on_disk:
                self.error("index.json", f"indexed skill '{name}' not found on disk")
                ok = False

        # 磁盘上有但 index 中没有
        for name in skills_on_disk:
            if name not in skills_in_index:
                self.warn("index.json", f"skill '{name}' on disk but not in index")

        return ok

    def report(self):
        print(f"\nChecked {self.checked} skill(s).")
        if self.warnings:
            print(f"\n{'=' * 60}")
            print(f"Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  {w}")

        if self.errors:
            print(f"\n{'=' * 60}")
            print(f"Errors ({len(self.errors)}):")
            for e in self.errors:
                print(f"  {e}")
            print(f"\nValidation FAILED.")
            return 1

        print("\nValidation PASSED.")
        return 0


def main():
    parser = argparse.ArgumentParser(description="Validate SKILL.md format compliance")
    parser.add_argument("--skill", help="Validate a specific skill directory")
    parser.add_argument("--index", action="store_true", help="Validate index.json only")
    args = parser.parse_args()

    validator = Validator()

    if args.index:
        validator.validate_index()
        return validator.report()

    if args.skill:
        skill_path = PROJECT_ROOT / args.skill
        if not skill_path.exists():
            print(f"Skill path not found: {skill_path}", file=sys.stderr)
            return 1
        validator.validate_skill(skill_path)
    else:
        # 扫描所有 skill
        if not SKILLS_DIR.exists():
            print(f"Skills directory not found: {SKILLS_DIR}", file=sys.stderr)
            return 1

        for category_dir in sorted(SKILLS_DIR.iterdir()):
            if not category_dir.is_dir():
                continue
            for skill_dir in sorted(category_dir.iterdir()):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    validator.validate_skill(skill_dir)

        validator.validate_index()

    return validator.report()


if __name__ == "__main__":
    sys.exit(main())
