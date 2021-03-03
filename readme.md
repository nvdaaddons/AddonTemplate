# NVDA Add-on Scons Template #

This package contains a basic template structure for NVDA add-on development, building, distribution and localization.
For details about NVDA add-on development, please see the [NVDA Add-on Development Guide](https://github.com/nvdaaddons/DevGuide/wiki/NVDA-Add-on-Development-Guide).
The NVDA add-on development/discussion list [is here](https://nvda-addons.groups.io/g/nvda-addons)

Copyright (C) 2012-2021 NVDA Add-on team contributors.

This package is distributed under the terms of the GNU General Public License, version 2 or later. Please see the file COPYING.txt for further details.

## Features

This template provides the following features you can use during NVDA add-on development and packaging:

* Automatic add-on package creation, with naming and version loaded from a centralized build variables file (buildVars.py) or command-line interface.
	* See packaging section for details on using command-line switches when packaging add-ons with custom version information.
* Manifest file creation using a template (manifest.ini.tpl). Build variables are replaced on this template. See below for add-on manifest specification.
* Compilation of gettext mo files before distribution, when needed.
	* To generate a gettext pot file, please run scons pot. A **addon-name.pot** file will be created with all gettext messages for your add-on. You need to check the buildVars.i18nSources variable to comply with your requirements.
* Automatic generation of manifest localization files directly from gettext po files. Please make sure buildVars.py is included in i18nFiles.
* Automatic generation of HTML documents from markdown (.md) files, to manage documentation in different languages.

## Requirements

You need the following software to use this code for your NVDA add-on development and packaging:

* a Python distribution (3.7 or later is recommended). Check the [Python Website](https://www.python.org) for Windows Installers.
* Scons - [Website](https://www.scons.org/) - version 3.1.0 or later. You can instlal it via PIP.
* GNU Gettext tools, if you want to have localization support for your add-on - Recommended. Any Linux distro or cygwin have those installed. You can find windows builds [here](https://gnuwin32.sourceforge.net/downlinks/gettext.php).
* Markdown 3.1.0 or later, if you want to convert documentation files to HTML documents. You can install it via PIP.

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

### To manage documentation files for your addon:

1. Copy the **readme.md** file for your add-on to the first created folder, where you copied **buildVars.py**. You can also copy **style.css** to improve the presentation of HTML documents.
2. Documentation files (named **readme.md**) must be placed into addon\doc\<lang>/.

### To package the add-on for distribution:

1. Open a command line, change to the folder that has the **sconstruct** file (usually the root of your add-on development folder) and run the **scons** command. The created add-on, if there were no errors, is placed in the current directory.
2. You can further customize variables in the **buildVars.py** file.
3. You can also customize version and update channel information from command line by passing the following switches when running scons:
	* version: add-on version string.
	* channel: update channel (do not use this switch unless you know what you are doing).
	* dev: suitable for development builds, names the add-on according to current date (yyyymmdd) and sets update channel to "dev".

Note that this template only provides a basic add-on structure and build infrastructure. You may need to adapt it for your specific needs.

If you have any issues please use the NVDA addon list mentioned above.
