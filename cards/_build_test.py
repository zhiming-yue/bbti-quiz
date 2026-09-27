# -*- coding: utf-8 -*-
# 构建 BBTI 测试：20 道选择题（翻页式）→ 命中最匹配的人物卡片。
# 图片 base64 内嵌，单文件离线可用。
import base64, os, json, re
from collections import Counter

BASE = r"D:\想法\sbti"
IMGDIR = os.path.join(BASE, "人物图片")
OUT = os.path.join(BASE, "BBTI测试.html")

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp"}

def data_uri(fn):
    p = os.path.join(IMGDIR, fn)
    ext = os.path.splitext(fn)[1].lower()
    with open(p, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (MIME.get(ext, "application/octet-stream"), b)

# 12 张卡牌数据（与 人物卡片.html 一致）
cards = [
 {"name":"老绷家","code":"A极·老绷家","img":"老绷家.jpg","pos":"正位 · 表情封印",
  "reading":"天塌下来也绷得住。你修的是「不笑」这门绝学，红唇一贴、万事不惊。外人看你是块木头，实则内心戏比谁都多——绷，是你的护体神功。",
  "meme":"<b>热梗：</b>杨幂红唇贴纸梗，表情管理大师、憋笑高手。遇事不破功者，谓之老绷家。"},
 {"name":"奶龙","code":"ESTC","img":"奶龙.webp","pos":"正位 · 沙雕显化",
  "reading":"奶萌其外，沙雕其中。你一出场就自带笑点，自信到没边，当场发疯全场记住你。看似幼稚，实则是用最天真的脸，干最疯的事。",
  "meme":"<b>热梗：</b>搞笑动画龙，奶萌又沙雕。开心时奶、发疯时猛，反差即萌点。"},
 {"name":"糯糯","code":"ESFA","img":"糯糯.webp","pos":"正位 · 软糯聚气",
  "reading":"软乎乎却能热场。你是气氛的黏合剂，谁尴尬你都能化开，自己却绝不先笑场。温柔是你的武器，糯到骨子里，却把全场托得稳稳的。",
  "meme":"<b>热梗：</b>软糯可爱、温温柔柔。以柔克刚，用亲和力把冷场悄悄捂热。"},
 {"name":"菲比就比","code":"ENTB","img":"菲比就比.webp","pos":"逆位 · 乖巧腹黑",
  "reading":"表面温顺小修女，暗地权谋大主教。你替所有人说话，却假装听不懂，谜之自信甩锅一流。人人都爱你——因为你把黑锅背得毫无痕迹。",
  "meme":"<b>热梗：</b>鸣潮「菲比啾比」，清纯修女反差人设，二创里化身万能背锅的腹黑大主教。"},
 {"name":"咕咕嘎嘎","code":"ENFB","img":"咕咕嘎嘎.gif","pos":"正位 · 鸽语敷衍",
  "reading":"你发真心话，他回一串咕咕嘎嘎。不是听不懂，是懒得接。用最呆萌的表情包把真情实感糊弄过去——鸽子式回应，是最高级的回避艺术。",
  "meme":"<b>热梗：</b>鸽/鸭式乱叫，呆萌敷衍。以「咕咕嘎嘎」四两拨千斤，把走心对话怼回表情包。"},
 {"name":"鼠鼠","code":"INFB","img":"鼠鼠.jpg","pos":"逆位 · 蛰伏自嘲",
  "reading":"鼠鼠我啊，实则装傻躲事。你把自己缩成一只小老鼠，说社恐、说卑微，遇到麻烦就缩回洞里。自嘲是盾，躲事是术，谁也别想逮着我。",
  "meme":"<b>热梗：</b>「鼠鼠我啊」社恐自嘲/打工人自比老鼠。以弱示人，换取不被打扰的清净。"},
 {"name":"胆子肥嘟嘟","code":"ESTA","img":"胆子肥嘟嘟.jpg","pos":"正位 · 虚张声势",
  "reading":"「你看你胆子真是肥嘟嘟的」——明明心虚，偏要装得底气十足。表面绷得住，实则膨胀到可爱。你用最萌的嚣张，掩盖最虚的自信。",
  "meme":"<b>热梗：</b>「你胆子真是肥嘟嘟的」装可爱虚张声势。外强中萌，虚张但可爱。"},
 {"name":"牛来","code":"NEW·牛来","img":"牛来.jpg","pos":"正位 · 绊倒召唤",
  "reading":"妈妈牛来！你越认真越翻车，却仍坚持甩手喊完。土味喜庆的召唤术，是认命式乐观：牛没来，先绊一跤接福。松弛，是你给生活的玄学。",
  "meme":"<b>热梗：</b>2026 抽象电影梗，谐音「牛市来」。「妈妈牛来！」+ 绊倒体，翻车亦释怀。"},
 {"name":"你已急哭","code":"NEW·急哭","img":"你已急哭.png","pos":"逆位 · 破防急泪",
  "reading":"被戳一下就破防，眼泪比道理来得快。你情绪外显、喜怒写在脸上，急了就哭、哭了再刚。看似软弱，实则是把真性情摊开给人看的人。",
  "meme":"<b>热梗：</b>「你已急哭」破防反应包。情绪不设防，真心比城府来得更直接。"},
 {"name":"邪修","code":"NEW·邪修","img":"邪修.webp","pos":"逆位 · 旁门证道",
  "reading":"正道苦修十年，不如邪修灵机一动。你不按常理出牌，用最离谱的法子把事办成。离谱表象下藏着精巧——野路子，是你对抗标准化的松弛武器。",
  "meme":"<b>热梗：</b>修仙反派修炼法→「看似离谱却高效」的野路子解法。万物皆可邪修。"},
 {"name":"瓦学弟","code":"NEW·瓦学弟","img":"瓦学弟.gif","pos":"逆位 · 认妈谄媚",
  "reading":"嘴上喊着「妈妈」，实则黏人小狗一只。你资历浅却积极性爆棚，见到强者就前呼后拥、谄媚讨好，以「我是小狗」刷屏求宠。把撒娇炼成社交武器的社交悍匪。",
  "meme":"<b>热梗：</b>无畏契约(Valorant)玩家别称。游戏圈认妈成风、见人喊妈、自称小狗的谄媚文化。"},
 {"name":"麻麻","code":"NEW·麻麻","img":"麻麻.jpg","pos":"正位 · 温柔母体",
  "reading":"你是被全员黏着喊「麻麻」的那一位。温柔包容、自带安抚力场，再闹腾的小狗到你面前也乖。不争不抢，却稳坐情感食物链顶端——被依赖，就是你的统治方式。",
  "meme":"<b>热梗：</b>「妈妈」谐音网语。在瓦学弟认妈语境里，麻麻即被黏人小狗集体认领的温柔大家长。"},
]

# 20 道题从「测试题目.md」读取（单一数据源，方便修改）。
# 每个选项指向一张卡的 name（必须匹配 cards 里的 name）。12 张在 80 个选项位里均匀铺开（6~7 次）。
QFILE = os.path.join(BASE, "测试题目.md")

def load_questions(path):
    """解析 测试题目.md：
          N. 题干
          - 选项文字 => 卡名
       # 开头行与空行忽略。"""
    questions, cur = [], None
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            m = re.match(r'^\s*(\d+)\.\s*(.+)$', line)
            if m:
                cur = {"q": m.group(2).strip(), "opts": []}
                questions.append(cur)
                continue
            m = re.match(r'^\s*-\s*(.+?)\s*=>\s*(.+?)\s*$', line)
            if m and cur is not None:
                cur["opts"].append((m.group(1).strip(), m.group(2).strip()))
            else:
                raise ValueError("题目文件解析失败，请检查格式: " + line)
    assert len(questions) == 20, "题目数应为 20，实际 %d" % len(questions)
    for q in questions:
        assert len(q["opts"]) == 4, "每题应为 4 个选项: " + q["q"]
    return questions

questions = load_questions(QFILE)

# —— 平衡性自检 ——
names = [c["name"] for c in cards]
cnt = Counter()
for q in questions:
    for (_, c) in q["opts"]:
        assert c in names, "未知卡名: %s" % c
        cnt[c] += 1
print("题数:", len(questions), " 选项总数:", sum(len(q["opts"]) for q in questions))
print("各卡出现次数:", dict(cnt))
assert all(6 <= cnt[c] <= 7 for c in names), "分布不均！应为 6~7"
print("平衡性 OK")

imgs = {c["img"]: data_uri(c["img"]) for c in cards}
imgs_js = json.dumps(imgs, ensure_ascii=False)
cards_js = json.dumps(cards, ensure_ascii=False)
# 题目转成 {q, opts:[{t,c}]}
q_js = json.dumps(
    [{"q": q["q"], "opts": [{"t": t, "c": c} for (t, c) in q["opts"]]} for q in questions],
    ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BBTI 人格测试 · 你是哪张卡？</title>
<style>
  :root{
    --ink:#2b2440; --sub:#6b5e8c; --gold:#b08d3c; --line:#d8c9a3;
    --card:#fbf6ea; --bg1:#f3ece0; --bg2:#e7ddf0; --accent:#7b4ea3;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:"PingFang SC","Microsoft YaHei",serif;
    background:radial-gradient(circle at 20% 0%,var(--bg2),var(--bg1) 60%);
    color:var(--ink); padding:28px 16px 60px; min-height:100vh;}
  .wrap{max-width:680px; margin:0 auto}
  header{text-align:center; margin-bottom:18px}
  .decor{color:var(--gold); letter-spacing:8px; font-size:13px; margin:6px 0 2px}
  h1{font-size:26px; letter-spacing:3px}
  .sub{color:var(--sub); font-size:13px; margin-top:6px}

  /* 进度条 */
  .progress{height:8px; background:#e7ddf0; border-radius:6px; overflow:hidden; margin:18px 0 6px}
  .bar{height:100%; width:0; background:linear-gradient(90deg,var(--gold),var(--accent)); transition:width .3s}
  .ptxt{text-align:right; color:var(--sub); font-size:12px; margin-bottom:14px; letter-spacing:1px}

  .panel{background:var(--card); border:1px solid var(--line); border-radius:16px;
    padding:26px 24px; box-shadow:0 8px 22px rgba(70,50,90,.12); position:relative}
  .panel::before{content:""; position:absolute; inset:7px; border:1px solid var(--line);
    border-radius:11px; pointer-events:none}

  .qtitle{font-size:19px; line-height:1.7; font-weight:700; margin-bottom:20px; position:relative}
  .opts{display:flex; flex-direction:column; gap:12px; position:relative}
  .opt{display:flex; align-items:center; gap:12px; padding:14px 16px; border:1px solid var(--line);
    border-radius:12px; cursor:pointer; background:#fff; transition:.18s; font-size:15px; line-height:1.5}
  .opt:hover{border-color:var(--accent); background:#faf4ff; box-shadow:0 4px 12px rgba(123,78,163,.12)}
  .opt.sel{background:var(--accent); color:#fff; border-color:var(--accent); box-shadow:0 6px 16px rgba(123,78,163,.3)}
  .opt .dot{width:18px; height:18px; border-radius:50%; border:2px solid var(--line); flex:0 0 auto}
  .opt.sel .dot{background:#fff; border-color:#fff}

  .nav{display:flex; justify-content:space-between; margin-top:22px; gap:12px; position:relative}
  button.b{padding:11px 22px; border:none; border-radius:24px; font-size:14px; letter-spacing:1px;
    cursor:pointer; box-shadow:0 4px 12px rgba(123,78,163,.25)}
  .b.prev{background:#efe6d2; color:var(--ink)}
  .b.next{background:var(--accent); color:#fff}
  .b:disabled{opacity:.4; cursor:not-allowed; box-shadow:none}

  /* 开场 / 结果 */
  .center{text-align:center}
  .start p{color:var(--sub); line-height:1.9; font-size:14px; margin:14px 0 22px}
  .start .b{background:var(--accent); color:#fff; font-size:16px; padding:13px 38px}
  .result .rtitle{color:var(--sub); letter-spacing:3px; font-size:14px}
  .result .rname{font-size:34px; font-weight:800; letter-spacing:2px; margin:4px 0 2px}
  .result .rcode{color:var(--gold); letter-spacing:2px; font-size:13px; margin-bottom:18px}

  /* 卡片 */
  .card{background:var(--card); border:1px solid var(--line); border-radius:16px; overflow:hidden;
    position:relative; box-shadow:0 10px 28px rgba(70,50,90,.18)}
  .card::before{content:""; position:absolute; inset:7px; border:1px solid var(--line);
    border-radius:11px; pointer-events:none; z-index:2}
  .imgwrap{background:linear-gradient(135deg,#efe6d2,#e3d6f0); display:flex; align-items:center; justify-content:center; overflow:hidden; padding:12px}
  .imgwrap img{width:100%; max-height:380px; object-fit:contain; display:block; border-radius:8px}
  .pos{position:absolute; top:14px; left:14px; z-index:3; background:rgba(43,36,64,.82); color:#f3e9c8;
    font-size:12px; letter-spacing:1px; padding:4px 10px; border-radius:20px; border:1px solid var(--gold)}
  .body{padding:16px 18px 20px}
  .name{font-size:20px; font-weight:700; letter-spacing:1px}
  .code{font-size:12px; color:var(--gold); letter-spacing:2px; margin-left:8px; font-weight:400}
  .reading{margin:12px 0; font-size:14.5px; line-height:1.95; text-align:justify}
  .meme{font-size:12px; color:var(--sub); border-top:1px dashed var(--line); padding-top:10px; line-height:1.7}
  .meme b{color:var(--accent); font-weight:600}
  .restart{display:block; margin:22px auto 0; background:var(--accent); color:#fff;
    border:none; border-radius:24px; padding:11px 30px; font-size:14px; cursor:pointer; letter-spacing:1px}
  .hidden{display:none}
  footer{text-align:center; color:var(--sub); font-size:12px; margin-top:26px; letter-spacing:1px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="decor">✦ ☽ ✦ ☼ ✦ ☾ ✦</div>
    <h1>BBTI 人格测试</h1>
    <div class="sub">20 题看清你的本命人格卡 · 塔罗签文风</div>
  </header>

  <!-- 开场 -->
  <section id="start" class="panel start center">
    <p>你究竟是绷得住的<b>老绷家</b>，还是炸场的<b>奶龙</b>？<br>
    20 道选择题，翻页作答，最后为你翻开命中的那张人格卡。<br>
    <span style="color:var(--gold)">仅供娱乐 · 自嘲向 · 图已内嵌可离线</span></p>
    <button class="b" onclick="startTest()">✦ 开始测试 ✦</button>
  </section>

  <!-- 答题 -->
  <section id="quiz" class="panel hidden">
    <div class="progress"><div class="bar" id="bar"></div></div>
    <div class="ptxt" id="ptxt"></div>
    <div class="qtitle" id="qtitle"></div>
    <div class="opts" id="opts"></div>
    <div class="nav">
      <button class="b prev" id="prev" onclick="go(-1)">← 上一步</button>
      <button class="b next" id="next" onclick="go(1)">下一步 →</button>
    </div>
  </section>

  <!-- 结果 -->
  <section id="result" class="panel result center hidden">
    <div class="rtitle">你的本命人格卡是</div>
    <div class="rname" id="rname"></div>
    <div class="rcode" id="rcode"></div>
    <div class="card" id="rcard"></div>
    <button class="restart" onclick="resetTest()">↻ 重新测一次</button>
  </section>

  <footer>BBTI · 于图片热梗中照见你的本命人格</footer>
</div>

<script>
const IMGS = /*__IMGS__*/;
const CARDS = /*__CARDS__*/;
const QUESTIONS = /*__QUESTIONS__*/;
const cardByName = {}; CARDS.forEach(c=>cardByName[c.name]=c);

let cur = 0;
let answers = new Array(QUESTIONS.length).fill(null);
let order = new Array(QUESTIONS.length).fill(null);   // 缓存每题乱序后的选项顺序，避免重渲染时跳动

function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}

function startTest(){ document.getElementById('start').classList.add('hidden');
  document.getElementById('quiz').classList.remove('hidden'); render(); }

function render(){
  const total = QUESTIONS.length;
  document.getElementById('bar').style.width = ((cur)/total*100)+'%';
  document.getElementById('ptxt').textContent = '第 '+(cur+1)+' / '+total+' 题';
  document.getElementById('qtitle').textContent = QUESTIONS[cur].q;
  const optsBox = document.getElementById('opts'); optsBox.innerHTML='';
  if(!order[cur]) order[cur] = shuffle(QUESTIONS[cur].opts);   // 每题只乱序一次，点选后不再重排
  const opts = order[cur];
  opts.forEach(o=>{
    const div = document.createElement('div');
    div.className = 'opt' + (answers[cur]===o.c ? ' sel':'');
    div.innerHTML = '<span class="dot"></span><span>'+o.t+'</span>';
    div.onclick = ()=>{ answers[cur]=o.c; render(); };
    optsBox.appendChild(div);
  });
  document.getElementById('prev').disabled = (cur===0);
  const nextBtn = document.getElementById('next');
  nextBtn.textContent = (cur===total-1) ? '✨ 查看结果' : '下一步 →';
  nextBtn.disabled = (answers[cur]===null);
}

function go(d){
  if(d>0 && answers[cur]===null) return;
  cur += d;
  if(cur >= QUESTIONS.length){ finish(); return; }
  if(cur < 0) cur = 0;
  render();
}

function finish(){
  const tally = {}; CARDS.forEach(c=>tally[c.name]=0);
  answers.forEach(c=>{ if(c) tally[c]++; });
  let best=null, bestN=-1;
  CARDS.forEach(c=>{ if(tally[c.name]>bestN){ bestN=tally[c.name]; best=c.name; } });
  const card = cardByName[best];
  document.getElementById('quiz').classList.add('hidden');
  document.getElementById('result').classList.remove('hidden');
  document.getElementById('rname').textContent = card.name;
  document.getElementById('rcode').textContent = card.code;
  document.getElementById('rcard').innerHTML =
    '<div class="imgwrap"><img src="'+IMGS[card.img]+'" alt="'+card.name+'"></div>'+
    '<span class="pos">'+card.pos+'</span>'+
    '<div class="body"><div class="name">'+card.name+'<span class="code">'+card.code+'</span></div>'+
    '<div class="reading">'+card.reading+'</div><div class="meme">'+card.meme+'</div></div>';
  report(best);
  window.scrollTo({top:0,behavior:'smooth'});
}

function report(resultName){
  try{
    fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},
      body: JSON.stringify({answers:answers, result:resultName})}).catch(function(){});
  }catch(e){}
}
function resetTest(){ cur=0; answers=new Array(QUESTIONS.length).fill(null); order=new Array(QUESTIONS.length).fill(null);
  document.getElementById('result').classList.add('hidden');
  document.getElementById('start').classList.remove('hidden'); }
</script>
</body>
</html>
'''

HTML = (HTML.replace("/*__IMGS__*/", imgs_js)
            .replace("/*__CARDS__*/", cards_js)
            .replace("/*__QUESTIONS__*/", q_js))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK", OUT, os.path.getsize(OUT), "bytes")
