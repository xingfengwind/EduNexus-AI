# Phase 0 version matrix

Scope: browser Web + Java backend + Python AI; no native clients.

## Runtime

- Node.js 24.14.0 / npm 11.9.0 (observed locally)
- Java 21.0.10; package root com.edunexus
- Maven Wrapper 3.9.11 (generated); system Maven 3.10.0 used for first unit validation
- Python 3.12.14 / uv 0.13.7
- Docker Engine 29.6.1 (connected after user startup)

## Resolved frontend versions

- @playwright/test: 1.65.0
- @types/node: 24.19.2
- @vitejs/plugin-vue: 6.0.10
- @vue/test-utils: 2.4.6
- axios: 1.21.1
- element-plus: 2.14.8
- eslint: 9.39.5
- eslint-plugin-vue: 10.12.0
- jsdom: 26.1.0
- pinia: 3.0.4
- prettier: 3.9.10
- typescript: 5.9.3
- typescript-eslint: 8.72.1
- vite: 7.3.8
- vitest: 5.1.0
- vue: 3.5.45
- vue-router: 4.6.4
- vue-tsc: 3.3.14

## Backend

Spring Boot 3.5.16, MyBatis Starter 3.0.5, json-schema-validator 1.5.9. Remaining dependency versions come from the Boot BOM. The Maven `verify` lifecycle passed unit, contract and Testcontainers integration tests against MySQL 8.4.8, including repeatable Flyway startup and health/security checks.

## Python

Exact transitive versions are recorded in ai-service/uv.lock; uv sync --locked and all three tests passed. FastAPI 0.162.2, Pydantic 2.14.3, Uvicorn 0.54.0. AI orchestration/Parser packages are deferred to phase 2.

## Infrastructure

Compose pins MySQL 8.4.8, Redis 7.4.8, RustFS 1.0.0-alpha.76. A local restart test verified persistence in all three services and rejected anonymous RustFS object access. Flyway currently warns that MySQL 8.4 is newer than its formally tested range; MySQL 8.4 is retained because it is the supported LTS line, and this compatibility warning must be tracked before production. RustFS is prerelease; production suitability and upgrade path require separate assessment.

GitHub Actions pins Ubuntu 24.04, checkout v7, setup-node v7, setup-java v6 and setup-uv v10.3.2. A deliberately failing unit assertion was rejected remotely and the restored clean checkout passed all four jobs.

References: https://docs.spring.io/spring-boot/3.5/system-requirements.html and https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/ .
