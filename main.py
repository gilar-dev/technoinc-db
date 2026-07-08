# FastAPI
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

# Locals
from configuration import config
from routers import contribution, cloudinary, wiki

# Initialize server
app = FastAPI(title="TechnoBackend")

# Add middleware configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins = config.origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Redirect to specific router
app.include_router(contribution.router)
app.include_router(cloudinary.router)
app.include_router(wiki.router)

# Entry url
@app.get("/")
async def entry():
    try:
        return {
            "status": "Success",
            "message": "Welcome to the official API of TechnoInc World!",
            "website": "https://technoinc.world",
            "description": "Start reading a journey of five years Minecraft survival world!"
        }
    
    except HTTPException as httperror:
        raise HTTPException(status_code=404, detail=f"Cannot connect to database: {httperror}")
    
    except Exception as e:
        return { "status": "Error", "message": str(e) }

# Ignore favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)