DROP TABLE IF EXISTS elements;
DROP TABLE IF EXISTS gamma;
DROP TABLE IF EXISTS xray;
DROP TABLE IF EXISTS reactions;
DROP TABLE IF EXISTS crossSection;

-- Element Table
CREATE TABLE IF NOT EXISTS elements (
    name text PRIMARY KEY,
    halfLife text NOT NULL,
    abundance real,
    parity text NOT NULL,
    betaPlusDecay integer,
    betaMinusDecay integer,
    ecDecay integer
    );

-- Gamma Table
CREATE TABLE IF NOT EXISTS gamma (
id integer PRIMARY KEY,
elementId text NOT NULL,
value real NOT NULL,
intensity real NOT NULL,
FOREIGN KEY (elementId) 
    REFERENCES elements (name)
);

-- Xray Table
CREATE TABLE IF NOT EXISTS xray (
id integer PRIMARY KEY,
elementId text NOT NUll,
value real NOT NULL,
intensity real NOT NULL,
FOREIGN KEY (elementId) 
    REFERENCES elements (name)
);

-- Reactions Table
CREATE TABLE IF NOT EXISTS reactions (
id integer PRIMARY KEY,
targetId text NOT NULL,
type text NOT NULL,
productId text NOT NULL,
energyMin real,
energyMax real,
dataPoint integer,
qValue real NOT NULL,
source text,
FOREIGN KEY (targetId) 
    REFERENCES elements (name),
FOREIGN KEY (productId) 
    REFERENCES elements (name)
);

-- Cross Sections Table
CREATE TABLE IF NOT EXISTS crossSection (
id integer PRIMARY KEY,
targetId text NOT NULL,
reaction text NOT NULL,
energy real NOT NULL,
crossSection real,
FOREIGN KEY (targetId)
    REFERENCES elements (name)
);