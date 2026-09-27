# BBTI 人格测试 · 你是哪张网络梗卡？
# BBTI Personality Quiz — Which Meme Card Are You?

> 类 MBTI 的网页人格测试，用 12 张网络热梗人物卡做结果，20 道翻页选择题，答完匹配一张卡并展示画像签文。
>
> An MBTI-style web personality quiz that matches you to one of 12 internet-meme character cards through 20 flip-style questions, then shows a tarot/horoscope-style reading for your card.

---

## 🚀 在线体验 / Live Demo

**https://bbti-quiz.app.workbuddy.host/**

手机、电脑直接打开即可作答，无需安装任何东西。
Open on phone or desktop — no install required.

---

## 📖 项目简介 / Project Introduction

BBTI 是一套「抽象搞怪风」的本土化人格测试。它沿用 MBTI 的四维思路（社交能量 / 脑回路 / 处世 / 麻烦应对），但把晦涩的心理学标签换成了 12 张大家熟悉的网络热梗人物卡——老绷家、奶龙、糯糯、菲比就比、鼠鼠、瓦学弟、麻麻……你做完 20 道题后，系统会根据选项分布匹配出最像你的那张卡，并附上一段塔罗牌 / 星座解说风格的「画像签文」，还会点出这张卡背后的热梗出处。

BBTI is a goofy, meme-flavored take on personality typing. It keeps MBTI's four-dimension logic (social energy / thinking pattern / dealing-with-people / handling-trouble) but swaps the clinical labels for 12 recognizable internet-meme personas. After 20 flip-style questions, it tallies your answers, matches you to the most "you" card, and serves up a tarot/horoscope-style one-card reading with a note on the meme's origin.

> ⚠️ 纯娱乐，非心理测评，结果请勿当真。
> ⚠️ For fun only — not a psychological assessment.

---

## ✨ 特性 / Features

- **20 题翻页交互 + 进度条**：纯前端实现，选项只在首次进入时洗牌，点选不会再跳动。
  *20 flip-style questions with a progress bar. Pure front-end; options shuffle once on entry so they never jump when you click.*
- **12 张人物卡画廊 + 塔罗/星座风签文**：每张卡约 50 字人格解读，含正位/逆位牌位与热梗溯源。
  *12 character cards with ~50-word tarot/horoscope readings, including upright/reversed positions and meme origins.*
- **题目单一数据源**：所有题目写在 `测试题目.md`，改完重跑脚本即重建测试页，无需动 HTML。
  *Single source of truth: all questions live in `测试题目.md`; rerun the build script to regenerate — no HTML editing needed.*
- **图片 base64 内嵌，单文件离线可用**：测试页与画廊页均为自包含 HTML，断网也能打开。
  *Images are base64-embedded, so the pages are self-contained and work offline.*
- **可选作答数据回收**：后端支持把答卷写入飞书多维表格（详见 `app/接入指引.md`）。
  *Optional answer collection into a Feishu base table (see `app/接入指引.md`).*

---

## ⚡ 快速开始 / Quick Start

环境要求：Python 3，**无需安装任何第三方依赖**（后端只用标准库）。
Requirements: Python 3, **no third-party dependencies** (standard library only).

```bash
cd app
python app.py          # 默认监听 :3000
# 想换端口：PORT=8080 python app.py
```

然后浏览器打开 **http://localhost:3000** 即可游玩。
Then open **http://localhost:3000** in your browser.

> 未配置飞书也能正常运行——此时答卷只做本地备份（`app/submissions.jsonl`），不会写任何外部表格。
> Runs fine without Feishu configured — answers are just backed up locally to `app/submissions.jsonl`.

---

## 🛠️ 改题与重建前端 / Edit Questions & Rebuild

1. 编辑题目源文件 `测试题目.md`，格式为：

   ```markdown
   1. 题干写在这里
   - 选项文字 A => 老绷家
   - 选项文字 B => 奶龙
   - 选项文字 C => 糯糯
   - 选项文字 D => 鼠鼠
   ```

2. 重新构建测试页：

   ```bash
   python cards/_build_test.py
   ```

   脚本会读取 `测试题目.md`，生成根目录的 `BBTI测试.html`（含 12 张图 base64 内嵌）。

3. **重要**：构建脚本只产出根目录那份 `BBTI测试.html`。若要让后端 `app/app.py` 的 `GET /` 返回最新版，需要把生成的文件**复制为 `app/index.html`**：

   ```bash
   copy BBTI测试.html app/index.html        # Windows
   # cp BBTI测试.html app/index.html        # macOS / Linux
   ```

