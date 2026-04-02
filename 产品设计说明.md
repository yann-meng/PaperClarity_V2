# PaperClarity 产品设计说明

## 1. 产品定位

PaperClarity 是一款面向研究者、工程师、学生与论文复现者的本地优先论文理解工具。它的核心目标不是“简单做一个 PDF 阅读器 + 聊天框”，而是构建一个“可插拔的论文理解工作台”：

* 左侧：论文加载、渲染、定位、段落/公式/图表选择
* 右侧：大模型理解与推理区
* 中间能力层：文档解析、结构识别、上下文构建、Prompt 编排、结果缓存
* 上层能力：论文总览、段落精读、公式拆解、实验分析、复现指南，以及后续可持续扩展的技能组件（skills）

设计原则：

1. **本地优先**：论文从本地加载，优先在本地完成文件解析、切块、索引与缓存。
2. **模型可替换**：支持 OpenAI 兼容接口、本地模型（如 vLLM / Ollama）或其他推理后端。
3. **组件解耦**：每项能力都以 skill/component 的方式独立实现，统一注册、自动发现、动态加载。
4. **可解释**：回答尽可能带来源锚点（页码、段落编号、公式编号、图表编号）。
5. **围绕论文任务流设计**：不是泛问答，而是按“读懂 → 深读 → 分析 → 复现 → 做笔记”闭环组织功能。

---

## 2. 用户画像与典型使用场景

### 2.1 用户画像

* 论文初读者：想快速理解论文讲了什么
* 研究生 / 博士：要读相关工作、方法、实验并做比较
* 工程复现者：需要从论文中提取可执行步骤
* 面试 / 汇报准备者：需要快速形成结构化理解
* 团队研究负责人：需要组织多人阅读与沉淀

### 2.2 核心场景

1. 打开一篇论文，先获得全局理解
2. 选中一个段落，要求逐句精读
3. 选中一个公式，要求逐项解释变量含义，并把公式翻译为直觉
4. 查看实验章节，分析对比实验、消融实验、指标设置、潜在缺陷
5. 让系统生成“复现指南”：环境、数据、训练流程、坑点、待确认项
6. 对关键段落添加笔记，后续导出为 Markdown / JSON / study note

---

## 3. 产品目标

### 3.1 核心目标

构建一个桌面/本地 Web 论文理解平台，满足：

* 本地加载 PDF、Markdown、TXT、HTML、LaTeX 等论文源文件
* 左侧文档视图 + 右侧模型交互区的双栏结构
* 面向论文任务的技能组件系统
* 支持段落级、公式级、图表级、章节级交互
* 支持上下文感知 Prompt 编排
* 支持多模型、多插件扩展

### 3.2 非目标

第一阶段不强求：

* 完整多人协作系统
* 云端论文库运营
* 全自动高精度 OCR 引擎自研
* 完整文献管理器替代品（如 Zotero 全套功能）

---

## 4. 功能设计

## 4.1 文档加载与显示

### 支持格式

* PDF
* TXT
* Markdown
* HTML
* LaTeX 源文件（优先解析 tex 主文件）
* 可扩展：DOCX、EPUB

### 左侧阅读区功能

* 显示论文内容
* PDF 页码跳转
* 缩放、搜索、目录导航
* 文本选择（段落 / 跨段）
* 公式区域选择（初期可通过文本或块级定位实现）
* 图表区域定位（图题、表题、引用定位）
* 高亮当前模型回答引用到的段落
* 点击右侧回答中的锚点，左侧自动滚动定位

### 推荐实现方式

* 前端：React + TypeScript
* PDF 渲染：PDF.js
* 富文本文档：统一转成内部 `DocumentModel`
* 页面与块映射：保存 `page -> block_ids`、`block_id -> source_range`

---

## 4.2 右侧大模型专属区域

右侧不是简单聊天框，而是“任务驱动的论文助手面板”。

### UI 区块建议

1. **模式切换栏**

   * 总览
   * 段落精读
   * 公式拆解
   * 实验分析
   * 复现指南
   * 自定义 Prompt

2. **上下文来源栏**

   * 当前整篇论文
   * 当前章节
   * 当前选中段落
   * 当前选中公式
   * 当前选中图表
   * 用户附加上下文

3. **对话主区域**

   * 展示模型输出
   * 折叠显示中间推理结构（非 chain of thought，而是可展示的 reasoning summary）
   * 显示引用锚点（页码/块编号/章节）

4. **动作区**

   * 复制结果
   * 插入到笔记
   * 导出 Markdown
   * 保存为卡片
   * 再追问

---

## 4.3 大模型功能设计

### 4.3.1 总控 Prompt：理解整篇论文

目标：让模型基于整篇论文内容输出结构化理解。

#### 输入

* 论文元信息：标题、作者、摘要
* 章节结构
* 分块后的正文
* 图表/公式索引

#### 输出建议结构

1. 一句话总结
2. 论文要解决的问题
3. 核心方法
4. 与已有方法的差异
5. 关键假设
6. 关键公式 / 模块
7. 训练或推理流程
8. 实验设置与主要结果
9. 优点
10. 局限性
11. 复现难点
12. 适合继续追问的 5 个问题

