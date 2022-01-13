from browser import document, window

href = document.location.href
protocol, rest = href.split("://")
# protocol: http
# rest: 127.0.0.1:6806/widgets/weight-brython-editor/
host, addr = rest.split("/", 1)
# host: 127.0.0.1:6806
# addr: widgets/widget-brython-editor/

token = "7wxk0gcex0xsmr4f"

headers = {
    'Content-Type': 'application/json',
    # 'Authorization': f'Token {token}',
}

siyuan_widget_block = window.frameElement.parentElement.parentElement
siyuan_widget_block_id = siyuan_widget_block.dataset.nodeId

api_url = {
    'lsNotebooks': "/api/notebook/lsNotebooks",
    'openNotebook': "/api/notebook/openNotebook",
    'closeNotebook': "/api/notebook/closeNotebook",
    'renameNotebook': "/api/notebook/renameNotebook",
    'createNotebook': "/api/notebook/createNotebook",
    'removeNotebook': "/api/notebook/removeNotebook",
    'getNotebookConf': "/api/notebook/getNotebookConf",
    'setNotebookConf': "/api/notebook/setNotebookConf",
    'createDocWithMd': "/api/filetree/createDocWithMd",
    'renameDoc': "/api/filetree/renameDoc",
    'removeDoc': "/api/filetree/removeDoc",
    'moveDoc': "/api/filetree/moveDoc",
    'getHPathByPath': "/api/filetree/getHPathByPath",
    'getBlockAttrs': "/api/attr/getBlockAttrs",
    'setBlockAttrs': "/api/attr/setBlockAttrs",
    'sql': "/api//query/sql",
    'exportMdContent': "/api/export/exportMdContent",
    'bootProgress': "/api/system/bootProgress",
    'version': "/api/system/version",
    'currentTime': "/api/system/currentTime",
}

# 输出面板主题颜色
OUTPUT_THEME = {
    'follow': {
        'color': "var(--b3-theme-on-surface)",
        'background-color': "var(--b3-theme-surface)",
    },
    'light': {
        'color': "#1F1F1F",
        'background-color': "#FFF",
    },
    'dark': {
        'color': "#CCC",
        'background-color': "#1F1F1F",
    },
}

DEFAULT_USER_CONFIG = {
    'py_src': 'print(globals())\nprint(dir(__builtins__))',
    'theme': 'one_dark',
    'output_theme': 'follow',
    'font_size': 16,
    'wrap_flag': True,
    'debug_flag': True,
    'output_flag': True,
}

THEMES = {
    "ambiance": "ambiance",
    "chaos": "chaos",
    "chrome": "chrome",
    "clouds": "clouds",
    "clouds midnight": "clouds_midnight",
    "cobalt": "cobalt",
    "crimson editor": "crimson_editor",
    "dawn": "dawn",
    "dracula": "dracula",
    "dreamweaver": "dreamweaver",
    "eclipse": "eclipse",
    "github": "github",
    "gob": "gob",
    "gruvbox": "gruvbox",
    "idle fingers": "idle_fingers",
    "iplastic": "iplastic",
    "katzenmilch": "katzenmilch",
    "kr theme": "kr_theme",
    "kuroir": "kuroir",
    "merbivore": "merbivore",
    "merbivore soft": "merbivore_soft",
    "monokai": "monokai",
    "mono industrial": "mono_industrial",
    "nord dark": "nord_dark",
    "one dark": "one_dark",
    "pastel on dark": "pastel_on_dark",
    "solarized dark": "solarized_dark",
    "solarized light": "solarized_light",
    "sqlserver": "sqlserver",
    "terminal": "terminal",
    "textmate": "textmate",
    "tomorrow": "tomorrow",
    "tomorrow night": "tomorrow_night",
    "tomorrow night blue": "tomorrow_night_blue",
    "tomorrow night bright": "tomorrow_night_bright",
    "tomorrow night eighties": "tomorrow_night_eighties",
    "twilight": "twilight",
    "vibrant ink": "vibrant_ink",
    "xcode": "xcode",
}
