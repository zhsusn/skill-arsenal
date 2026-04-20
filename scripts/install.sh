#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# skill-arsenal 安装脚本
# 支持将 skill 安装到多种 AI 编程助手的本地 skill 目录
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 默认配置
TOOL=""
TARGET=""
SKILL=""
ALL=false
FORCE=false

# 各平台默认全局路径
declare -A GLOBAL_PATHS=(
    [kimi]="${HOME}/.kimi/skills"
    [claude]="${HOME}/.claude/skills"
    [cursor]="${HOME}/.cursor/skills"
    [codex]="${HOME}/.codex/skills"
    [gemini]="${HOME}/.gemini/skills"
    [windsurf]="${HOME}/.windsurf/skills"
)

# 各平台项目级路径
declare -A PROJECT_PATHS=(
    [kimi]=".kimi/skills"
    [claude]=".claude/skills"
    [cursor]=".cursor/skills"
    [codex]=".codex/skills"
    [gemini]=".gemini/skills"
    [windsurf]=".windsurf/skills"
)

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
    --tool <name>       目标平台：kimi, claude, cursor, codex, gemini, windsurf
    --target <path>     安装到指定项目路径（默认安装到全局路径）
    --skill <path>      指定要安装的 skill 目录（相对于项目根目录）
    --all               安装 skills/ 下的所有 skill
    --force             强制覆盖已存在的 skill
    --help              显示此帮助信息

Examples:
    # 安装全部 skill 到 Kimi 全局目录
    $(basename "$0") --tool kimi --all

    # 安装单个 skill 到当前项目
    $(basename "$0") --tool claude --skill skills/development/code-review --target .

    # 安装到 Cursor 项目目录（会自动转换格式）
    $(basename "$0") --tool cursor --all --target .
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --tool)
                TOOL="$2"
                shift 2
                ;;
            --target)
                TARGET="$2"
                shift 2
                ;;
            --skill)
                SKILL="$2"
                shift 2
                ;;
            --all)
                ALL=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1" >&2
                usage
                exit 1
                ;;
        esac
    done
}

validate_args() {
    if [[ -z "${TOOL}" ]]; then
        echo "Error: --tool is required." >&2
        usage
        exit 1
    fi

    if ! [[ -v "GLOBAL_PATHS[${TOOL}]" ]]; then
        echo "Error: unsupported tool '${TOOL}'. Supported: ${!GLOBAL_PATHS[*]}" >&2
        exit 1
    fi

    if [[ "${ALL}" == false && -z "${SKILL}" ]]; then
        echo "Error: specify --skill or --all." >&2
        usage
        exit 1
    fi
}

resolve_dest_dir() {
    local dest=""
    if [[ -n "${TARGET}" ]]; then
        # 项目级安装
        if [[ -v "PROJECT_PATHS[${TOOL}]" ]]; then
            dest="${TARGET}/${PROJECT_PATHS[${TOOL}]}"
        else
            dest="${TARGET}/.skills"
        fi
    else
        # 全局安装
        dest="${GLOBAL_PATHS[${TOOL}]}"
    fi
    echo "${dest}"
}

install_skill() {
    local src="$1"
    local dest="$2"
    local skill_name
    skill_name="$(basename "${src}")"

    local target_path="${dest}/${skill_name}"

    if [[ -d "${target_path}" && "${FORCE}" == false ]]; then
        echo "  ⚠️  Skipped (already exists): ${skill_name}"
        return 0
    fi

    mkdir -p "${dest}"

    if [[ "${TOOL}" == "cursor" ]]; then
        # Cursor 需要转换为 .mdc 格式
        python3 "${SCRIPT_DIR}/convert.py" --tool cursor --input "${src}" --output "${target_path}" --quiet
    else
        cp -r "${src}" "${target_path}"
    fi

    echo "  ✅ Installed: ${skill_name} -> ${target_path}"
}

main() {
    parse_args "$@"
    validate_args

    local dest_dir
    dest_dir="$(resolve_dest_dir)"

    echo "Installing skills for tool: ${TOOL}"
    echo "Destination: ${dest_dir}"
    echo ""

    local count=0

    if [[ "${ALL}" == true ]]; then
        for category_dir in "${PROJECT_ROOT}"/skills/*/; do
            [[ -d "${category_dir}" ]] || continue
            for skill_dir in "${category_dir}"*/; do
                [[ -d "${skill_dir}" ]] || continue
                install_skill "${skill_dir}" "${dest_dir}"
                ((count++)) || true
            done
        done
    else
        local src_path="${PROJECT_ROOT}/${SKILL}"
        if [[ ! -d "${src_path}" ]]; then
            echo "Error: skill directory not found: ${src_path}" >&2
            exit 1
        fi
        install_skill "${src_path}" "${dest_dir}"
        count=1
    fi

    echo ""
    echo "Done. ${count} skill(s) processed."
}

main "$@"
