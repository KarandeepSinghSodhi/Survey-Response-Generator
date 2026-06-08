from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Defer importing the heavy generator until it's needed so the API can start
create_synthetic_dataset = None
build_report = None
OUTPUT_CSV = "responses.csv"
OUTPUT_REPORT = "quality_report.html"
_generator_import_error = None

def _ensure_generator():
    """Attempt to import the generator modules on demand. Returns True if available."""
    global create_synthetic_dataset, build_report, OUTPUT_CSV, OUTPUT_REPORT, _generator_import_error
    if create_synthetic_dataset is not None:
        return True
    try:
        from survey_generator import create_synthetic_dataset as _create, build_report as _build, OUTPUT_CSV as _csv, OUTPUT_REPORT as _rep
        create_synthetic_dataset = _create
        build_report = _build
        OUTPUT_CSV = _csv
        OUTPUT_REPORT = _rep
        _generator_import_error = None
        return True
    except Exception as e:
        import traceback
        _generator_import_error = traceback.format_exc()
        return False

app = FastAPI(title="Survey Sensum Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    count: int = 200


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(req: GenerateRequest):
    # ensure the generator modules are importable
    ok = _ensure_generator()
    if not ok:
        return JSONResponse({
            "error": "Backend generator import failed. Install dependencies and run from repo root.",
            "trace": _generator_import_error.splitlines()[-10:] if _generator_import_error else None,
        }, status_code=500)

    results = create_synthetic_dataset(req.count)
    df = results["df"]
    df.to_csv(OUTPUT_CSV, index=False)

    # build HTML report if available
    try:
        build_report(results)
    except Exception:
        pass

    return {"summary": results.get("summary", {}), "responses": len(df)}


@app.get("/responses")
def responses_file():
    if not os.path.exists(OUTPUT_CSV):
        return JSONResponse({"error": "responses.csv not found. Generate data first."}, status_code=404)
    return FileResponse(OUTPUT_CSV, media_type="text/csv", filename="responses.csv")


@app.get("/report")
def report_file():
    if not os.path.exists(OUTPUT_REPORT):
        return JSONResponse({"error": "quality_report.html not found. Generate data first."}, status_code=404)
    return FileResponse(OUTPUT_REPORT, media_type="text/html", filename="quality_report.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
