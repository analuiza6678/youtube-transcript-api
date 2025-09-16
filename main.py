from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

app = FastAPI(title="API de transcrição do YouTube")

@app.get("/")
def health():
    return {"ok": True}

@app.get("/transcript/{video_id}")
def transcript(video_id: str, languages: str = Query("pt,en")):
    try:
        langs = [l.strip() for l in languages.split(",")]
        data = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
        return {"video_id": video_id, "transcript": data}
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        raise HTTPException(status_code=404, detail=str(e))
