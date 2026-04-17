from fastapi.responses import StreamingResponse
import json

class SSEStream:
    @staticmethod
    def event(data: dict | str) -> str:
        if isinstance(data, dict):
            payload = json.dumps(data, ensure_ascii=False)
        else:
            payload = data
        return f"data: {payload}\n\n"

def sse_response(generator):
    return StreamingResponse(generator, media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    })
