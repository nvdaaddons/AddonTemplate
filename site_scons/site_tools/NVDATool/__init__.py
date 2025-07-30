"""
This tool generates NVDA extensions.

Builders:

- NVDAAddon: Creates a .nvda-addon zip file. Requires the `excludePatterns` environment variable.

"""

from SCons.Script import Environment, Builder

from .addon import createAddonBundleFromPath



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

def exists():
	return True
