from browser import window, document
import browser.widgets.menu as menu

import config

editor = window.ace.edit("editor")

Menu = menu.Menu

trans_menu = {
    "menu_console": {
        'zh-cn': "控制台",
        "en": "Console",
        "es": "Consola",
        "fr": "Console",
    },
    "menu_editor": {
        'zh-cn': "编辑器",
        "en": "Editor",
        "es": "Editor",
        "fr": "Editeur",
    },
    "menu_demo": {
        'zh-cn': "演示",
        "en": "Demo",
        "es": "Demo",
        "fr": "D\u00e9mo",
    },
    "menu_gallery": {
        'zh-cn': "画廊",
        "en": "Gallery",
        "es": "Galer\u00eda",
        "fr": "Galerie",
    },
    "menu_doc": {
        'zh-cn': "文档",
        "en": "Documentation",
        "es": "Documentaci\u00f3n",
        "fr": "Documentation",
    },
    "menu_download": {
        'zh-cn': "下载",
        "en": "Download",
        "es": "Descargas",
        "fr": "T\u00e9l\u00e9chargement",
    },
    "menu_dev": {
        'zh-cn': "开发",
        "en": "Development",
        "es": "Desarrollo",
        "fr": "D\u00e9veloppement",
    },
    "menu_ex": {
        'zh-cn': "示例",
        "en": "Examples",
        "es": "Ejemplos",
        "fr": "Exemples",
    },
    "menu_groups": {
        'zh-cn': "社区",
        "en": "Community",
        "es": "Comunidad",
        "fr": "Communaut\u00e9",
    },
    "menu_ref": {
        'zh-cn': "参考",
        "en": "Reference",
        "es": "Referencia",
        "fr": "R\u00e9f\u00e9rence",
    },
    "menu_resources": {
        'zh-cn': "资源",
        "en": "Resources",
        "es": "Recursos",
        "fr": "Ressources",
    },
    "menu_tutorial": {
        'zh-cn': "指导",
        "en": "Tutorial",
        "es": "Tutorial",
        "fr": "Tutoriel",
    }
}

links = {
    "home": "/index.html",
    "console": "/tests/console.html",
    "demo": "/demo.html",
    "editor": "/tests/editor.html",
    "gallery": "/gallery/gallery_{language}.html",
    "doc": "/static_doc/{language}/intro.html",
    "download": "https: //github.com/brython-dev/brython/releases",
    "dev": "https: //github.com/brython-dev/brython",
    "groups": "/groups.html",
    "tutorial": "/static_tutorial/{language}/index.html"
}

languages = [
    ['zh-cn', "简体中文"],
    ["en", "English"],
    # ["fr", "Fran\u00e7ais"],
    # ["es", "Espa\u00f1ol"]
]

supported_languages = [
    'zh-cn',
    "en",
    # "fr",
    # "es",
]

themes = [
    ("ambiance", "ambiance"),
    ("chaos", "chaos"),
    ("chrome", "chrome"),
    ("clouds", "clouds"),
    ("clouds_midnight", "clouds midnight"),
    ("cobalt", "cobalt"),
    ("crimson_editor", "crimson editor"),
    ("dawn", "dawn"),
    ("dracula", "dracula"),
    ("dreamweaver", "dreamweaver"),
    ("eclipse", "eclipse"),
    ("github", "github"),
    ("gob", "gob"),
    ("gruvbox", "gruvbox"),
    ("idle_fingers", "idle fingers"),
    ("iplastic", "iplastic"),
    ("katzenmilch", "katzenmilch"),
    ("kr_theme", "kr theme"),
    ("kuroir", "kuroir"),
    ("merbivore", "merbivore"),
    ("merbivore_soft", "merbivore soft"),
    ("monokai", "monokai"),
    ("mono_industrial", "mono industrial"),
    ("nord_dark", "nord dark"),
    ("one_dark", "one dark"),
    ("pastel_on_dark", "pastel on dark"),
    ("solarized_dark", "solarized dark"),
    ("solarized_light", "solarized light"),
    ("sqlserver", "sqlserver"),
    ("terminal", "terminal"),
    ("textmate", "textmate"),
    ("tomorrow", "tomorrow"),
    ("tomorrow_night", "tomorrow night"),
    ("tomorrow_night_blue", "tomorrow night blue"),
    ("tomorrow_night_bright", "tomorrow night bright"),
    ("tomorrow_night_eighties", "tomorrow night eighties"),
    ("twilight", "twilight"),
    ("vibrant_ink", "vibrant ink"),
    ("xcode", "xcode"),
]


def show(language=None, theme=None):

    if language is None:
        qs_lang = document.query.getfirst("lang")

    language = qs_lang or "zh-cn"
    theme = theme or "one_dark"

    return language, theme
