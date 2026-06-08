import { useMemo, useState } from "react";
import Link from "next/link";
import { generateSyntheticResponses, SyntheticResponse } from "../lib/generator";
import { ArrowRight, BarChart3, Sparkle, FileText } from "lucide-react";

const DEFAULT_COUNT = 200;

const summaryFromData = (data: SyntheticResponse[]) => {
  const average = data.reduce((sum, row) => sum + row.satisfaction, 0) / data.length;
  const npsAverage = data.reduce((sum, row) => sum + row.nps, 0) / data.length;
  const onTime = data.filter((row) => row.delivery === "Yes").length;
  return {
    average: average.toFixed(2),
    npsAverage: npsAverage.toFixed(1),
    onTimeRate: ((onTime / data.length) * 100).toFixed(0),
  };
};

export default function Home() {
  const [responseCount, setResponseCount] = useState(DEFAULT_COUNT);
  const [dataset, setDataset] = useState<SyntheticResponse[] | null>(null);

  const summary = useMemo(() => (dataset ? summaryFromData(dataset) : null), [dataset]);

  const handleGenerate = () => {
    const rows = generateSyntheticResponses(responseCount);
    setDataset(rows);
    window.localStorage.setItem("survey-sensum-responses", JSON.stringify(rows));
  };

  return (
    <div className="container">
      <section className="section" style={{ paddingTop: 60 }}>
        <div className="grid-two" style={{ alignItems: "center", gap: "38px" }}>
          <div>
            <div className="hero-badge">
              <Sparkle size={18} />
              Synthetic survey generation for e-commerce analysis
            </div>
            <h1 className="page-title">Build realistic e-commerce survey responses in one click.</h1>
            <p className="subtitle" style={{ marginTop: 24 }}>
              A polished front-end for the assignment survey. Generate coherent customer answers, explore the analytics report, and inspect every response from a responsive dashboard.
            </p>
            <div style={{ marginTop: 36, display: "flex", flexWrap: "wrap", gap: 16 }}>
              <button className="button" onClick={handleGenerate}>Generate {responseCount} responses</button>
              <Link href="/survey" className="button secondary">Add responses manually</Link>
              <Link href="/report" className="button secondary">View report</Link>
              <Link href="/responses" className="button secondary">View responses</Link>
            </div>
          </div>
          <div className="glass-card" style={{ padding: 32 }}>
            <h2 className="card-title">Survey definition</h2>
            <p style={{ marginBottom: 24, color: "#c7cffb" }}>
              This demo uses the exact assignment questions and creates N plausible responses with consistent satisfaction, NPS, category, delivery, and open feedback.
            </p>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>1. Satisfaction</h3>
                <p>1–5 scale</p>
              </div>
              <div className="stat-card">
                <h3>2. Likelihood to recommend</h3>
                <p>0–10 NPS</p>
              </div>
              <div className="stat-card">
                <h3>3. Category</h3>
                <p>Electronics / Clothing / Home / Other</p>
              </div>
              <div className="stat-card">
                <h3>4. Delivery</h3>
                <p>Yes / No</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="glass-card" style={{ padding: 32 }}>
          <div className="grid-two">
            <div>
              <h2 className="card-title">Instant dataset preview</h2>
              <p style={{ color: "#c7cffb" }}>
                Generate synthetic responses client-side and store them in the browser. Then browse the report or view the raw table instantly.
              </p>
            </div>
            <div style={{ display: "flex", justifyContent: "flex-end", gap: 12, alignItems: "center" }}>
              <div className="badge">Best for demo</div>
              <div className="badge">Static generation</div>
            </div>
          </div>

          <div className="card-grid" style={{ marginTop: 28 }}>
            <div className="stat-card">
              <h3>Responses</h3>
              <p>{dataset ? dataset.length : 0}</p>
            </div>
            <div className="stat-card">
              <h3>Average satisfaction</h3>
              <p>{summary ? summary.average : "—"}</p>
            </div>
            <div className="stat-card">
              <h3>Average NPS</h3>
              <p>{summary ? summary.npsAverage : "—"}</p>
            </div>
            <div className="stat-card">
              <h3>On-time rate</h3>
              <p>{summary ? `${summary.onTimeRate}%` : "—"}</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="glass-card" style={{ padding: 32 }}>
          <h2 className="card-title">How it works</h2>
          <div className="grid-three">
            <div className="stat-card">
              <BarChart3 size={20} />
              <h3 style={{ marginTop: 16 }}>Survey definition</h3>
              <p style={{ color: "#c7cffb" }}>Matches the assignment questions exactly and uses a structured synthetic generation model.</p>
            </div>
            <div className="stat-card">
              <FileText size={20} />
              <h3 style={{ marginTop: 16 }}>Plausible feedback</h3>
              <p style={{ color: "#c7cffb" }}>Open-text comments are conditioned on satisfaction, delivery, and category so answers stay coherent.</p>
            </div>
            <div className="stat-card">
              <Sparkle size={20} />
              <h3 style={{ marginTop: 16 }}>Instant analytics</h3>
              <p style={{ color: "#c7cffb" }}>Built-in report pages show the full dataset and summary analysis in a polished interface.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
