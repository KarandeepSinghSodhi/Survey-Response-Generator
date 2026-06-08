import { useEffect, useState } from "react";
import Link from "next/link";
import { SyntheticResponse } from "../lib/generator";
import { Search, ListChecks } from "lucide-react";

export default function Responses() {
  const [rows, setRows] = useState<SyntheticResponse[]>([]);
  const [filter, setFilter] = useState("");
  const [dataSource, setDataSource] = useState<"survey" | "synthetic">("synthetic");

  useEffect(() => {
    // Try to load survey responses first, then fall back to synthetic responses
    const surveyResponses = window.localStorage.getItem("survey-responses");
    const syntheticResponses = window.localStorage.getItem("survey-sensum-responses");
    
    if (surveyResponses) {
      setRows(JSON.parse(surveyResponses));
      setDataSource("survey");
    } else if (syntheticResponses) {
      setRows(JSON.parse(syntheticResponses));
      setDataSource("synthetic");
    }
  }, []);

  const filteredRows = rows.filter((row) =>
    [row.category, row.delivery, row.feedback, row.persona].some((value) =>
      value.toLowerCase().includes(filter.toLowerCase()),
    ),
  );

  return (
    <div className="container">
      <section className="section" style={{ paddingTop: 60 }}>
        <div className="grid-two" style={{ gap: 28, alignItems: "flex-start" }}>
          <div>
            <div className="hero-badge">
              <ListChecks size={18} />
              Browse every response in a modern table layout
            </div>
            <h1 className="page-title">Responses</h1>
            <p className="subtitle" style={{ marginTop: 24 }}>
              {dataSource === "survey" 
                ? "View all manually entered survey responses with detailed feedback."
                : "Search by category, delivery, persona, or commentary to inspect the dataset."}
            </p>
            <div style={{ marginTop: 32, display: "flex", gap: 16, flexWrap: "wrap" }}>
              <Link href="/" className="button secondary">Back home</Link>
              {dataSource === "survey" && <Link href="/survey" className="button secondary">Add more responses</Link>}
              <Link href="/report" className="button">View report</Link>
            </div>
          </div>
          <div className="glass-card" style={{ padding: 32 }}>
            <h2 className="card-title">Dataset details</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total rows</h3>
                <p className="stat-value">{rows.length}</p>
              </div>
              <div className="stat-card">
                <h3>Visible rows</h3>
                <p className="stat-value">{filteredRows.length}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="glass-card" style={{ padding: 24 }}>
          <div className="grid-two" style={{ gap: 20, alignItems: "end" }}>
            <div>
              <h2 className="card-title">Response table</h2>
              <p style={{ color: "#c7cffb" }}>Search the generated dataset or scroll through the full response feed.</p>
            </div>
            <div style={{ width: "100%", maxWidth: 360 }}>
              <label className="label" htmlFor="search">Search responses</label>
              <div style={{ position: "relative" }}>
                <Search size={18} style={{ position: "absolute", top: 18, left: 16, color: "#97a0ff" }} />
                <input
                  id="search"
                  className="input"
                  style={{ paddingLeft: 44 }}
                  value={filter}
                  onChange={(event) => setFilter(event.target.value)}
                  placeholder="Type category, delivery, persona..."
                />
              </div>
            </div>
          </div>

          <div className="table-wrapper" style={{ marginTop: 22 }}>
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Category</th>
                  <th>Satisfaction</th>
                  <th>NPS</th>
                  <th>Delivery</th>
                  {dataSource === "synthetic" && <th>Persona</th>}
                  <th>Feedback</th>
                </tr>
              </thead>
              <tbody>
                {filteredRows.map((row) => (
                  <tr key={row.id}>
                    <td>{row.id}</td>
                    <td>{row.category}</td>
                    <td>{row.satisfaction}</td>
                    <td>{row.nps}</td>
                    <td>{row.delivery}</td>
                    {dataSource === "synthetic" && <td>{(row as any).persona}</td>}
                    <td>{row.feedback}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}
