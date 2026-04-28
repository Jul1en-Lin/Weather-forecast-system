-- 创建数据库
CREATE DATABASE IF NOT EXISTS meteo_assistant
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE meteo_assistant;

-- users（用户表）
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,   -- bcrypt
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- conversations（对话表）
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,            -- UUID
    user_id INT NOT NULL,
    title VARCHAR(200) DEFAULT '新对话',
    model_id VARCHAR(64) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- messages（消息表）
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL,
    role ENUM('user', 'assistant', 'system', 'tool') NOT NULL,
    content TEXT NOT NULL,
    tool_calls JSON DEFAULT NULL,          -- LangChain tool_calls JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- terms（气象术语库）
CREATE TABLE terms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    term VARCHAR(100) NOT NULL,            -- 术语名
    category VARCHAR(50),                  -- 分类：如天气现象、预报用语
    definition TEXT NOT NULL,              -- 释义
    source VARCHAR(200),                   -- 来源标准/文献
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- alerts（预警信号库）
CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL,       -- 预警类型：台风、暴雨、高温…
    level ENUM('蓝','黄','橙','红') NOT NULL,
    criteria TEXT NOT NULL,                -- 发布标准
    response_guide TEXT,                   -- 防御指南
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);



-- 后端启动时会通过 SQLAlchemy 自动创建表，无需手动执行 CREATE TABLE
-- 若需手动建表，可直接复制粘贴上述sql语句执行


