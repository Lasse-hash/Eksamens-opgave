create database if not exists vending;
use vending;

create table if not exists vending_machines (
	id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255) NOT NULL,
    status ENUM("OK", "LOW", "EMPTY", "OFFLINE") DEFAULT "OK",
    last_refill DATETIME
);


create table if not exists items (
	id INT AUTO_INCREMENT PRIMARY KEY,
    vending_machine_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INT DEFAULT 0,
    low_threshold INT default 5,
    
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machine(id)
);