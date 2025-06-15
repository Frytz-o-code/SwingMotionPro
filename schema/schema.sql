-- Enable UUID and timezone support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table with roles
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'coach', 'player')),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Insert a sample admin user ("admin123" bcrypt-hashed)
INSERT INTO users (email, password_hash, role)
VALUES (
  'admin@example.com',
  '$2b$12$5WYpDfK2.2VZ0s4wZ3h13OuufYAFjlpXjYS2rSrBMnupvqhEtQjpS',  -- "admin123"
  'admin'
)
ON CONFLICT DO NOTHING;

-- Golf shots with extra CSV-provided username
CREATE TABLE IF NOT EXISTS golf_shots (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    csv_username TEXT,  -- Name wie in der CSV
    shot_time TIMESTAMPTZ,
    club_type TEXT,
    smash_factor DOUBLE PRECISION,
    carry_distance DOUBLE PRECISION,
    total_distance DOUBLE PRECISION,
    ball_speed_kph DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT now()
);