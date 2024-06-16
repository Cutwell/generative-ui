from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import pkg_resources

from demos.skye.src.internals.llm import DynamicUIChat


@asynccontextmanager
async def lifespan(app: FastAPI):
    ############
    # Startup
    ############

    # define defaults
    app.state.about = {
        "author": "Zachary",
        "profile": "https://github.com/Cutwell",
        "description": "An emotional-health companion that escapes the chat box to learn more about you.",
    }
    app.state.project = {
        "homepage": "https://github.com/Cutwell/generative-ui",
        "license": "https://github.com/Cutwell/generative-ui/blob/main/LICENSE",
        "issues": "https://github.com/Cutwell/generative-ui/issues/new",
    }
    app.state.page = {
        "name": "Skye - your emotional health companion",
        "icon": "☀️",
        "css": [
            "https://unpkg.com/normalize.css@8.0.1/normalize.css",
            "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css",
        ],
    }

    app.state.chat = DynamicUIChat()

    yield  # wait for shutdown

    ############
    # Shutdown
    ############

    return


app = FastAPI(lifespan=lifespan)

# Get the path to the templates directory within your package
templates_path = pkg_resources.resource_filename(__name__, "templates")

# Create Jinja2Templates instance with the templates directory
templates = Jinja2Templates(directory=templates_path)

# check /static exists before mounting (as optional)
if os.path.exists("static") and os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/index", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
@app.post("/index", response_class=HTMLResponse)
async def get_html_page(
    request: Request,
):
    """
    Render current conversation as HTML form.

    Returns:
        html: Rendered index.html page, displaying the state the user as reached so far.
    """

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "form": app.state.chat.get_full_html(),
            "page": app.state.page,
            "about": app.state.about,
            "project": app.state.project,
        },
    )


@app.post("/submit", response_class=HTMLResponse)
async def post_html_page(
    request: Request
):
    """
    Update current conversation.

    Returns:
        html: Rendered index.html page, displaying the state the user as reached so far.
    """

    form = await request.json()
    html = app.state.chat.next_state(form_contents=form)

    return JSONResponse(content={"content": html})


@app.get("/reset", response_class=RedirectResponse)
@app.post("/reset", response_class=RedirectResponse)
async def reset(request: Request):
    """
    Reset chat state.

    Returns:
        html: Rendered index.html page, displaying the state the user as reached so far.
    """

    app.state.chat.reset()

    return "/"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