#### 总控 Prompt 模板（建议）

```text
你是一个严格、清晰、面向研究者的论文理解助手。
请基于给定论文内容，输出结构化理解结果。
要求：
1. 不要泛泛而谈；
2. 明确指出“论文试图解决什么问题”；
3. 用尽量简洁但专业的语言解释核心方法；
4. 如果论文中有关键公式或模块，请指出它们的作用；
5. 对实验结果给出结论，而不是简单复述表格；
6. 明确区分“论文中明确写出”与“你的合理推断”；
7. 尽量引用章节、页码或段落编号。

输出格式：
- 一句话总结
- 问题定义
- 方法概览
- 关键机制
- 实验结论
- 优点
- 局限
- 复现提示
- 推荐继续深挖的问题
```

---

### 4.3.2 手动选择段落：段落精读

#### 用户操作

* 左侧选择一段或多段文本
* 右侧点击“段落精读”

#### 输出建议

* 逐句解释
* 本段核心论点
* 本段与上下文关系
* 术语解释
* 隐含假设
* 可能看不懂的原因
* 通俗重述

#### Prompt 模板

```text
你现在只分析用户选中的论文段落。
请完成：
1. 用更易懂的话重述段落；
2. 逐句解释每句话在说什么；
3. 指出本段中的关键术语与其含义；
4. 说明这段在整篇论文中的作用；
5. 如果这段存在隐藏前提、简写跳步、默认知识，请补充出来；
6. 不要脱离原文臆造。
```

---

### 4.3.3 公式逐项拆解

#### 输入

* 用户选中的公式
* 公式前后文
* 符号定义出现位置

#### 输出建议

* 公式原文
* 符号表（每个符号含义、维度/形状、来源）
* 公式在做什么
* 各项如何相互作用
* 与前一公式 / 后一公式关系
* 如果是优化目标：每项损失的作用
* 如果是概率表达：每个条件项表示什么

#### Prompt 模板

```text
请对给定公式做逐项拆解：
1. 列出每个符号的含义；
2. 说明哪些符号在上下文中被定义过，哪些需要推断；
3. 解释公式整体在做什么；
4. 解释每一项对结果的影响；
5. 如果这是目标函数/更新式/概率分解，请指出其数学角色；
6. 给出一个小型直观例子帮助理解。
```

---

### 4.3.4 公式 → 直觉转换

目标：把数学表达翻译成研究者真正能“感觉到”的机制。

#### 输出建议

* 一句话直觉
* 类比解释
* 这个公式“鼓励/惩罚”什么
* 参数变化会导致什么现象
* 为什么作者需要这个公式而不是更简单的替代方案

#### Prompt 模板

```text
请把这个公式从“数学形式”翻译成“研究直觉”：
1. 它想鼓励什么、抑制什么？
2. 如果某一项变大/变小，会发生什么？
3. 这个公式背后的设计动机是什么？
4. 能否用一个非数学类比解释？
5. 给出研究者视角下的直觉总结。
```

---

### 4.3.5 实验分析

目标：不仅复述实验，而是分析实验设计是否充分。

#### 自动提取对象

* 数据集
* 评价指标
* 对比方法
* 消融项
* 主结果表格
* 可视化结果描述

#### 输出建议

* 实验目标是什么
* 实验设计是否验证了方法核心主张
* 指标是否合理
* 对比基线是否充分
* 消融实验是否覆盖关键模块
* 结果最有说服力的部分
* 可能存在的问题或偏差
* 还应补做哪些实验

#### Prompt 模板

```text
请分析论文实验部分，不要只复述结果。
重点回答：
1. 实验想验证哪些主张？
2. 每类实验分别支撑了什么结论？
3. 数据集与指标是否合理？
4. baseline 是否充分、公平？
5. 消融实验是否真的证明了各模块的必要性？
6. 是否存在统计不足、比较不公平、样本偏置、指标失真等问题？
7. 如果你是审稿人，你会追问什么？
```

---

### 4.3.6 复现指南

目标：把论文转换成工程可执行路线。

#### 输出建议

* 任务定义
* 输入输出定义
* 所需环境
* 数据准备
* 模型结构
* 训练流程
* 推理流程
* 超参数表
* 难点与不确定点
* 最小可运行版本建议
* 复现检查清单

#### Prompt 模板

```text
请为这篇论文生成一份“工程可执行”的复现指南：
1. 明确任务输入与输出；
2. 拆解训练/推理流程；
3. 提取文中已给出的关键超参数与实现细节；
4. 标注论文没有说清楚、但复现必须补全的部分；
5. 给出建议的数据结构、模块划分、训练顺序；
6. 给出最小复现版本和完整复现版本两条路线；
7. 最后输出一份 checklist。
```

---

## 5. 组件化 / Skills 设计

这是 PaperClarity 的核心差异化设计。

### 5.1 设计目标

每个功能都应尽量解耦为一个 skill。skill 是一个具备以下能力的独立组件：

* 定义自身元信息
* 定义适用输入类型
* 定义 UI 参数
* 定义 Prompt 模板或执行逻辑
* 定义结果结构
* 可被自动发现与注册

