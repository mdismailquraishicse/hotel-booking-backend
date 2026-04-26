-- CREATE TABLE room (
--     room_id INT PRIMARY KEY,
--     image TEXT,
--     room_type VARCHAR(255),
--     price FLOAT,
--     capacity INT
-- );

-- CREATE TABLE room_amenities (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     room_id INT,
--     amenity VARCHAR(255),
--     FOREIGN KEY (room_id) REFERENCES room(room_id)
-- );

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname TEXT,
    gender TEXT,
    email TEXT UNIQUE,
    password TEXT,
    mobile VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS room_type (
    id SERIAL PRIMARY KEY,
    image TEXT,
    type_name TEXT,
    price REAL,
    capacity INTEGER,
    amenities JSONB DEFAULT '[]',
    descriptions VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    room_no VARCHAR(10) UNIQUE,
    room_type_id INTEGER,
    status VARCHAR(25) DEFAULT 'available',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER,
    room_id INTEGER,
    check_in DATE,
    check_out DATE,
    guests INTEGER,
    price REAL,
    status VARCHAR(15),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (room_id)
        REFERENCES rooms(id)
        ON DELETE CASCADE,

    CHECK (check_out >= check_in)
);

CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    razor_id VARCHAR(35),
    booking_id UUID,
    amount REAL,
    descriptions VARCHAR(100),
    user_id INTEGER,
    status VARCHAR(25),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
)



-- INSERT INTO room_type (image, type_name, price, capacity, amenities, descriptions)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Standard',
-- 1000, 2, NULL, 'Basic room with 1 bed maximum 2 person allowed');

-- INSERT INTO room_type (image, type_name, price, capacity, amenities, descriptions)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Deluxe',
-- 2000, 2, NULL, 'Basic room with 1 bed maximum 2 person allowed');

-- INSERT INTO room_type (image, type_name, price, capacity, amenities, descriptions)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Premium',
-- 3000, 2, NULL, 'Basic room with 1 bed maximum 2 person allowed');

-- INSERT INTO room_type (image, type_name, price, capacity, amenities, descriptions)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Suite',
-- 4000, 5, NULL, 'Basic room with 1 bed maximum 2 person allowed');



-- INSERT ROOMS

-- INSERT INTO rooms (room_no, room_type_id, status)
-- VALUES (101, 1, 'available');

-- INSERT INTO rooms (room_no, room_type_id, status)
-- VALUES (102, 2, 'available');

-- INSERT INTO rooms (room_no, room_type_id, status)
-- VALUES (103, 3, 'available');

-- INSERT INTO rooms (room_no, room_type_id, status)
-- VALUES (104, 4, 'available');

-- INSERT INTO rooms (room_no, room_type_id, status)
-- VALUES (105, 5, 'available');

-- INSERT INTO rooms (room_no, room_type_id, status)
-- VALUES (106, 6, 'available');