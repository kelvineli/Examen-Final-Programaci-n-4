CREATE DATABASE IF NOT EXISTS quicktickets_db;
USE quicktickets_db;

CREATE TABLE IF NOT EXISTS ticket (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  client_id VARCHAR(255),
  subject VARCHAR(255),
  description TEXT,
  priority VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);