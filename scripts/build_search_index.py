#!/usr/bin/env python3
"""Regenerates docs/search-index.json from the repo's resource pack folders.

Run this whenever a pack or guide document is added/removed/renamed:

    python3 scripts/build_search_index.py
"""
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(REPO_ROOT, "docs", "search-index.json")

EXCLUDE_DIRS = {".git", "assets", "docs", "Monthly Newsletter", "Reference", "scripts"}

# Short description shown under each result; mirrors the root README table.
PACK_DESCRIPTIONS = {
    "AI - Center of Excellence": "Establish an AICOE — charter, governance, Copilot adoption playbook, and leadership deck",
    "Getting Started with GitHub": "Plans, licensing, instance types, admin setup, and launching a trial",
    "GitHub Actions and CICD": "Workflows, runners, starter templates, migration from other CI tools",
    "GitHub Copilot Adoption": "Business case, rollout strategy, prompt engineering, measuring ROI",
    "Security and Compliance": "GHAS rollout, supply chain security, compliance frameworks, incident response",
    "InnerSource Playbook": "Cross-team collaboration, contribution guidelines, governance, metrics",
    "Migration and Onboarding": "Migrate from Azure DevOps, GitLab, Bitbucket, SVN + developer onboarding",
    "Platform Engineering": "Template repos, rulesets, GitHub Apps, internal developer portals",
    "AI Models in GitHub Copilot": "Model catalog, comparison, pricing, Auto selection, admin policies",
    "Executive and Leadership": "TCO analysis, ROI frameworks, competitive positioning, exec presentation templates",
    "App Modernization": "Legacy codebase modernization with Copilot — architecture analysis, phased migration, CI/CD",
    "Usage-Based Billing and Cost Governance": "Metered billing model, token budgets, cost allocation, spending limits, FinOps reporting",
    "Agentic Workflows and AI Agents": "Copilot Coding Agent, MCP registry setup, agent guardrails, use cases, custom agents",
    "Enterprise Identity and Access Management": "SSO/OIDC, Entra ID + SCIM, PAT hardening, fine-grained permissions, zero trust",
    "Leveling Up": "Certifications, courses, agentic AI skills, and classroom resources",
}

GUIDE_FILENAME_RE = re.compile(r"^\d\d-.*\.md$")


def guide_title(path):
    with open(path, encoding="utf-8") as f:
        first_line = f.readline().strip()
    return re.sub(r"^#+\s*(\d+\s*-\s*)?", "", first_line).strip()


def build_index():
    items = []
    for pack in sorted(os.listdir(REPO_ROOT)):
        full = os.path.join(REPO_ROOT, pack)
        if not os.path.isdir(full) or pack in EXCLUDE_DIRS or pack.startswith("."):
            continue
        readme = os.path.join(full, "README.md")
        if not os.path.exists(readme):
            continue

        description = PACK_DESCRIPTIONS.get(pack, "")
        items.append({
            "title": pack,
            "type": "pack",
            "description": description,
            "path": f"{pack}/README.md",
        })

        for filename in sorted(os.listdir(full)):
            if GUIDE_FILENAME_RE.match(filename):
                items.append({
                    "title": guide_title(os.path.join(full, filename)),
                    "type": "guide",
                    "pack": pack,
                    "description": description,
                    "path": f"{pack}/{filename}",
                })
    return items


if __name__ == "__main__":
    index = build_index()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
    print(f"Wrote {len(index)} items to {OUTPUT_PATH}")
