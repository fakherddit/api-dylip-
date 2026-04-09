-- هاد الكود كتبو مباشرة فشي أدة بحال DBeaver ولا TablePlus ولا PGAdmin
-- باش تنشأ الطابلو ديال السوارت فالـ Koyeb

CREATE TABLE IF NOT EXISTS user_keys (
    id SERIAL PRIMARY KEY,
    key_string VARCHAR(255) UNIQUE NOT NULL, -- الساروت
    hwid VARCHAR(255) DEFAULT NULL,          -- ايدي ديال التليفون (كيكون خاوي في الأول)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إلا بغيتي تزيد ساروت تجريبي باش تجرب:
INSERT INTO user_keys (key_string) VALUES ('TEST-VIP-KEY-123');
