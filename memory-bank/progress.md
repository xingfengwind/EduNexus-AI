# 项目进度记忆

更新日期：2026-11-11

## 当前状态

第 0 阶段基础工程已在 `feature/phase-0` 独立工作树实施。P00-02—P00-08 与 P00-10 已完成本地验证；P00-01 等待业务规则，P00-09 等待 GitHub Actions 真实运行。项目只开发浏览器 Web，同时保留 Java 主后端和 Python AI 服务，不开发原生移动端或桌面端。

## 已完成产物

- Vue 3 / TypeScript / Vite 前端脚手架、单测、构建和桌面/移动视口端到端测试。
- Java 21 / Spring Boot 3.5 / MyBatis 后端、健康端点、默认拒绝访问、安全测试、Flyway 迁移及 Testcontainers 集成测试。
- Python 3.12 / FastAPI AI 服务、锁定依赖、健康接口和共享事件契约测试。
- OpenAPI 初始契约、事件信封 JSON Schema 及合法/非法共享 fixture。
- MySQL 8.4、Redis 7.4、RustFS 的 Compose 环境和跨重启持久性验证脚本。
- GitHub Actions 前端、后端、Python 与 Compose 配置检查工作流。
- 阿里云百炼 `kimi-k3.1-pro` 后端配置占位；精确北京接入地址已记录，真实密钥未写入文件。

## 验证记录

详细命令和结论见 `docs/verification/phase-0.md`。本地已通过：

- 前端安装、lint、类型检查、1 项单测、生产构建、桌面和移动视口 E2E；全依赖无高危/严重项，生产依赖 0 项漏洞。
- 后端 Maven `verify`，包含健康/安全、事件契约及 MySQL 迁移集成测试。
- Python 锁定同步、Ruff、格式检查和 3 项 pytest。
- Compose 配置解析及 MySQL/Redis/RustFS 写入、重启、持久性与私有对象验证。

## 未完成与风险

1. P00-01：默认注册角色/状态、学生核验、教师审核、管理员初始化与角色授予、上传配额及格式规则仍未确认。
2. P00-09：工作流尚未在 GitHub Actions 中完成一次故意失败再修正的红/绿记录，也未验证远程干净检出。
3. Flyway 对 MySQL 8.4 有正式测试范围告警；本地通过不等于生产兼容承诺。
4. RustFS 当前固定预发布版本，生产升级与恢复路径待评估。
5. 前端开发工具链仍有 10 项中等级传递依赖告警，等待上游修复或兼容升级。
6. 聊天模型已确认；Embedding、OCR、数据外发政策与额度待第 2 阶段确定。

## Git 与远程

- 基础工作区：`D:/development/software1`；第 0 阶段工作区：`D:/development/software1-phase0`。
- 当前分支：`feature/phase-0`；首个工程提交：`3ccc39e`。
- 目标仓库：`https://github.com/xingfengwind/EduNexus-AI.git`。
- 本轮只进行明确暂存和本地提交；在远程结果可核验前，不把 P00-09 标记完成，不强推覆盖历史。

## 下一步

1. 用户确认 P00-01 五类业务规则后形成最终决策记录。
2. 推送功能分支并观察 GitHub Actions；保留失败阻断和修复通过记录，关闭 P00-09。
3. 第 0 阶段全部关闭后，再进入身份、权限和文件基础的第 1 阶段。

## 更新规则

每次任务结束记录新增产物、实际验证结果、未完成事项和阻塞。设计建议、已选方案、已实现功能、已通过验证、已部署分别记录。不要保存密钥、真实学生数据或其他敏感信息。
