from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uuid
import pkg_resources

from demos.goose.src.internals.llm import ChatUser
from demos.goose.src.internals.mem import MemCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    ############
    # Startup
    ############

    # define defaults
    app.state.about = {
        "author": "Zachary",
        "profile": "https://github.com/Cutwell",
        "description": "A Goose chatbot demo.",
    }
    app.state.project = {
        "homepage": "https://github.com/Cutwell/generative-ui",
        "license": "https://github.com/Cutwell/generative-ui/blob/main/LICENSE",
        "issues": "https://github.com/Cutwell/generative-ui/issues/new",
    }
    app.state.page = {
        "name": "Goose",
        "icon": "🪿",
        "css": [
            "https://unpkg.com/normalize.css@8.0.1/normalize.css",
            "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css",
        ],
    }

    app.state.cache = MemCache()

    # Create test user for internal testing
    app.state.cache.set(key="test", value=ChatUser(guid="test"))

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

# Mount /static directory to serve JS and CSS and images
app.mount("/static", StaticFiles(directory="demos/goose/src/static"), name="static")


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page": app.state.page,
            "about": app.state.about,
            "project": app.state.project,
        },
    )


@app.get("/new", response_class=RedirectResponse)
def new_chat(
    request: Request,
):
    """
    Create a new user chat object and redirect to unique chat page.

    Returns:
        RedirectResponse: redirect to a unique URL for the user's chat.
    """

    guid = str(uuid.uuid4())

    new_user = ChatUser(guid=guid)

    app.state.cache.set(key=guid, value=new_user)

    return f"/chat/{guid}"


@app.get("/chat/{user_uuid}", response_class=HTMLResponse)
def load_chat(request: Request, user_uuid: str):
    """
    Load a chat from URL parameter UUID.

    Returns:
        html: Rendered index.html page, with chat history
    """

    user = app.state.cache.get(key=user_uuid)

    if not user:
        raise HTTPException(status_code=404, detail="User UUID not found")
    
    html = user.get_all_html_blocks()

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat": html,
            "page": app.state.page,
            "about": app.state.about,
            "project": app.state.project,
        },
    )


async def stream_response(user: ChatUser, message: str):
    for chunk in user.chat(message=message):
        yield chunk


@app.post("/chat/{user_uuid}", response_class=HTMLResponse)
async def post_html_page(request: Request, user_uuid: str):
    """
    Update current conversation.

    Returns:
        JSONResponse: next HTML component for conversation.
    """

    data = await request.json()

    user = app.state.cache.get(key=user_uuid)

    if not user:
        raise HTTPException(status_code=404, detail="User UUID not found")

    return StreamingResponse(stream_response(user=user, message=data["message"]))


@app.post("/settings/{user_uuid}", response_class=HTMLResponse)
async def post_settings_page(request: Request, user_uuid: str):
    """
    Update LLM.

    Returns:
        JSONResponse: action sucesss message.
    """

    data = await request.json()

    user = app.state.cache.get(key=user_uuid)

    if not user:
        raise HTTPException(status_code=404, detail="User UUID not found")

    res = user.update_settings(
        model_name=data["model"], openai_api_key=data["api-token"]
    )

    return JSONResponse(content={"response": res})


@app.get("/reset/{user_uuid}", response_class=RedirectResponse)
@app.post("/reset/{user_uuid}", response_class=RedirectResponse)
def reset(request: Request, user_uuid: str):
    """
    Delete chat history assigned to UUID.

    Returns:
        RedirectResponse: Redirect to index.html to establish new chat.
    """

    success = app.state.cache.delete(key=user_uuid)

    return "/new"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
