# -*- coding: utf-8 -*-
# BBTI 测试后端：单端口 HTTP 服务
#   GET  /         -> 返回测试页 index.html
#   POST /submit   -> 接收 {answers:[卡名...], result:卡名}，写入飞书多维表格 + 本地 JSON 备份
# 仅用 Python 标准库，免装依赖。监听 $PORT，绑定 0.0.0.0。
import os, json, urllib.request, urllib.error
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE_DIR, "index.html")
BACKUP = os.path.join(BASE_DIR, "submissions.jsonl")
CONFIG = os.path.join(BASE_DIR, "feishu_config.json")

# 加载飞书配置（缺失则仅做本地备份，不写飞书）
try:
    with open(CONFIG, encoding="utf-8") as f:
        CFG = json.load(f)
    def _good(v):
        return isinstance(v, str) and v != "" and not v.startswith("YOUR_")
    FEISHU_OK = _good(CFG.get("app_id")) and _good(CFG.get("app_secret")) and (
        _good(CFG.get("wiki_node_token")) or _good(CFG.get("app_token"))
    )
except Exception:
    CFG, FEISHU_OK = None, False

FIELD_NAMES = ["提交时间", "最终命中"] + ["Q%d" % i for i in range(1, 21)]


def log(msg):
    try:
        with open(os.path.join(BASE_DIR, "feishu.log"), "a", encoding="utf-8") as f:
            f.write("[%s] %s\n" % (datetime.now().isoformat(timespec="seconds"), msg))
    except Exception:
        pass


# ---------- 飞书多维表格写入 ----------
def _post(url, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(url, token):
    headers = {}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def get_token():
    host = CFG.get("feishu_host", "https://open.feishu.cn").rstrip("/")
    url = host + "/open-apis/auth/v3/tenant_access_token/internal"
    return _post(url, {"app_id": CFG["app_id"], "app_secret": CFG["app_secret"]})["tenant_access_token"]


def resolve_bitable_token(tenant_token):
    """返回真正可写 Bitable 的 app_token：优先用 wiki 节点 token 直接解析，否则用配置里的 app_token。

    关键经验：飞书 Wiki 内嵌多维表格的 node_token 本身就是（别名指向）那张 bitable 的 app_token，
    直接拿它调 bitable 接口即可拿到真实 app_token；不要再走 wiki/v2/spaces/get_node（该接口鉴权
    签名异常，稳定返回 131005 not found）。
    """
    host = CFG.get("feishu_host", "https://open.feishu.cn").rstrip("/")
    wiki = (CFG.get("wiki_node_token") or "").strip()
    if wiki and not wiki.startswith("YOUR_"):
        try:
            info = _get(host + "/open-apis/bitable/v1/apps/" + wiki, tenant_token)
            real = info.get("data", {}).get("app", {}).get("app_token")
            if real:
                return real
        except Exception as e:
            log("resolve wiki->bitable warn: %s" % e)
        # 兜底：wiki 节点 token 多数情况下可直接当 app_token 用
        return wiki
    app = (CFG.get("app_token") or "").strip()
    if app and not app.startswith("YOUR_"):
        return app
    raise RuntimeError("缺少 app_token 或 wiki_node_token")


def ensure_table(token, app):
    """优先用配置里的 table_id（已有表），否则按 table_name 自动建表。"""
    tid = (CFG.get("table_id") or "").strip()
    if tid and not tid.startswith("YOUR_"):
        return tid
    host = CFG.get("feishu_host", "https://open.feishu.cn").rstrip("/")
    name = CFG.get("table_name", "BBTI答卷")
    tables = _get(host + "/open-apis/bitable/v1/apps/%s/tables" % app, token).get("data", {}).get("items", [])
    for t in tables:
        if t.get("name") == name:
            return t["table_id"]
    new = _post(host + "/open-apis/bitable/v1/apps/%s/tables" % app,
                {"name": name, "default_view_name": "视图1"}, token)
    return new["data"]["table_id"]


def ensure_fields(token, app, table_id):
    host = CFG.get("feishu_host", "https://open.feishu.cn").rstrip("/")
    existing = [f["field_name"] for f in
                _get(host + "/open-apis/bitable/v1/apps/%s/tables/%s/fields" % (app, table_id), token)
                .get("data", {}).get("items", [])]
    for fn in FIELD_NAMES:
        if fn not in existing:
            _post(host + "/open-apis/bitable/v1/apps/%s/tables/%s/fields" % (app, table_id),
                  {"field_name": fn, "type": 1}, token)  # type 1 = 文本


def append_record(token, app, table_id, fields):
    host = CFG.get("feishu_host", "https://open.feishu.cn").rstrip("/")
    url = host + "/open-apis/bitable/v1/apps/%s/tables/%s/records/batch_create" % (app, table_id)
    _post(url, {"records": [{"fields": fields}]}, token)


def write_feishu(answers, result):
    token = get_token()
    app = resolve_bitable_token(token)
    tid = ensure_table(token, app)
    ensure_fields(token, app, tid)
    fields = {"提交时间": datetime.now().isoformat(timespec="seconds"), "最终命中": result or ""}
    for i, a in enumerate(answers, 1):
        if a:
            fields["Q%d" % i] = a
    append_record(token, app, tid, fields)


# ---------- 答卷处理 ----------
def handle_submit(body):
    answers = body.get("answers", []) or []
    result = body.get("result", "") or ""
    ts = datetime.now().isoformat(timespec="seconds")
    # 本地备份（万一并飞书失败也不丢）
    try:
        with open(BACKUP, "a", encoding="utf-8") as f:
            f.write(json.dumps({"time": ts, "answers": answers, "result": result},
                               ensure_ascii=False) + "\n")
    except Exception as e:
        log("backup fail: %s" % e)
    if not FEISHU_OK:
        return {"ok": True, "feishu": False, "note": "未配置飞书，仅本地备份"}
    try:
        write_feishu(answers, result)
        return {"ok": True, "feishu": True}
    except Exception as e:
        log("feishu fail: %s" % e)
        return {"ok": True, "feishu": False, "error": str(e)}


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.split("?")[0] != "/":
            self.send_error(404)
            return
        try:
            with open(INDEX, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception:
            self.send_error(404)

    def do_POST(self):
        if self.path.split("?")[0] != "/submit":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(n).decode("utf-8")
            body = json.loads(raw)
        except Exception:
            self._json(400, {"ok": False, "error": "bad json"})
            return
        self._json(200, handle_submit(body))

    def log_message(self, *a):
        pass


def main():
    port = int(os.environ.get("PORT", 3000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
