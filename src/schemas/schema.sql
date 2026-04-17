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
    user_id SERIAL PRIMARY KEY,
    name TEXT,
    gender TEXT,
    email TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS rooms (
    room_id SERIAL PRIMARY KEY,
    image TEXT,
    room_type TEXT,
    price REAL,
    capacity INTEGER,
    amenities JSONB DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    room_id INTEGER,
    check_in DATE,
    check_out DATE,
    guests INTEGER,
    price REAL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (room_id)
        REFERENCES rooms(room_id)
        ON DELETE CASCADE,

    CHECK (check_out > check_in)
);

-- INSERT INTO rooms (image, room_type, price, capacity, amenities)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Standard', 1000, 2, NULL);

-- INSERT INTO rooms (image, room_type, price, capacity, amenities)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Deluxe',
-- 2000, 2, NULL);

-- INSERT INTO rooms (image, room_type, price, capacity, amenities)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Premium',
-- 3000, 2, NULL);

-- INSERT INTO rooms (image, room_type, price, capacity, amenities)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Suite',
-- 4000, 5, NULL);

-- INSERT INTO rooms (image, room_type, price, capacity, amenities)
-- VALUES ('https://images.pexels.com/photos/7201513/pexels-photo-7201513.jpeg', 'Standard',
-- 1000, 2, NULL);