CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    total_amount DECIMAL(10, 2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- استخدام IGNORE يتجاهل الخطأ إذا كان الـ ID موجوداً مسبقاً
INSERT IGNORE INTO orders (order_id, product_name, total_amount) VALUES 
(1, 'iPhone 15', 999.99),
(2, 'MacBook Pro', 2499.00),
(3, 'AirPods', 199.00);