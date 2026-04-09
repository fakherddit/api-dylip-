const TelegramBot = require('node-telegram-bot-api');
const { Pool } = require('pg');

const dbUrl = "postgres://koyeb-adm:npg_bYgGQ7lZJo8d@ep-patient-hill-alza9ryd.c-3.eu-central-1.pg.koyeb.app/koyebdb";
const token = '8308447806:AAGpj-E-_1jOTvA7vk9Nq1zKH48sC3YCjK8';
const ADMIN_ID = 7210704553;

const pool = new Pool({
    connectionString: dbUrl,
    ssl: { rejectUnauthorized: false }
});

const bot = new TelegramBot(token, { polling: true });

console.log("🤖 Telegram Bot is running with Inline Buttons...");

const adminMenu = {
    reply_markup: {
        inline_keyboard: [
            [
                { text: "🔑 مفتاح عادي (Normal)", callback_data: "gen_key" },
                { text: "🌍 مفتاح عام (Global)", callback_data: "gen_global_key" }
            ],
            [
                { text: "🗑️ حذف مفتاح", callback_data: "ask_delete_key" },
                { text: "⏸️ تعطيل/إيقاف", callback_data: "ask_disable_key" }
            ],
            [{ text: "📊 الإحصائيات (Stats)", callback_data: "show_stats" }]
        ]
    }
};

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    if (chatId !== ADMIN_ID) {
        bot.sendMessage(chatId, "❌ ماعندكش الصلاحية تصاوب السوارت!");
        return;
    }
    bot.sendMessage(chatId, "مرحبا بيك فلوحة التحكم الفخمة 🟢🔥\nاختار شنو بغيتي دير من الأزرار لتحت:", adminMenu);
});

bot.on('callback_query', async (query) => {
    const chatId = query.message.chat.id;
    if (chatId !== ADMIN_ID) return;

    const data = query.data;

    if (data === 'gen_key') {
        const randomString = Math.random().toString(36).substring(2, 10).toUpperCase();
        const newKey = \FAKHER- + "" + \;
        try {
            await pool.query('INSERT INTO user_keys (key_string) VALUES ()', [newKey]);
            bot.sendMessage(chatId, \✅ تم صنع الساروت بنجاح!\n\n🔑 الساروت: \ + "\\" + newKey + "\" + \\n\nصيفطو للكليان دابا.\, { parse_mode: 'Markdown' });
        } catch (err) {
            bot.sendMessage(chatId, "❌ وقع مشكل فالاتصال بقاعدة البيانات.");
        }
    } 
    else if (data === 'gen_global_key') {
        const randomString = Math.random().toString(36).substring(2, 8).toUpperCase();
        const newKey = \FAKHER-GLOBAL- + "" + \;
        try {
            await pool.query('INSERT INTO user_keys (key_string) VALUES ()', [newKey]);
            bot.sendMessage(chatId, \🌍 تم صنع مفتاح عام (للجميع) بنجاح!\n\n🔑 الساروت: \ + "\\" + newKey + "\" + \\n\nهاد الساروت صالح للاستعمال المتعدد.\, { parse_mode: 'Markdown' });
        } catch (err) {
            bot.sendMessage(chatId, "❌ وقع مشكل فالاتصال بقاعدة البيانات.");
        }
    }
    else if (data === 'show_stats') {
        try {
            const result = await pool.query('SELECT COUNT(*) FROM user_keys');
            const count = result.rows[0].count;
            bot.sendMessage(chatId, \📊 الإحصائيات:\nعندك حاليا \ + count + \ ساروت مسجل في قاعدة البيانات.\);
        } catch (err) {
            bot.sendMessage(chatId, "❌ وقع مشكل فجلب الإحصائيات.");
        }
    }
    else if (data === 'ask_delete_key') {
        bot.sendMessage(chatId, "🗑️ لحذف ساروت، صيفط الأمر بهاد الشكل:\n/delkey FAKHER-XXXXX", { parse_mode: 'Markdown' });
    }
    else if (data === 'ask_disable_key') {
        bot.sendMessage(chatId, "⏸️ لتعطيل ساروت مؤقتا (بون ما تمسحو)، استعمل الحذف كحل بديل مباشر:", { parse_mode: 'Markdown' });
    }

    bot.answerCallbackQuery(query.id);
});

bot.onText(/\/delkey (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    if (chatId !== ADMIN_ID) return;

    const keyToDelete = match[1];

    try {
        const result = await pool.query('DELETE FROM user_keys WHERE key_string =  RETURNING *', [keyToDelete]);
        if (result.rowCount > 0) {
            bot.sendMessage(chatId, \✅ تم حذف الساروت بنجاح:\n\ + "\\" + keyToDelete + "\", { parse_mode: 'Markdown' });
        } else {
            bot.sendMessage(chatId, \❌ مالقيتش هاد الساروت فالداتابيز:\n\ + "\\" + keyToDelete + "\", { parse_mode: 'Markdown' });
        }
    } catch (err) {
        bot.sendMessage(chatId, "❌ مشكل فالحذف.");
    }
});
