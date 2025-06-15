-- schema/schema.sql

-- Erweiterung für UUID & Zeit
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users mit Rolle
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'coach', 'player')),
    created_at TIMESTAMPTZ DEFAULT now()
);
-- Beispiel-Admin-Nutzer (Passwort: "admin123", gehasht mit bcrypt)
INSERT INTO users (email, password_hash, role)
VALUES (
  'admin@example.com',
  '$2b$12$5WYpDfK2.2VZ0s4wZ3h13OuufYAFjlpXjYS2rSrBMnupvqhEtQjpS',  -- "admin123"
  'admin'
)

ON CONFLICT DO NOTHING;

-- Golf Sessions
CREATE TABLE IF NOT EXISTS golf_shots (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    datum TIMESTAMP,
    schlaegerart TEXT,
    smash_factor DOUBLE PRECISION,
    carry_distanz DOUBLE PRECISION,
    gesamtstrecke DOUBLE PRECISION,
    ballgeschwindigkeit DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT now()
);