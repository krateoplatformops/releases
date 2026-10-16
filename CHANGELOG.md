# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Previous changes not listed in this document can be traced using Git history.

## [3.0.7] - Unreleased

### Added

- Added `POST /can-i` to check many permissions for the current user in one call, e.g. one call instead of one per namespace in a blueprint form RESTAction (`resources-presenter` 0.10.5)

## [3.0.6] - 2026-10-16

### Changed

- Changed the pre-upgrade cleanup job to run as a non-root user (UID 1000), so cluster policies that forbid root containers no longer block it

## [3.0.5] - 2026-10-14

### Added

- Added `displayingDependencies` to the `Form` widget to show or hide a field based on another field (`frontend` 1.0.30, re-tagged)

## [3.0.4] - 2026-10-14

### Fixed

- Fixed slow portal page loads with many routes by loading all routes in one request (`frontend` 1.0.30, `portal` 1.3.5)
- Fixed `Form` `autocomplete` and `dependencies` fields never loading their options (`frontend` 1.0.30)

## [3.0.3] - 2026-10-08

### Fixed

- Fixed `authn` client certificate expiring by renewing it automatically (`authn` 0.23.0)
- Fixed slow loading of portal routes (`snowplow` 0.20.7, `resources-presenter` 0.10.4)

## [3.0.2] - 2026-07-17

### Fixed

- Fixed OAuth and GitHub login (`frontend` 1.0.27)
- Fixed ArgoCD example jobs installing 3.0.0 instead of the current release

## [3.0.1] - 2026-07-16

### Fixed

- Fixed OAuth and GitHub login (`frontend` 1.0.23-fix). This chart version was never published, so the install fails: use 3.0.2 instead
