# SEO-GEO-Master（若水）— WordPress 全站 SEO/GEO 优化流水线

> **上善若水。** 如水般润泽用户——你不用学命令，说"帮我看看网站哪里不好"它就懂了。

## 是什么

一条 Claude Code 技能，为任何 WordPress 站点编排 **Plan → Do → Check → Act** 四阶段闭环。融合 **SEO**（搜索引擎优化）和 **GEO**（生成式引擎优化——让你的内容被 ChatGPT、Perplexity、Google AI Overviews、Gemini、Claude 引用）。

**不记命令。** 说"检查我的网站"或"写一篇关于XX的文章"，它自然流向正确的位置。

## 快速开始

```
/seo-geo-master 帮我看看 example.com 哪里不好
/seo-geo-master 对 example.com 做一个完整的 PDCA 循环
/seo-geo-master 写一篇关于"关键词"的文章并发布
/seo-geo-master 最近排名怎么样
/seo-geo-master 刷新 example.com 的旧内容
```

## 哲学根基：三经合一

| 经 | 圣 | 法则 | 在此技能中的体现 |
|----|-----|------|-----------------|
| 道德经 | 老子 | 上善若水·道法自然 | 如水般柔顺：不记命令，说人话就行 |
| 孙子兵法 | 孙子 | 五事七计·先胜后战 | 五维评分 + 安全优先的发布门禁 |
| 原点哲学 | 稻盛和夫 | 作为人何谓正确·利他 | 每篇内容的原点："这真的帮到搜索者了吗？" |

完整哲学：见 `PHILOSOPHY.md`。

## 架构

```
/seo-geo-master（单一入口）
    ├── 步骤 0：读取状态文件
    ├── 意图路由（自然语言 → PDCA 阶段）
    ├── PLAN：关键词 + 竞品 + SERP + GSC 机会
    ├── DO：SEO 写作 + GEO 优化 + meta + schema + WP 发布
    ├── CHECK：WP 审计 + 页面审计 + 技术 + 排名 + GSC
    └── ACT：三重安全门 → 修复 → QA → 报告 → 迭代
```

### 三重安全门

改编自 [seo-survival-kit](https://github.com/maxschottke-spec/seo-survival-kit)（MIT）。

| 门 | 作用 |
|----|------|
| **Change Governor** | 6 种模式（默认 audit_only）。每个变更计风险积分 0-10 × 乘数。26 条硬停止。 |
| **Settlement Gate** | 批量变更后 → 5-14 天强制等待 → 数据验证 → 下一轮 |
| **Hypothesis Verification** | 修复仅在根因被真实 WP API / GSC 数据验证为 `verified` 时执行 |

### 状态持久化

6 个 JSON/NDJSON 文件跨会话追踪一切：
- `pdca-state.json` — 阶段、门禁、五维评分卡
- `content-queue.json` — 6 状态生命周期
- `keyword-bank.json` — 去重关键词库存
- `change-history.ndjson` — 追加式变更日志
- `hypotheses.json` — 5 阶段假设验证
- `run-history.ndjson` — 追加式 PDCA 运行日志

## 前提条件

- **WordPress MCP 服务**已连接
- **Google Search Console MCP**已认证（推荐，非必需时会降级）
- **aaron-seo-geo 插件**已安装（推荐，含 20 个专项 SEO/GEO 子技能）

## 安装

```bash
# 方式 1：直接 clone 到 Claude Code skills 目录
git clone https://github.com/YOUR_USERNAME/seo-geo-master.git ~/.claude/skills/seo-geo-master

# 方式 2：clone 到任意位置，软链
git clone https://github.com/YOUR_USERNAME/seo-geo-master.git /path/to/seo-geo-master
ln -s /path/to/seo-geo-master ~/.claude/skills/seo-geo-master
```

## 安全模型致谢

三重安全门禁改编自 [seo-survival-kit](https://github.com/maxschottke-spec/seo-survival-kit)（Max Schottke, MIT）。内容队列模式参考 [the-four-systems](https://github.com/NicoSKOOL/the-four-systems)。技能路由依托 [aaron-seo-geo](https://github.com/mshojaei77/aio-seo-geo)（Apache 2.0）。

## 许可证

MIT — 见 `LICENSE`。