### 5.2 Skill 抽象接口建议

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseSkill(ABC):
    name: str = "base"
    display_name: str = "Base Skill"
    description: str = ""
    supported_contexts: List[str] = []  # paper, section, paragraph, formula, figure, table

    @abstractmethod
    def build_prompt(self, context: Dict[str, Any], user_input: str | None = None) -> str:
        ...

    @abstractmethod
    def run(self, context: Dict[str, Any], llm_client: Any, user_input: str | None = None) -> Dict[str, Any]:
        ...

    def output_schema(self) -> Dict[str, Any]:
        return {}
```

### 5.3 Skill 目录结构建议

```text
paperclarity/
  skills/
    __init__.py
    registry.py
    base.py
    paper_overview/
      skill.py
      prompt.txt
      config.yaml
    paragraph_close_reading/
      skill.py
      prompt.txt
      config.yaml
    equation_breakdown/
      skill.py
      prompt.txt
      config.yaml
    intuition_translation/
      skill.py
      prompt.txt
      config.yaml
    experiment_analysis/
      skill.py
      prompt.txt
      config.yaml
    reproduction_guide/
      skill.py
      prompt.txt
      config.yaml
```

### 5.4 自动发现机制

启动时扫描 `skills/` 目录：

* 查找包含 `skill.py` 的子目录
* 动态 import
* 校验类是否继承 `BaseSkill`
* 注册到 SkillRegistry
* 在 UI 中显示可用技能

#### 注册器示例

```python
class SkillRegistry:
    def __init__(self):
        self._skills = {}

    def register(self, skill):
        self._skills[skill.name] = skill

    def get(self, name):
        return self._skills[name]

    def list_all(self):
        return list(self._skills.values())
```

---

## 6. 系统架构设计

## 6.1 总体架构

```text
[Frontend: React/TS]
    |
    | HTTP / WebSocket
    v
[Backend API: FastAPI]
    |
    +-- Document Service
    |     +-- file loader
    |     +-- parser
    |     +-- chunker
    |     +-- structure extractor
    |
    +-- Context Service
    |     +-- paragraph context builder
    |     +-- formula context builder
    |     +-- section retriever
    |
    +-- Skill Engine
    |     +-- registry
    |     +-- skill runtime
    |     +-- prompt renderer
    |
    +-- LLM Gateway
    |     +-- OpenAI-compatible client
    |     +-- local model adapter
    |
    +-- Cache / Index
    |     +-- SQLite
    |     +-- optional vector store
    |
    +-- Export / Notes Service
```

---

## 6.2 推荐技术栈

### 后端

* Python 3.11+
* FastAPI
* Pydantic
* Uvicorn
* SQLAlchemy / SQLModel
* SQLite（第一阶段足够）
* optional: FAISS / Chroma（向量检索）
* PDF 解析：PyMuPDF、pdfplumber、unstructured（二选一或组合）
* 公式/结构提取：结合规则 + LLM

### 前端

* React
* TypeScript
* Vite / Next.js（本地应用建议 Vite + Electron/Tauri）
* Zustand / Redux Toolkit
* Tailwind CSS
* PDF.js
* CodeMirror / Monaco（Prompt 编辑器）

### 桌面封装

优先推荐：

* **Tauri**：轻量，前端用 React，后端服务可独立运行
* 或 Electron：生态成熟，但更重

推荐方案：

* 前端 React + 后端 FastAPI + Tauri 壳

---

## 7. 核心数据模型

## 7.1 文档内部统一模型

```python
class Document:
    id: str
    title: str
    source_path: str
    doc_type: str
    metadata: dict
    sections: list["Section"]
    blocks: list["Block"]
    figures: list["Figure"]
    tables: list["Table"]
    equations: list["Equation"]

class Block:
    id: str
    page: int
    section_id: str | None
    block_type: str  # paragraph/title/caption/equation/table/figure
    text: str
    bbox: list[float] | None
    order: int

class Equation:
    id: str
    page: int
    latex: str | None
    raw_text: str
    block_id: str
    symbols: dict
```

---

## 7.2 任务上下文模型

```python
class SkillContext:
    document_id: str
    context_type: str  # paper/section/paragraph/equation/figure/table
    selected_block_ids: list[str]
    selected_equation_id: str | None
    user_note: str | None
    extra_context: dict
