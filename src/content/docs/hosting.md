---
title: Hosting projects on GitHub
section: introduction
label: learn
order: 40
summary: Basic GitHub practice for font projects.
callout: Font projects are hosted on GitHub. The repository is the unit of work for building, checking, training and publishing. This chapter covers the practices the rest of the guide assumes you know.
background: [tools]
next: [upstream]
---

## Why a repository

A font family is a set of source files that change over years. Version control records every change, lets several people work on the same family, and gives automated tools a stable address for the files. The Font Garden build, check and corpus tools all read from a Git repository.

## Public or private

A repository can be private while the family is in progress. It must be public before the family enters the catalog. See [Open fonts and open weights](/docs/culture/).

## Branches and pull requests

- Work on a branch. Keep `main` in a state that builds.
- Open a pull request for any change you want reviewed. The automated checks run on pull requests.
- Merge only when the build and the checks pass, or when the failures are documented and accepted.

## Commits

Write commit messages that state what changed and why. A message like `Widen the counter of O to 520` is useful. A message like `fixes` is not. Commit source changes separately from generated files.

## Generated files

Compiled fonts, proofs and reports are generated from the sources. They can be committed so that users can download them, but they must never be edited by hand. A change to a compiled font that is not reproduced by a build will be lost at the next build.

## Releases

Tag a release in GitHub when a version of the family is ready for the catalog. The tag name is the version number from the source, for example `v1.002`. Attach the compiled fonts to the release.
