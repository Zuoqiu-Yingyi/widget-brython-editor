import sys
import time
import base64

import tb as traceback
import javascript

from browser import document, window, bind, html
import browser.widgets.dialog as dialog

from . import utils, config

href = document.location.href
protocol, rest = href.split("://")
host, addr = rest.split("/", 1)

has_ace = True
try:
    editor = window.ace.edit("editor")
    # TODO 在这里设置编辑器默认模式
    # editor.setTheme("ace/theme/one_dark")
    editor.session.setMode("ace/mode/python")
    # editor.session.setUseWrapMode(True)
    # editor.setFontSize(16)
    editor.focus()

    editor.setOptions({
        # 'enableLiveAutocompletion': True,
        'highlightActiveLine': True,
        'highlightSelectedWord': True
    })
except Exception:
    editor = html.TEXTAREA(rows=16, cols=76)
    document["editor"] <= editor
    def get_value(): return editor.value
    def set_value(x): editor.value = x
    editor.getValue = get_value
    editor.setValue = set_value
    has_ace = False


if hasattr(window, 'localStorage'):
    from browser.local_storage import storage
else:
    storage = None


def changeOutputPanelStatus(unfold):
    if unfold:
        document['left'].style.width = '50%'
        document['right'].style.width = '50%'
    else:
        document['left'].style.width = '100%'
        document['right'].style.width = '0%'


def changeDebugStatus(debug):
    if debug:
        __BRYTHON__.debug = 1
    else:
        __BRYTHON__.debug = 0


# 更改主题
def change_theme(theme):
    old_theme = editor.getTheme()
    if theme != old_theme:
        editor.setTheme("ace/theme/%s" % theme)
    storage['brython_editor_theme'] = theme


# 更改输出面板主题
def change_output_theme(theme):
    element = document['console']
    element.style.color = config.OUTPUT_THEME.get(theme).get('color')
    element.style.backgroundColor = config.OUTPUT_THEME.get(theme).get('background-color')
    storage['brython_output_theme'] = theme


def str2bool(s):
    return True if s.lower() == 'true' else False


def reset_src():
    if "code" in document.query:
        code = document.query.getlist("code")[0]
        editor.setValue(code)
    else:
        py_src = storage['brython_editor_py_src'] \
            if (storage is not None and 'brython_editor_py_src' in storage) \
            else config.DEFAULT_USER_CONFIG.get('py_src')
        theme = storage['brython_editor_theme'] \
            if (storage is not None and 'brython_editor_theme' in storage) \
            else config.DEFAULT_USER_CONFIG.get('theme')
        output_theme = storage['brython_output_theme'] \
            if (storage is not None and 'brython_output_theme' in storage) \
            else config.DEFAULT_USER_CONFIG.get('output_theme')
        font_size = int(storage['brython_editor_font_size']) \
            if (storage is not None and 'brython_editor_font_size' in storage) \
            else config.DEFAULT_USER_CONFIG.get('font_size')
        wrap_flag = str2bool(storage['brython_editor_wrap_flag']) \
            if (storage is not None and 'brython_editor_wrap_flag' in storage) \
            else config.DEFAULT_USER_CONFIG.get('wrap_flag')
        debug_flag = str2bool(storage['brython_editor_debug_flag']) \
            if (storage is not None and 'brython_editor_debug_flag' in storage) \
            else config.DEFAULT_USER_CONFIG.get('debug_flag')
        output_flag = str2bool(storage['brython_editor_output_flag']) \
            if (storage is not None and 'brython_editor_output_flag' in storage) \
            else config.DEFAULT_USER_CONFIG.get('output_flag')

        editor.setValue(py_src)
        editor.setFontSize(font_size)
        document['console'].style.fontSize = f"{font_size}px"
        editor.setOptions({'enableLiveAutocompletion': wrap_flag})
        document['set_debug'].checked = debug_flag
        document['set_output'].checked = output_flag
        change_theme(theme)
        change_output_theme(output_theme)
        changeDebugStatus(debug_flag)
        changeOutputPanelStatus(output_flag)

    editor.scrollToRow(0)
    editor.gotoLine(0)


def reset_src_area():
    if storage and 'brython_editor_py_src' in storage:
        editor.value = storage['brython_editor_py_src']
    else:
        editor.value = config.DEFAULT_USER_CONFIG.get('py_src')


if has_ace:
    reset_src()
else:
    reset_src_area()


def clear_editor(ev):
    editor.setValue("")


def clear_console(ev):
    document["console"].value = ""


class cOutput:
    encoding = 'utf-8'

    def __init__(self):
        self.cons = document["console"]
        self.buf = ''

    def write(self, data):
        self.buf += str(data)

    def flush(self):
        self.cons.value += self.buf
        self.buf = ''

    def __len__(self):
        return len(self.buf)


if "console" in document:
    cOut = cOutput()
    sys.stdout = cOut
    sys.stderr = cOut


