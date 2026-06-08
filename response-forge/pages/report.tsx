import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from "recharts";
import { SyntheticResponse } from "../lib/generator";
import { ArrowRight, Activity } from "lucide-react";

const COLORS = ["#7c5cff", "#3bc7ff", "#1b8eff", "#d27fff"];

const groupBy = (rows: SyntheticResponse[], key: keyof SyntheticResponse) =>
  rows.reduce<Record<string, number>>((acc, row) => {
    const value = String(row[key]);
    acc[value] = (acc[value] ?? 0) + 1;
    return acc;
  }, {});

const createPieData = (rows: SyntheticResponse[], key: keyof SyntheticResponse) =>
  Object.entries(groupBy(rows, key)).map(([name, value]) => ({ name, value }));

const formatNumber = (value: number) => value.toFixed(1);

const summaryMeasures = (rows: SyntheticResponse[]) => {
  const avgSatisfaction = rows.reduce((sum, row) => sum + row.satisfaction, 0) / rows.length;
  const avgNps = rows.reduce((sum, row) => sum + row.nps, 0) / rows.length;
  const onTimeRate = rows.filter((row) => row.delivery === "Yes").length / rows.length;
  return { avgSatisfaction, avgNps, onTimeRate };
};

export default function Report() {
  const [rows, setRows] = useState<SyntheticResponse[]>([]);

  useEffect(() => {
    // Try to load survey responses first, then fall back to synthetic responses
    const surveyResponses = window.localStorage.getItem("survey-responses");
    const syntheticResponses = window.localStorage.getItem("survey-sensum-responses");
    
    if (surveyResponses) {
      setRows(JSON.parse(surveyResponses));
    } else if (syntheticResponses) {
      setRows(JSON.parse(syntheticResponses));
    }
  }, []);

  const summary = useMemo(() => (rows.length ? summaryMeasures(rows) : null), [rows]);
  const categoryData = useMemo(() => createPieData(rows, "category"), [rows]);
  const deliveryData = useMemo(() => createPieData(rows, "delivery"), [rows]);

  if (!rows.length) {
    return (
      <div className="container">
        <section className="section" style={{ paddingTop: 60 }}>
          <div className="glass-card" style={{ padding: 40 }}>
            <h1 className="page-title">Create data first</h1>
            <p className="subtitle">Generate a synthetic dataset on the homepage before opening the report.</p>
            <Link href="/" className="button" style={{ marginTop: 24 }}>Back to generator</Link>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="container">
      <section className="section" style={{ paddingTop: 60 }}>
        <div className="grid-two" style={{ gap: 28, alignItems: "flex-start" }}>
          <div>
            <div className="hero-badge">
              <Activity size={18} />
              Interactive analysis for your synthetic survey dataset
            </div>
            <h1 className="page-title">Report & analysis</h1>
            <p className="subtitle" style={{ marginTop: 24 }}>
              A clean dashboard view of satisfaction, NPS, category mix, delivery reliability, and the exact response distribution.
            </p>
            <div style={{ marginTop: 32, display: "flex", gap: 16, flexWrap: "wrap" }}>
              <Link href="/" className="button secondary">Back to generator</Link>
              <Link href="/responses" className="button">View response table</Link>
            </div>
          </div>
          <div className="glass-card" style={{ padding: 32 }}>
            <h2 className="card-title">Dataset summary</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total responses</h3>
                <p className="stat-value">{rows.length}</p>
              </div>
              <div className="stat-card">
                <h3>Avg satisfaction</h3>
                <p className="stat-value">{summary ? formatNumber(summary.avgSatisfaction) : "—"}</p>
              </div>
              <div className="stat-card">
                <h3>Avg NPS</h3>
                <p className="stat-value">{summary ? formatNumber(summary.avgNps) : "—"}</p>
              </div>
              <div className="stat-card">
                <h3>On-time delivery</h3>
                <p className="stat-value">{summary ? `${Math.round(summary.onTimeRate * 100)}%` : "—"}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="grid-two">
          <div className="glass-card" style={{ padding: 28 }}>
            <h2 className="card-title">Category mix</h2>
            <ResponsiveContainer width="100%" height={320}>
              <PieChart>
                <Pie data={categoryData} dataKey="value" nameKey="name" innerRadius={58} outerRadius={108} paddingAngle={4}>
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip cursor={{ fill: "rgba(255,255,255,0.06)" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="glass-card" style={{ padding: 28 }}>
            <h2 className="card-title">Delivery reliability</h2>
            <ResponsiveContainer width="100%" height={320}>
              <PieChart>
                <Pie data={deliveryData} dataKey="value" nameKey="name" innerRadius={58} outerRadius={108} paddingAngle={4}>
                  {deliveryData.map((entry, index) => (
                    <Cell key={`delivery-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip cursor={{ fill: "rgba(255,255,255,0.06)" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="glass-card" style={{ padding: 28 }}>
          <h2 className="card-title">Satisfaction distribution</h2>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={Array.from({ length: 5 }, (_, i) => ({ name: `${i + 1}`, value: rows.filter((row) => row.satisfaction === i + 1).length }))}>
              <XAxis dataKey="name" stroke="#a3b1ff" />
              <YAxis stroke="#a3b1ff" />
              <Tooltip cursor={{ fill: "rgba(255,255,255,0.06)" }} />
              <Bar dataKey="value" fill="#7c5cff" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}
