const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Jul1en_lin';
pres.title = '大语言模型气象业务应用平台';
pres.subject = '项目汇报';

// ===== Color Palette: Ocean Gradient =====
const C = {
  deepBlue: "065A82",
  teal: "1C7293",
  midnight: "21295C",
  lightCyan: "E0F7FA",
  white: "FFFFFF",
  offWhite: "F0F4F8",
  textDark: "1E293B",
  textGray: "64748B",
};

// ===== Helper: fresh shadow factory =====
const makeShadow = (opacity = 0.12) => ({
  type: "outer",
  blur: 8,
  offset: 3,
  angle: 135,
  color: "000000",
  opacity,
});

// ===== Helper: card shape factory =====
const makeCard = (x, y, w, h, fillColor = C.white) => ({
  shape: pres.shapes.RECTANGLE,
  x, y, w, h,
  fill: { color: fillColor },
  shadow: makeShadow(0.1),
});

// ============================================
// SLIDE 1: Title
// ============================================
let s1 = pres.addSlide();
s1.background = { color: C.midnight };

// Decorative accent bar on left
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: C.teal },
});

s1.addText("大语言模型气象业务应用平台", {
  x: 1, y: 1.6, w: 8, h: 1,
  fontSize: 40,
  fontFace: "Arial",
  color: C.white,
  bold: true,
  align: "left",
  valign: "middle",
});

s1.addText("项目汇报", {
  x: 1, y: 2.7, w: 8, h: 0.6,
  fontSize: 22,
  fontFace: "Arial",
  color: C.teal,
  align: "left",
  valign: "middle",
});

s1.addText("基于 Vue 3 + FastAPI 的智能气象问答系统", {
  x: 1, y: 3.3, w: 8, h: 0.5,
  fontSize: 14,
  fontFace: "Calibri",
  color: "94A3B8",
  align: "left",
  valign: "middle",
});

// ============================================
// SLIDE 2: Project Overview
// ============================================
let s2 = pres.addSlide();
s2.background = { color: C.offWhite };

s2.addText("项目概述", {
  x: 0.5, y: 0.4, w: 9, h: 0.7,
  fontSize: 32,
  fontFace: "Arial",
  color: C.midnight,
  bold: true,
  valign: "middle",
});

s2.addText("面向气象业务的大语言模型智能应用平台，采用前后端分离架构，提供智能气象问答对话界面。", {
  x: 0.5, y: 1.1, w: 9, h: 0.6,
  fontSize: 14,
  fontFace: "Calibri",
  color: C.textDark,
  valign: "middle",
});

// 5 feature cards
const features = [
  { title: "智能对话", desc: "多轮对话 · SSE流式输出 · 4模型可选" },
  { title: "知识库", desc: "气象术语库 · 预警信号库 · SQL注入Prompt" },
  { title: "工具调用", desc: "天气实时查询 · 气象预警查询 · API增强" },
  { title: "对话管理", desc: "创建 · 切换 · 重命名 · 删除 · 历史持久化" },
  { title: "用户认证", desc: "Session-Cookie 登录认证 · 状态持久化" },
];

const cardW = 2.8;
const cardH = 1.6;
const startX = 0.5;
const gap = 0.35;
const row1Y = 2.0;
const row2Y = 3.8;

// Row 1: 3 cards
for (let i = 0; i < 3; i++) {
  const x = startX + i * (cardW + gap);
  s2.addShape(makeCard(x, row1Y, cardW, cardH).shape, {
    x, y: row1Y, w: cardW, h: cardH,
    fill: { color: C.white },
    shadow: makeShadow(0.1),
  });
  s2.addShape(pres.shapes.RECTANGLE, {
    x, y: row1Y, w: 0.08, h: cardH,
    fill: { color: C.teal },
  });
  s2.addText(features[i].title, {
    x: x + 0.25, y: row1Y + 0.2, w: cardW - 0.4, h: 0.4,
    fontSize: 16,
    fontFace: "Arial",
    color: C.midnight,
    bold: true,
    valign: "middle",
    margin: 0,
  });
  s2.addText(features[i].desc, {
    x: x + 0.25, y: row1Y + 0.65, w: cardW - 0.4, h: 0.8,
    fontSize: 12,
    fontFace: "Calibri",
    color: C.textGray,
    valign: "top",
    margin: 0,
  });
}

