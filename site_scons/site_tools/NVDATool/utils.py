from collections.abc import Mapping

from .typings import Strable



def _(arg: str) -> str:
	"""
	A function that passes the string to it without doing anything to it.
	Needed for recognizing strings for translation by Gettext.
	"""
	return arg


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
