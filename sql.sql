CREATE DATABASE IF NOT EXISTS blog;

USE blog;

CREATE TABLE IF NOT EXISTS users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL COMMENT 'username',
    password_hash VARCHAR(255) NOT NULL COMMENT 'password hash',
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'when the user was created',
    status TINYINT DEFAULT 1 COMMENT 'status of the user',
    UNIQUE KEY uk_username (username)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS posts(
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL COMMENT 'title of the post',
    content TEXT NOT NULL COMMENT 'content of the post',
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INT COMMENT 'category id of the post',
    user_id INT COMMENT 'user id of the post',
    status TINYINT DEFAULT 1 COMMENT 'status of the post',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS categories(
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL COMMENT 'name of the category',
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tags(
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(255) NOT NULL COMMENT 'name of the tag',
    description TEXT COMMENT 'description of the tag'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS comments(
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL COMMENT 'content of the comment',
    post_id INT COMMENT 'post id of the comment',
    status TINYINT DEFAULT 1 COMMENT 'status of the comment',
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT COMMENT 'user id of the comment',
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS post_tag_category(
    post_id INT,
    tag_id INT,
    category_id INT,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