info = sys.implementation.version
version = '%s.%s.%s' % (info.major, info.minor, info.micro)
if info.releaselevel == "rc":
    version += f"rc{info.serial}"
document['version'].text = version

output = ''


def show_console(ev):
    document["console"].value = output
    document["console"].cols = 60


# 从挂件快属性中加载存档
def load(ev):
    def __load(data):
        code = data.get('custom-code')
        output = data.get('custom-output')
        if code is not None:
            editor.setValue(
                base64.b64decode(
                    data.get('custom-code').encode('utf-8')
                ).decode('utf-8')
            )
        if output is not None:
            document["console"].value = base64.b64decode(
                data.get('custom-output').encode('utf-8')
            ).decode('utf-8')

        editor.scrollToRow(0)
        editor.gotoLine(0)

    utils.getBlockAttrs(
        id=config.siyuan_widget_block_id,
    ).then(
        lambda response:
            __load(response.to_dict().get('data'))
            if response.to_dict().get('code') == 0
            else print(f"ERROR:\n{response.to_dict().get('msg')}")
    )


# 保存代码与输出结果
def save(ev):
    utils.setBlockAttrs(
        id=config.siyuan_widget_block_id,
        attrs={
            'custom-code': base64.b64encode(editor.getValue().encode('utf-8')).decode('utf-8'),
            'custom-output': base64.b64encode(
                document["console"].value.encode('utf-8')
            ).decode('utf-8'),
            'data-export-md': f"```python\n{editor.getValue()}\n```\n\n```plaintext\n{document['console'].value}\n```",
        }
    ).then(
        lambda response:
            _
            if response.to_dict().get('code') == 0
            else print(f"ERROR:\n{response.to_dict().get('msg')}")
    )

# run a script, in global namespace if in_globals is True
def run(*args):
    global output
    document["console"].value = ''
    src = editor.getValue()
    if storage is not None:
        storage['brython_editor_py_src'] = src

    t0 = time.perf_counter()
    try:
        ns = {'__name__': '__main__'}
        exec(src, ns)
        state = 1
    except Exception:
        traceback.print_exc(file=sys.stderr)
        state = 0
    sys.stdout.flush()
    output = document["console"].value

    print('<completed in %6.2f ms>' % ((time.perf_counter() - t0) * 1000.0))
    return state


def show_js(ev):
    src = editor.getValue()
    document["console"].value = javascript.py2js(src, '__main__')


def share_code(ev):
    src = editor.getValue()
    if len(src) > 2048:
        d = dialog.InfoDialog(
            "共享 URL",
            f"代码字符数量须 < 2048<br>实际字符数量 {len(src)}",
            # style={"text-align": "center"},
            ok=True,
        )
    else:
        # href = window.location.href.rsplit("?", 1)[0]
        query = document.query
        query["code"] = src
        url = f"https://brython.info/tests/editor.html{query}"
        url = url.replace("(", "%28").replace(")", "%29")
        d = dialog.Dialog("复制 URL")
        area = html.TEXTAREA(rows=0, cols=0)
        d.panel <= area
        area.value = url
        # copy to clipboard
        area.focus()
        area.select()
        document.execCommand("copy")
        d.remove()
        d = dialog.Dialog("共享 URL")
        d.panel <= html.DIV("分享链接已写入剪贴板<br>请复制链接以共享代码")
        buttons = html.DIV()
        ok = html.BUTTON("确认")
        buttons <= html.DIV(ok, style={"text-align": "center"})
        d.panel <= html.BR() + buttons

        @bind(ok, "click")
        def click(evt):
            d.remove()


# 更改语言
def change_language(lang):
    head = f"{protocol}://{host}"
    elts = addr.split("?")
    new_href = f"{head}/{elts[0]}?lang={lang}"
    document.location.href = new_href


# 更改字号
def change_font_size(font_size):
    try:
        font_size = int(font_size)
        old_size = editor.getFontSize()
        if font_size != old_size:
            editor.setFontSize(font_size)
            document['console'].style.fontSize = f"{font_size}px"
        storage['brython_editor_font_size'] = str(font_size)
    except Exception:
        pass


# 刷新折叠状态
def refresh_warp():
    wrap_flag = editor.session.getUseWrapMode()
    editor.session.setUseWrapMode(not wrap_flag)
    editor.session.setUseWrapMode(wrap_flag)


# 更改折叠状态
def change_wrap(*args):
    wrap_flag = not editor.session.getUseWrapMode()
    editor.session.setUseWrapMode(wrap_flag)
    storage['brython_editor_wrap_flag'] = str(wrap_flag)


def set_debug(ev):
    wrap_flag = ev.target.checked
    changeDebugStatus(wrap_flag)
    storage['brython_editor_debug_flag'] = str(wrap_flag)


def set_output(ev):
    output_flag = ev.target.checked
    changeOutputPanelStatus(output_flag)
    storage['brython_editor_output_flag'] = str(output_flag)
    refresh_warp()
