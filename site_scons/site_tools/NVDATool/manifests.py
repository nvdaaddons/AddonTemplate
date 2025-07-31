
import codecs
import gettext
from collections.abc import Mapping

from site_scons.site_tools.NVDATool.typings import AddonInfo, BrailleTables, SymbolDictionaries, Strable # NOQA: E402



def format_nested_section(
	section_name: str,
	data: Mapping[str, Mapping[str, Strable]]
) -> str:
	lines = [f"\n[{section_name}]"]
	for item_name, inner_dict in data.items():
		lines.append(f"[[{item_name}]]")
		for key, val in inner_dict.items():
			lines.append(f"{key} = {val}")
	return "\n".join(lines) + "\n"


def generateManifest(
		source: str,
		dest: str,
		addon_info: AddonInfo,
		brailleTables: BrailleTables,
		symbolDictionaries: SymbolDictionaries,
	):
	# Prepare the root manifest section
	with codecs.open(source, "r", "utf-8") as f:
		manifest_template = f.read()
	manifest = manifest_template.format(**addon_info)
	# Add additional manifest sections such as custom braile tables
	# Custom braille translation tables
	if brailleTables:
		manifest += format_nested_section("brailleTables", brailleTables)

	# Custom speech symbol dictionaries
	if symbolDictionaries:
		manifest += format_nested_section("symbolDictionaries", symbolDictionaries)

	with codecs.open(dest, "w", "utf-8") as f:
		f.write(manifest)


def generateTranslatedManifest(
		source: str,
		dest: str,
		language: str,
		localeDir: str,
		addon_info: AddonInfo,
		brailleTables: BrailleTables,
		symbolDictionaries: SymbolDictionaries,
	):
	_ = gettext.translation("nvda", localedir=localeDir, languages=[language]).gettext
	vars: dict[str, str] = {}
	for var in ("addon_summary", "addon_description"):
		vars[var] = _(addon_info[var])
	with codecs.open(source, "r", "utf-8") as f:
		manifest_template = f.read()
	manifest = manifest_template.format(**vars)

	def _format_section_only_with_displayName(section_name: str, data: Mapping[str, Mapping[str, Strable]]) -> str:
		lines = [f"\n[{section_name}]"]
		for item, inner_dict in data.items():
			lines.append(f"[[{item}]]")
			# Fetch display name only.
			lines.append(f"displayName = {_(str(inner_dict['displayName']))}")
		return "\n".join(lines) + "\n"

	# Add additional manifest sections such as custom braile tables
	# Custom braille translation tables
	if brailleTables:
		manifest += _format_section_only_with_displayName("brailleTables", brailleTables)

	# Custom speech symbol dictionaries
	if symbolDictionaries:
		manifest += _format_section_only_with_displayName("symbolDictionaries", symbolDictionaries)

	with codecs.open(dest, "w", "utf-8") as f:
		f.write(manifest)
