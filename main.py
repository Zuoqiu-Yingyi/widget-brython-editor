from browser import document
from browser.widgets.menu import Menu

from package import editor, config

__BRYTHON__.language = 'zh-cn'


def init(language=None, theme=None):

    if language is None:
        qs_lang = document.query.getfirst("lang")

    language = qs_lang or "zh-cn"
    theme = theme or "one_dark"

    return language, theme


language, theme = init()

trans = {
    'report_bugs': {
        'zh-cn': '请提交错误至 ',
        'en': 'Please report bugs in the ',
    },
    'test_page': {
        'zh-cn': '测试页面',
        'en': 'Tests page',
    },
    'run': {
        'zh-cn': '▶ 运行代码',
        'en': '▶ run code',
    },
    'language': {
        'zh-cn': '语言',
        'en': 'language',
    },
    'share_code': {
        'zh-cn': '分享',
        'en': 'Share code',
    },
    'load': {
        'zh-cn': '加载存档',
        'en': 'reload',
    },
    'save': {
        'zh-cn': '保存存档',
        'en': 'save',
    },
    'debug': {
        'zh-cn': '调试',
        'en': 'Debug',
    },
    'output': {
        'zh-cn': '输出面板',
        'en': 'output panel',
    },
    'clear_editor': {
        'zh-cn': '清空编辑器',
        'en': 'clear editor',
    },
    'clear_console': {
        'zh-cn': '清空输出面板',
        'en': 'clear output pannel',
    },
    'wrap': {
        'zh-cn': '自动换行',
        'en': 'line wrap',
    },
    'theme': {
        'zh-cn': '主题',
        'en': 'theme',
    },
    'version_label': {
        'zh-cn': 'Brython 版本: ',
        'en': 'Brython version: ',
    },
    'font_size': {
        'zh-cn': '字号',
        'en': 'font size',
    },
    'File': {
        'zh-cn': '文件',
        'en': 'File',
    },
    'Edit': {
        'zh-cn': '编辑',
        'en': 'Edit',
    },
    'Setting': {
        'zh-cn': '设置',
        'en': 'Setting',
    },
    'Run': {
        'zh-cn': '运行',
        'en': 'Run',
    },
}

themes = config.THEMES

for key in trans:
    if key in document:
        document[key].html = trans[key].get(language, trans[key]['zh-cn'])


__BRYTHON__.debug = int(document['set_debug'].checked)

# bindings
document['set_debug'].bind('change', editor.set_debug)
document['set_output'].bind('change', editor.set_output)

menu = Menu(document["menu"])
file_menu = menu.add_menu(trans['File'].get(language, trans['File']['zh-cn']))
edit_menu = menu.add_menu(trans['Edit'].get(language, trans['Edit']['zh-cn']))
setting_menu = menu.add_menu(trans['Setting'].get(language, trans['Setting']['zh-cn']))
run_menu = menu.add_menu(trans['Run'].get(language, trans['Run']['zh-cn']))

file_menu.add_item(
    trans['load'].get(language, trans['load']['zh-cn']),
    callback=editor.load,
)
file_menu.add_item(
    trans['save'].get(language, trans['save']['zh-cn']),
    callback=editor.save,
)

edit_menu.add_item(
    trans['clear_editor'].get(language, trans['clear_editor']['zh-cn']),
    callback=editor.clear_editor,
)
edit_menu.add_item(
    trans['clear_console'].get(language, trans['clear_console']['zh-cn']),
    callback=editor.clear_console,
)
edit_menu.add_item(
    trans['wrap'].get(language, trans['wrap']['zh-cn']),
    callback=editor.change_wrap,
)

language_menu = setting_menu.add_menu(trans['language'].get(language, trans['language']['zh-cn']))
theme_menu = setting_menu.add_menu(trans['theme'].get(language, trans['theme']['zh-cn']))
font_size_menu = setting_menu.add_menu(trans['font_size'].get(language, trans['font_size']['zh-cn']))

for k, v in themes.items():
    theme_menu.add_item(
        k,
        callback=lambda *args: editor.change_theme(themes.get(args[0].target.innerText)),
    )

for i in range(8, 33):
    font_size_menu.add_item(
        i,
        callback=lambda *args: editor.change_font_size(args[0].target.innerText),
    )

language_menu.add_item(
    '简体中文',
    callback=lambda *args: editor.change_language('zh-cn'),
)
language_menu.add_item(
    'English',
    callback=lambda *args: editor.change_language('en'),
)

run_menu.add_item(
    trans['run'].get(language, trans['run']['zh-cn']),
    callback=lambda *args: editor.run(),
)
run_menu.add_item(
    'Python',
    callback=editor.show_console,
)
run_menu.add_item(
    'JavaScript',
    callback=editor.show_js,
)
run_menu.add_item(
    trans['share_code'].get(language, trans['share_code']['zh-cn']),
    callback=editor.share_code,
)

# 加载存档
editor.load(0)
