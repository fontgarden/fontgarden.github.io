---
title: Hosting sources on GitHub
section: sources
label: learn
order: 110
summary: Basic GitHub practice for the collection's source repositories.
callout: The sources of the collection are hosted on GitHub under the fontgarden organization and the maintainers' accounts. The repository is the unit of work for building, checking, training and grading. This chapter covers the practices the rest of the guide assumes you know.
background: [tools]
next: [sources]
---

## Why a repository

A set of masters changes over years. Version control records every change, lets several people work on the same sources, and gives the tools a stable address for the files. The build, the checks and the corpus builder all read from a Git repository at a named revision.

The history is also data. The difference between a purple draft and the green outline that the designer kept is the record of a correction. For this reason drafts are committed before they are graded. See [Proposals and grading](/docs/proposals/).

## Branches and pull requests

- Work on a branch. Keep `main` in a state that builds.
- Open a pull request for any change you want reviewed. The automated checks run on pull requests.
- Merge only when the build and the checks pass, or when the failures are documented and accepted.

## Commits

Write commit messages that state what changed and why. `Widen the counter of O to 520` is useful. `fixes` is not. Commit source changes separately from generated files. Commit machine drafts separately from human corrections.

## Generated files

Compiled fonts, proofs and reports are generated from the sources. They can be committed so that users can download them, but they are never edited by hand. A change to a compiled font that is not reproduced by a build is lost at the next build.

## Reference fonts

Fonts used for comparison go in a `reference-fonts` directory at the repository root, and that directory is listed in `.gitignore` before any licensed font is put there. Runebender reads reference fonts from the nearest Git root and picks the nearest weight.

## Releases

Tag a release when a revision of the sources is used for a model training run or a font release. The tag name is the version number from the source, for example `v1.002`. The corpus manifest and the model card cite the tag.
