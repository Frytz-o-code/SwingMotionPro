-- Nutzer
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'coach', 'player')),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Sessions = z. B. Trainings- oder Spieltage
CREATE TABLE golf_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Schläge innerhalb einer Session
CREATE TABLE shots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES golf_sessions(id) ON DELETE CASCADE,
    club TEXT NOT NULL,                -- z. B. "Driver", "7 Iron"
    carry_m REAL,
    deviation_deg REAL,
    spin_rpm INTEGER,
    smash_factor REAL,
    impact_quality TEXT,              -- "good", "miss", "toe", "heel"...
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Scorecard (optional erweiterbar mit Front9/Back9)
CREATE TABLE scorecards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    round_date DATE,
    course_name TEXT,
    holes_played INTEGER,
    strokes_total INTEGER,
    fairways_hit INTEGER,
    greens_in_reg INTEGER,
    putts_total INTEGER,
    created_at TIMESTAMPTZ DEFAULT now()
);