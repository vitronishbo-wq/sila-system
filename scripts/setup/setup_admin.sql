-- SQL script to set up admin user

CREATE TABLE IF NOT EXISTS admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO admin_users (username, password_hash)
VALUES ('admin', 'hashed_password')
ON CONFLICT (username) DO NOTHING;

-- Add any additional setup queries here
