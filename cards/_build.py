# -*- coding: utf-8 -*-
# 把「人物图片」文件夹里的图 base64 内嵌进单文件 HTML，彻底避免预览路径问题。
import base64, os, json

BASE = r"D:\想法\sbti"
IMGDIR = os.path.join(BASE, "人物图片")
OUT = os.path.join(BASE, "cards", "人物卡片.html")

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp"}

def data_uri(fn):
    p = os.path.join(IMGDIR, fn)
    ext = os.path.splitext(fn)[1].lower()
    with open(p, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (MIME.get(ext, "application/octet-stream"), b)

# 卡牌数据（img 字段只写文件名，构建时查 IMGS 取真实数据）
data = [
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
  "reading":"嘴上喊着「妈妈」，实则黏人小狗一只。你资历浅却积极性爆棚，见到强者就前呼后拥、谄媚讨好，以「我是小狗」刷屏求宠。外弱内勇——把撒娇炼成社交武器的社交悍匪。",
  "meme":"<b>热梗：</b>无畏契约(Valorant)玩家别称，CS 玩家调侃其为「后起学弟」。游戏圈认妈成风、见人喊妈、自称小狗的谄媚文化。"},

 {"name":"麻麻","code":"NEW·麻麻","img":"麻麻.jpg","pos":"正位 · 温柔母体",
  "reading":"你是被全员黏着喊「麻麻」的那一位。温柔包容、自带安抚力场，再闹腾的小狗到你面前也乖。不争不抢，却稳坐情感食物链顶端——被依赖，就是你的统治方式。",
  "meme":"<b>热梗：</b>「妈妈」谐音网语（闽南语 mámá 与「麻」同音，2013 起流行）。在瓦学弟认妈语境里，麻麻即被黏人小狗集体认领的温柔大家长。"},
]

imgs = {d["img"]: data_uri(d["img"]) for d in data}
imgs_js = json.dumps(imgs, ensure_ascii=False)
data_js = json.dumps(data, ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BBTI 人格卡牌 · 塔罗签文</title>
<style>
  :root{
    --ink:#2b2440; --sub:#6b5e8c; --gold:#b08d3c; --line:#d8c9a3;
    --card:#fbf6ea; --bg1:#f3ece0; --bg2:#e7ddf0; --accent:#7b4ea3;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    font-family:"PingFang SC","Microsoft YaHei",serif;
    background:radial-gradient(circle at 20% 0%,var(--bg2),var(--bg1) 60%);
    color:var(--ink); padding:32px 16px 64px; min-height:100vh;
  }
  header{text-align:center; margin-bottom:8px}
  h1{font-size:26px; letter-spacing:4px; color:var(--ink)}
  .decor{color:var(--gold); letter-spacing:8px; font-size:13px; margin:6px 0 2px}
  .sub{color:var(--sub); font-size:13px; margin-bottom:18px}
  .draw{
    display:block; margin:0 auto 26px; padding:9px 22px; cursor:pointer;
    background:var(--accent); color:#fff; border:none; border-radius:24px;
    font-size:14px; letter-spacing:2px; box-shadow:0 4px 14px rgba(123,78,163,.3);
  }
  .draw:hover{opacity:.9}
  .grid{
    display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
    gap:22px; max-width:1180px; margin:0 auto;
  }
  .card{
    background:var(--card); border:1px solid var(--line); border-radius:16px;
    overflow:hidden; position:relative; transition:transform .25s, box-shadow .25s;
    box-shadow:0 6px 18px rgba(70,50,90,.12);
  }
  .card.dim{opacity:.35; filter:grayscale(.5)}
  .card.lit{transform:translateY(-6px); box-shadow:0 14px 34px rgba(176,141,60,.4)}
  .card::before{
    content:""; position:absolute; inset:7px; border:1px solid var(--line);
    border-radius:11px; pointer-events:none; z-index:2;
  }
  .imgwrap{height:240px; background:linear-gradient(135deg,#efe6d2,#e3d6f0); display:flex; align-items:center; justify-content:center; overflow:hidden; padding:10px}
  .imgwrap img{width:100%; height:100%; object-fit:contain; display:block}
  .pos{
    position:absolute; top:14px; left:14px; z-index:3;
    background:rgba(43,36,64,.82); color:#f3e9c8;
    font-size:12px; letter-spacing:1px; padding:4px 10px; border-radius:20px; border:1px solid var(--gold);
  }
  .body{padding:16px 18px 20px}
  .name{font-size:20px; font-weight:700; letter-spacing:1px}
  .code{font-size:12px; color:var(--gold); letter-spacing:2px; margin-left:8px; font-weight:400}
  .reading{
    margin:12px 0 12px; font-size:14.5px; line-height:1.95; color:var(--ink);
    text-align:justify; text-justify:inter-ideograph;
  }
  .meme{
    font-size:12px; color:var(--sub); border-top:1px dashed var(--line);
    padding-top:10px; line-height:1.7;
  }
  .meme b{color:var(--accent); font-weight:600}
  footer{text-align:center; color:var(--sub); font-size:12px; margin-top:30px; letter-spacing:1px}
</style>
</head>
<body>
<header>
  <div class="decor">✦ ☽ ✦ ☼ ✦ ☾ ✦</div>
  <h1>BBTI 人格卡牌</h1>
  <div class="sub">塔罗签文 · 星座解说风 — 于图片热梗中照见你的本命人格</div>
</header>
<button class="draw" onclick="drawCard()">✦ 随机抽一张 ✦</button>
<div class="grid" id="grid"></div>
<footer>每张牌皆自嘲向 · 仅供娱乐 · 图已内嵌，单文件可离线查看</footer>

<script>
const IMGS = /*__IMGS__*/;
const data = /*__DATA__*/;

const grid = document.getElementById('grid');
data.forEach((d,i)=>{
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `
    <div class="imgwrap"><img src="${IMGS[d.img]}" alt="${d.name}" loading="lazy"></div>
    <span class="pos">${d.pos}</span>
    <div class="body">
      <div class="name">${d.name}<span class="code">${d.code}</span></div>
      <div class="reading">${d.reading}</div>
      <div class="meme">${d.meme}</div>
    </div>`;
  grid.appendChild(card);
});

function drawCard(){
  const cards = [...document.querySelectorAll('.card')];
  cards.forEach(c=>c.classList.add('dim'));
  const pick = cards[Math.floor(Math.random()*cards.length)];
  pick.classList.remove('dim');
  pick.classList.add('lit');
  pick.scrollIntoView({behavior:'smooth', block:'center'});
}
</script>
</body>
</html>
'''

HTML = HTML.replace("/*__IMGS__*/", imgs_js).replace("/*__DATA__*/", data_js)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK", OUT, os.path.getsize(OUT), "bytes")
