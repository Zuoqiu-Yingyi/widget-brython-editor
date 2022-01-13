from browser import document, window, bind
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
        'en': 'load',
    },
    'save': {
        'zh-cn': '保存存档',
        'en': 'save',
    },
    'open_file': {
        'zh-cn': '打开文件',
        'en': 'open file',
    },
    'save_file': {
        'zh-cn': '保存文件',
        'en': 'save file',
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
        'zh-cn': '编辑器主题',
        'en': 'editor theme',
    },
    'theme_output': {
        'zh-cn': '输出面板主题',
        'en': 'output pannel theme',
    },
    'light': {
        'zh-cn': '亮色',
        'en': 'light',
    },
    'dark': {
        'zh-cn': '暗色',
        'en': 'dark',
    },
    'follow': {
        'zh-cn': '跟随全局',
        'en': 'follow the global',
    },
    'version_label': {
        'zh-cn': 'Brython 版本: ',
        'en': 'Brython version: ',
    },
    'font_size': {
        'zh-cn': '字号',
        'en': 'font size',
    },
    'Archive': {
        'zh-cn': '存档',
        'en': 'Archive',
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
    'test': {
        'zh-cn': '测试↗',
        'en': 'Test↗',
    },
    'demo': {
        'zh-cn': '示例↗',
        'en': 'Demo↗',
    },
    'document': {
        'zh-cn': '文档↗',
        'en': 'Document↗',
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


open_btn = document["file"]
save_btn = document["save_file"]

file_name = "brython.py"


@bind(open_btn, "input")
def file_read(ev):
    def onload(event):
        """
        Triggered when file is read. The FileReader instance is event.target.
        The file content, as text, is the FileReader instance's "result" attribute.
        """
        editor.editor.setValue(event.target.result)
        # set attribute "download" to file name
        save_btn.attrs["download"] = file.name

    # Get the selected file as a DOM File object
    file = open_btn.files[0]
    # Create a new DOM FileReader instance
    reader = window.FileReader.new()
    # Read the file content as text
    reader.readAsText(file)
    reader.bind("load", onload)


@bind(save_btn, "click")
def file_save(evt):
    """
    Create a "data URI" to set the downloaded file content
    Cf. https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs
    """
    content = window.encodeURIComponent(editor.editor.getValue())
    # set attribute "href" of save link
    save_btn.attrs["href"] = f"data:text/plain;charset=UTF-8,{content}"


menu = Menu(document["menu"])
file_menu = menu.add_menu(trans['Archive'].get(language, trans['Archive']['zh-cn']))
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
theme_output_menu = setting_menu.add_menu(trans['theme_output'].get(language, trans['theme_output']['zh-cn']))
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

theme_output_menu.add_item(
    trans['follow'].get(language, trans['follow']['zh-cn']),
    callback=lambda *args: editor.change_output_theme('follow'),
)
theme_output_menu.add_item(
    trans['light'].get(language, trans['light']['zh-cn']),
    callback=lambda *args: editor.change_output_theme('light'),
)
theme_output_menu.add_item(
    trans['dark'].get(language, trans['dark']['zh-cn']),
    callback=lambda *args: editor.change_output_theme('dark'),
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
