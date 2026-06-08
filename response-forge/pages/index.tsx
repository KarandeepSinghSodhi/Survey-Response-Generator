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
  const [deliveryRate, setDeliveryRate] = useState(0.8);
  const [sentimentBias, setSentimentBias] = useState(0.0);
  const [dataset, setDataset] = useState<SyntheticResponse[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const summary = useMemo(() => (dataset ? summaryFromData(dataset) : null), [dataset]);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${apiUrl}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          count: responseCount,
          delivery_rate: deliveryRate,
          sentiment_bias: sentimentBias,
        }),
      });
      if (!res.ok) throw new Error("Server returned an error status");
      
      const data = await res.json();
      if (data && data.records) {
        setDataset(data.records);
        window.localStorage.setItem("survey-sensum-responses", JSON.stringify(data.records));
        setLoading(false);
        return;
      }
    } catch (e) {
      console.warn("Backend API not reachable. Falling back to local offline generation.", e);
      setError("Backend unreachable (or booting up). Fell back to offline generation.");
      
      // Fallback to client-side generation
      const rows = generateSyntheticResponses(responseCount, deliveryRate, sentimentBias);
      setDataset(rows);
      window.localStorage.setItem("survey-sensum-responses", JSON.stringify(rows));
      
      // Clear error after 5 seconds
      setTimeout(() => setError(null), 5000);
    }
    setLoading(false);
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

            {/* Parameter Adjustment Panel */}
            <div style={{ marginTop: 28, background: "rgba(255, 255, 255, 0.03)", padding: 20, borderRadius: 20, border: "1px solid rgba(255, 255, 255, 0.06)" }}>
              <h3 style={{ margin: "0 0 16px", fontSize: "0.95rem", color: "#9aa7ff", fontWeight: 600 }}>Generator Controls</h3>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: 16 }}>
                <div>
                  <label className="label" style={{ fontSize: "0.8rem", color: "#bec7ff", marginBottom: 4 }}>Response Count (N)</label>
                  <input
                    type="number"
                    min="10"
                    max="500"
                    value={responseCount}
                    onChange={(e) => setResponseCount(Math.min(500, Math.max(10, parseInt(e.target.value) || 10)))}
                    className="input"
                    style={{ padding: "8px 12px", borderRadius: 10, fontSize: "0.9rem", height: 40 }}
                  />
                </div>
                <div>
                  <label className="label" style={{ fontSize: "0.8rem", color: "#bec7ff", marginBottom: 4 }}>On-Time Delivery Rate</label>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, height: 40 }}>
                    <input
                      type="range"
                      min="10"
                      max="100"
                      value={deliveryRate * 100}
                      onChange={(e) => setDeliveryRate(parseInt(e.target.value) / 100)}
                      style={{ width: "100%", accentColor: "#7c5cff", cursor: "pointer" }}
                    />
                    <span style={{ fontSize: "0.85rem", color: "#fff", fontWeight: 600, width: 36, textAlign: "right" }}>{Math.round(deliveryRate * 100)}%</span>
                  </div>
                </div>
                <div>
                  <label className="label" style={{ fontSize: "0.8rem", color: "#bec7ff", marginBottom: 4 }}>Satisfaction Bias</label>
                  <select
                    value={sentimentBias}
                    onChange={(e) => setSentimentBias(parseFloat(e.target.value))}
                    className="select"
                    style={{ padding: "8px 12px", borderRadius: 10, fontSize: "0.9rem", height: 40 }}
                  >
                    <option value="-0.2">Negative Skew</option>
                    <option value="0.0">Balanced / Neutral</option>
                    <option value="0.2">Positive Skew</option>
                  </select>
                </div>
              </div>
            </div>

            <div style={{ marginTop: 28, display: "flex", flexWrap: "wrap", gap: 16, alignItems: "center" }}>
              <button className="button" onClick={handleGenerate} disabled={loading}>
                {loading ? "Generating..." : `Generate ${responseCount} responses`}
              </button>
              <Link href="/survey" className="button secondary">Add responses manually</Link>
              <Link href="/report" className="button secondary">View report</Link>
              <Link href="/responses" className="button secondary">View responses</Link>
            </div>
            {error && (
              <div style={{ marginTop: 16, color: "#ff8c8c", fontSize: "0.9rem", display: "flex", gap: 8, alignItems: "center" }}>
                <span>⚠️</span> {error}
              </div>
            )}
          </div>
          <div className="glass-card" style={{ padding: 32 }}>
            <h2 className="card-title">Survey definition</h2>
            <p style={{ marginBottom: 24, color: "#c7cffb" }}>
              This demo uses the exact assignment questions and creates N plausible responses with consistent satisfaction, NPS, category, delivery, and open feedback.
            </p>
            <div className="definition-list">
              <div className="definition-item">
                <div className="definition-badge">1</div>
                <div className="definition-content">
                  <h4 className="definition-title">Satisfaction</h4>
                  <p className="definition-desc">1–5 scale rating of overall purchase happiness</p>
                </div>
              </div>
              <div className="definition-item">
                <div className="definition-badge">2</div>
                <div className="definition-content">
                  <h4 className="definition-title">Likelihood to recommend</h4>
                  <p className="definition-desc">0–10 standard Net Promoter Score (NPS)</p>
                </div>
              </div>
              <div className="definition-item">
                <div className="definition-badge">3</div>
                <div className="definition-content">
                  <h4 className="definition-title">Category</h4>
                  <p className="definition-desc">Product type: Electronics / Clothing / Home / Other</p>
                </div>
              </div>
              <div className="definition-item">
                <div className="definition-badge">4</div>
                <div className="definition-content">
                  <h4 className="definition-title">Delivery</h4>
                  <p className="definition-desc">Was the delivery received on-time? (Yes / No)</p>
                </div>
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
              <p className="stat-value">{dataset ? dataset.length : 0}</p>
            </div>
            <div className="stat-card">
              <h3>Average satisfaction</h3>
              <p className="stat-value">{summary ? summary.average : "—"}</p>
            </div>
            <div className="stat-card">
              <h3>Average NPS</h3>
              <p className="stat-value">{summary ? summary.npsAverage : "—"}</p>
            </div>
            <div className="stat-card">
              <h3>On-time rate</h3>
              <p className="stat-value">{summary ? `${summary.onTimeRate}%` : "—"}</p>
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
