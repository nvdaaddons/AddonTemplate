"""
This tool allows you to generate HTML files from Markdown.

Adds the following Builder to the constructed environment:

- md2html: Build HTML from Markdown

The following variables are required in the environment:

- localeDir
- localeFileName
- mdExtensions
- addon_summary
- addon_version


"""

import gettext
import codecs
from pathlib import Path

import markdown
from SCons.Script import Environment



def md2html(
		source: str|Path,
		dest: str,
		*,
		localeDir: Path,
		loacleFileName: str,
		mdExtensions: list[str],
		addonSummary: str,
		addonVersion: str
	):
	if isinstance(source, str):
		source = Path(source)

	# Use extensions if defined.
	localeLang = source.parent.name
	lang = localeLang.replace("_", "-")
	try:
		_ = gettext.translation(
			loacleFileName,
			localedir=localeDir,
			languages=[localeLang]
		).gettext
		summary = _(addonSummary)
	except Exception:
		summary = addonSummary
	title = f"{summary} {addonVersion}"
	headerDic = {
		'[[!meta title="': "# ",
		'"]]': " #",
	}
	with codecs.open(str(source), "r", "utf-8") as f:
		mdText = f.read()
	for k, v in headerDic.items():
		mdText = mdText.replace(k, v, 1)
	htmlText = markdown.markdown(mdText, extensions=mdExtensions)
	# Optimization: build resulting HTML text in one go instead of writing parts separately.
	docText = "\n".join(
		(
			"<!DOCTYPE html>",
			f'<html lang="{lang}">',
			"<head>",
			'<meta charset="UTF-8">',
			'<meta name="viewport" content="width=device-width, initial-scale=1.0">',
			'<link rel="stylesheet" type="text/css" href="../style.css" media="screen">',
			f"<title>{title}</title>",
			"</head>\n<body>",
			htmlText,
			"</body>\n</html>",
		)
	)
	with codecs.open(dest, "w", "utf-8") as f:
		f.write(docText)


def generate(env: Environment):
	env.SetDefault(localeDir = Path("locale/"))
	env.SetDefault(localeFileName = "messages")
	env.SetDefault(mdExtensions = {})

	mdAction = env.Action(
		lambda target, source, env: md2html(
			source[0].path,
			target[0].path,
			localeDir=env["localeDir"],
			loacleFileName=env["localeFileName"],
			mdExtensions=env["mdExtensions"],
			addonSummary=env["addon_summary"],
			addonVersion=env["addon_version"]
		) and None,
		lambda target, source, env: f"Generating {target[0]}",
	)
	mdBuilder = env.Builder(
		action=mdAction,
		suffix=".html",
		src_suffix=".md",
	)
	env["BUILDERS"]["md2html"] = mdBuilder


def exists():
	return True
