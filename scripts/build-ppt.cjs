/**
 * 项目汇报 PPT 生成脚本
 * 主题：大语言模型气象业务应用平台
 * 配色：深海蓝主色 #0F4C81 · 冰蓝辅色 #CADCFC · 暖橙强调 #D97757
 * 字体：标题 Microsoft YaHei · 正文 Microsoft YaHei
 */
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625
pres.title = "大语言模型气象业务应用平台 — 项目汇报";
pres.author = "Jul1en_lin";

// ===== 设计令牌 =====
const C = {
  primary: "0F4C81",   // 深海蓝 - 主色
  secondary: "CADCFC", // 冰蓝 - 辅色
  accent: "D97757",    // 暖橙 - 强调
  bg: "FAFAFA",        // 浅灰白背景
  dark: "1A1A2E",      // 深色文字
  muted: "6B7280",     // 次要文字
  white: "FFFFFF",
};

const FONT = {
  heading: "Microsoft YaHei",
  body: "Microsoft YaHei",
};

const SZ = {
  hero: 44,
  title: 32,
  subtitle: 20,
  body: 14,
  caption: 12,
  stat: 56,
};

// ===== 辅助：圆角卡片 =====
function addCard(slide, x, y, w, h, opts = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: opts.fill || C.white },
    rectRadius: 0.08,
    shadow: opts.shadow !== false ? {
      type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08
    } : undefined,
  });
}

// ===== 辅助：章节标题 =====
function addSectionHeader(slide, num, title) {
  // 编号标签（圆角矩形背景）
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 0.4, w: 0.55, h: 0.32,
    fill: { color: C.accent }, rectRadius: 0.06,
  });
  slide.addText(num, {
    x: 0.5, y: 0.4, w: 0.55, h: 0.32,
    fontSize: SZ.caption, fontFace: FONT.heading, color: C.white,
    bold: true, align: "center", valign: "middle", margin: 0,
  });
  // 标题
  slide.addText(title, {
    x: 1.2, y: 0.35, w: 8, h: 0.45,
    fontSize: SZ.title, fontFace: FONT.heading, color: C.dark,
    bold: true, margin: 0, valign: "middle",
  });
}

// ============================================================
// SLIDE 1 — 封面
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.primary };

  // 左侧装饰色块
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.15, h: 5.625,
    fill: { color: C.accent },
  });

  // 英文标签
  s.addText("Meteo LLM Platform", {
    x: 0.6, y: 1.6, w: 8, h: 0.4,
    fontSize: SZ.subtitle, fontFace: FONT.heading, color: C.secondary,
    margin: 0,
  });

  // 主标题
  s.addText("大语言模型气象\n业务应用平台", {
    x: 0.6, y: 2.1, w: 7, h: 1.4,
    fontSize: SZ.hero, fontFace: FONT.heading, color: C.white,
    bold: true, margin: 0, lineSpacing: 36,
  });

  // 副标题
  s.addText("基于 Vue 3 + FastAPI 的智能气象问答系统", {
    x: 0.6, y: 3.6, w: 8, h: 0.35,
    fontSize: SZ.body, fontFace: FONT.body, color: C.secondary,
    margin: 0,
  });

  // 底部信息
  s.addText("项目汇报  |  2026年4月", {
    x: 0.6, y: 4.9, w: 5, h: 0.3,
    fontSize: SZ.caption, fontFace: FONT.body, color: "A0B4D0",
    margin: 0,
  });
}

// ============================================================
// SLIDE 2 — 项目概述
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  addSectionHeader(s, "01", "项目概述");

  // 核心定位 — 大卡片
  addCard(s, 0.5, 1.1, 9, 1.6, { fill: C.white });
  s.addText("项目定位", {
    x: 0.75, y: 1.25, w: 2, h: 0.3,
    fontSize: SZ.caption, fontFace: FONT.heading, color: C.accent,
    bold: true, margin: 0,
  });
  s.addText("将通用大语言模型转化为具备气象专业知识的智能业务助手，支持多模型切换、知识库增强与实时天气工具调用，为气象业务人员提供高效、准确的智能问答服务。", {
    x: 0.75, y: 1.6, w: 8.5, h: 0.9,
    fontSize: SZ.body, fontFace: FONT.body, color: C.dark,
    margin: 0, lineSpacing: 22,
  });

  // 四个要点 — 小卡片网格
  const highlights = [
    { title: "前后端分离", desc: "Vue 3 SPA + FastAPI 后端" },
    { title: "多模型支持", desc: "Kimi / DeepSeek / MiniMax / Ollama" },
    { title: "流式对话", desc: "SSE 实时输出 + Markdown 渲染" },
    { title: "Apple 风格 UI", desc: "原生 CSS 设计令牌 + 玻璃态背景" },
  ];
  highlights.forEach((item, i) => {
    const x = 0.5 + (i % 2) * 4.55;
    const y = 3.0 + Math.floor(i / 2) * 1.2;
    addCard(s, x, y, 4.4, 1.05, { fill: C.white });
    s.addText(item.title, {
      x: x + 0.2, y: y + 0.15, w: 4, h: 0.3,
      fontSize: SZ.subtitle - 2, fontFace: FONT.heading, color: C.dark,
      bold: true, margin: 0,
    });
    s.addText(item.desc, {
      x: x + 0.2, y: y + 0.52, w: 4, h: 0.35,
      fontSize: SZ.body, fontFace: FONT.body, color: C.muted,
      margin: 0,
    });
  });
}

