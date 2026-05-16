from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.sentiment import analyze_sentiment
from backend.database import conn, cursor

app = FastAPI()

templates = Jinja2Templates(directory="backend/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
    history = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='POSITIVE'")
    positive_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='NEGATIVE'")
    negative_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='NEUTRAL'")
    neutral_count = cursor.fetchone()[0]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "history": history,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count
        }
    )


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, feedback: str = Form(...)):

    result = analyze_sentiment(feedback)

    sentiment = result["sentiment"]
    confidence = result["confidence"]
    issues = ", ".join(result["issues"])

    cursor.execute(
        """
        INSERT INTO feedback
        (feedback_text, sentiment, confidence, issues)
        VALUES (?, ?, ?, ?)
        """,
        (feedback, sentiment, confidence, issues)
    )

    conn.commit()

    cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
    history = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='POSITIVE'")
    positive_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='NEGATIVE'")
    negative_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='NEUTRAL'")
    neutral_count = cursor.fetchone()[0]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": result,
            "feedback": feedback,
            "history": history,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count
        }
    )