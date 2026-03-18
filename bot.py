import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")  # 从环境变量读取，安全！
SAVE_DIR = "/tmp/downloads"
os.makedirs(SAVE_DIR, exist_ok=True)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        filename = f"{SAVE_DIR}/photo_{photo.file_id}.jpg"
        await file.download_to_drive(filename)
        await update.message.reply_text(f"✅ 图片已保存！")
    except Exception as e:
        await update.message.reply_text(f"❌ 保存失败：{e}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        video = update.message.video
        file = await context.bot.get_file(video.file_id)
        filename = f"{SAVE_DIR}/video_{video.file_id}.mp4"
        await file.download_to_drive(filename)
        await update.message.reply_text(f"✅ 视频已保存！")
    except Exception as e:
        await update.message.reply_text(f"❌ 保存失败：{e}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        doc = update.message.document
        if doc.mime_type and ("video" in doc.mime_type or "image" in doc.mime_type):
            file = await context.bot.get_file(doc.file_id)
            ext = doc.file_name.split(".")[-1] if doc.file_name else "file"
            filename = f"{SAVE_DIR}/doc_{doc.file_id}.{ext}"
            await file.download_to_drive(filename)
            await update.message.reply_text(f"✅ 文件已保存！")
    except Exception as e:
        await update.message.reply_text(f"❌ 保存失败：{e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

print("Bot 启动！")
app.run_polling()
```

---

### 文件2：`requirements.txt`
```
python-telegram-bot==20.7
```

---

### 文件3：`Procfile`（注意没有扩展名）
```
worker: python bot.py
