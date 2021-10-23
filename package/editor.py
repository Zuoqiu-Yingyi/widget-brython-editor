import sys
import time
import base64

import tb as traceback
import javascript

from browser import document, window, bind, html
import browser.widgets.dialog as dialog

from package import utils, config

href = document.location.href
protocol, rest = href.split("://")
host, addr = rest.split("/", 1)

has_ace = True
try:
    editor = window.ace.edit("editor")
    # TODO 在这里设置编辑器默认模式
    editor.setTheme("ace/theme/one_dark")
    editor.session.setMode("ace/mode/python")
    editor.session.setUseWrapMode(True)
    editor.setFontSize(16)
    editor.focus()

    editor.setOptions({
        'enableLiveAutocompletion': True,
        'highlightActiveLine': False,
        'highlightSelectedWord': True
    })
except Exception:
    editor = html.TEXTAREA(rows=20, cols=70)
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

if 'set_debug' in document:
    __BRYTHON__.debug = int(document['set_debug'].checked)


def reset_src():
    if "code" in document.query:
        code = document.query.getlist("code")[0]
        editor.setValue(code)
    else:
        if storage is not None and "py_src" in storage:
            editor.setValue(storage["py_src"])
        else:
            editor.setValue('for i in range(10):\n\tprint(i)')
    editor.scrollToRow(0)
    editor.gotoLine(0)


def reset_src_area():
    if storage and "py_src" in storage:
        editor.value = storage["py_src"]
    else:
        editor.value = 'for i in range(10):\n\tprint(i)'


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


def to_str(xx):
    return str(xx)


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
            else print(f"保存运行结果失败, 错误信息{response.to_dict().get('msg')}")
    )


# 保存代码与输出结果
def save(ev):
    utils.setBlockAttrs(
        id=config.siyuan_widget_block_id,
        attrs={
            'custom-output': base64.b64encode(
                document["console"].value.encode('utf-8')
            ).decode('utf-8'),
        }
    ).then(
        lambda response:
            print("保存运行结果成功")
            if response.to_dict().get('code') == 0
            else print(f"保存运行结果失败, 错误信息{response.to_dict().get('msg')}")
    )

    utils.setBlockAttrs(
        id=config.siyuan_widget_block_id,
        attrs={
            'custom-code': base64.b64encode(editor.getValue().encode('utf-8')).decode('utf-8'),
        }
    ).then(
        lambda response:
            print("保存代码成功")
            if response.to_dict().get('code') == 0
            else print(f"保存代码失败, 错误信息{response.to_dict().get('msg')}")
    )


# run a script, in global namespace if in_globals is True


def run(*args):
    global output
    document["console"].value = ''
    src = editor.getValue()
    if storage is not None:
        storage["py_src"] = src

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
        href = window.location.href.rsplit("?", 1)[0]
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


if has_ace:
    reset_src()
else:
    reset_src_area()


# 更改语言
def change_language(lang):
    head = f"{protocol}://{host}"
    elts = addr.split("?")
    new_href = f"{head}/{elts[0]}?lang={lang}"
    document.location.href = new_href


# 更改主题
def change_theme(theme):
    old_theme = editor.getTheme()
    if theme != old_theme:
        editor.setTheme("ace/theme/%s" % theme)


# 更改字号
def change_font_size(size):
    try:
        size = int(size)
        old_size = editor.getFontSize()
        if size != old_size:
            editor.setFontSize(size)
            document['console'].style.fontSize = f"{size}px"
    except Exception:
        pass


# 刷新折叠状态
def refresh_warp():
    change_wrap()
    change_wrap()


# 更改折叠状态
def change_wrap(*args):
    editor.session.setUseWrapMode(not editor.session.getUseWrapMode())
