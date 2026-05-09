# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`notion-twitter-auto-post` is an early-stage project. As of the initial commit, no application code, dependencies, or tooling have been added yet. This file should be updated as the project takes shape.

## Current State

- `README.md` exists but is empty.
- No language runtime, package manager, or build system has been chosen yet.
- No tests, linter, or CI configuration exists.

## Next Steps for Setup

When the project is initialized, update this file to include:

1. **Build / run commands** — how to install dependencies, start the app, and run tests.
2. **Architecture overview** — how the Notion polling/webhook side connects to the Twitter posting side (authentication flow, data transformation, scheduling).
3. **Environment variables** — which secrets are required (Notion API key, Twitter/X bearer token, OAuth credentials) and where they are loaded from (e.g., `.env`, secret manager).
4. **Data flow** — the pipeline from a Notion page/database entry being detected as "ready to publish" through to a tweet being posted and the Notion record being marked as done.
