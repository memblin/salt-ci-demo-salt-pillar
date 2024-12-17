# Demo salt pillar content

This repository contains a set of data, workflows and scripts written to
demonstrate various things that can be done in a Salt managed infrastructure.

## Contents

### GPG

The [gpg](gpg) directory contains ascii armored and encrypted where appropriate GPG key content for use with this pillar data.

### Pillar

The [pillar](pillar) directory is a pillar tree that can be used by a Salt controller.

### Scripts

Scripts called by workflows, pre-commit, or used as utility helpers for other repository needs are in the [scripts](scripts) directory.

- [scripts/salt-ci-pillar-validation.py](scripts/salt-ci-pillar-validation.py):
  - Imports Actions Variables and Secrets into ENV Vars for use in the python script.
  - Calls the `/login` salt-api endpoint to establish a session
  - Runs a `citools.validate_pr` with PR appropriate parameters
  - Consolidates the returned data into something more useable
  - Outputs for GitHub Actions consumption 

### Workflows

- Salt CI Pillar Validation via [.github/workflows/salt_pillar_validation.yml](.github/workflows/salt_pillar_validation.yml)
  - This workflow compares the currently live/target salt pillar content with the rendered content from the incoming PR branch. Pillar differences are reported as `Pillar trees added`, `Pillar trees removed`, `Pillar trees modified` for each affected minion.
  - Checkout the repo because we need access to `scripts` for the workflow
  - Run the `salt-ci-pillar-validation.py` validation script
  - Write the status and the validation summary to the PR comments
