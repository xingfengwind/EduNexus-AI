# EduNexus AI 技术栈选型

版本：V1.0

日期：2026-11-10

依据：[PRD.md](PRD.md)、[design-document.md](design-document.md)及本地总体设计基线。

## 1. 选型结论

采用 Vue 3 响应式 Web、Spring Boot 模块化单体与独立 Python AI 服务。MySQL 保存正式业务数据，RustFS 保存文件，RabbitMQ 承担可靠异步任务；Redis、Elasticsearch、Milvus、MongoDB 各自承担缓存、全文、向量与文档型中间数据职责。

本文区分“基线已确认”和“本次补充选定”：前者来自已有文档，后者用于补齐构建、测试和工程工具。技术选型不等于依赖已安装或兼容性已验证。精确版本在工程初始化时锁定，不使用浮动 latest，不把待验证版本写成已确认事实。

## 2. 前端

| 技术 | 状态 | 用途与约束 |
| --- | --- | --- |
| Vue 3 | 基线已确认 | Composition API、script setup；按业务模块组织页面 |
| TypeScript | 基线已确认 | API、页面和状态类型；开启严格检查 |
| Vite | 基线已确认 | 本地开发与生产构建 |
| Element Plus | 基线已确认 | 表单、表格、弹窗等基础组件；统一主题与交互 |
| Pinia | 基线已确认 | 会话和必要跨页面状态，避免无界缓存服务端数据 |
| Vue Router | 基线已确认 | 路由和入口权限展示，实际授权仍由 Java 执行 |
| Axios | 基线已确认 | 请求封装、错误和刷新令牌并发协调 |
| 原生 CSS / CSS Variables | 本次补充选定 | 主题、响应式布局及组件样式；优先复用现有组件能力 |
| npm + package-lock.json | 本次补充选定 | 依赖管理，CI 使用 npm ci |
| ESLint、Prettier、vue-tsc | 本次补充选定 | 静态检查、格式和 Vue 类型检查 |
| Vitest、Vue Test Utils | 本次补充选定 | 单元及组件测试 |
| Playwright | 本次补充选定 | 关键用户流程和响应式端到端测试 |

