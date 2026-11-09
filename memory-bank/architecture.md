# 架构记忆

更新日期：2026-11-10

## 产品与权威文档

EduNexus AI 是面向全校教师、学生、管理员、教学管理人员的教学资料智能处理与知识服务平台。

需求见 [PRD](../PRD.md)，设计见 [design-document](../design-document.md)，技术选型见 [tech-stack](../tech-stack.md)，协作规则见 [AGENTS](../AGENTS.md)。本地原始说明为 docs/EduNexus_AI.md，不随本次工作发布。

## 已确认决策

| 层次 | 方案 | 边界 |
| --- | --- | --- |
| Web | Vue 3 / TypeScript / Vite / Element Plus，Pinia / Vue Router / Axios | 响应式浏览器客户端，业务统一访问 Java |
| 主业务 | Java / Spring Boot / Spring Security + JWT / MyBatis | 模块化单体，管理正式数据与全部业务授权 |
| AI | Python / FastAPI / Pydantic / LangChain，复杂流程按需 LangGraph | 内部 API 与 Worker 分开运行，不直接写 Java 核心表 |
| 权威数据 | MySQL | 身份、课程、资源元数据、任务、考试、成绩、审核 |
| 辅助数据 | Redis、Elasticsearch、Milvus、MongoDB | 缓存、全文、向量、解析及中间结构；索引可重建 |
| 异步 | RabbitMQ + Outbox | 至少一次、幂等、重试、死信、尝试版本和迟到结果保护 |
| 文件 | RustFS + S3 兼容 API | 私有对象，统一文件服务，MySQL 管授权和版本 |
| 交付 | Docker / Compose / Nginx / Git | 阶段化启用，开发测试生产隔离 |

## 模块与关键不变量

业务模块为 user/organization、resource、ai、course、teaching-resource、teaching-learning、interaction、analytics、system。普通模块 MVC，复杂模块 DDD 分层；一张表一个写入归属，跨域经公开服务和事件。

- RBAC 叠加组织、课程、资源、版本与发布状态校验；管理员不默认读取私人资料及问答。
- AI 候选正文发送模型前授权，返回前再次校验；资源撤回不能等待索引清理才生效。
- AI 生成内容先草稿审核；正式成绩教师确认，AI 只提供评分建议。
- 考试发布固定题目快照；保存和交卷以服务端时间及状态为准，成绩修改保留版本审计。
- 文件对象与元数据通过补偿协调；删除先检查引用，保留原文件及版本。
- 任务和事件持久化后投递；取消、超时及重试不允许旧执行结果覆盖新尝试。

## 补充选型与未决项

tech-stack.md 已补充选择 Maven Wrapper、Flyway、Spring AMQP、Uvicorn、aio-pika、uv、npm、测试工具与监控方案；它们尚未安装或联调，不等同于已有运行环境。

待确认：运行时及组件精确版本、身份核验和默认角色、文件配额和存储参数、模型与 OCR/解析库、Embedding 和 Milvus 依赖、消息策略、考试和互动细则、统计公式、容量与恢复目标。编码前按对应阶段关闭。

## 实施顺序

1. 身份权限、资料文件、课程、工作台与消息基础。
2. AI 服务、队列、解析、七工具、检索和审核。
3. 教学资源、题库、练习作业考试和成绩。
4. 互动、计划和学习教学分析。
5. 安全性能、响应式完善、部署监控和恢复验收。

不因技能包含 React 或 PostgreSQL 示例而改变 Vue/MySQL 基线；不在初期引入未经需求支持的微服务或 Kubernetes。
