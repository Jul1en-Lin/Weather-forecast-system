-- SQLite 数据库初始化脚本
-- 迁移自 MySQL 版本，适配 SQLite 语法差异

-- 启用外键约束
PRAGMA foreign_keys = ON;

-- users（用户表）
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- conversations（对话表）
CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) DEFAULT '新对话',
    model_id VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- messages（消息表）
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id VARCHAR(36) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    tool_calls TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- terms（气象术语库）
CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    definition TEXT NOT NULL,
    source VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- alerts（预警信号库）
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type VARCHAR(50) NOT NULL,
    level VARCHAR(10) NOT NULL,
    criteria TEXT NOT NULL,
    response_guide TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (level IN ('蓝', '黄', '橙', '红'))
);

-- 索引（可选，SQLite 下查询压力小，可按需创建）
-- CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
-- CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);

-- 后端启动时会通过 SQLAlchemy 自动创建表，无需手动执行本脚本
-- 若需手动初始化，命令行执行：sqlite3 database.sqlite < init.sql