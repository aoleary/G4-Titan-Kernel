#!/usr/bin/env python3

from pathlib import Path

path = Path("cpufreq_schedutil.c")
src = path.read_text()

needle = "if (target_freq == sg_policy->cached_raw_freq &&"

insert = """
/*
 * Avoid unnecessary transitions between adjacent operating points.
 * Ignore frequency changes smaller than 5 percent.
 */
if (prev_target_freq &&
    abs((int)target_freq - (int)prev_target_freq) <
    prev_target_freq / 20)
    target_freq = prev_target_freq;

"""

if needle not in src:
    raise SystemExit("Patch 01: insertion point not found")

if "Ignore frequency changes smaller than 5 percent" in src:
    raise SystemExit("Patch 01 already applied")

src = src.replace(needle, insert + needle, 1)

path.write_text(src)

print("Patch 01 applied successfully")
