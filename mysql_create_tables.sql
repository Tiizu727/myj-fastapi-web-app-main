CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maker VARCHAR(50),
    name VARCHAR(255),
    price DECIMAL(10,2),
    image_url TEXT,
    information_url TEXT,
    part_id INT
);

CREATE TABLE dospara (
    product_id INT PRIMARY KEY,
    product_url TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE pc-koubou (
    product_id INT PRIMARY KEY,
    product_url TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE sofmap (
    product_id INT PRIMARY KEY,
    product_url TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category ENUM('CPU', 'GPU', 'Memory', 'Motherboard', 'Storage', 'PSU', 'Case', 'Cooler') NOT NULL
);

ALTER TABLE cpu_specs
ADD core INT, ADD thread INT, ADD base_clock DECIMAL(4,2), ADD boost_clock DECIMAL(4,2);
DROP TABLE IF EXISTS cpu_performance;

CREATE TABLE cpu_specs (
    part_id INT PRIMARY KEY,
    socket_type VARCHAR(50),
    tdp INT,
    series VARCHAR(100),
    passmark INT,
    memory_type VARCHAR(20),
    memory_speed INT,
    graphic BOOLEAN,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

ALTER TABLE gpu_specs
ADD vram INT, ADD cuda INT, ADD base_clock INT, ADD boost_clock INT;

DROP TABLE IF EXISTS gpu_performance;

CREATE TABLE gpu_specs (
    part_id INT PRIMARY KEY,
    interface VARCHAR(50),
    tdp INT,
    power_supply INT,
    width DECIMAL(5,2),
    height DECIMAL(5,2),
    depth DECIMAL(5,2),
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE memory_specs (
    part_id INT PRIMARY KEY,
    memory_type VARCHAR(20),
    capacity_gb INT,
    speed_mhz INT,
    module_count INT,
    tdp INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

ALTER TABLE motherboard_specs
ADD displayport INT, ADD HDMI INT, ADD USB VARCHAR(100), ADD wifi BOOLEAN, ADD bluetooth BOOLEAN, ADD LAN BOOLEAN;

DROP TABLE IF EXISTS motherboard_performance;

CREATE TABLE motherboard_specs (
    part_id INT PRIMARY KEY,
    socket_type VARCHAR(50),
    chipset VARCHAR(100),
    form_factor VARCHAR(20),
    memory_type VARCHAR(20),
    memory_slots INT,
    max_memory INT,
    PCIe16x5 INT,
    PCIe16x4 INT,
    PCIe16x3 INT,
    SATA INT,
    M2 INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE motherboard_M2type (
    part_id INT PRIMARY KEY,
    type_id INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE M2_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50) NOT NULL
);

ALTER TABLE storage_specs
ADD capacity_gb INT, ADD read_speed INT, ADD write_speed INT;

DROP TABLE IF EXISTS storage_performance;

CREATE TABLE storage_specs (
    part_id INT PRIMARY KEY,
    storage_type ENUM('HDD', 'SSD', 'NVMe') NOT NULL,
    interface VARCHAR(50),
    tdp INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE psu_specs (
    part_id INT PRIMARY KEY,
    wattage INT,
    efficiency_rating VARCHAR(20),
    standard VARCHAR(20),
    modular BOOLEAN,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE case_specs (
    part_id INT PRIMARY KEY,
    max_gpu_length INT,
    psu_standard VARCHAR(20),
    max_cooler_height INT,
    liquid_cooler BOOLEAN,
    drive35 INT,
    drive25 INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE case_radiator (
    part_id INT PRIMARY KEY,
    radiator_id INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE radiator_sizes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    size INT
);

CREATE TABLE case_motherboard (
    part_id INT PRIMARY KEY,
    motherboard_id INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE motherboard_sizes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    size VARCHAR(20) NOT NULL
);

ALTER TABLE cooler_specs
ADD radiator_size INT, ADD air_cooler_height INT;

DROP TABLE IF EXISTS liguidcooler_size;
DROP TABLE IF EXISTS aircooler_size;

CREATE TABLE cooler_specs (
    part_id INT PRIMARY KEY,
    cooling_type ENUM('Air', 'Liquid'),
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE cooler_socket (
    part_id INT PRIMARY KEY,
    socket_id INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE socket_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(20) NOT NULL
);