4. 换卡面图：把新图放进 `人物图片\`，并相应更新 `cards/_build_test.py` 里的图片清单，重跑脚本即可。
   To swap card images: drop new files into `人物图片\`, update the image list in `cards/_build_test.py`, and rerun.

> 构建脚本内 `BASE` 路径为硬编码的 Windows 绝对路径，换机器使用时请相应修改。
> Note: the build script hardcodes a Windows `BASE` path — adjust it if you move the project.

---

## 📂 项目结构 / Project Structure

```text
sbti/
├── app/
│   ├── app.py              # 后端 HTTP 服务（仅标准库）：GET / 返回测试页，POST /submit 回收答卷
│   ├── index.html          # 服务实际返回的测试页（由 BBTI测试.html 复制而来）
│   ├── 接入指引.md          # 飞书多维表格接入与发布说明
│   └── feishu_config.json  # 飞书凭证（已被 .gitignore 排除，不会入库）
├── cards/
│   ├── _build_test.py      # 从 测试题目.md 构建测试页 BBTI测试.html
│   ├── _build.py           # 构建 12 卡画廊 人物卡片.html
│   └── index.html / 人物卡片.html
├── 人物图片\              # 12 张人物卡原图（老绷家/奶龙/糯糯/菲比就比/咕咕嘎嘎/鼠鼠/胆子肥嘟嘟/牛来/你已急哭/邪修/瓦学弟/麻麻）
├── 测试题目.md            # 20 道题单一数据源
├── personas.md            # 24 型人格标签与四维模型设计文档
└── BBTI测试.html          # 构建产物：离线条测页（复制到 app/index.html 生效）
```

```text
sbti/
├── app/
│   ├── app.py             # Backend HTTP server (stdlib only): GET / serves quiz, POST /submit collects answers
│   ├── index.html         # The quiz page actually served (copied from BBTI测试.html)
│   ├── 接入指引.md         # Feishu base-table setup & deployment guide
│   └── feishu_config.json # Feishu credentials (gitignored, never committed)
├── cards/
│   ├── _build_test.py     # Builds BBTI测试.html from 测试题目.md
│   ├── _build.py          # Builds the 12-card gallery 人物卡片.html
│   └── index.html / 人物卡片.html
├── 人物图片\             # 12 source card images
├── 测试题目.md           # Single source of truth for the 20 questions
├── personas.md           # 24-type design doc & four-dimension model
└── BBTI测试.html         # Build output: offline quiz page (copy to app/index.html to activate)
```

---

## 🃏 梗来源与鸣谢 / Meme Sources & Credits

12 张人物卡均取材自公开网络热梗，仅作娱乐二次创作，非商用、无官方授权，版权归原梗出处所有。

The 12 cards are based on public internet memes for fan-created entertainment only — not commercial, no official endorsement; rights belong to the original sources.

| 卡名 Card | 梗义出处 / Meme origin |
|---|---|
| 老绷家 | 「绷」系网络语，指遇事稳住、表面淡定内心已崩的人 |
| 奶龙 | 国民级动画 IP「小奶龙」衍生的呆萌/搞事表情包 |
| 糯糯 | 软糯可爱人设，自带「贴贴」属性 |
| 菲比就比 | 出自游戏《鸣潮》角色「菲比」，谐音「啾比」，腹黑大主教梗 |
| 咕咕嘎嘎 | 抽象鹅系叫唤梗，象征话多爱整活 |
| 鼠鼠 | 「鼠鼠我啊」自嘲梗，社恐卑微打工人写照 |
| 胆子肥嘟嘟 | 台词「我看你胆子真是肥嘟嘟的」，指又菜又爱硬刚 |
| 牛来 | 2026 抽象电影梗，谐音「牛市来」+ 绊倒体 |
| 你已急哭 | 嘲讽对方心态崩了的挑衅梗 |
| 邪修 | 看似离谱却意外高效的野路子解法 |
| 瓦学弟 | 游戏《无畏契约(Valorant)》玩家别称，圈内「认妈」成风、自称小狗谄媚 |
| 麻麻 | 「妈妈」谐音网语，瓦学弟认妈语境里的温柔大家长 |

> 如有梗义解读与你的理解不同，欢迎在 `测试题目.md` / `personas.md` 里自行替换文案。
> If any meme reading feels off, feel free to edit the copy in `测试题目.md` / `personas.md`.

---

## 📜 许可证 / License

本项目当前**未设定开源许可证**。代码与文案仅供学习、娱乐与二次创作参考；如需商用、转载或改编，请先联系作者并取得许可。

This project currently has **no open-source license**. Code and text are provided for learning, entertainment, and remix reference only. For commercial use, reposting, or adaptation, please contact the author first.

---

<p align="center">Made with 🤪 for meme lovers · 仅供娱乐</p>
