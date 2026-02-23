CREATE DATABASE IF NOT EXISTS cf_database;
USE cf_database;

CREATE TABLE baros (
    baro_id INT AUTO_INCREMENT PRIMARY KEY,
    baro_name VARCHAR(255) NOT NULL UNIQUE,
    city VARCHAR(255) NOT NULL
);

CREATE TABLE law_firms (
    law_firm_id INT AUTO_INCREMENT PRIMARY KEY,
    firm_name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    email VARCHAR(255)
);

CREATE TABLE lawyers (
    lawyer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    baro_id INT,
    bar_number VARCHAR(50),
    law_firm_id INT,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baro_id) REFERENCES baros(baro_id),
    FOREIGN KEY (law_firm_id) REFERENCES law_firms(law_firm_id),
    UNIQUE (baro_id, bar_number)
);

CREATE TABLE cases (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    case_title VARCHAR(255) NOT NULL,
    case_number VARCHAR(100) UNIQUE,
    -- Translated ENUM values below
    case_status ENUM('Preparation', 'In Trial', 'Awaiting Decision', 'Closed') NOT NULL,
    case_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_date DATE,
    last_hearing_date DATETIME,
    next_hearing_date DATETIME,
    decision_date DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE case_lawyers (
    case_id INT,
    lawyer_id INT,
    PRIMARY KEY (case_id, lawyer_id),
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id)
);

CREATE TABLE clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
	fullname VARCHAR(255) NOT NULL,
    tc_number VARCHAR(11) UNIQUE,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE opponents (
    opponent_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    tc_number VARCHAR(11) UNIQUE,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE case_clients (
    case_id INT,
    client_id INT,
    PRIMARY KEY (case_id, client_id),
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE case_opponents (
    case_id INT,
    opponent_id INT,
    PRIMARY KEY (case_id, opponent_id),
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (opponent_id) REFERENCES opponents(opponent_id)
);

CREATE TABLE case_notes (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT,
    lawyer_id INT,
    note_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id)
);

CREATE TABLE calendar_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT,
    lawyer_id INT,
    -- Translated ENUM values below
    event_type ENUM('Hearing', 'Meeting', 'Discovery', 'Other') NOT NULL,
    event_date DATETIME NOT NULL,
    event_description TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id)
);

CREATE TABLE documents (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT,
    lawyer_id INT,
    document_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id)
);

CREATE TABLE financial_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT,
    lawyer_id INT,
    client_id INT,
    opponent_id INT,
    -- Translated ENUM values below
    transaction_type ENUM('Income', 'Expense') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    transaction_date DATE,
    receipt_path VARCHAR(500) DEFAULT NULL,
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id),
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (opponent_id) REFERENCES opponents(opponent_id)
);

-- Veritabanını kullan
USE cf_database;

-- 1. Bağımsız Tablolara Veri Ekleme (FOREIGN KEY içermeyenler)

-- Baro Ekleme
INSERT INTO baros (baro_name, city) 
VALUES ('İzmir Barosu', 'İzmir');

-- Hukuk Bürosu Ekleme
INSERT INTO law_firms (firm_name, password, address, phone_number, email) 
VALUES ('123', '123', 'Adalet Mah. 123. Sokak No: 4, Bayraklı/İzmir', '02325551234', 'info@guvenhukuk.com');

-- Müvekkil Ekleme
INSERT INTO clients (fullname, tc_number, phone_number, email, address) 
VALUES ('Ayşe Kaya', '11122233344', '05331112233', 'ayse.kaya@email.com', 'Bostanlı Mah. Örnek Cad. No: 5, Karşıyaka/İzmir');

-- Karşı Taraf Ekleme
INSERT INTO opponents (name, surname, tc_number, phone_number, email, address) 
VALUES ('Mehmet Öztürk', 'Öztürk', '55566677788', '05445556677', 'mehmet.ozturk@email.com', 'Alsancak Mah. Test Sok. No: 10, Konak/İzmir');

-- 2. İlişkili Tablolara Veri Ekleme

-- Avukat Ekleme (baro_id=1 ve law_firm_id=1 olarak varsayılmıştır)
INSERT INTO lawyers (name, surname, email, password, phone_number, baro_id, bar_number, law_firm_id, is_admin) 
VALUES ('Ahmet', 'Yılmaz', 'ahmet.yilmaz@guvenhukuk.com', '1', '05559876543', 1, '1', 1, TRUE);

-- Dava Ekleme
INSERT INTO cases (case_title, case_number, case_status, case_description, file_date, next_hearing_date) 
VALUES ('Kaya vs. Öztürk - Tazminat Davası', '2025/123 E.', 'In Trial', 'Maddi ve manevi tazminat talepli alacak davası.', '2025-05-10', '2025-11-20 10:30:00');

-- 3. Bağlantı (Junction) Tablolarına ve Diğer İlişkili Tablolara Veri Ekleme
-- (Tüm ID'lerin 1 olduğu varsayılmıştır)

-- Davaya Avukat Atama
INSERT INTO case_lawyers (case_id, lawyer_id) 
VALUES (1, 1);

-- Davaya Müvekkil Atama
INSERT INTO case_clients (case_id, client_id) 
VALUES (1, 1);

-- Davaya Karşı Taraf Atama
INSERT INTO case_opponents (case_id, opponent_id) 
VALUES (1, 1);

-- Dava Notu Ekleme
INSERT INTO case_notes (case_id, lawyer_id, note_content) 
VALUES (1, 1, 'Karşı tarafın tanık listesi mahkemeye sunuldu. Bir sonraki duruşma için delillerimizi hazırlamamız gerekiyor.');

-- Takvim Etkinliği Ekleme (Duruşma)
INSERT INTO calendar_events (case_id, lawyer_id, event_type, event_date, event_description) 
VALUES (1, 1, 'Hearing', '2025-11-20 10:30:00', 'İzmir 3. Asliye Hukuk Mahkemesi, Duruşma Salonu 2.');

-- Doküman Ekleme
INSERT INTO documents (case_id, lawyer_id, document_name, file_path) 
VALUES (1, 1, 'Dava Dilekçesi.pdf', 'C:\Users\Emine\Desktop\CF\Petition Samples\anlasmali-bosanma-dilekcesi.doc');

-- Finansal İşlem Ekleme (Müvekkilden alınan vekalet ücreti)
INSERT INTO financial_transactions (case_id, lawyer_id, client_id, transaction_type, amount, description, transaction_date) 
VALUES (1, 1, 1, 'Income', 5000.00, 'Vekalet ücreti peşinatı.', '2025-05-15');