// ============================================================
// SLIDE 3 — 核心功能
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  addSectionHeader(s, "02", "核心功能");

  const features = [
    {
      title: "智能对话",
      desc: "多轮对话上下文记忆，SSE 流式输出，前端支持 Markdown 渲染与代码高亮",
      color: C.primary,
    },
    {
      title: "多模型切换",
      desc: "支持 Kimi K2.5、DeepSeek Reasoner、MiniMax-M2.5、Ollama 本地模型一键切换",
      color: C.accent,
    },
    {
      title: "气象知识库",
      desc: "术语库与预警信号库通过 SQL 查询注入 Prompt，增强模型回答专业性",
      color: C.primary,
    },
    {
      title: "工具调用",
      desc: "天气实时查询（Tavily 搜索增强）、气象预警查询（QWeather API 实时数据）",
      color: C.accent,
    },
  ];

  features.forEach((f, i) => {
    const x = 0.5 + (i % 2) * 4.55;
    const y = 1.15 + Math.floor(i / 2) * 2.1;
    addCard(s, x, y, 4.4, 1.9, { fill: C.white });

    // 左侧色条
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.2, y: y + 0.25, w: 0.06, h: 0.45,
      fill: { color: f.color },
    });

    s.addText(f.title, {
      x: x + 0.4, y: y + 0.22, w: 3.8, h: 0.4,
      fontSize: SZ.subtitle, fontFace: FONT.heading, color: C.dark,
      bold: true, margin: 0,
    });
    s.addText(f.desc, {
      x: x + 0.25, y: y + 0.75, w: 3.9, h: 0.9,
      fontSize: SZ.body, fontFace: FONT.body, color: C.muted,
      margin: 0, lineSpacing: 20,
    });
  });
}

// ============================================================
// SLIDE 4 — 技术架构
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  addSectionHeader(s, "03", "技术架构");

  const layers = [
    {
      label: "前端",
      color: C.primary,
      items: ["Vue 3 Composition API", "Vite + TypeScript", "Pinia 状态管理", "Vue Router", "原生 CSS Apple 风格"],
    },
    {
      label: "后端",
      color: C.accent,
      items: ["FastAPI + Uvicorn", "LangChain LLM 编排", "SQLAlchemy 2.0 ORM", "Pydantic 数据校验", "SSE 流式封装"],
    },
    {
      label: "数据/模型",
      color: "0D9488",
      items: ["SQLite", "Tavily 天气搜索", "QWeather 实时预警", "Session-Cookie 认证", "OpenAPI 3.0 规范"],
    },
  ];

  layers.forEach((layer, i) => {
    const x = 0.5 + i * 3.07;
    const y = 1.1;
    const w = 2.95;
    const h = 4.0;

    addCard(s, x, y, w, h, { fill: C.white });

    // 顶部色条
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h: 0.12,
      fill: { color: layer.color },
    });

    s.addText(layer.label, {
      x: x + 0.2, y: y + 0.3, w: w - 0.4, h: 0.4,
      fontSize: SZ.subtitle, fontFace: FONT.heading, color: C.dark,
      bold: true, margin: 0,
    });

    layer.items.forEach((item, idx) => {
      s.addShape(pres.shapes.OVAL, {
        x: x + 0.25, y: y + 0.95 + idx * 0.6, w: 0.08, h: 0.08,
        fill: { color: layer.color },
      });
      s.addText(item, {
        x: x + 0.45, y: y + 0.88 + idx * 0.6, w: w - 0.65, h: 0.35,
        fontSize: SZ.body, fontFace: FONT.body, color: C.dark,
        margin: 0, valign: "middle",
      });
    });
  });
}

