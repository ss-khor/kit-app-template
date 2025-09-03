# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
## [108.0.0] - 2025-08-19

### Changed
- Updated to `Kit 108.0.0`
  - [Kit 108.0 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/108_0.html)
  - [Kit 108.0 Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/108_0_highlights.html)
- Changed "Omniverse Cloud Streaming" application layer to "NVCF Streaming" to align underlying technology and use case.
- Updated streaming extensions to `omni.kit.livestream.app` and `omni.services.livestream.session` to support NVCF Streaming.
- Removed omni.services.transport.server.http.port overrides.  Aligned all template applications to use default ports.
- Updated repository documentation to reflect changes in streaming changes.
- Updated crash reporter settings to compress crash reports.
- Update Windows `omni.kit.window.modifier.titlebar` extension version
- Update repo tooling to most recent versions
- Updated application icon images for Composer and Explorer templates
- Enabled testing for USD Viewer Template messaging extension

### Fixed
- Fix duplicate key `.kit` file issues related to `settings.app.exts`

## [107.3.0] - 2025-05-27

### Added
- Added `repo template modify` tooling enabling developers to add Template Layers to existing applications created with 107.3 or newer.

### Changed
- Updated to `Kit 107.3.0`
  - [Kit 107.3 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/107_3.html)
  - [Kit 107.3 Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/107_3_highlights.html)
