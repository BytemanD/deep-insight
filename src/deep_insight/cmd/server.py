import uvicorn

from . import app


@app.command()
def master():
    """Start master server"""

    uvicorn.run("deep_insight.master.wsgi:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    app()
