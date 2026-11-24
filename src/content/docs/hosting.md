---
title: Source repositories on GitHub
section: sources
order: 110
summary: The GitHub practice for the source repositories of the collection.
introduction: The sources of the collection are on GitHub, in the fontgarden organization and in the accounts of the maintainers. The build, the checks, the training and the grades all operate on a repository. The other chapters of the guide assume the practice of this chapter.
background: [tools]
next: [sources]
---

## Purpose of a repository

A set of masters changes for years. Version control records each change. It makes it possible for more than one person to work on the same sources. It also gives the tools a stable address for the files. The build, the checks and the corpus builder read a Git repository at a named revision.

The history is also data. The difference between a purple draft and the green outline of the designer is the record of a correction. Thus, commit a draft before the designer grades it. See [Proposals and grading](/docs/proposals/).

## Branches and pull requests

- Do the work on a branch. Keep `main` in a condition that builds.
- Open a pull request for each change that needs a review. The automatic checks run on pull requests.
- Merge only when the build and the checks pass. As an alternative, document each failure and get agreement on it.

## Commits

Write a commit message that states the change and its reason. `Widen the counter of O to 520` is a useful message. `fixes` is not. Commit source changes and generated files in different commits. Commit the drafts of a machine and the corrections of a person in different commits.

## Generated files

The build generates the compiled fonts, the proofs and the reports from the sources. A repository can hold these files so that users can download them. Do not edit a generated file. The next build removes each edit.

## Reference fonts

Fonts for comparison go into the `reference-fonts` directory at the root of the repository. Add that directory to `.gitignore` before you put a licensed font there. Runebender reads the reference fonts from the nearest Git root, and it selects the nearest weight.

## Releases

Tag a revision of the sources when a model trains on it or when a font release uses it. The tag name is the version number of the source, for example `v1.002`. The corpus manifest and the model card give the tag.