// ============================================================
// SLIDE 5 — 数据库设计
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  addSectionHeader(s, "04", "数据库设计");

  const tables = [
    { name: "users", desc: "用户表：用户名 + bcrypt 密码哈希", rows: "用户数据" },
    { name: "conversations", desc: "对话表：UUID 主键、用户外键、模型 ID、标题", rows: "对话记录" },
    { name: "messages", desc: "消息表：角色、内容、工具调用 JSON", rows: "消息历史" },
    { name: "terms", desc: "气象术语库：术语名、分类、释义、来源", rows: "术语数据" },
    { name: "alerts", desc: "预警信号库：类型、级别、发布标准、防御指南", rows: "预警数据" },
  ];

  // 表头
  addCard(s, 0.5, 1.1, 9, 0.5, { fill: C.primary, shadow: false });
  s.addText("表名", {
    x: 0.7, y: 1.15, w: 1.8, h: 0.35,
    fontSize: SZ.body, fontFace: FONT.heading, color: C.white,
    bold: true, margin: 0, valign: "middle",
  });
  s.addText("说明", {
    x: 2.6, y: 1.15, w: 5.5, h: 0.35,
    fontSize: SZ.body, fontFace: FONT.heading, color: C.white,
    bold: true, margin: 0, valign: "middle",
  });

  tables.forEach((t, i) => {
    const y = 1.65 + i * 0.7;
    const isEven = i % 2 === 0;
    addCard(s, 0.5, y, 9, 0.65, { fill: isEven ? C.white : "F8F9FA", shadow: false });

    s.addText(t.name, {
      x: 0.7, y: y + 0.12, w: 1.8, h: 0.35,
      fontSize: SZ.body, fontFace: FONT.body, color: C.accent,
      bold: true, margin: 0, valign: "middle",
    });
    s.addText(t.desc, {
      x: 2.6, y: y + 0.12, w: 6.5, h: 0.35,
      fontSize: SZ.body, fontFace: FONT.body, color: C.dark,
      margin: 0, valign: "middle",
    });
  });
}

// ============================================================
// SLIDE 6 — API 接口
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  addSectionHeader(s, "05", "API 接口设计");

  const apis = [
    { method: "POST", path: "/api/v1/auth/login", desc: "用户登录（Session-Cookie）" },
    { method: "POST", path: "/api/v1/auth/logout", desc: "用户登出" },
    { method: "GET", path: "/api/v1/assistant/models", desc: "获取可用模型列表" },
    { method: "GET", path: "/api/v1/assistant/knowledge-bases", desc: "获取知识库列表" },
    { method: "GET", path: "/api/v1/assistant/tools", desc: "获取工具列表" },
    { method: "POST", path: "/api/v1/assistant/chat/stream", desc: "流式对话（SSE）" },
    { method: "GET", path: "/api/v1/assistant/conversations", desc: "获取对话列表" },
    { method: "POST", path: "/api/v1/assistant/conversations", desc: "创建新对话" },
    { method: "GET", path: "/api/v1/assistant/conversations/{id}", desc: "获取对话详情" },
    { method: "PUT", path: "/api/v1/assistant/conversations/{id}", desc: "重命名对话" },
    { method: "DELETE", path: "/api/v1/assistant/conversations/{id}", desc: "删除对话" },
  ];

  // 表头
  addCard(s, 0.5, 1.1, 9, 0.45, { fill: C.primary, shadow: false });
  s.addText("方法", { x: 0.7, y: 1.13, w: 1.0, h: 0.3, fontSize: SZ.caption, fontFace: FONT.heading, color: C.white, bold: true, margin: 0, valign: "middle" });
  s.addText("路径", { x: 1.8, y: 1.13, w: 4.5, h: 0.3, fontSize: SZ.caption, fontFace: FONT.heading, color: C.white, bold: true, margin: 0, valign: "middle" });
  s.addText("说明", { x: 6.4, y: 1.13, w: 2.8, h: 0.3, fontSize: SZ.caption, fontFace: FONT.heading, color: C.white, bold: true, margin: 0, valign: "middle" });

  apis.forEach((api, i) => {
    const y = 1.58 + i * 0.36;
    const isEven = i % 2 === 0;
    addCard(s, 0.5, y, 9, 0.35, { fill: isEven ? C.white : "F8F9FA", shadow: false });

    const methodColor = api.method === "GET" ? "0D9488" : api.method === "POST" ? C.accent : api.method === "PUT" ? C.primary : "DC2626";
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.65, y: y + 0.06, w: 0.9, h: 0.22,
      fill: { color: methodColor }, rectRadius: 0.04,
    });
    s.addText(api.method, {
      x: 0.65, y: y + 0.06, w: 0.9, h: 0.22,
      fontSize: 10, fontFace: FONT.body, color: C.white,
      bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(api.path, {
      x: 1.8, y: y + 0.04, w: 4.5, h: 0.27,
      fontSize: 11, fontFace: FONT.body, color: C.dark,
      margin: 0, valign: "middle",
    });
    s.addText(api.desc, {
      x: 6.4, y: y + 0.04, w: 2.8, h: 0.27,
      fontSize: 11, fontFace: FONT.body, color: C.muted,
      margin: 0, valign: "middle",
    });
  });
}

