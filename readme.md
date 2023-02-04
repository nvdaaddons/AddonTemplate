# NVDA Add-on Scons Template #

This package contains a basic template structure for NVDA add-on development, building, distribution and localization.
For details about NVDA add-on development, please see the [NVDA Add-on Development Guide](https://github.com/nvdaaddons/DevGuide/wiki/NVDA-Add-on-Development-Guide).
The NVDA add-on development/discussion list [is here](https://nvda-addons.groups.io/g/nvda-addons)

Copyright (C) 2012-2022 NVDA Add-on team contributors.

This package is distributed under the terms of the GNU General Public License, version 2 or later. Please see the file COPYING.txt for further details.



[alekssamos](https://github.com/alekssamos/) added automatic package of add-ons through Github Actions.

For details about Github Actions  please see the [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).

Copyright (C) 2022 alekssamos


## Features

This template provides the following features you can use during NVDA add-on development and packaging:

* Automatic add-on package creation, with naming and version loaded from a centralized build variables file (buildVars.py) or command-line interface.
	* See packaging section for details on using command-line switches when packaging add-ons with custom version information.
	* This process will happen automatically when receiving a pull request, and there is also the possibility of manual launch.
	* To let the workflow run automatically when pushing to main or master (development) branch, remove the comment for branches line in GitHub Actions (.github/workflow/build_addon.yml).
	* If you have created a tag (E.G.: `git tag v1.0 && git push --tag`), then a release will be automatically created and the add-on file will be uploaded as an asset.
	* Otherwise, with normal commits or with manual startup, you can download the artifacts from the Actions page of your repository.
* Manifest file creation using a template (manifest.ini.tpl). Build variables are replaced on this template. See below for add-on manifest specification.
* Compilation of gettext mo files before distribution, when needed.
	* To generate a gettext pot file, please run scons pot. A **addon-name.pot** file will be created with all gettext messages for your add-on. You need to check the buildVars.i18nSources variable to comply with your requirements.
* Automatic generation of manifest localization files directly from gettext po files. Please make sure buildVars.py is included in i18nFiles.
* Automatic generation of HTML documents from markdown (.md) files, to manage documentation in different languages.

In addition, this template includes configuration files for the following tools for use in add-on development and testing (see "additional tools" section for details):

* Flake8 (flake8.ini): a base configuration file for Flake8 linting tool based on NVDA's own Flake8 configuration file.
* Configuration for VS Code. It requires NVDA`s repo at the same level that add-on repos, with prepared source code (`scons source`).
	* Press `control+shift+m`after saving a file to search for problems.
	* Use arrow and tab keys for the autocompletion feature.
	* Press `control+shift+p`to open the commands palette and search for recommended extensions to install or check if they are installed.

## Requirements

You need the following software to use this code for your NVDA add-on development and packaging:

* a Python distribution (3.7 or later is recommended). Check the [Python Website](https://www.python.org) for Windows Installers.
* Scons - [Website](https://www.scons.org/) - version 4.3.0 or later. You can install it via PIP.
* GNU Gettext tools, if you want to have localization support for your add-on - Recommended. Any Linux distro or cygwin have those installed. You can find windows builds [here](https://gnuwin32.sourceforge.net/downlinks/gettext.php).
* Markdown 3.3.0 or later, if you want to convert documentation files to HTML documents. You can install it via PIP.

## Usage

### To create a new NVDA add-on using this template:

1. Create an empty folder to hold the files for your add-on.
2. Copy the **site_scons** folder, and the following files, into your new empty folder: **buildVars.py**, **manifest.ini.tpl**, **manifest-translated.ini.tpl**, **sconstruct**, **.gitignore**, and **.gitattributes**
3. Create an **addon** folder inside your new folder. Inside the **addon* folder, create needed folders for the add-on modules (e.g. appModules, synthDrivers, etc.). An add-on may have one or more module folders.
4. In the **buildVars.py** file, change variable **addon_info** with your add-on's information (name, summary, description, version, author and url).
5. Put your code in the usual folders for NVDA extension, under the **addon** folder. For instance: globalPlugins, synthDrivers, etc.
6. Gettext translations must be placed into addon\locale\<lang>/LC_MESSAGES\nvda.po. 

#### Add-on manifest specification

An add-on manifest generated manually or via **buildVars.py** must include the following information:

* Name (string): a unique identifier for the add-on. It must use camel case (e.g. someModule).
* Summary (string): name as shown on NVDA's Add-ons Manager.
* Description (string): a short detailed description about the add-on.
* Version (string)
* Author (string and an email address): one or more add-on author contact information in the form "name <email@address>".
* URL (string): a web address where the add-on information can be found (typically community add-ons website address (https://addons.nvda-project.org) is used).
* docFileName (string): name of the documentation file.
* minimumNVDAVersion (year.major or year.major.minor): the earliest version of NVDA the add-on is compatible with (e.g. 2019.3). Add-ons are expected to use features introduced in this version of NVDA or declare compatibility with it.
* lastTestedNVDAVersion (year.major or year.major.minor): the latest or last tested version of NVDA the add-on is said to be compatible with (e.g. 2020.3). Add-on authors are expected to declare this value after testing add-ons with the version of NVDA specified.
* addon_updateChannel (string or None): the update channel for the add-on release.

In addition, the following information must be filled out (not used in the manifest):

* sourceURL (string): repository URL for the add-on source code.
* license (string): the license of the add-on and its source code.
* licenseURL: the URL for the license file.

### To manage documentation files for your addon:

1. Copy the **readme.md** file for your add-on to the first created folder, where you copied **buildVars.py**. You can also copy **style.css** to improve the presentation of HTML documents.
2. Documentation files (named **readme.md**) must be placed into addon\doc\<lang>/.

### To package the add-on for distribution:

1. Open a command line, change to the folder that has the **sconstruct** file (usually the root of your add-on development folder) and run the **scons** command. The created add-on, if there were no errors, is placed in the current directory.
2. You can further customize variables in the **buildVars.py** file.
3. You can also customize version and update channel information from command line by passing the following switches when running scons:
	* version: add-on version string.
	* versionNumber: add-on version number of the form major.minor.patch (all integers)
	* channel: update channel (do not use this switch unless you know what you are doing).
	* dev: suitable for development builds, names the add-on according to current date (yyyymmdd) and sets update channel to "dev".

### Additional tools

The template includes configuration files for use with additional tools such as linters. These include:

* Flake8 (flake8.ini): a Python code linter (3.7.9 or later, can be installed with PIP).

Read the documentation for the tools you wish to use when building and developing add-ons.

Note that this template only provides a basic add-on structure and build infrastructure. You may need to adapt it for your specific needs such as using additional tools.

If you have any issues please use the NVDA addon list mentioned above.