```

---

## 8. 解析与上下文构建策略

## 8.1 文档解析流程

1. 用户选择文件
2. Loader 判断类型
3. Parser 提取文本、页面、块、目录、公式候选、图表标题
4. Chunker 生成逻辑块
5. Structure Extractor 识别章节层级
6. Indexer 建立 block / section / page 映射
7. 存入 SQLite + 缓存目录

## 8.2 上下文构建

### 整篇论文模式

* 标题
* 摘要
* 章节标题
* 每节摘要块
* 关键公式列表
* 关键实验块

### 段落模式

* 当前段
* 前后各 1~3 段
* 所属章节标题
* 引用该段的图表或公式

### 公式模式

* 当前公式
* 前后相关段落
* 最近符号定义
* 相关图表和算法步骤

### 实验模式

* 实验章节全部内容
* 表格说明
* 数据集、指标、基线、消融块

---

## 9. UI 设计建议

## 9.1 主界面布局

```text
+--------------------------------------------------------------+
| 顶栏: 打开论文 | 模型选择 | 索引状态 | 设置 | 导出 |
+-----------------------------+--------------------------------+
| 左侧论文视图                | 右侧 AI 工作台                 |
|                             |                                |
| PDF / 文本渲染              | 技能选择 Tabs                  |
| 目录树                      | 上下文信息条                   |
| 搜索                        | 输出结果区                     |
| 高亮/选择                   | Prompt 预览/编辑               |
| 注释锚点                    | 操作按钮                       |
+-----------------------------+--------------------------------+
| 底栏: 当前页 / 当前块 / Token / 缓存状态 / 日志               |
+--------------------------------------------------------------+
```

## 9.2 关键交互

* 选中文本后浮出快捷菜单：

  * 精读
  * 解释公式
  * 转直觉
  * 写笔记
* 右侧回答中点击“定位原文”时，左侧自动跳转
* 回答可保存为笔记卡片
* 支持会话历史，按论文维度保存

---

## 10. 附加增强功能（建议加入）

这些功能不是用户明示要求，但很值得补充。

### 10.1 论文结构自动摘要导航

系统自动生成：

* 论文地图（Problem / Method / Experiment / Limitation）
* 章节摘要树
* 关键公式目录
* 图表目录

### 10.2 审稿人模式

新增一个 skill：

* 从 novelty、technical soundness、evaluation、clarity 四个维度评审论文
* 输出潜在弱点与审稿问题

### 10.3 Related Work 对比模式

后续可扩展：

* 同时加载多篇论文
* 按问题、方法、实验、优缺点自动对比

### 10.4 术语卡片生成

对选中段落自动生成：

* 术语定义
* 相关概念
* 前置知识建议

### 10.5 笔记与导出

* 导出为 Markdown
* 导出为 JSON
* 导出为“论文阅读报告”
* 记录用户高亮和 AI 输出绑定关系

### 10.6 Prompt Studio

每个 skill 的 Prompt 可见、可编辑、可另存为团队模板。

---

## 11. API 设计建议

## 11.1 文档相关

* `POST /api/documents/load`
* `GET /api/documents/{doc_id}`
* `GET /api/documents/{doc_id}/blocks`
* `GET /api/documents/{doc_id}/sections`
* `GET /api/documents/{doc_id}/equations`

## 11.2 Skill 相关

* `GET /api/skills`
* `POST /api/skills/{skill_name}/run`
* `GET /api/skills/{skill_name}/schema`

## 11.3 会话与笔记

* `GET /api/sessions/{doc_id}`
* `POST /api/notes`
* `GET /api/notes/{doc_id}`
* `POST /api/export/markdown`

## 11.4 模型配置

* `GET /api/models`
* `POST /api/models/test-connection`
* `POST /api/settings/llm`

---

## 12. 目录结构建议

```text
paperclarity/
  app/
    backend/
      api/
      core/
      db/
      models/
      schemas/
      services/
        document_service.py
        parser_service.py
        context_service.py
        llm_service.py
        note_service.py
      skills/
      utils/
      main.py
    frontend/
      src/
        components/
        pages/
        stores/
        hooks/
        services/
        types/
      package.json
    desktop/
      tauri/
  data/
    cache/
    documents/
    indexes/
  tests/
  scripts/
  docs/
  README.md