// Row 2: 2 cards (centered)
for (let i = 0; i < 2; i++) {
  const x = startX + 0.6 + i * (cardW + gap);
  s2.addShape(makeCard(x, row2Y, cardW, cardH).shape, {
    x, y: row2Y, w: cardW, h: cardH,
    fill: { color: C.white },
    shadow: makeShadow(0.1),
  });
  s2.addShape(pres.shapes.RECTANGLE, {
    x, y: row2Y, w: 0.08, h: cardH,
    fill: { color: C.deepBlue },
  });
  s2.addText(features[i + 3].title, {
    x: x + 0.25, y: row2Y + 0.2, w: cardW - 0.4, h: 0.4,
    fontSize: 16,
    fontFace: "Arial",
    color: C.midnight,
    bold: true,
    valign: "middle",
    margin: 0,
  });
  s2.addText(features[i + 3].desc, {
    x: x + 0.25, y: row2Y + 0.65, w: cardW - 0.4, h: 0.8,
    fontSize: 12,
    fontFace: "Calibri",
    color: C.textGray,
    valign: "top",
    margin: 0,
  });
}

// ============================================
// SLIDE 3: Tech Stack
// ============================================
let s3 = pres.addSlide();
s3.background = { color: C.white };

s3.addText("技术栈", {
  x: 0.5, y: 0.4, w: 9, h: 0.7,
  fontSize: 32,
  fontFace: "Arial",
  color: C.midnight,
  bold: true,
  valign: "middle",
});

// Left column: Frontend
s3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.3, w: 4.3, h: 3.8,
  fill: { color: C.offWhite },
});
s3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.3, w: 4.3, h: 0.5,
  fill: { color: C.deepBlue },
});
s3.addText("前端", {
  x: 0.5, y: 1.3, w: 4.3, h: 0.5,
  fontSize: 18,
  fontFace: "Arial",
  color: C.white,
  bold: true,
  align: "center",
  valign: "middle",
  margin: 0,
});

const frontendItems = [
  "Vue 3 + Vite + TypeScript",
  "Composition API，严格模式",
  "Pinia 状态管理",
  "Vue Router history 模式",
  "原生 CSS（Apple 风格）",
];
s3.addText(
  frontendItems.map((t, i) => ({
    text: t,
    options: { bullet: true, breakLine: i < frontendItems.length - 1 },
  })),
  { x: 0.8, y: 2.1, w: 3.7, h: 2.8, fontSize: 14, fontFace: "Calibri", color: C.textDark, valign: "top" }
);

// Right column: Backend
s3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.3, w: 4.3, h: 3.8,
  fill: { color: C.offWhite },
});
s3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.3, w: 4.3, h: 0.5,
  fill: { color: C.teal },
});
s3.addText("后端", {
  x: 5.2, y: 1.3, w: 4.3, h: 0.5,
  fontSize: 18,
  fontFace: "Arial",
  color: C.white,
  bold: true,
  align: "center",
  valign: "middle",
  margin: 0,
});

const backendItems = [
  "FastAPI + Uvicorn (Python >= 3.10)",
  "SQLAlchemy 2.0 + SQLite",
  "LangChain 多模型编排",
  "Moonshot / DeepSeek / MiniMax / Ollama",
  "Tavily + QWeather API",
];
s3.addText(
  backendItems.map((t, i) => ({
    text: t,
    options: { bullet: true, breakLine: i < backendItems.length - 1 },
  })),
  { x: 5.5, y: 2.1, w: 3.7, h: 2.8, fontSize: 14, fontFace: "Calibri", color: C.textDark, valign: "top" }
);

// ============================================
// SLIDE 4: Core Features
// ============================================
let s4 = pres.addSlide();
s4.background = { color: C.offWhite };

