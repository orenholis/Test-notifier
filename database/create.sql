CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    date TIMESTAMP(0) NOT NULL,
    teacher VARCHAR(255),
    note VARCHAR(1024)
)