```

---

## 13. 第一阶段实现优先级（MVP）

## P0：必须

1. 本地加载 PDF
2. 左侧 PDF 阅读区
3. 右侧 AI 面板
4. 整篇论文总览 skill
5. 段落精读 skill
6. 公式拆解 skill（先支持文本公式/块级公式）
7. 实验分析 skill
8. 复现指南 skill
9. skill 自动注册机制
10. 基础笔记保存

## P1：重要

1. 图表识别与分析
2. Prompt 可编辑
3. 模型切换
4. 引用锚点回跳
5. Markdown 导出

## P2：增强

1. 多论文对比
2. 审稿人模式
3. 术语卡片
4. 向量检索增强问答
5. 团队模板库

---

## 14. 工程实现建议

## 14.1 后端设计原则

* 解析、上下文构建、技能执行三层分离
* skill 不直接依赖前端结构，只吃标准化 context
* 模型调用统一走 `LLMGateway`
* 所有 skill 输出尽量结构化 JSON，再由前端渲染

## 14.2 前端设计原则

* 阅读器状态与 AI 状态分离
* 文档选择高亮作为全局状态
* skill 输出面板组件化
* Prompt 编辑器和结果面板解耦

## 14.3 错误处理

* 文件解析失败时给出原因和回退策略
* 模型超时或失败时保留上下文，可重试
* skill 加载失败不影响主程序启动

---

## 15. 质量与评估指标

### 产品指标

* 加载一篇 20 页 PDF 的解析耗时
* skill 首次响应时间
* 引用定位准确率
* 公式识别可用率
* 用户导出笔记次数

### 模型效果指标

* 总览摘要完整性
* 段落解释准确性
* 公式拆解正确性
* 实验分析深度
* 复现指南可执行性

---

## 16. 给 Codex 的最终实现说明

你要实现一个名为 **PaperClarity** 的本地优先论文理解工具。

### 核心要求

1. 后端主语言使用 Python，推荐 FastAPI。
2. 前端使用 React + TypeScript。
3. 工具支持加载本地论文文件，至少支持 PDF。
4. 界面采用左右双栏布局：

   * 左侧为论文阅读区，支持 PDF 显示、页码跳转、文本选择、高亮。
   * 右侧为 AI 工作区，支持选择不同 skill 执行论文理解任务。
5. 所有 AI 功能要设计成可插拔的 skill 组件，并存放在统一目录。
6. 程序启动时自动扫描并加载 skills，展示在 UI 中供用户选择。

### 必做 skills

1. `paper_overview`：理解整篇论文并输出结构化总结
2. `paragraph_close_reading`：对用户选中的段落进行精读
3. `equation_breakdown`：对用户选中的公式做逐项拆解
4. `intuition_translation`：把公式翻译成研究直觉
5. `experiment_analysis`：分析实验设计与结果
6. `reproduction_guide`：生成复现指南

### 技术要求

* 设计统一的 `BaseSkill` 抽象类
* 设计 `SkillRegistry` 自动注册机制
* 设计统一的 `DocumentModel` 与 `SkillContext`
* 设计 `LLMGateway` 以兼容不同模型提供商
* skill 的 Prompt 模板尽量外置为独立文件，便于修改
* skill 输出优先为结构化 JSON

### MVP 范围

* 能加载 PDF
* 能显示论文
* 能选择段落
* 能运行至少 6 个基础 skills
* 能保存 AI 输出为笔记
* 能导出 Markdown

### 推荐实现顺序

1. 搭建项目骨架（backend/frontend/skills）
2. 实现 PDF 加载与渲染
3. 定义内部文档模型
4. 实现技能注册系统
5. 接入 LLM Gateway
6. 逐个实现基础 skills
7. 实现笔记与导出
8. 增加引用定位与上下文增强

### 风格要求

* 代码清晰、模块化、可扩展
* 优先保证结构正确，而不是一次做很多花哨功能
* 所有核心模块添加类型标注与基础测试
* skill 设计要便于后续新增更多论文分析能力

---

## 17. 一句话总结

PaperClarity 不应被实现成“带聊天框的 PDF 阅读器”，而应被实现成“一个围绕论文理解任务构建、以 skills 为核心扩展单元、支持段落/公式/实验/复现多层分析的本地研究工作台”。

---

## 18. Codex 可直接开工的任务拆分清单（按文件/模块拆解）

下面是一份可以直接交给 Codex 执行的任务拆解。目标不是一次把所有高级功能做完，而是优先把可运行的 MVP 主链路打通。

## 18.1 第一阶段交付目标

需要实现一个可运行版本，满足以下闭环：

1. 打开本地 PDF
2. 左侧显示 PDF
3. 用户在左侧选中段落
4. 右侧可选择一个 skill
5. 后端构造上下文并调用 LLM
6. 右侧展示结构化结果
7. 用户可保存结果为笔记
8. 用户可导出 Markdown

---

## 18.2 仓库初始化任务

### 任务 A1：创建 monorepo 目录结构

```text
paperclarity/
  app/
    backend/
    frontend/
    desktop/
  data/
  docs/
  scripts/
  tests/
  README.md
