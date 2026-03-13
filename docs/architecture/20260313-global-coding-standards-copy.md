# 全局 Cursor AI 编程标准（副本）

> 本文档为 **~/.cursor/rules/global-standards.mdc** 的副本，供本仓库内查阅与对齐。  
> 作用域：全局（所有项目）| 原位置：~/.cursor/rules/global-standards.mdc

---

## 核心理念

- **代理优先**：复杂任务委托给专门子代理（planner / architect / tdd-guide 等），不单打独斗
- **并行执行**：多个独立子任务同时启动，不串行等待
- **先计划后执行**：复杂、有多种方案权衡的任务，先切换 Plan Mode 讨论再动手
- **测试驱动**：先写测试（TDD），再写实现代码
- **安全第一**：任何情况下安全检查不可跳过

---

## 代码风格

### 通用规范
- 不使用表情符号（代码、注释、文档均不用）
- 优先不可变性：不直接 mutate 对象或数组，返回新值
- 多个小文件优于少数大文件：典型 200-400 行，最大 800 行/文件
- 注释只写非显而易见的意图、权衡或约束；不写叙述代码行为的注释

### Python
- PEP 8 + 类型注解（Type Hints）全覆盖
- 异步优先：FastAPI + asyncio
- 测试覆盖率 ≥ 80%（pytest）
- 错误处理：自定义异常类 + 统一错误响应格式

### Dart / Flutter
- 遵循 Flutter 官方规范
- 状态管理：Riverpod（禁用 setState 于复杂状态）
- 响应式设计：适配不同屏幕/窗口尺寸

### SQL / 数据库
- PostgreSQL 15+：善用 JSONB、GIN 索引、全文搜索
- 所有查询加索引分析（EXPLAIN ANALYZE）
- 迁移脚本必须可回滚

---

## Git 规范

- **Conventional Commits**：`feat:` `fix:` `refactor:` `docs:` `test:` `chore:`
- 提交前本地测试必须通过
- 小而聚焦的提交，每次只包含一个关注点
- PR 必须：代码审查通过 + CI 绿灯 + 无安全告警

---

## 安全规范

- 日志输出必须脱敏；禁止记录 API Key / Token / 密码 / JWT
- 分享或输出任何内容前，检查并移除敏感数据
- 强制触发安全审查的场景：
  - 用户认证 / 授权逻辑
  - 文件上传 / 下载
  - API 密钥管理
  - 数据导出功能
  - 外部输入处理（防注入、XSS）

---

## 测试规范

- TDD 工作流：先写测试，后写实现
- 最低覆盖率：80%
- 关键路径覆盖：单元测试 + 集成测试 + E2E 测试
- 测试命名：`test_<被测功能>_<场景>_<预期结果>`

---

## 代理使用策略

复杂任务时，自动选用或建议使用以下专门代理：

| 场景 | 推荐代理 |
|---|---|
| 新功能规划、任务拆解 | `planner` |
| 系统设计、架构决策 | `architect` |
| TDD 引导、测试编写 | `tdd-guide` |
| 代码质量审查 | `code-reviewer` |
| 安全漏洞分析 | `security-reviewer` |
| 构建/编译错误修复 | `build-error-resolver` |
| E2E 测试（Playwright） | `e2e-runner` |
| 死代码清理、重构 | `refactor-cleaner` |
| 文档更新 | `doc-updater` |

---

## 文档生成规范

**所有生成的文档必须写入项目 `docs/` 目录。**

### 文件命名规则

```
docs/<分类>/<日期>-<主题>.md
```

- **日期**：生成文档前先获取系统当前日期（`date +%Y%m%d`），格式为 `YYYYMMDD`，不得硬编码
- **分类**：按内容类型归入对应子目录
- **主题**：简短英文短语，单词间用 `-` 连接，全小写

### 分类目录对照表

| 分类目录 | 适用内容 |
|---|---|
| `docs/product/` | 产品需求、用户故事、PRD、功能规格 |
| `docs/ux/` | UI/UX 设计、线框图、用户流程、设计系统 |
| `docs/architecture/` | 系统架构、技术选型、数据库设计、API 设计 |
| `docs/features/` | 功能特性说明、实现方案、开发笔记 |
| `docs/retrospective/` | 复盘、问题记录、经验总结、事故分析 |
| `docs/api/` | API 文档、接口规范、OpenAPI 说明 |
| `docs/deployment/` | 部署流程、运维手册、CI/CD 配置说明 |

### 示例路径

```
docs/product/20260226-user-auth-requirements.md
docs/architecture/20260226-database-schema-design.md
docs/ux/20260226-onboarding-flow.md
docs/features/20260226-image-upload-spec.md
docs/retrospective/20260226-sprint-1-review.md
```

### 执行步骤

1. 先执行 `date +%Y%m%d` 获取系统当前日期
2. 目录不存在时先 `mkdir -p docs/<分类>/` 再写入文件
3. 文档首行为 `# <主题标题>`，次行注明日期和生成目的

---

## 响应与沟通规范

- 回复使用中文（除非用户切换语言）
- 工具调用前不解释要干什么，工具调用后再说明发现和结论
- 展示已存在代码时使用 `startLine:endLine:filepath` 引用格式
- 展示新代码时使用带语言标签的 markdown 代码块
- 不主动创建文件，除非任务明确需要；优先编辑已有文件

---

## 成功标准

每次任务完成后，检查：

- [ ] 所有测试通过（覆盖率 ≥ 80%）
- [ ] 无安全漏洞（安全检查通过）
- [ ] 代码可读、可维护（无多余注释、无 magic number）
- [ ] 满足用户需求（功能验收）
- [ ] 无 linter 错误
- [ ] Git 提交格式规范（若有提交）

---

**理念**：代理优先设计 · 并行执行 · 先计划后行动 · 先测试后代码 · 安全始终第一

**副本生成日期**：2026-03-13