// ============================================================
// SLIDE 7 — 关键数字
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.primary };

  // 左侧装饰条
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.15, h: 5.625,
    fill: { color: C.accent },
  });

  s.addText("关键数字", {
    x: 0.6, y: 0.5, w: 5, h: 0.5,
    fontSize: SZ.title, fontFace: FONT.heading, color: C.white,
    bold: true, margin: 0,
  });

  const stats = [
    { num: "4", label: "大语言模型", sub: "Kimi / DeepSeek / MiniMax / Ollama" },
    { num: "5", label: "数据库表", sub: "用户 / 对话 / 消息 / 术语 / 预警" },
    { num: "11", label: "API 接口", sub: "RESTful + SSE 流式对话" },
    { num: "2", label: "知识库", sub: "气象术语库 + 预警信号库" },
  ];

  stats.forEach((st, i) => {
    const x = 0.6 + (i % 2) * 4.5;
    const y = 1.4 + Math.floor(i / 2) * 1.9;

    addCard(s, x, y, 4.25, 1.7, { fill: "FFFFFF" });

    s.addText(st.num, {
      x: x + 0.25, y: y + 0.2, w: 2, h: 0.7,
      fontSize: SZ.stat, fontFace: FONT.heading, color: C.accent,
      bold: true, margin: 0, valign: "top",
    });
    s.addText(st.label, {
      x: x + 0.25, y: y + 0.95, w: 3.8, h: 0.3,
      fontSize: SZ.subtitle - 2, fontFace: FONT.heading, color: C.dark,
      bold: true, margin: 0,
    });
    s.addText(st.sub, {
      x: x + 0.25, y: y + 1.3, w: 3.8, h: 0.25,
      fontSize: SZ.caption, fontFace: FONT.body, color: C.muted,
      margin: 0,
    });
  });
}

// ============================================================
// SLIDE 8 — 已实现功能
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  addSectionHeader(s, "06", "已实现功能");

  const items = [
    "用户登录 / 登出（Session-Cookie 认证）",
    "智能助手对话界面（流式输出、Markdown 渲染、代码高亮）",
    "多模型切换（Kimi K2.5 / DeepSeek Reasoner / MiniMax-M2.5 / Ollama）",
    "对话历史管理（创建、切换、重命名、删除）",
    "气象术语知识库（SQL 查询注入 Prompt 增强）",
    "预警信号知识库（QWeather 实时 API + SQL 查询注入）",
    "天气查询工具（Tavily 搜索 + 查询词增强）",
    "当前日期动态注入（System Prompt 自动追加）",
    "前端消息 Markdown 渲染 + 代码高亮",
    "响应式布局适配",
  ];

  const leftItems = items.slice(0, 5);
  const rightItems = items.slice(5);

  [leftItems, rightItems].forEach((col, colIdx) => {
    const baseX = 0.5 + colIdx * 4.6;
    col.forEach((item, i) => {
      const y = 1.2 + i * 0.85;
      addCard(s, baseX, y, 4.4, 0.7, { fill: C.white, shadow: false });

      s.addShape(pres.shapes.OVAL, {
        x: baseX + 0.2, y: y + 0.22, w: 0.14, h: 0.14,
        fill: { color: C.accent },
      });
      s.addText("✓", {
        x: baseX + 0.2, y: y + 0.19, w: 0.14, h: 0.2,
        fontSize: 10, fontFace: FONT.body, color: C.white,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(item, {
        x: baseX + 0.5, y: y + 0.1, w: 3.7, h: 0.45,
        fontSize: SZ.body - 1, fontFace: FONT.body, color: C.dark,
        margin: 0, valign: "middle",
      });
    });
  });
}

// ============================================================
// SLIDE 9 — 结语
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.primary };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.15, h: 5.625,
    fill: { color: C.accent },
  });

  s.addText("让 AI 看得懂天气", {
    x: 0.6, y: 2.0, w: 8, h: 0.8,
    fontSize: SZ.hero, fontFace: FONT.heading, color: C.white,
    bold: true, margin: 0,
  });

  s.addText("术语 · 预警 · 实时数据 · 流式对话", {
    x: 0.6, y: 2.9, w: 8, h: 0.35,
    fontSize: SZ.subtitle, fontFace: FONT.body, color: C.secondary,
    margin: 0,
  });

  s.addText("Thanks for watching", {
    x: 0.6, y: 4.5, w: 5, h: 0.3,
    fontSize: SZ.body, fontFace: FONT.body, color: "A0B4D0",
    italic: true, margin: 0,
  });
}

// ============================================================
pres.writeFile({ fileName: "项目汇报.pptx" }).then(name => {
  console.log("✓ generated:", name);
});