```

### 任务 A2：初始化 backend 工程

在 `app/backend/` 中完成：

* 创建 Python 项目
* 安装依赖：FastAPI、uvicorn、pydantic、sqlmodel 或 sqlalchemy、pymupdf
* 创建 `requirements.txt` 或 `pyproject.toml`
* 创建 `main.py`
* 创建基础健康检查接口 `/api/health`

### 任务 A3：初始化 frontend 工程

在 `app/frontend/` 中完成：

* 使用 React + TypeScript + Vite 初始化
* 安装 PDF.js
* 安装 Zustand
* 安装 React Router
* 安装基础 UI 库或 Tailwind

### 任务 A4：本地启动脚本

在根目录提供：

* `scripts/dev_backend.sh`
* `scripts/dev_frontend.sh`
* `scripts/dev_all.sh`

并在 README 中说明运行方式。

---

## 18.3 后端模块拆分

## 模块 B1：后端入口与配置

### 文件

```text
app/backend/main.py
app/backend/core/config.py
app/backend/core/logging.py
```

### 要求

* `main.py` 启动 FastAPI
* 统一挂载 `/api`
* 从环境变量加载配置
* 配置日志输出
* 支持 CORS

### Codex 任务描述

* 创建 FastAPI 应用入口
* 增加健康检查路由
* 增加基础配置类，读取模型 API 地址、API Key、缓存目录、数据库路径
* 增加统一日志工具

---

## 模块 B2：数据模型定义

### 文件

```text
app/backend/models/document.py
app/backend/models/block.py
app/backend/models/equation.py
app/backend/models/section.py
app/backend/models/note.py
app/backend/models/session.py
app/backend/models/skill_context.py
```

### 要求

定义内部核心数据结构：

* `Document`
* `Section`
* `Block`
* `Equation`
* `Note`
* `ChatSession`
* `SkillContext`

### Codex 任务描述

* 使用 Pydantic 或 SQLModel 定义上述模型
* 保证字段有类型标注
* `Block` 至少包含：`id/page/section_id/block_type/text/bbox/order`
* `Equation` 至少包含：`id/page/raw_text/latex/block_id/symbols`
* `SkillContext` 至少包含：`document_id/context_type/selected_block_ids/selected_equation_id/extra_context`

---

## 模块 B3：数据库与持久化

### 文件

```text
app/backend/db/engine.py
app/backend/db/tables.py
app/backend/db/repositories/document_repo.py
app/backend/db/repositories/note_repo.py
app/backend/db/repositories/session_repo.py
```

### 要求

* 使用 SQLite
* 保存文档元信息
* 保存解析结果索引
* 保存笔记
* 保存会话历史

### Codex 任务描述

* 初始化 SQLite 连接
* 创建文档、笔记、会话三类表
* 实现基础 CRUD repository
* 提供初始化数据库函数

---

## 模块 B4：文档加载与解析

### 文件

```text
app/backend/services/document_loader.py
app/backend/services/pdf_parser.py
app/backend/services/document_service.py
app/backend/services/structure_extractor.py
app/backend/services/chunker.py
```

### 要求

* 支持加载本地 PDF
* 将 PDF 解析为内部 `DocumentModel`
* 产出 blocks、sections、equations 候选
* 初版允许公式识别较粗糙

### Codex 任务描述

* `document_loader.py`：接收本地文件路径，判断文件类型
* `pdf_parser.py`：用 PyMuPDF 提取每页文本和块
* `chunker.py`：把文本分成 paragraph/title/caption 等 block
* `structure_extractor.py`：基于标题样式或规则识别章节
* `document_service.py`：封装加载、解析、缓存、持久化流程

### 最低可用标准

* 成功读取 PDF 文本
* 每个 block 有 page 和 order
* 能按 page 返回 blocks

---

## 模块 B5：上下文构建服务

### 文件

```text
app/backend/services/context_service.py
```

### 要求

根据不同 skill 构造上下文。

### Codex 任务描述

实现以下方法：

* `build_paper_context(document_id)`
* `build_section_context(document_id, section_id)`
* `build_paragraph_context(document_id, block_ids)`
* `build_equation_context(document_id, equation_id)`
* `build_experiment_context(document_id)`

### 逻辑要求

* 段落上下文需要包含前后相邻段
* 公式上下文需要包含前后文块
* 实验上下文优先抓取标题中含 `experiment`, `results`, `evaluation`, `ablation` 的 section

---

## 模块 B6：LLM 网关

### 文件

```text
app/backend/services/llm_gateway.py
app/backend/services/providers/openai_compatible.py
app/backend/services/providers/mock_provider.py
```

### 要求

统一封装模型调用。

### Codex 任务描述

* 定义 `BaseLLMProvider`
* 实现 `OpenAICompatibleProvider`
* 实现 `MockProvider` 便于本地开发
* 提供统一接口：

  * `generate(prompt, system_prompt=None, temperature=0.2)`
  * `generate_json(...)`

### 额外要求

* 超时处理
* 重试机制
* 错误信息统一返回

---

## 模块 B7：Skills 基础框架

### 文件

```text
app/backend/skills/base.py
app/backend/skills/registry.py
app/backend/skills/loader.py
```

### 要求

* 定义 `BaseSkill`
* 定义 `SkillRegistry`
* 定义目录扫描自动加载逻辑

### Codex 任务描述

* `BaseSkill` 提供统一接口
* `registry.py` 负责注册和查询
* `loader.py` 扫描 `app/backend/skills/` 下子目录
* 自动加载每个 skill 的 `skill.py`
* 程序启动时执行技能加载

### 最低可用标准

* 只要新增一个合规 skill 目录，就能被系统识别

---

## 模块 B8：内置 Skills 实现

### 目录与文件

```text
app/backend/skills/paper_overview/skill.py
app/backend/skills/paper_overview/prompt.txt
app/backend/skills/paragraph_close_reading/skill.py
app/backend/skills/paragraph_close_reading/prompt.txt
app/backend/skills/equation_breakdown/skill.py
app/backend/skills/equation_breakdown/prompt.txt
app/backend/skills/intuition_translation/skill.py
app/backend/skills/intuition_translation/prompt.txt
app/backend/skills/experiment_analysis/skill.py
app/backend/skills/experiment_analysis/prompt.txt
app/backend/skills/reproduction_guide/skill.py
app/backend/skills/reproduction_guide/prompt.txt
```

### Codex 任务描述

每个 skill 都要完成：

* 元信息定义
* `supported_contexts`
* 加载 `prompt.txt`
* `build_prompt()`
* `run()`
* 输出统一结构

### 统一输出建议

```json
{
  "title": "...",
  "summary": "...",
  "sections": [
    {"label": "...", "content": "..."}
  ],
  "citations": [
    {"page": 3, "block_id": "b12"}
  ],
  "raw_text": "..."
}
```

---

## 模块 B9：Prompt 模板加载器

### 文件

```text
app/backend/services/prompt_service.py
```

### Codex 任务描述

* 支持从 skill 目录读取 `prompt.txt`
* 支持变量替换，如：`{{paper_title}}`、`{{selected_text}}`
* 支持默认 system prompt
* 后续兼容 yaml/json prompt 配置

---

## 模块 B10：API 路由层

### 文件

```text
app/backend/api/routes/health.py
app/backend/api/routes/documents.py
app/backend/api/routes/skills.py
app/backend/api/routes/notes.py
app/backend/api/routes/sessions.py
app/backend/api/routes/settings.py
```

### Codex 任务描述

实现以下接口：

#### 文档接口

* `POST /api/documents/load`
* `GET /api/documents/{doc_id}`
* `GET /api/documents/{doc_id}/blocks`
* `GET /api/documents/{doc_id}/sections`
* `GET /api/documents/{doc_id}/equations`

#### Skills 接口

* `GET /api/skills`
* `POST /api/skills/{skill_name}/run`

#### 笔记接口

* `POST /api/notes`
* `GET /api/notes/{doc_id}`

#### 会话接口

* `GET /api/sessions/{doc_id}`

#### 设置接口

* `GET /api/settings/llm`
* `POST /api/settings/llm`

---

## 模块 B11：Markdown 导出

### 文件

```text
app/backend/services/export_service.py
app/backend/api/routes/export.py
```

### Codex 任务描述

* 把某篇论文下的笔记和 AI 输出导出为 Markdown
* 支持导出结构：

  * 论文标题
  * 阅读时间
  * 各条笔记
  * AI 输出内容
  * 引用锚点

---

## 模块 B12：测试

### 文件

```text
tests/backend/test_health.py
tests/backend/test_skill_registry.py
tests/backend/test_pdf_parser.py
tests/backend/test_context_service.py
tests/backend/test_prompt_service.py
```

### Codex 任务描述

至少补齐以下测试：

* 健康检查可用
* skill 自动注册正常
* PDF 文本提取成功
* 段落上下文构造正确
* prompt 模板变量替换正常

---

## 18.4 前端模块拆分

## 模块 F1：前端应用骨架

### 文件

```text
app/frontend/src/main.tsx
app/frontend/src/App.tsx
app/frontend/src/router.tsx
app/frontend/src/layouts/MainLayout.tsx
```

### Codex 任务描述

* 初始化应用入口
* 配置基本路由
* 建立主布局：顶部栏 + 左右双栏 + 底栏

---

## 模块 F2：全局状态管理

### 文件

```text
app/frontend/src/stores/documentStore.ts
app/frontend/src/stores/skillStore.ts
app/frontend/src/stores/uiStore.ts
app/frontend/src/stores/noteStore.ts
```

### Codex 任务描述

* `documentStore`：当前文档、页码、选中文本、block ids
* `skillStore`：技能列表、当前技能、运行状态、输出结果
* `uiStore`：布局状态、错误提示、加载状态
* `noteStore`：笔记列表、保存状态

---

## 模块 F3：API 请求封装

### 文件

```text
app/frontend/src/services/api.ts
app/frontend/src/services/documentApi.ts
app/frontend/src/services/skillApi.ts
app/frontend/src/services/noteApi.ts
app/frontend/src/services/settingsApi.ts
```

### Codex 任务描述

* 封装 HTTP 请求
* 统一错误处理
* 提供 typed response

---

## 模块 F4：主页面

### 文件

```text
app/frontend/src/pages/ReaderPage.tsx
```

### Codex 任务描述

* 页面加载后显示左右双栏
* 左侧为文档阅读器
* 右侧为 AI 工作台
* 顶部有模型与文件操作入口

---

## 模块 F5：论文阅读器组件

### 文件

```text
app/frontend/src/components/viewer/PdfViewer.tsx
app/frontend/src/components/viewer/PageNavigator.tsx
app/frontend/src/components/viewer/OutlinePanel.tsx
app/frontend/src/components/viewer/TextSelectionOverlay.tsx
```

### Codex 任务描述

* 使用 PDF.js 渲染 PDF
* 支持翻页与跳页
* 支持缩放
* 支持文本选择
* 选择后回传选中文本与 block ids

### 最低可用标准

* 能稳定显示 PDF
* 能获取用户选中的文本字符串

---

## 模块 F6：AI 工作台组件

### 文件

```text
app/frontend/src/components/assistant/SkillTabs.tsx
app/frontend/src/components/assistant/ContextBar.tsx
app/frontend/src/components/assistant/OutputPanel.tsx
app/frontend/src/components/assistant/PromptPreview.tsx
app/frontend/src/components/assistant/RunSkillButton.tsx
```

### Codex 任务描述

* 展示技能列表
* 展示当前上下文来源
* 点击运行 skill 调用后端
* 渲染结构化输出
* Prompt 预览初版可只读

---

## 模块 F7：笔记组件

### 文件

```text
app/frontend/src/components/notes/NoteList.tsx
app/frontend/src/components/notes/SaveToNoteButton.tsx
```

### Codex 任务描述

* 支持将当前 AI 输出保存为笔记
* 支持查看当前文档下所有笔记

---

## 模块 F8：设置面板

### 文件

```text
app/frontend/src/components/settings/ModelSettingsPanel.tsx
```

### Codex 任务描述

* 支持配置模型 API 地址
* 支持配置 API Key
* 支持切换 provider 类型

---

## 模块 F9：通用组件

### 文件

```text
app/frontend/src/components/common/TopBar.tsx
app/frontend/src/components/common/BottomStatusBar.tsx
app/frontend/src/components/common/SplitPane.tsx
app/frontend/src/components/common/Loading.tsx
app/frontend/src/components/common/EmptyState.tsx
app/frontend/src/components/common/ErrorBanner.tsx
```

### Codex 任务描述

* 实现左右布局容器
* 顶栏显示文件加载、模型状态
* 底栏显示当前页、当前选中 block、运行状态

---

## 18.5 桌面封装任务（可选）

## 模块 D1：Tauri 壳

### 文件

```text
app/desktop/tauri/
```

### Codex 任务描述

* 创建 Tauri 项目
* 将 React 前端作为 UI
* 本地启动 FastAPI 服务
* 提供本地文件选择能力

如果第一版时间紧张，可以先不做 Tauri，只先做浏览器版本地 Web 应用。

---

## 18.6 开发顺序建议（最适合 Codex 执行）

### 第 1 轮：先打通最小闭环

1. 初始化 backend/frontend
2. 做 PDF 加载与渲染
3. 做文档解析与 block 结构
4. 做 skill registry
5. 做 `paper_overview`
6. 做右侧输出面板

### 第 2 轮：补选择式分析

1. 做文本选择
2. 做 `paragraph_close_reading`
3. 做 `equation_breakdown`
4. 做 `intuition_translation`

### 第 3 轮：补论文任务链

1. 做 `experiment_analysis`
2. 做 `reproduction_guide`
3. 做笔记保存
4. 做 Markdown 导出

### 第 4 轮：补体验与扩展性

1. Prompt 可视化
2. 引用锚点回跳
3. 模型设置页
4. 错误处理与测试

---

## 18.7 可直接分配给 Codex 的 issue 列表

### Issue 1：初始化后端 FastAPI 工程

交付物：

* `main.py`
* `/api/health`
* `config.py`
* `logging.py`

### Issue 2：初始化前端 React 工程

交付物：

* Vite + TS
* 主布局
* 路由

### Issue 3：实现 PDF 文档加载与解析

交付物：

* `document_loader.py`
* `pdf_parser.py`
* `document_service.py`

### Issue 4：定义核心数据模型

交付物：

* `Document`
* `Block`
* `Section`
* `Equation`
* `SkillContext`

### Issue 5：实现 Skill 基础框架

交付物：

* `BaseSkill`
* `SkillRegistry`
* `loader.py`

### Issue 6：实现 `paper_overview` skill

交付物：

* `skill.py`
* `prompt.txt`
* API 接入

### Issue 7：实现 PDF 阅读器 UI

交付物：

* `PdfViewer.tsx`
* 翻页、缩放、基础选择

### Issue 8：实现 AI 工作台 UI

交付物：

* skill tabs
* output panel
* run button

### Issue 9：实现段落精读 skill

交付物：

* `paragraph_close_reading/`

### Issue 10：实现公式拆解与直觉转换 skills

交付物：

* `equation_breakdown/`
* `intuition_translation/`

### Issue 11：实现实验分析与复现指南 skills

交付物：

* `experiment_analysis/`
* `reproduction_guide/`

### Issue 12：实现笔记与 Markdown 导出

交付物：

* `note_repo.py`
* `export_service.py`
* 前端笔记面板

### Issue 13：实现模型设置面板

交付物：

* 模型 API 配置页
* settings API

### Issue 14：补基础测试

交付物：

* backend tests
* 至少 5 个关键测试

---

## 18.8 Codex 执行要求

给 Codex 的额外要求如下：

1. 优先生成可运行代码，而不是只生成伪代码。
2. 每个模块都要包含最小可工作的实现。
3. 每个 skill 都要能独立运行。
4. 核心类和函数必须有类型标注。
5. 新增 skill 时不应修改主程序太多代码。
6. 不要把 prompt 写死在 Python 代码里，尽量外置。
7. 所有 API 返回统一 JSON 结构。
8. 所有关键异常都要有明确错误信息。
9. README 要能指导本地启动。
10. 每完成一个模块，优先保证能跑通再继续扩展。

---

## 18.9 最终一句给 Codex 的执行口令

请按照以上模块拆分逐步实现 PaperClarity，优先完成 MVP 主链路：**本地 PDF 加载 → 左侧阅读 → 右侧 skill 执行 → 结构化输出 → 笔记保存 → Markdown 导出**。先保证架构清晰、模块解耦、代码可运行，再逐步增强公式识别、图表理解、引用回跳等高级能力。