运行时选择仍受支持的 Node.js LTS，并满足锁定 Vite 的最低版本要求。Node 精确版本与前端依赖同时写入版本文件和 CI，不仅依赖开发者本机环境。Vite 的环境要求以[官方指南](https://vite.dev/guide/)为准。

前端静态产物由 Nginx 托管。浏览器不直连 Python、数据库、消息队列或模型供应商；模型密钥不进入打包产物。

## 3. Java 主业务后端

| 技术 | 状态 | 用途与约束 |
| --- | --- | --- |
| Java | 基线已确认 | 主业务语言；选择受支持 LTS，精确版本随 Spring Boot 兼容矩阵锁定 |
| Spring Boot | 基线已确认 | 单体部署、业务模块隔离、统一配置与服务入口 |
| Spring MVC | 本次补充选定 | REST、参数校验和 SSE；业务规则置于应用及领域层 |
| Spring Security + JWT | 基线已确认 | 认证、接口授权、会话撤销与刷新令牌轮换 |
| MyBatis | 基线已确认 | MySQL 持久化；复杂 SQL 使用 XML |
| Spring Transaction | 基线已确认 | 本地业务事务与 Outbox 原子写入，不覆盖长时间模型调用 |
| Jakarta Bean Validation | 本次补充选定 | DTO 参数及字段约束 |
| Maven Wrapper | 本次补充选定 | 统一构建入口与 Maven 版本；依赖由 Boot BOM 和显式版本约束管理 |
| Flyway | 本次补充选定 | 数据库迁移、初始化和变更历史；按选定版本引入所需 MySQL 支持模块 |
| Spring AMQP | 本次补充选定 | RabbitMQ 发布确认、消费确认和消息转换 |
| Spring Data Redis | 本次补充选定 | 缓存、限流辅助和短期协调 |
| Spring Boot Actuator + Micrometer | 本次补充选定 | 健康、指标、调用耗时与监控接入；管理端点受保护 |
| JUnit Jupiter、Mockito、Spring Boot Test | 本次补充选定 | 领域单测、服务及接口测试；版本随兼容 BOM 锁定 |
| Testcontainers | 本次补充选定 | 使用真实 MySQL、RabbitMQ 等容器做集成验证 |

初始化时先验证 Spring Boot、Java、MyBatis Starter、Spring Security、Flyway 和测试组件的共同兼容版本，再生成 pom.xml，不能分别追逐最新版本。Java 与构建要求参见 [Spring Boot 官方系统要求](https://docs.spring.io/spring-boot/system-requirements.html)；容器集成测试参见[官方测试支持](https://docs.spring.io/spring-boot/reference/testing/testcontainers.html)。

普通业务模块采用 MVC；课程、资源审核、任务、考试成绩等复杂域使用 DDD 思想分层。模块之间通过公开服务及事件协作，不直接访问其他模块 Mapper。

## 4. Python AI 服务

| 技术 | 状态 | 用途与约束 |
| --- | --- | --- |
| Python | 基线已确认 | 解析、检索、模型调用和工作流；运行时版本与解析/模型依赖共同验证 |
| FastAPI、Pydantic | 基线已确认 | 内部 API 和输入输出 Schema 校验 |
| Uvicorn | 本次补充选定 | ASGI 服务运行；API 与 Worker 分容器部署 |
| LangChain | 基线已确认 | 模型、Prompt、加载及检索组件适配 |
| LangGraph | 基线已确认，按需启用 | 仅用于需要状态、分支、重试或人工审核的复杂工作流 |
| aio-pika | 本次补充选定 | RabbitMQ 异步消费、结果发布和确认；与执行租约及幂等设计配合 |
| HTTPX | 本次补充选定 | 访问内部 Java 授权服务及适用的 HTTP Provider |
| boto3 | 本次补充选定 | 在受控授权下通过 S3 接口读取文件或写处理产物 |
| uv、pyproject.toml、uv.lock | 本次补充选定 | Python 依赖与环境锁定；CI 使用锁定依赖 |
| pytest、pytest-asyncio、Ruff | 本次补充选定 | 同步/异步测试、静态检查与格式检查 |

按 FastAPI 的[容器部署说明](https://fastapi.tiangolo.com/deployment/docker/)构建项目自己的镜像。Worker 负责持久任务消费，FastAPI 进程内后台任务不作为长任务可靠队列。

文档解析实现采用 Parser 接口；PDF、Word、PPT、TXT、MD 的具体解析库在样本验证后锁定，验证页码保真、加密/损坏文件、中文、表格及许可。OCR、Embedding、聊天与重排序模型分别配置 Provider，不假设一个模型覆盖所有能力。模型供应商、模型标识、向量维度、额度、外发数据政策仍待确认。

Python 不直接写 Java 核心业务表；结构校验通过后仍由 Java 执行业务校验和正式发布。

## 5. 数据、检索、消息和文件

| 技术 | 状态 | 权威职责 | 实施约束 |
| --- | --- | --- | --- |
| MySQL | 基线已确认 | 身份、组织、课程、资源元数据、审核、题库、考试、成绩、任务主记录 | 使用事务型引擎、迁移脚本、唯一约束、乐观锁；正式业务事实来源 |
| Redis | 基线已确认 | 缓存、限流、幂等辅助、短时锁和会话辅助 | 缓存失效可回源，不作为成绩或答卷唯一存储 |
| Elasticsearch | 基线已确认 | 全文、关键词和文档片段索引 | 可重建；Java/Python 客户端与服务端共同锁定兼容版本 |
| Milvus | 基线已确认 | Embedding 向量检索 | 向量及模型版本可追踪，支持重建和索引切换 |
| MongoDB | 基线已确认 | 解析 JSON、中间结果及适用检查点 | 不替代 MySQL 核心关系数据；使用稳定业务 ID 关联 |
| RabbitMQ | 基线已确认 | 异步任务与业务事件 | Outbox、发布确认、手动确认、有限重试和死信；至少一次投递与业务幂等 |
| RustFS | 基线已确认 | 原文件、处理产物、导出文件 | 私有对象；业务经 FileStorageService 和 S3 兼容接口访问 |
| S3 兼容 SDK | 本次补充选定 | Java 选 AWS SDK for Java v2 S3；Python 选 boto3 | 联调端点、签名、寻址方式、流式上传和下载；兼容性必须实测 |

Milvus 所需元数据及对象存储组件按选定版本的部署要求确定，教学文件 RustFS 与 Milvus 配套存储是否共用仍须部署验证。RustFS Bucket、容量、生命周期、备份及拓扑待定。

检索元数据只用于缩小候选集，最终授权回到 Java 与 MySQL；候选正文发往模型或外部重排序服务前完成授权。索引异步清理不替代即时权限检查。

## 6. 契约、可靠性与安全

| 领域 | 选定方案 |
| --- | --- |
| 外部 API | REST JSON、`/api/v1`、OpenAPI 契约；统一错误码、traceId 和分页 |
| 内部 API | `/internal/v1`、服务身份认证、私网隔离；不使用浏览器用户凭据冒充服务身份 |
| 任务进度 | SSE 为实时展示方案，轮询作为恢复及兼容路径；持久化任务记录为准 |
| 消息契约 | JSON Schema/明确结构版本；eventId、taskId、attemptId、traceId 和输入版本引用 |
| 去重与并发 | MySQL 唯一约束、条件更新与 Outbox；Redis 仅作辅助；Worker 使用执行租约和过期结果保护 |
| 访问控制 | Spring Security + RBAC + 组织、课程、资源和版本范围校验 |
| 密码与令牌 | 使用 Spring Security PasswordEncoder；刷新令牌存哈希、轮换、可撤销；参数详细设计确认 |
| 文件安全 | 格式和实际内容校验、私有 Bucket、短时签名或授权代理、受限解析容器 |
| AI 安全 | Prompt/Schema 版本化、引用校验、人工审核、授权上下文、敏感数据最小化 |
| 审计 | 关键操作持久化审计，日志脱敏，不记录明文令牌、密钥和签名链接 |

不额外引入分布式事务协调器：数据库事务、可靠事件和补偿机制共同处理跨存储一致性。考试发布使用不可变试卷版本，保存和交卷使用状态条件更新，AI 评分建议与正式成绩分离。

## 7. 部署与工程交付

| 技术 / 工具 | 状态 | 用途 |
| --- | --- | --- |
| Docker、Docker Compose | 基线已确认 | 开发、测试和初期部署；阶段化启动服务 |
| Nginx | 基线已确认 | HTTPS 入口、静态托管、反向代理和 SSE 转发配置 |
| Git、GitHub | 基线及目标仓库已明确 | 版本管理、评审和阶段发布记录 |
| GitHub Actions | 本次补充选定 | 前端类型/测试/构建、Java 验证、Python 检查及容器构建；发布权限单独配置 |
| Prometheus、Grafana | 本次补充选定，阶段 5 接入 | 指标采集和仪表盘，告警阈值随容量和服务目标确认 |
| JSON 结构化日志 | 本次补充选定 | traceId/taskId/attemptId/eventId 关联；容器日志轮转 |

初期不预设 Kubernetes 或微服务拆分。Java 单体按域保持边界，Python API/Worker 独立伸缩；只有负载和运维需求成立时再新增基础设施。

生产部署固定镜像版本或摘要，数据使用持久卷或受控外部存储，数据库等内部组件不直接暴露公网。开发、测试、生产凭据隔离，配置模板只放占位值。备份协调 MySQL 元数据与 RustFS 对象，并验证 MongoDB 恢复、索引重建和消息重放幂等性。

## 8. 分阶段启用

| 阶段 | 必要技术与能力 |
| --- | --- |
| 1 平台基础 | Vue 全栈前端、Java/Security/MyBatis、MySQL、Redis、RustFS、迁移和基础测试；建立 Compose 与 CI |
| 2 AI 能力 | FastAPI/Worker、RabbitMQ、LangChain、按需 LangGraph、解析器、ES/Milvus/MongoDB、模型 Provider、AI 评测 |
| 3 教学学习 | 沿用现有技术，增加试卷快照、答卷持久化、批改和成绩版本规则 |
| 4 协作分析 | 沿用事件及持久化体系，补齐互动通知、统计投影和口径版本 |
| 5 上线完善 | 指标告警、安全性能测试、恢复演练、兼容性和运维交付 |

阶段 1 不必运行全部 AI 基础设施；阶段 2 再按功能引入，避免基础环境先于业务无界膨胀。

## 9. 版本锁定与初始化验收

1. 建立运行时矩阵：Node.js、Java、Python、Docker/Compose 与各服务端版本。
2. 校验 Spring Boot 与 MyBatis、安全、迁移、测试依赖的兼容组合；校验 Vue/Vite/Element Plus 与 Node；校验 LangChain/LangGraph、Pydantic、解析器及 Python。
3. 生成 package-lock.json、uv.lock、Maven Wrapper 和显式服务镜像版本。核心库精确版本记录到仓库，升级通过 PR 验证。
4. 执行空工程构建、数据库迁移、认证接口、S3 文件读写、RabbitMQ 重复消息、Python/Java 契约、检索权限和文件解析样本验证。
5. 完成许可证与依赖漏洞检查，记录例外；验证成功后将精确版本写入本文件或独立版本清单。

待确认项：具体运行时及组件版本、模型供应商、解析器/OCR 实现、Milvus 部署依赖、存储参数、容量与恢复指标。它们不改变已选技术类别，但必须在对应功能实施前关闭。

本文仅形成技术选型，尚未创建工程、安装依赖或完成兼容性联调。
