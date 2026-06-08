import { useState } from "react";
import Link from "next/link";
import { Plus, ArrowRight, AlertCircle } from "lucide-react";

const CATEGORIES = ["Electronics", "Clothing", "Home", "Other"];

type SurveyFormData = {
  satisfaction: number;
  nps: number;
  category: string;
  delivery: "Yes" | "No";
  feedback: string;
};

export default function SurveyForm() {
  const [formData, setFormData] = useState<SurveyFormData>({
    satisfaction: 3,
    nps: 5,
    category: "Electronics",
    delivery: "Yes",
    feedback: "",
  });

  const [submitted, setSubmitted] = useState(false);
  const [responses, setResponses] = useState<(SurveyFormData & { id: number })[]>([]);

  const handleSliderChange = (field: "satisfaction" | "nps", value: number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleCategoryChange = (category: string) => {
    setFormData((prev) => ({ ...prev, category }));
  };

  const handleDeliveryChange = (delivery: "Yes" | "No") => {
    setFormData((prev) => ({ ...prev, delivery }));
  };

  const handleFeedbackChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormData((prev) => ({ ...prev, feedback: e.target.value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Add to responses
    const newResponse = { ...formData, id: responses.length + 1 };
    const updatedResponses = [...responses, newResponse];
    setResponses(updatedResponses);

    // Save to localStorage
    window.localStorage.setItem("survey-responses", JSON.stringify(updatedResponses));

    // Reset form
    setFormData({
      satisfaction: 3,
      nps: 5,
      category: "Electronics",
      delivery: "Yes",
      feedback: "",
    });
    setSubmitted(true);

    // Hide success message after 2 seconds
    setTimeout(() => setSubmitted(false), 2000);
  };

  const satisfactionLabels: { [key: number]: string } = {
    1: "Very Unsatisfied",
    2: "Unsatisfied",
    3: "Neutral",
    4: "Satisfied",
    5: "Very Satisfied",
  };

  const npsLabels: { [key: number]: string } = {
    0: "Very Unlikely",
    5: "Neutral",
    10: "Very Likely",
  };

  return (
    <div className="container">
      <section className="section" style={{ paddingTop: 60 }}>
        <div style={{ maxWidth: "820px", margin: "0 auto" }}>
          <div className="hero-badge">
            <Plus size={18} />
            Add survey responses manually
          </div>
          <h1 className="page-title">Survey Response Form</h1>
          <p className="subtitle" style={{ marginTop: 16 }}>
            Fill out the survey questions below. Add as many responses as you'd like, then view the aggregated report and analysis dashboard.
          </p>
        </div>
      </section>

      <section className="section">
        <div style={{ maxWidth: "820px", margin: "0 auto" }}>
          <div className="glass-card" style={{ padding: 40 }}>
            <form onSubmit={handleSubmit}>
              {/* Satisfaction Slider */}
              <div style={{ marginBottom: 40 }}>
                <label className="label">
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span>Product Satisfaction</span>
                    <span style={{ fontSize: "1.1rem", color: "#7c5cff", fontWeight: 600 }}>
                      {formData.satisfaction}/5
                    </span>
                  </div>
                  <div style={{ marginTop: 8, color: "#a3b1ff", fontSize: "0.9rem" }}>
                    {satisfactionLabels[formData.satisfaction]}
                  </div>
                </label>
                <input
                  type="range"
                  min="1"
                  max="5"
                  value={formData.satisfaction}
                  onChange={(e) => handleSliderChange("satisfaction", parseInt(e.target.value))}
                  style={{
                    width: "100%",
                    height: "8px",
                    marginTop: 16,
                    cursor: "pointer",
                    accentColor: "#7c5cff",
                  }}
                />
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", color: "#7a81b8", marginTop: 8 }}>
                  <span>Very Unsatisfied</span>
                  <span>Very Satisfied</span>
                </div>
              </div>

              {/* NPS Slider */}
              <div style={{ marginBottom: 40 }}>
                <label className="label">
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span>Likelihood to Recommend (NPS)</span>
                    <span style={{ fontSize: "1.1rem", color: "#3bc7ff", fontWeight: 600 }}>
                      {formData.nps}/10
                    </span>
                  </div>
                  <div style={{ marginTop: 8, color: "#a3b1ff", fontSize: "0.9rem" }}>
                    {formData.nps <= 6 ? "Detractor" : formData.nps <= 8 ? "Passive" : "Promoter"}
                  </div>
                </label>
                <input
                  type="range"
                  min="0"
                  max="10"
                  value={formData.nps}
                  onChange={(e) => handleSliderChange("nps", parseInt(e.target.value))}
                  style={{
                    width: "100%",
                    height: "8px",
                    marginTop: 16,
                    cursor: "pointer",
                    accentColor: "#3bc7ff",
                  }}
                />
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", color: "#7a81b8", marginTop: 8 }}>
                  <span>Very Unlikely (0)</span>
                  <span>Very Likely (10)</span>
                </div>
              </div>

              {/* Category Selector */}
              <div style={{ marginBottom: 40 }}>
                <label className="label">Product Category</label>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 }}>
                  {CATEGORIES.map((cat) => (
                    <button
                      key={cat}
                      type="button"
                      onClick={() => handleCategoryChange(cat)}
                      style={{
                        padding: "14px 18px",
                        border: formData.category === cat ? "2px solid #7c5cff" : "1px solid rgba(255,255,255,0.12)",
                        borderRadius: "14px",
                        background: formData.category === cat ? "rgba(124, 92, 255, 0.12)" : "rgba(10, 12, 22, 0.88)",
                        color: formData.category === cat ? "#d7e1ff" : "#a3b1ff",
                        cursor: "pointer",
                        fontWeight: formData.category === cat ? 600 : 500,
                        transition: "all 0.2s ease",
                      }}
                    >
                      {cat}
                    </button>
                  ))}
                </div>
              </div>

              {/* Delivery Toggle */}
              <div style={{ marginBottom: 40 }}>
                <label className="label">Was delivery on time?</label>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 }}>
                  {(["Yes", "No"] as const).map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => handleDeliveryChange(opt)}
                      style={{
                        padding: "14px 18px",
                        border: formData.delivery === opt ? "2px solid #1b8eff" : "1px solid rgba(255,255,255,0.12)",
                        borderRadius: "14px",
                        background: formData.delivery === opt ? "rgba(27, 142, 255, 0.12)" : "rgba(10, 12, 22, 0.88)",
                        color: formData.delivery === opt ? "#d7e1ff" : "#a3b1ff",
                        cursor: "pointer",
                        fontWeight: formData.delivery === opt ? 600 : 500,
                        transition: "all 0.2s ease",
                      }}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>

              {/* Feedback Text */}
              <div style={{ marginBottom: 40 }}>
                <label className="label">Additional Feedback</label>
                <textarea
                  className="textarea"
                  value={formData.feedback}
                  onChange={handleFeedbackChange}
                  placeholder="Share your thoughts about the product, delivery, or shopping experience..."
                  style={{ minHeight: "120px", resize: "vertical" }}
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="button"
                style={{
                  width: "100%",
                  marginBottom: submitted ? 16 : 0,
                }}
              >
                <Plus size={20} style={{ marginRight: 8 }} />
                Add Response
              </button>

              {submitted && (
                <div
                  style={{
                    padding: "16px",
                    borderRadius: "14px",
                    background: "rgba(27, 200, 100, 0.12)",
                    border: "1px solid rgba(27, 200, 100, 0.24)",
                    color: "#7effca",
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                  }}
                >
                  <AlertCircle size={20} />
                  Response added! Total: {responses.length}
                </div>
              )}
            </form>
          </div>
        </div>
      </section>

      {/* Responses Summary */}
      {responses.length > 0 && (
        <section className="section">
          <div style={{ maxWidth: "820px", margin: "0 auto" }}>
            <div className="glass-card" style={{ padding: 40 }}>
              <h2 className="card-title">Responses Collected ({responses.length})</h2>
              <div className="stats-grid" style={{ marginBottom: 32 }}>
                <div className="stat-card">
                  <h3>Avg Satisfaction</h3>
                  <p>
                    {(responses.reduce((sum, r) => sum + r.satisfaction, 0) / responses.length).toFixed(1)}
                  </p>
                </div>
                <div className="stat-card">
                  <h3>Avg NPS</h3>
                  <p>
                    {(responses.reduce((sum, r) => sum + r.nps, 0) / responses.length).toFixed(1)}
                  </p>
                </div>
                <div className="stat-card">
                  <h3>On-time Delivery</h3>
                  <p>{Math.round((responses.filter((r) => r.delivery === "Yes").length / responses.length) * 100)}%</p>
                </div>
                <div className="stat-card">
                  <h3>Top Category</h3>
                  <p>
                    {
                      Object.entries(responses.reduce<Record<string, number>>((acc, r) => {
                        acc[r.category] = (acc[r.category] ?? 0) + 1;
                        return acc;
                      }, {})).sort(([, a], [, b]) => b - a)[0]?.[0]
                    }
                  </p>
                </div>
              </div>

              <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
                <Link href="/report" className="button">
                  View Report
                  <ArrowRight size={18} style={{ marginLeft: 8 }} />
                </Link>
                <Link href="/responses" className="button secondary">
                  View All Responses
                </Link>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Navigation */}
      <section className="section">
        <div style={{ maxWidth: "820px", margin: "0 auto", textAlign: "center" }}>
          <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
            <Link href="/" className="button secondary">
              Back Home
            </Link>
            {responses.length > 0 && (
              <>
                <Link href="/report" className="button secondary">
                  View Report
                </Link>
              </>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
