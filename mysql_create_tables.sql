CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maker VARCHAR(50),
    name VARCHAR(255),
    price DECIMAL(10,2),
    image_url TEXT,
    part_id INT
);

CREATE TABLE parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category ENUM('CPU', 'GPU', 'Memory', 'Motherboard', 'Storage', 'PSU', 'Case', 'Cooler') NOT NULL
);

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

CREATE TABLE cpu_performance (
    part_id INT,
    core INT,
    thread INT,
    base_clock DECIMAL(4,2),
    boost_clock DECIMAL(4,2),
    PRIMARY KEY (part_id),
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

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

CREATE TABLE gpu_performance (
    part_id INT PRIMARY KEY,
    vram INT,
    cuda INT,
    base_clock INT,
    boost_clock INT,
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

CREATE TABLE motherboard_performance (
    part_id INT PRIMARY KEY,
    displayport INT,
    HDMI INT,
    USB VARCHAR(100),
    wifi BOOLEAN,
    bluetooth BOOLEAN,
    LAN BOOLEAN,
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

CREATE TABLE storage_specs (
    part_id INT PRIMARY KEY,
    storage_type ENUM('HDD', 'SSD', 'NVMe') NOT NULL,
    interface VARCHAR(50),
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE storage_performance (
    part_id INT PRIMARY KEY,
    capacity_gb INT,
    read_speed INT,
    write_speed INT,
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
    form_factor VARCHAR(20),
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

CREATE TABLE luquidcooler_size (
    part_id INT PRIMARY KEY,
    radiator_id INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);

CREATE TABLE aircooler_size (
    part_id INT PRIMARY KEY,
    height INT,
    FOREIGN KEY (part_id) REFERENCES parts(id)
);