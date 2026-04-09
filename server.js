const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// هنا حطينا رابط الداتابيز لي عطيتيني (تقدر ديرو ف Environment Variable فاش تدير ديبلاي للسيرفر)
const dbUrl = process.env.DATABASE_URL || "postgres://koyeb-adm:npg_bYgGQ7lZJo8d@ep-patient-hill-alza9ryd.c-3.eu-central-1.pg.koyeb.app/koyebdb";

const pool = new Pool({
    connectionString: dbUrl,
    ssl: { rejectUnauthorized: false } // ضرورية ل Koyeb باش مايعطيش مشكل فالاتصال
});

// التجربة باش نعرفو السيرفر خدام
app.get('/', (req, res) => {
    res.send("API is running! (Global Key Enhanced)");
});

// المسار (Endpoint) لي غيصيفط ليه ال dylib
app.post('/api/verify', async (req, res) => {
    const { key, hwid } = req.body;

    if (!key || !hwid) {
        return res.status(400).json({ error: "Missing key or hwid" });
    }

    try {
        const result = await pool.query('SELECT * FROM user_keys WHERE key_string = $1', [key]);

        if (result.rows.length === 0) {
            return res.status(401).json({ error: "Invalid Key" });
        }

        const dbKey = result.rows[0];

        // ⭐ التخطي (Bypass): يلا كان الساروت فيه كلمة GLOBAL، غيخدم بلا ما يشوف واش مسجل لشي تليفون آخر! ⭐
        if (key.includes("GLOBAL")) {
            return res.json({
                status: "success",
                payload: "VIP_FEATURES_UNLOCKED_5C"
            });
        }

        if (!dbKey.hwid) {
            // أول مرة: غنسجلو ليه ال HWID ديال هاد التليفون
            await pool.query('UPDATE user_keys SET hwid = $1 WHERE key_string = $2', [hwid, key]);
            return res.json({
                status: "success",
                payload: "VIP_FEATURES_UNLOCKED_5C" // هاد القيمة غيكون ال dylib كيتسناها باش يتخدم
            });

        } else if (dbKey.hwid === hwid) {
            // الساروت مسجل ديجا، والـ hwid بحال بحال ديالنا (نفس التليفون)
            return res.json({
                status: "success",
                payload: "VIP_FEATURES_UNLOCKED_5C"
            });

        } else {
            // الساروت مسجل لـ HWID آخر (تم تسريب الساروت أو استعماله فجهاز ثاني)
            return res.status(403).json({ error: "HWID Mismatch / Key used on another device" });
        }

    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: "Database error" });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
