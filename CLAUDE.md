# Working on the ThreeFold Manual

Notes for anyone (human or agent) picking this repo up. Written after a session
that fixed ~300 broken links, rewrote the disk-wipe guide, and added the first
pre-merge CI this repo ever had. The point is that you don't rediscover any of
it the hard way.

## What this repo is

A Docusaurus 3.7 site published at <https://manual.grid.tf>. Four doc trees,
each a separate plugin instance with its own `routeBasePath`:

| tree | path | URL prefix | pages |
| --- | --- | --- | --- |
| labs | `labs/docs/` | `/labs/` | 425 |
| users | `users/docs/` | `/users/` | 13 |
| farmers | `farmers/docs/` | `/farmers/` | 10 |
| (default) | `docs/` | `/docs/` | 1 |

**They are separate plugin instances.** A relative link cannot cross from
`farmers/` to `labs/` — use an absolute path like
`/labs/documentation/farmers/farming_troubleshooting/farming_troubleshooting_tips`.

## Git and tooling

- Default branch is `development`. Work goes to `development`, then a
  `development` → `master` PR syncs it. Pushing to `master` triggers the live
  deploy; pushing to `development` deploys `manual.dev.grid.tf`.
- Use plain `git` and `gh`. This repo is on **github.com**. The `lab` CLI in
  the global instructions is a **Forgejo** toolkit (`forge.ourworld.tf`) and
  does not apply here.
- **`yarn` is not installed and `yarn.lock` is gitignored, but
  `package-lock.json` is committed.** Use npm, not the Makefile's `yarn`
  targets: `npm install`, then `npm start` (dev server on :3000) or
  `npm run build`.
- `npm start` / `npm run build` skip the Makefile's `prepare-data` step, which
  fetches live TFT pricing. Fine for editing content; you only need
  `make prebuild` if you're touching the generated pricing values.
- The dev server renders client-side, so `curl` gets an empty shell. To check
  rendered output, either read `build/**/index.html` after a build, or drive a
  real browser.

## CI — what runs, and what it will not let you merge

| workflow | trigger | what it does |
| --- | --- | --- |
| `pr_check.yml` | pull request | **the gate** — builds the site, lints documented shell commands |
| `manual_update_development.yml` | push to `development` | deploys `manual.dev.grid.tf` |
| `manual_update_master.yml` | push to `master` | deploys `manual.grid.tf` |
| `manual_weekly_link_check.yml` | Friday 06:00 UTC + manual | external link rot → opens a tracking issue |

`onBrokenLinks` and `onBrokenAnchors` are **`throw`**. A broken internal link
or a broken `#anchor` fails the build, so it fails the PR. Keep it that way —
the whole 100+ dead-link mess happened while these were `warn`.

External links are deliberately **not** checked on PRs or deploys. Third-party
URLs rot on their own schedule with no change here, and gating on them just
trains everyone to ignore a red X. The weekly job files an issue instead.

`manual_update_development_split.yml` is dormant (its branch doesn't exist) and
still carries the old pre-deploy link-check pattern. Don't copy it.

## `scripts/check_docs_commands.py`

Runs in CI. Two checks, both aimed at "a farmer copies a command and it
doesn't work":

1. **shellcheck** (severity=error) on every shell block.
2. **Twin drift** — command blocks that differ between the `farmers/` and
   `labs/` copies of the five shared build pages.

Run it locally before pushing: `python3 scripts/check_docs_commands.py`.

**Why shellcheck and not `bash -n`:** `bash -n` only checks syntax. The bug
that started all this —

```text
for i in /dev/sd*; do if [ "$i"!= "/dev/sdX"* ]; then wipefs -af $i; fi; done
```

— is syntactically **valid**. It fails at runtime (`unary operator expected`),
so it silently wiped nothing and farmers got un-bootable nodes. `bash -n`
passes it; shellcheck catches it (`SC1108`).

It checks **untagged** ``` blocks too, not just ` ```bash `. Most of the
manual's commands are untagged and that broken loop lived in one.

## Conventions the checker respects — follow them

- **`<placeholder>`** for values the reader substitutes. Consistent across the
  manual; the checker normalises it before linting.
- **Command output is not a command.** Tag pasted `--help` text, JSON
  responses, terminal transcripts and file paths as ` ```text ` or
  ` ```console `, never ` ```bash `. Mislabelling them is what produces
  spurious CI failures.
- **Never put prose inside a command.** `dd if=FILE.ISO(or .IMG)` and
  `chmod 777 /path (optional)` are shell syntax errors. Put the note in the
  surrounding text or use a `#` comment.
- **Don't end a block on a trailing `\`.** A copied command then hangs waiting
  for a continuation line.

## Traps that have actually bitten

**`farmers/` and `labs/` share five build pages.**
`2_bootstrap_image`, `3_set_hardware`, `4_wipe_all_disks`, `5_set_bios_uefi`,
`6_boot_3node`. They are *not* duplicates to be merged — the farmers versions
are deliberate condensations for a different reader (22 lines vs 166). But the
**commands in them must stay identical**, and a fix applied to one tree and not
the other is the single most repeated mistake here. It's how a V3 bootstrap
page ended up illustrated with V4 screenshots. The drift check now catches it.

**GitHub does not redirect `/issues/N` after a repo rename.** Repo roots and
`/tree/…` paths 301 correctly, so links *look* fine, but issue deep-links hard
404. ~40 ThreeFold repos were renamed (`tfchain` → `ledger_chain`,
`tfgrid-sdk-go` → `zos_sdk_go`, `tfgrid-sdk-ts` → `zos_sdk_ts`,
`pulumi-threefold` → `grid_pulumi`, `home` → `grid_wiki`, `info_grid` → this
repo), several moving to the `threefoldtecharchive` org. Verify a repo's real
name with `gh api repos/threefoldtech/<name> -q .full_name`, which follows
renames.

**`github.io` URLs need the same treatment** and are easy to miss — a
find-and-replace over `github.com/…` will not touch
`threefoldtech.github.io/<repo>/…`.

**The external link checker only crawls ~93 pages.** Passing it is a floor,
not proof the manual is link-clean. To actually sweep, extract every URL from
the markdown and check them directly.

**Docusaurus slug rules that cause "broken" links that look correct:**
- Numeric filename prefixes are stripped — `4_wipe_all_disks.md` serves at
  `…/wipe_all_disks`.
- A file named after its parent folder becomes the **folder index** —
  `documentation/threefold_token/threefold_token.md` serves at
  `/labs/documentation/threefold_token/`, *not* `…/threefold_token/threefold_token`.

**Duplicate `sidebar_position` values** in one folder make ordering arbitrary.
Check before adding a page.

## Recent work (July 2026)

PRs #853–#867. Merged the seven open doc PRs and closed all eight issues, then
fixed what that surfaced: ~300 dead links from the repo renames; a
`manual_update_master.yml` fix that lived only on `master` and would have been
reverted by the next sync; a `manual_weekly_link_check.yml` that had **never
run** because three step `id`s contained spaces (invalid workflow → a failed
run spawned on every push); the disk-wipe guide rewrite; and the CI above.

Full detail is in the PR descriptions — they were written to be read later.
