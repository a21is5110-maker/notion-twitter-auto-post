# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This repository is intended to build an automation tool that reads content from Notion and automatically posts it to Twitter/X. The `claude/fortune-telling-guidance-8jn3y` branch contains an early example of tweet copy (Japanese fortune-telling promotional text), which illustrates the target content type.

## Current State

The repository is in its initial stage — no source code, build system, or runtime exists yet. The only file on `main` is an empty `README.md`. Development of the actual automation tool has not started.

## Expected Architecture (to be built)

Based on the project name, the system will likely need:

- **Notion integration** — reading pages or database entries via the Notion API
- **Twitter/X integration** — posting content via the Twitter API v2 (OAuth 2.0)
- **Scheduler or trigger** — running the pipeline periodically (cron, GitHub Actions, etc.)

When the codebase is established, update this file with:
- The language/runtime and how to install dependencies
- How to run, test, and lint the project
- Environment variables required (Notion token, Twitter credentials, etc.)
- The data flow from Notion → transformation → Twitter post