s4.addText("核心功能", {
  x: 0.5, y: 0.4, w: 9, h: 0.7,
  fontSize: 32,
  fontFace: "Arial",
  color: C.midnight,
  bold: true,
  valign: "middle",
});

// Three feature blocks side by side
const coreFeatures = [
  {
    title: "智能对话",
    items: ["多轮上下文", "SSE 流式输出", "4 个模型可选", "Markdown 渲染"],
    color: C.deepBlue,
  },
  {
    title: "知识库增强",
    items: ["气象术语库", "预警信号库", "SQL 注入 Prompt", "动态日期注入"],
    color: C.teal,
  },
  {
    title: "工具调用",
    items: ["天气实时查询", "气象预警查询", "Tavily 搜索增强", "QWeather API"],
    color: C.midnight,
  },
];

const fW = 2.8;
const fH = 3.2;
const fGap = 0.4;
const fStartX = 0.5;
const fY = 1.3;

for (let i = 0; i < 3; i++) {
  const x = fStartX + i * (fW + fGap);
  s4.addShape(pres.shapes.RECTANGLE, {
    x, y: fY, w: fW, h: fH,
    fill: { color: C.white },
    shadow: makeShadow(0.1),
  });
  // Top colored bar
  s4.addShape(pres.shapes.RECTANGLE, {
    x, y: fY, w: fW, h: 0.5,
    fill: { color: coreFeatures[i].color },
  });
  s4.addText(coreFeatures[i].title, {
    x, y: fY, w: fW, h: 0.5,
    fontSize: 16,
    fontFace: "Arial",
    color: C.white,
    bold: true,
    align: "center",
    valign: "middle",
    margin: 0,
  });
  s4.addText(
    coreFeatures[i].items.map((t, j) => ({
      text: t,
      options: { bullet: true, breakLine: j < coreFeatures[i].items.length - 1 },
    })),
    { x: x + 0.2, y: fY + 0.7, w: fW - 0.4, h: 2.2, fontSize: 14, fontFace: "Calibri", color: C.textDark, valign: "top" }
  );
}

// ============================================
// SLIDE 5: Architecture
// ============================================
let s5 = pres.addSlide();
s5.background = { color: C.white };

s5.addText("系统架构", {
  x: 0.5, y: 0.4, w: 9, h: 0.7,
  fontSize: 32,
  fontFace: "Arial",
  color: C.midnight,
  bold: true,
  valign: "middle",
});

// Architecture diagram boxes
// Frontend box
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.5, w: 4, h: 2.2,
  fill: { color: C.lightCyan },
  shadow: makeShadow(0.08),
});
s5.addText("前端 (Vue 3 SPA)", {
  x: 0.5, y: 1.5, w: 4, h: 0.5,
  fontSize: 16,
  fontFace: "Arial",
  color: C.deepBlue,
  bold: true,
  align: "center",
  valign: "middle",
  margin: 0,
});
s5.addText(
  ["登录/对话界面", "Pinia 状态管理", "localStorage 持久化"].map((t, i, arr) => ({
    text: t,
    options: { bullet: true, breakLine: i < arr.length - 1 },
  })),
  { x: 0.7, y: 2.1, w: 3.6, h: 1.4, fontSize: 13, fontFace: "Calibri", color: C.textDark, valign: "top" }
);

// Arrow between frontend and backend
s5.addShape(pres.shapes.LINE, {
  x: 4.6, y: 2.6, w: 0.8, h: 0,
  line: { color: C.teal, width: 2, endArrowType: "arrow" },
});
s5.addText("REST / SSE", {
  x: 4.5, y: 2.75, w: 1, h: 0.3,
  fontSize: 10,
  fontFace: "Calibri",
  color: C.textGray,
  align: "center",
  margin: 0,
});

