from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.ascloud_service import AIService 
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI(title="Z0ramp")

ai_service = AIService()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class = HTMLResponse)
async def index(request: Request):
    full_data = await ai_service.get_hub_status()
    return templates.TemplateResponse(
        request,
        "index.html",
        {"ai_data": full_data}
    )

@app.get("/api/status/card", response_class = HTMLResponse)
async def get_status_fragment(request: Request):
    full_data = await ai_service.get_hub_status()
    
    return templates.TemplateResponse(
        request,
        "partials/card_content.html",
        {"ai_data": full_data}
    )


@app.get('/api/config/node/{id}', response_class = HTMLResponse)
async def get_config_node(request: Request, id: str):
    full_data = await ai_service.get_hub_status()

    current_node = next((node for node in full_data if node["node_id"] == id), None)
    if not current_node:
        return HTMLResponse('<p>Not found</p>', status_code=404)

    return templates.TemplateResponse(
        request,
        "partials/config.html",
        {"node": current_node}
    )


@app.put('/api/config/node/{id}', response_class = HTMLResponse)
async def update_config_node(request: Request, id: str):
    form_data = await request.form()
    full_data = await ai_service.get_hub_status()

    for node in full_data:
        if node["node_id"] == id:
            node["name"] = form_data.get("name", node["name"])
            node["base_url"] = form_data.get("base_url", node["base_url"])
            node["node_type"] = form_data.get("node_type", node["node_type"])
            node["node_tier"] = int(form_data.get("node_tier", node["node_tier"]) or 0)

            for model_name, services in node.get("active_services", {}).items():
                for s in services:
                    s["n_ctx"] = int(form_data.get(f"services[{model_name}][n_ctx]", s["n_ctx"]) or 0)
                    s["n_gpu_layers"] = int(form_data.get(f"services[{model_name}][n_gpu_layers]", s["n_gpu_layers"]) or 0)
                    s["priority"] = int(form_data.get(f"services[{model_name}][priority]", s["priority"]) or 0)
                    s["total_slots"] = int(form_data.get(f"services[{model_name}][total_slots]", s["total_slots"]) or 0)
            break

    return templates.TemplateResponse(
        request,
        "partials/card_content.html",
        {"ai_data": full_data}
    )
