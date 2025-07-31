"""
This tool generates NVDA extensions.

Builders:

- NVDAAddon: Creates a .nvda-addon zip file. Requires the `excludePatterns` environment variable.
- NVDAManifest: Creates the manifest.ini file.
- NVDATranslatedManifest: Creates the manifest.ini file with only translated information.

The following environment variables are required to create the manifest:

- addon_info: .typing.AddonInfo
- brailleTables: .typings.BrailleTables
- symbolDictionaries: .typings.SymbolDictionaries

"""

from pathlib import Path

from SCons.Script import Environment, Builder

from .addon import createAddonBundleFromPath
from .manifests import generateManifest, generateTranslatedManifest



def generate(env: Environment):
	env.SetDefault(excludePatterns=tuple())

	addonAction = env.Action(
		lambda target, source, env: createAddonBundleFromPath(
			source[0].abspath, target[0].abspath, env["excludePatterns"]
		) and None,
		lambda target, source, env: f"Generating Addon {target[0]}",
	)
	env["BUILDERS"]["NVDAAddon"] = Builder(
		action=addonAction,
		suffix=".nvda-addon",
		src_suffix="/"
	)

	env.SetDefault(brailleTables={})
	env.SetDefault(symbolDictionaries={})

	manifestAction = env.Action(
		lambda target, source, env: generateManifest(
			source[0].abspath,
			target[0].abspath,
			addon_info=env["addon_info"],
			brailleTables=env["brailleTables"],
			symbolDictionaries=env["symbolDictionaries"],
		) and None,
		lambda target, source, env: f"Generating manifest {target[0]}",
	)
	env["BUILDERS"]["NVDAManifest"] = Builder(
		action=manifestAction,
		suffix=".ini",
		src_siffix=".ini.tpl"
	)

	translatedManifestAction = env.Action(
		lambda target, source, env: generateTranslatedManifest(
			source[1].abspath,
			target[0].abspath,
			mo=source[0].abspath,
			addon_info=env["addon_info"],
			brailleTables=env["brailleTables"],
			symbolDictionaries=env["symbolDictionaries"],
		) and None,
		lambda target, source, env: f"Generating translated manifest {target[0]}",
	)

	env["BUILDERS"]["NVDATranslatedManifest"] = Builder(
		action=translatedManifestAction,
		suffix=".ini",
		src_siffix=".ini.tpl"
	)


def exists():
	return True
