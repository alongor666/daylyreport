#!/usr/bin/env python3
"""
Compare the business agent column from the raw CSV with the master mapping JSON.

The script enforces the \"员工号+姓名\" primary key, checks status coverage, and
prints actionable discrepancies so data stewards can fix them before a release.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Mapping, Tuple

KEY_PATTERN = re.compile(r"^\d{6,}\S+$")  # 至少6位员工号 + 姓名
VALID_STATUS = {"在岗", "历史", "待入职"}
STATUS_ALIASES = {"active": "在岗", "history": "历史", "pending": "待入职"}


def load_csv_agents(
    csv_path: Path, agent_field: str, org_field: str
) -> Tuple[set[str], Mapping[str, Counter]]:
    agents: set[str] = set()
    org_counter: Dict[str, Counter] = defaultdict(Counter)

    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if agent_field not in reader.fieldnames:
            raise SystemExit(f"CSV缺少字段：{agent_field}")
        if org_field and org_field not in reader.fieldnames:
            raise SystemExit(f"CSV缺少字段：{org_field}")

        for row in reader:
            agent = (row.get(agent_field) or "").strip()
            if not agent:
                continue
            agents.add(agent)
            if org_field:
                org_value = (row.get(org_field) or "未填").strip() or "未填"
                org_counter[agent][org_value] += 1

    return agents, org_counter


def load_json_master(json_path: Path) -> Dict[str, dict]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("JSON主数据结构必须是对象/dict")
    return data


def summarize_non_hr_agents(
    agents: Iterable[str], org_counter: Mapping[str, Counter]
) -> str:
    lines: list[str] = []
    for agent in sorted(agents):
        counts = org_counter.get(agent)
        if not counts:
            continue
        total = sum(counts.values())
        lines.append(f"- {agent}（共 {total} 条）")
        for org, value in counts.most_common():
            lines.append(f"    • {org}: {value}")
    return "\n".join(lines) if lines else ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验业务员主数据与事实表的一致性"
    )
    parser.add_argument(
        "--csv",
        default="车险清单_2025年10-11月_合并.csv",
        type=Path,
        help="含有业务员字段的CSV路径",
    )
    parser.add_argument(
        "--json",
        default="业务员机构团队归属.json",
        type=Path,
        help="业务员主数据JSON路径",
    )
    parser.add_argument(
        "--agent-field", default="业务员", help="CSV内业务员字段名"
    )
    parser.add_argument(
        "--org-field", default="三级机构", help="CSV内机构字段名"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="发现异常时返回非零退出码，便于CI使用",
    )
    args = parser.parse_args()

    csv_agents, org_counter = load_csv_agents(
        args.csv, args.agent_field, args.org_field
    )
    json_master = load_json_master(args.json)
    json_agents = set(json_master.keys())

    invalid_keys = [k for k in json_agents if not KEY_PATTERN.match(k)]
    missing_status: list[str] = []
    invalid_status: list[Tuple[str, str | None]] = []
    status_lookup: Dict[str, str] = {}

    for key, meta in json_master.items():
        raw_status = meta.get("status")
        if raw_status is None:
            missing_status.append(key)
            continue
        normalized = STATUS_ALIASES.get(raw_status, raw_status)
        if normalized not in VALID_STATUS:
            invalid_status.append((key, raw_status))
            status_lookup[key] = raw_status or "unknown"
        else:
            status_lookup[key] = normalized

    csv_only = sorted(csv_agents - json_agents)
    json_only = sorted(json_agents - csv_agents)

    json_only_by_status: Dict[str, list[str]] = defaultdict(list)
    for key in json_only:
        status = status_lookup.get(key, "unknown")
        json_only_by_status[status].append(key)

    non_hr_accounts = sorted(
        agent for agent in csv_agents if not KEY_PATTERN.match(agent)
    )

    print("=== 业务员主数据校验报告 ===")
    print(
        f"- CSV唯一业务员：{len(csv_agents)}\n"
        f"- JSON主数据：{len(json_agents)}\n"
        f"- CSV仅存在：{len(csv_only)}\n"
        f"- JSON仅存在：{len(json_only)}"
    )

    if invalid_keys:
        print("\n⚠️ 非规范主键（缺少“员工号+姓名”）:")
        for key in invalid_keys:
            status = json_master[key].get("status", "unknown")
            print(f"  - {key}（status={status}）")

    if missing_status:
        print("\n⚠️ 缺少status字段的记录:")
        for key in missing_status:
            print(f"  - {key}")

    if invalid_status:
        print("\n⚠️ status取值不合法（必须为“在岗/历史/待入职”）:")
        for key, value in invalid_status:
            print(f"  - {key}: {value or '未填写'}")

    if csv_only:
        print("\n❌ CSV存在但JSON缺失，需补齐归属信息:")
        for key in csv_only:
            print(f"  - {key}")

    if json_only:
        print("\nℹ️ JSON存在但CSV缺失（应该标记历史/待入职）:")
        for status, items in sorted(json_only_by_status.items()):
            print(f"  · status={status}: {len(items)}")
            for key in items:
                print(f"      - {key}")

    if non_hr_accounts:
        print("\n🔍 非人力账号/缺少工号的CSV记录（含三级机构分布）:")
        summary = summarize_non_hr_agents(non_hr_accounts, org_counter)
        print(summary or "  - 未找到关联数据")

    issues = any(
        [
            invalid_keys,
            missing_status,
            invalid_status,
            csv_only,
            json_only,
            non_hr_accounts,
        ]
    )

    if args.strict and issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