- Updated packman version to 7.29 to address customer issues with network restrictions [Issue #80](https://github.com/NVIDIA-Omniverse/kit-app-template/issues/80)

## [107.2.0] - 2025-05-05

### Added
- Added tooltip information to the VSCode debug extensions to clarify usage.
- Added tooling checks for path whitespace and OneDrive paths to improve developer experience.

### Changed
- Updated to `Kit 107.2.0`
  - [Kit 107.2 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/107_2.html)
  - [Kit 107.2 Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/107_2_highlights.html)
- Remove hard .git dependency from tooling
- Exclude `_repo` from packaging operations.

### Fixed
- Fixed nondeterministic tool loading behavior raised in [Issue #65](https://github.com/NVIDIA-Omniverse/kit-app-template/issues/65)
- Addressed spelling errors raised in [Issue #63](https://github.com/NVIDIA-Omniverse/kit-app-template/issues/63)
- Addressed default repository definition causing issues with bootstrapping thin packages from [Issue #70](https://github.com/NVIDIA-Omniverse/kit-app-template/issues/70)


## [107.0.3] - 2025-03-26

### Fixed
- Fixed issues with run time available registries by adding them directly to `.kit` templates
- Fixed issues with test time available registries by adding user.toml registry configurations

## [107.0.3] - 2025-03-20

### Added
- Added the ability select of application layers (streaming configurations) individually during templating
- Added a dedicated streaming configuration for NVCF based Omniverse Cloud (OVC) deployments
- Added C++ With Python Extension Template and Documentation
- Added streaming application creation and configuration documentation
- Added Developer Bundle extension by default to Base Editor, Composer, and Explorer templates
- Added an exclusion for Developer Bundle on streaming application layers

### Changed
- Updated to `Kit 107.0.3`
  - [Kit 107.0 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/107_0.html)
  - [Kit 107.0 Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/107_0_highlights.html)
  - Updated repo tooling UX to clarify tool use and improve user experience
  - Changed previous Omniverse Cloud (OVC) streaming configuration to Omniverse Cloud Streaming (Legacy)
  - Updated to `Cad Converter 203.0.0` Release
    - [Cad Converter Release Notes](https://docs.omniverse.nvidia.com/extensions/latest/ext_cad-converter/release-notes.html)
  - Moved extension `type` declaration to the extension definition section within the templates.toml file
  - Removed `omni.usd.fileformat.sbasar` and `omni.kit.property.sbsar` extensions from the USD Composer Template kit file. The extensions will be available at a later date.

### Fixed
- Fixed Windows long path issues during `repo package`


## [106.5.0] - 2024-12-12

### Added
- Added `app.environment` name setting for all kit file templates

### Removed
- Removed `WALK_VISIBLE_PATH` from USD Explorer Setup Extension

### Changed
- Updated to `Kit 106.5.0`
  - [Kit 106.5 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_5.html)
  - [Kit 106.5 Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_5_highlights.html)
- Updated Asset browser URLs
- Optimized OVC streaming file kit settings for OVC streaming deployments

### Fixed
- Updated Editor tutorial away from deprecated methods to use action based method for show/hide of menus

## [106.4.0] - 2024-11-18

### Added
- Added `stream_sdk.txt` to set timeout for stream SDK and updated container packaging to add it to container images
- Added `replay` to the `template new` tooling to allow for replaying app and extension creation to support automation
- Added companion tutorial section for using python pip packages

### Changed
- Updated to `Kit 106.4.0`
  - [Kit 106.4 Early Access Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_4.html)
  - [Kit 106.4 Early Access Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_4_highlights.html)
- Updated the `omni.kit.asset.browser` extension URLs to point to current asset libraries when not specified in Kit file
- Updated to `Cad Converter 202.0.0` Release
  - [Cad Converter Release Notes](https://docs.omniverse.nvidia.com/extensions/latest/ext_cad-converter/release-notes.html)

### Fixed
- Added missing notification of successful build `BUILD (RELEASE) SUCCEEDED` for Python only builds for Windows


## [106.3.0] - 2024-11-07

### Removed
- Removed the USD Viewer setup samples folder and the light_rigs folders from the USD Composer and USD Explorer setup templates. That data is now accessible from the `omni.usd_viewer.setup` and `omni.light_rigs` extension dependencies.


## [106.3.0] - 2024-11-04

### Added
- Built app containers support `NVDA_KIT_ARGS` and `NVDA_KIT_NUCLEUS` environment variables
  - `NVDA_KIT_ARGS` is passed directly into the kit executable
  - `NVDA_KIT_NUCLEUS` if set causes the container entrypoint to create an omniverse.toml configuration file with a single entry pointing at the provided nucleus server. This will also set the kit arg --/ovc/nucleus/server with the envvar value.
  - `repo launch --container` maps in these variables from the local environment as well
- Added `omni.kit.menu.common` to Kit Base Editor, USD Composer, and USD Explorer Template Kit files to enable Toggle Viewport Fullscreen and UI overlay with F7 and F11

### Changed
- Updated to `Kit 106.3.0`
  - [Kit 106.3 Early Access Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_3.html)
  - [Kit 106.3 Early Access Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_3_highlights.html)
- Updated build process to support auto-detection or user-specified host versions of `MSVC` and `WinSDK`, providing flexibility for Windows C++ developers to leverage their existing installations. [Windows C++ Developer Configuration](readme-assets/additional-docs/windows_developer_configuration.md)
- Updated `omni.kit.usd_explorer.main.menubar` to version 1.0.38 so that it works correctly with `omni.kit.menu.common`
- Moved Light Rig binary data from kit-app-template repo to `omni.light_rigs` extension and added the extension to Kit Base Editor, USD Composer, and USD Explorer Template Kit files
- Moved USD Viewer sample assets from kit-app-template repo to `omni.usd_viewer.samples` extension and added the extension USD Viewer Template Kit file
- Moved Kit Service Template to bottom of Application list
- BUILD (RELEASE) SUCCEEDED message not supported for all build configurations

### Removed
- Removed Services dependencies from USD Composer Template that caused a firewall popup on first launch


## [106.2.0] - 2024-10-03

### Changed
- Updated to `Kit 106.2.0`
  - [Kit 106.2 Early Access Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_2.html)
  - [Kit 106.2 Early Access Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_2_highlights.html)
- Refactored Viewer Template default tests to avoid unnecessary dependencies

### Removed
- Unused `simulation` menu item from USD Composer Template


## [106.1.0] - 2024-09-18

### Added
- Support for containerization of streaming applications and services via `repo package --container`
- Support extension only builds via `repo build`
- Support the ability to launch created containers via `repo launch --container`
- repo_usd tooling dependency
- Support for USD Viewer Template to send scene loading state to client via messaging

### Changed
- Updated to `Kit 106.1.0`
  - [Kit 106.1 Early Access Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_1.html)
  - [Kit 106.1 Early Access Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_1_highlights.html)
- Aligned default testing for applications and extensions
- Update and align code formatting/style across templates

### Fixed
- Extra setup extensions appear in standard extension template menu
- "Could not find cgroup memory limit" error during build
- Fixed default manipulator pivot back to "bounding box base" in USD Explorer Template


## [106.0.3] - 2024-09-18

### Changed
- Updated to `Kit 106.0.3`
  - [Kit 106.0.3 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_0_3.html)


## [106.0.2] - 2024-07-29

### Added
- Support for local streaming configurations for UI based Applications
- Support for multiple setup extensions per application
- Ability to pass arguments to Kit via the `repo launch` tool
- USD Composer Application Template and Documentation
- USD Viewer Application Template and Documentation
- USD Composer Setup Extension and Documentation
- USD Viewer Setup Extension and Documentation
- Repository Issue Templates Bug/Question/Feature Request
- Omniverse Product-Specific Terms (PRODUCT_TERMS_OMNIVERSE)
- Support for type ordering in templates.toml
- Metrics Assembler to Kit Base Editor Template to support unit correct assets
- Support for automatic launch if only single `.kit` file is present in `source/apps`

### Changed
- Updated to `Kit 106.0.2`
  - [Kit 106.0.2 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_0_2.html)
  - [Kit 106.0.1 Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_0_1.html)
- Updated all relevant application templates READMEs to reflect the addition of local streaming configurations
- Updated .gitattributes to ensure LFS is used for all relevant file types
- Updated .gitignore to exclude streaming app event traces
- Updated .vscode/launch.json to better support debugging behavior
- Updated LICENSE to separate NVIDIA License from Omniverse Product-Specific Terms
- Updated top level README.md to reflect additional templates and improve documentation clarity
- Updated Developer Bundle extension availability and corresponding documentation
- Updated public extension registry to reflect current Kit 106 registry location
- Updated templates.toml to support multiple setup extensions and new templates


## [106.0.0] - 2024-06-07

### Added
- Kit Base Editor Application Template and Documentation
- USD Explorer Application Template and Documentation
- USD Explorer Setup Extension and Documentation
- Kit Service Template and Documentation
- Simple Python Extension Template and Documentation
- Simple C++ Extension Template and Documentation
- Python UI Extension Template and Documentation
- Template configuration file (templates.toml)
- Added local `repo launch` tool for launching applications and fat packages directly
- Added local `repo package` functionality to improve package naming
- Omniverse EULA acceptance to Kit App Template via tooling
- tasks.json for better VSCode support
- SECURITY.md for security policy
- Notice for data collection and use
- Early access Developer Bundle extensions
- Kit App Template related Developer Bundle documentation (developer_bundle_extensions.md)
- Kit App Template related repo tools documentation (kit_app_template_tooling_guide.md)
- Usage and troubleshooting documentation for Kit App Template (usage_and_troubleshooting.md)
- repo_tools.toml to configure local repo tools

### Changed
- Updated to `Kit 106.0.0`
  - [Kit 106.0 Beta Release Notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_0.html)
  - [Kit 106.0 Release Highlights](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/106_0_highlights.html)
- Updated repo_kit_template tooling to support Applications and Extensions
- Updated repo_kit_template tooling to allow for application setup extensions
- Updated top level README.md to reflect updated tooling and templates
- Updated LICENSE.md to reflect updated tooling and templates
- Updated .gitattributes to reflect use of templates rather directly from source
- Added configuration to repo.toml to support new tools and templates

### Removed
- Top level build .bat/.sh scripts in favor of using `repo build` directly
- Predefined `define_app` declarations from `premake5.lua` in favor of developer defined applications
- Predefined source/apps in favor of templates for developers to build from