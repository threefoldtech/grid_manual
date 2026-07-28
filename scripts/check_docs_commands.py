#!/usr/bin/env python3
"""Validate the shell commands printed in the manual.

Two checks, both aimed at the same failure: a farmer copies a command out of
the manual and it does not work.

  1. SHELL -- every shell block is linted with shellcheck (severity=error),
     falling back to `bash -n` when shellcheck is unavailable.

     shellcheck rather than `bash -n` because `bash -n` only checks syntax.
     The disk-wipe loop that silently wiped nothing --

         for i in /dev/sd*; do if [ "$i"!= "/dev/sdX"* ]; then ... ; fi; done

     -- is syntactically VALID; it fails at runtime with "unary operator
     expected". `bash -n` passes it. shellcheck catches it (SC1108, "you need
     a space before and after the =").

     This covers ```bash / ```sh blocks AND untagged ``` blocks whose first
     line looks like a command. Untagged blocks matter: most of the manual's
     commands are untagged, and that wipe loop lived in one.

     The manual's own conventions are respected, not fought:
       - `<placeholder>` is normalised before linting, because angle brackets
         are shell redirection and every page uses them as placeholders.
       - Pasted terminal sessions (first line is a prompt) are skipped, since
         they are output rather than commands. Tag genuine output as ```text
         or ```console rather than ```bash.
       - Blocks containing a heredoc are skipped: the body is data, and
         shellcheck mis-parses it when the block is linted out of context.

  2. TWIN DRIFT -- farmers/ and labs/ deliberately carry two versions of the
     same five build pages, written for different audiences. The prose is
     meant to differ; the commands are not. This flags a command block that
     exists in both but has drifted, which is what happens when a fix lands
     in one tree and is forgotten in the other.

Exits non-zero if either check fails. Run from the repo root.
"""

import difflib
import os
import re
import subprocess
import sys
import tempfile

SKIP_DIRS = ('build', '.docusaurus', 'node_modules', '.git')
SHELL_LANGS = {'bash', 'sh', 'shell', 'zsh'}

# A pasted terminal session: "$ cmd", "# cmd", or "user@host ... $ cmd".
PROMPT = re.compile(r'^\s*(\$\s|#\s|\S+@\S+.*?[#$]\s)')
PLACEHOLDER = re.compile(r'<[A-Za-z0-9_\-. /]+>')
FENCE = re.compile(r'^(\s*)```(\S*)\s*$')

# An untagged block is treated as shell when its first line opens with a
# command. Deliberately conservative: it is better to skip an odd block than
# to fail the build on a config file someone forgot to tag.
SHELLY = re.compile(
    r'^\s*(sudo|apt|apt-get|wget|curl|git|cd|mkdir|echo|export|for |if |while '
    r'|docker|systemctl|chmod|chown|ln |cp |mv |rm |tar|ssh|scp|npm|yarn'
    r'|cargo|pip|make|set |source |\./)\b')

# Pages that exist in both trees. Prose may differ; commands must not.
TWINS = [
    ('farmers/docs/3node_building/{}.md',
     'labs/docs/documentation/farmers/3node_building/{}.md')
]
TWIN_PAGES = ['2_bootstrap_image', '3_set_hardware', '4_wipe_all_disks',
              '5_set_bios_uefi', '6_boot_3node']


def markdown_files():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(('.md', '.mdx')):
                yield os.path.join(root, f).replace('./', '', 1)


def code_blocks(path):
    """Yield (lang, start_line, body) for each fenced block."""
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        lang = m.group(2).lower()
        start = i + 1
        body = []
        i += 1
        while i < len(lines) and not lines[i].strip() == '```' and not FENCE.match(lines[i]):
            body.append(lines[i])
            i += 1
        yield lang, start, '\n'.join(body)
        i += 1


def have_shellcheck():
    try:
        subprocess.run(['shellcheck', '--version'],
                       capture_output=True, check=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def check_syntax():
    failures = []
    checked = 0
    sc = have_shellcheck()
    for path in sorted(markdown_files()):
        for lang, line, body in code_blocks(path):
            if not body.strip():
                continue
            first = next((l for l in body.split('\n') if l.strip()), '')
            if lang in SHELL_LANGS:
                pass
            elif lang == '' and SHELLY.match(first):
                pass  # untagged, but opens with a command
            else:
                continue
            if PROMPT.match(first):
                continue  # pasted session, not a command to run
            if '<<' in body:
                continue  # heredoc body is data, not shell
            checked += 1
            with tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False) as fh:
                fh.write('#!/bin/bash\n' + PLACEHOLDER.sub('PLACEHOLDER', body))
                tmp = fh.name
            try:
                if sc:
                    r = subprocess.run(
                        ['shellcheck', '-s', 'bash', '--severity', 'error',
                         '-f', 'gcc', tmp], capture_output=True, text=True)
                    detail = (r.stdout.strip().split('\n')[0].split(':', 3)[-1].strip()
                              if r.stdout.strip() else r.stderr.strip()[:80])
                else:
                    r = subprocess.run(['bash', '-n', tmp],
                                       capture_output=True, text=True)
                    detail = r.stderr.strip().split('\n')[0].split(': ', 1)[-1]
            finally:
                os.unlink(tmp)
            if r.returncode != 0:
                failures.append((path, line, detail, first.strip()[:60]))
    if not sc:
        print("  note: shellcheck not found, fell back to `bash -n`"
              " (syntax only -- weaker)")
    return checked, failures


def check_twin_drift():
    def shell_bodies(path):
        return [b.strip() for _, _, b in code_blocks(path) if b.strip()]

    drift = []
    shared = 0
    for fa_t, fb_t in TWINS:
        for page in TWIN_PAGES:
            fa, fb = fa_t.format(page), fb_t.format(page)
            if not (os.path.exists(fa) and os.path.exists(fb)):
                continue
            A, B = shell_bodies(fa), shell_bodies(fb)
            for a in A:
                if a in B:
                    shared += 1
                    continue
                best_ratio, best = 0.0, None
                for b in B:
                    r = difflib.SequenceMatcher(None, a, b).ratio()
                    if r > best_ratio:
                        best_ratio, best = r, b
                if best_ratio >= 0.75:
                    drift.append((fa, fb, best_ratio, a, best))
    return shared, drift


def main():
    ok = True

    checked, failures = check_syntax()
    print(f"shell blocks parsed : {checked}")
    if failures:
        ok = False
        print(f"FAILED              : {len(failures)}\n")
        for path, line, detail, first in failures:
            print(f"  {path}:{line}")
            print(f"      {detail}")
            print(f"      block starts: {first}")
        print("\n  If the block is command OUTPUT rather than commands, tag it")
        print("  ```text or ```console instead of ```bash.")
    else:
        print("  all parse cleanly")

    shared, drift = check_twin_drift()
    print(f"\nshared twin blocks  : {shared}")
    if drift:
        ok = False
        print(f"DRIFTED             : {len(drift)}\n")
        for fa, fb, ratio, a, b in drift:
            print(f"  {fa}")
            print(f"  {fb}")
            print(f"      {ratio:.0%} similar but not identical -- fix landed in one tree only?")
            print(f"      farmers: {a.splitlines()[0][:70]}")
            print(f"         labs: {b.splitlines()[0][:70]}")
    else:
        print("  no drift between farmers/ and labs/ command blocks")

    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