// Backend box
s5.addShape(pres.shapes.RECTANGLE, {
  x: 5.5, y: 1.5, w: 4, h: 2.2,
  fill: { color: C.lightCyan },
  shadow: makeShadow(0.08),
});
s5.addText("后端 (FastAPI)", {
  x: 5.5, y: 1.5, w: 4, h: 0.5,
  fontSize: 16,
  fontFace: "Arial",
  color: C.deepBlue,
  bold: true,
  align: "center",
  valign: "middle",
  margin: 0,
});
s5.addText(
  ["LangChain 模型编排", "知识库检索", "天气/预警工具", "SQLite 持久化"].map((t, i, arr) => ({
    text: t,
    options: { bullet: true, breakLine: i < arr.length - 1 },
  })),
  { x: 5.7, y: 2.1, w: 3.6, h: 1.4, fontSize: 13, fontFace: "Calibri", color: C.textDark, valign: "top" }
);

// External APIs box below
s5.addShape(pres.shapes.RECTANGLE, {
  x: 2.5, y: 4.2, w: 5, h: 1,
  fill: { color: C.offWhite },
  shadow: makeShadow(0.08),
});
s5.addText("外部 API：Moonshot · DeepSeek · MiniMax · Ollama · Tavily · QWeather", {
  x: 2.5, y: 4.2, w: 5, h: 1,
  fontSize: 12,
  fontFace: "Calibri",
  color: C.textGray,
  align: "center",
  valign: "middle",
  margin: 0,
});

// Connecting lines from backend to APIs
s5.addShape(pres.shapes.LINE, {
  x: 5.5, y: 3.7, w: 0, h: 0.5,
  line: { color: C.teal, width: 1.5, dashType: "dash" },
});
s5.addShape(pres.shapes.LINE, {
  x: 7.5, y: 3.7, w: 0, h: 0.5,
  line: { color: C.teal, width: 1.5, dashType: "dash" },
});
s5.addShape(pres.shapes.LINE, {
  x: 5.5, y: 4.2, w: 2, h: 0,
  line: { color: C.teal, width: 1.5 },
});

// ============================================
// SLIDE 6: Feature Checklist
// ============================================
let s6 = pres.addSlide();
s6.background = { color: C.offWhite };

s6.addText("已实现功能", {
  x: 0.5, y: 0.4, w: 9, h: 0.7,
  fontSize: 32,
  fontFace: "Arial",
  color: C.midnight,
  bold: true,
  valign: "middle",
});

// Left column
const leftItems = [
  "用户登录 / 登出（Session-Cookie）",
  "智能助手对话界面（流式输出）",
  "Markdown 渲染 + 代码高亮",
  "多模型切换（4 个模型）",
  "对话历史管理",
];
const rightItems = [
  "气象术语知识库",
  "预警信号知识库",
  "天气查询工具（Tavily）",
  "实时预警查询（QWeather）",
  "响应式布局",
];

s6.addText(
  leftItems.map((t, i) => ({
    text: t,
    options: { bullet: true, breakLine: i < leftItems.length - 1 },
  })),
  { x: 0.5, y: 1.3, w: 4.3, h: 3.5, fontSize: 15, fontFace: "Calibri", color: C.textDark, valign: "top" }
);

s6.addText(
  rightItems.map((t, i) => ({
    text: t,
    options: { bullet: true, breakLine: i < rightItems.length - 1 },
  })),
  { x: 5.2, y: 1.3, w: 4.3, h: 3.5, fontSize: 15, fontFace: "Calibri", color: C.textDark, valign: "top" }
);

// ============================================
// SLIDE 7: Closing
// ============================================
let s7 = pres.addSlide();
s7.background = { color: C.midnight };

s7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: C.teal },
});

s7.addText("谢谢", {
  x: 1, y: 1.8, w: 8, h: 1,
  fontSize: 48,
  fontFace: "Arial",
  color: C.white,
  bold: true,
  align: "left",
  valign: "middle",
});

s7.addText("大语言模型气象业务应用平台", {
  x: 1, y: 2.9, w: 8, h: 0.6,
  fontSize: 18,
  fontFace: "Calibri",
  color: C.teal,
  align: "left",
  valign: "middle",
});

// Save
pres.writeFile({ fileName: "项目汇报.pptx" })
  .then(() => console.log("PPT generated: 项目汇报.pptx"))
  .catch((err) => console.error("Error:", err));
