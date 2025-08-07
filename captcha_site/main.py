from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()
templates = Jinja2Templates(directory="templates")

RECAPTCHA_SECRET_KEY = "6Le2cZwrAAAAAAm9FQpECkSV6jNKv34MpTlQkz1A"

@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/verify", response_class=HTMLResponse)
async def verify(request: Request, name: str = Form(...), g_recaptcha_response: str = Form(alias="g-recaptcha-response")):
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': g_recaptcha_response
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = resp.json()
    
    if result.get("success"):
        return HTMLResponse(f"<h3>✅ Hello, {name}. reCAPTCHA passed.</h3>")
    else:
        return HTMLResponse("<h3>❌ reCAPTCHA failed. Try again.</h3>")
