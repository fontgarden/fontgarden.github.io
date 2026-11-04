---
title: Publishing a family on font.garden
section: catalog
label: team
order: 510
summary: The steps from a finished repository to a listing in the catalog.
callout: The catalog lists families that meet the requirements in this guide. This chapter is the checklist a publisher works through. The process is manual while the catalog is small.
background: [upstream, grades, qa]
---

## Requirements

Before a family is considered:

- The repository is public and follows [Source repository structure](/docs/upstream/).
- `OFL.txt`, `AUTHORS.txt` and `CONTRIBUTORS.txt` are present and correct.
- The README has a specimen image and working build instructions.
- `make build` succeeds from a fresh clone.
- `make qa-full` passes.
- `make lint-grid` passes on the source masters.
- No glyph in the declared character set is orange or red.
- A release is tagged and the compiled fonts are attached to it.

## Steps

1. Open an issue in the family's repository titled `Catalog: <Family>` with links to the tagged release, the proof PDF and the scoreboard.
2. A publisher clones the repository at the tag and repeats the build and the checks.
3. The publisher reviews the proof for shape and spacing problems that the checks do not detect.
4. If the family passes, the publisher adds it to the catalog and to the corpus manifest.
5. The issue is closed with a link to the listing.

## Updates

A new version follows the same steps. The version number in the designspace and in `fontinfo.plist` increases. The catalog serves the latest tagged release.

## Removal

An author can ask for a family to be removed from the catalog. Copies already distributed under the OFL remain valid, and samples already in a published corpus remain in it. See [Open fonts and open weights](/docs/culture/).
