/*
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
*/

INSERT INTO products (name, description, price, stock_quantity)
VALUES
    ('Laptop Pro 14', 'Portable developer laptop with 16GB RAM.', 1899.99, 20),
    ('Mechanical Keyboard', 'Compact keyboard with tactile switches.', 129.99, 75),
    ('USB-C Dock', 'Docking station with HDMI, Ethernet, and USB ports.', 219.50, 35)
ON DUPLICATE KEY UPDATE name = VALUES(name);
