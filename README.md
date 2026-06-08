# Survey Response Generator

This repository contains two main components:
- a Python-based synthetic survey response generator and analysis pipeline
- a Next.js frontend application located in `response-forge`

The system is built around the assignment survey definition for e-commerce customer satisfaction:
- Overall satisfaction (1–5)
- Likelihood to recommend (NPS 0–10)
- Category purchased (Electronics / Clothing / Home / Other)
- Was delivery on time? (Yes / No)
- What could we improve? (open text)

## Repository Structure

```
.
├── response-forge/          # Next.js frontend application
│   ├── pages/
│   │   ├── survey.tsx       # Survey submission form
│   │   ├── report.tsx       # Analytics dashboard
│   │   ├── responses.tsx    # Data table browser
│   │   ├── index.tsx        # Home page
│   │   └── _app.tsx         # Global app wrapper
│   ├── lib/
│   │   └── generator.ts     # Synthetic response generator helper
│   ├── package.json
│   ├── tsconfig.json
│   └── vercel.json
├── survey_generator.py       # Python orchestrator for synthetic data generation
├── survey_model.py           # Persona and latent state generation
├── survey_open_text.py       # Open-text feedback generation
├── survey_validator.py       # Response coherence validation
├── survey_analysis.py        # Data quality and statistics
├── report_builder.py         # HTML report generation
├── responses.csv             # Generated survey responses
├── quality_report.html       # Generated HTML quality report
├── requirements.txt          # Python dependencies
└── package.json              # Root deployment helper for Vercel
```

## Getting Started

### Python Backend

Install dependencies and generate the synthetic dataset:

```bash
pip install -r requirements.txt
python survey_generator.py
```

This produces:
- `responses.csv` — generated survey responses
- `quality_report.html` — summary report with analysis and charts

### Frontend Web App

Install dependencies and run the Next.js application:

```bash
cd response-forge
npm install
npm run dev
```

Open `http://localhost:3000` and use:
- `/survey` to submit responses manually
- `/report` to view analytics
- `/responses` to browse generated responses

## Build and Deployment

The root `package.json` is configured to build the frontend from the repository root. To verify locally from the project root:

```bash
npm run build
```

If you deploy on Vercel, the root `vercel.json` points to `response-forge/package.json` so the correct app is built.

### If using Vercel CLI

```bash
cd response-forge
vercel deploy
```

## Notes

- The current frontend app lives entirely under `response-forge`
- The Python generator lives in the repository root
- README references to deleted markdown files have been removed
- The repository is now structured for both local development and Vercel deployment

## Backend Deployment (optional)

I provide a minimal FastAPI wrapper to run the Python generator as a simple web service.

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run locally with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Endpoints:
- `GET /health` — health check
- `POST /generate` — JSON body `{ "count": 200 }` triggers generation and returns a summary
- `GET /responses` — download `responses.csv`
- `GET /report` — download `quality_report.html`

4. Deploy on a Python-friendly host (Render, Railway, Fly, Cloud Run):
- Ensure `requirements.txt` includes `fastapi` and `uvicorn[standard]` (already updated)
- Use the provided `Procfile` (start command uses Uvicorn)

Notes:
- The frontend currently reads/writes to `localStorage`. To integrate with the backend, update the frontend API calls to use these endpoints and authenticate as needed.


## License

Add a license here if desired.
