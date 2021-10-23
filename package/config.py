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
