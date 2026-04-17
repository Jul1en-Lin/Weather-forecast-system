-- 创建数据库
CREATE DATABASE IF NOT EXISTS meteo_assistant
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE meteo_assistant;

-- 后端启动时会通过 SQLAlchemy 自动创建表，无需手动执行 CREATE TABLE
-- 若需手动建表，参考 docs/project_spec.md 2.3 节
