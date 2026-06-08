import base64
import io
from typing import Any, Dict
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")


def fig_to_base64(fig: plt.Figure) -> str:
    buffer = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", dpi=120, facecolor="#12131f")
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close(fig)
    return encoded


def make_correlation_heatmap(corr_matrix: Any) -> str:
    fig, ax = plt.subplots(figsize=(5, 4), facecolor="#12131f")
    sns.heatmap(corr_matrix, annot=True, cmap="vlag", center=0, ax=ax, linewidths=0.5, linecolor="#2f3241")
    ax.set_title("Correlation Matrix", color="#f0f0f5")
    ax.tick_params(colors="#d8d8e8")
    return fig_to_base64(fig)


def make_satisfaction_distribution(df) -> str:
    fig, ax = plt.subplots(figsize=(5, 4), facecolor="#12131f")
    sns.countplot(x="satisfaction", data=df, color="#81ecec", ax=ax)
    ax.set_title("Satisfaction Distribution", color="#f0f0f5")
    ax.set_xlabel("Satisfaction", color="#d8d8e8")
    ax.set_ylabel("Count", color="#d8d8e8")
    ax.tick_params(colors="#d8d8e8")
    return fig_to_base64(fig)


def make_nps_distribution(df) -> str:
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#12131f")
    sns.histplot(df["nps"], bins=11, kde=False, color="#81ecec", ax=ax)
    ax.set_title("NPS Distribution", color="#f0f0f5")
    ax.set_xlabel("NPS", color="#d8d8e8")
    ax.set_ylabel("Count", color="#d8d8e8")
    ax.tick_params(colors="#d8d8e8")
    return fig_to_base64(fig)


def make_category_distribution(df) -> str:
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#12131f")
    order = df["category"].value_counts().index
    sns.countplot(x="category", data=df, order=order, color="#74b9ff", ax=ax)
    ax.set_title("Category Distribution", color="#f0f0f5")
    ax.set_xlabel("Category", color="#d8d8e8")
    ax.set_ylabel("Count", color="#d8d8e8")
    ax.tick_params(colors="#d8d8e8")
    return fig_to_base64(fig)


def make_delivery_pie(df) -> str:
    counts = df["delivery"].value_counts()
    fig, ax = plt.subplots(figsize=(4, 4), facecolor="#12131f")
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=["#00b894", "#d63031"], startangle=140, textprops={"color": "#f0f0f5"})
    ax.set_title("Delivery Outcome", color="#f0f0f5")
    return fig_to_base64(fig)


def make_persona_distribution(persona_counts: Dict[str, int]) -> str:
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#12131f")
    labels = list(persona_counts.keys())
    values = list(persona_counts.values())
    sns.barplot(x=values, y=labels, color="#fdcb6e", ax=ax)
    ax.set_title("Persona Distribution", color="#f0f0f5")
    ax.set_xlabel("Count", color="#d8d8e8")
    ax.set_ylabel("Persona", color="#d8d8e8")
    ax.tick_params(colors="#d8d8e8")
    return fig_to_base64(fig)


def make_funnel_chart(accepted: int, rejected: int) -> str:
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#12131f")
    values = [accepted + rejected, accepted]
    labels = ["Generated", "Accepted"]
    ax.barh(labels, values, color=["#74b9ff", "#55efc4"])
    ax.set_title("Acceptance / Rejection Funnel", color="#f0f0f5")
    ax.tick_params(colors="#d8d8e8")
    for i, value in enumerate(values):
        ax.text(value + max(1, int(value * 0.02)), i, str(value), va="center", color="#f0f0f5")
    return fig_to_base64(fig)


def make_confusion_matrix(cm, labels) -> str:
    fig, ax = plt.subplots(figsize=(5, 4), facecolor="#12131f")
    sns.heatmap(cm, annot=True, fmt="d", cmap="rocket", xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title("Persona Recovery Confusion Matrix", color="#f0f0f5")
    ax.set_xlabel("Predicted", color="#d8d8e8")
    ax.set_ylabel("Actual", color="#d8d8e8")
    ax.tick_params(colors="#d8d8e8")
    return fig_to_base64(fig)


def build_html_report(context: Dict[str, Any], output_path: str) -> None:
    template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Survey Response Quality Report</title>
    <style>
        :root {
            color-scheme: dark;
            --bg: #090b16;
            --panel: #12151f;
            --panel-strong: #1c2331;
            --border: rgba(103, 141, 255, 0.22);
            --text: #e9eef8;
            --muted: #9aa4c4;
            --accent: #5ed4ff;
            --accent-alt: #ffd56b;
            --success: #55efc4;
            --warning: #ffcc00;
            --danger: #ff7675;
        }

        * { box-sizing: border-box; }
        body { margin: 0; min-height: 100vh; background: radial-gradient(circle at top, rgba(94, 212, 255, 0.12), transparent 28%), linear-gradient(180deg, #090b16 0%, #080a13 100%); color: var(--text); font-family: Inter, Arial, sans-serif; }
        .page { padding: 32px; max-width: 1420px; margin: 0 auto; }
        .hero { display: grid; grid-template-columns: 1.5fr 1fr; gap: 24px; align-items: start; margin-bottom: 32px; }
        .hero h1 { margin: 0 0 12px; font-size: clamp(2.4rem, 3vw, 3.6rem); line-height: 1.05; }
        .hero p { margin: 0; color: var(--muted); font-size: 1.05rem; max-width: 780px; }
        .hero-meta { display: grid; gap: 12px; }
        .badge { display: inline-flex; align-items: center; gap: 8px; padding: 0.75rem 1rem; border-radius: 999px; background: rgba(60, 93, 255, 0.12); color: #dce6ff; border: 1px solid rgba(94, 212, 255, 0.18); font-size: 0.95rem; }
        .badge.highlight { background: rgba(85, 239, 196, 0.13); border-color: rgba(85, 239, 196, 0.3); color: #d8ffe7; }
        .section { margin-bottom: 42px; }
        .section-header { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px; }
        .section-header h2 { margin: 0; font-size: 1.75rem; }
        .section-header p { margin: 0; color: var(--muted); max-width: 680px; }
        .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; }
        .metric-card, .summary-card, .insight-card, .feedback-card, .chart-card, .diagram-step { background: var(--panel); border: 1px solid var(--border); border-radius: 20px; padding: 22px; box-shadow: 0 18px 60px rgba(0, 0, 0, 0.18); }
        .metric-card strong, .summary-card strong { display: block; margin-bottom: 10px; color: #f7f9ff; font-size: 0.95rem; letter-spacing: 0.02em; }
        .metric-card p, .summary-card p { margin: 0; font-size: 2rem; font-weight: 700; }
        .metric-card span.value { color: var(--accent); }
        .chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
        .chart-card { padding: 16px; }
        .chart-card img { width: 100%; border-radius: 16px; display: block; }
        .table-card { overflow-x: auto; background: linear-gradient(180deg, rgba(18, 23, 37, 0.9), rgba(18, 23, 37, 0.98)); border: 1px solid rgba(94, 212, 255, 0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 16px; color: var(--text); }
        th, td { padding: 14px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        th { text-align: left; color: #b3c2ec; font-weight: 600; background: rgba(255,255,255,0.03); }
        td { background: rgba(255,255,255,0.02); }
        .insight-list { display: grid; gap: 14px; }
        .insight-card { display: flex; gap: 14px; align-items: flex-start; }
        .insight-card span { display: inline-flex; width: 34px; height: 34px; align-items: center; justify-content: center; border-radius: 50%; background: rgba(94, 212, 255, 0.18); color: var(--accent); font-weight: 700; }
        .insight-card p { margin: 0; color: var(--text); line-height: 1.75; }
        .feedback-grid { display: grid; gap: 18px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
        .feedback-card { min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; }
        .feedback-card h3 { margin: 0 0 12px; font-size: 1rem; color: #eaf0ff; }
        .feedback-card p { margin: 0 0 16px; color: var(--muted); line-height: 1.7; }
        .feedback-card .meta { display: flex; flex-wrap: wrap; gap: 10px; font-size: 0.92rem; color: #b3c2ec; }
        .feedback-card .badge { padding: 0.45rem 0.85rem; font-size: 0.85rem; }
        .diagram { display: flex; flex-wrap: wrap; align-items: center; gap: 16px; justify-content: center; margin-top: 22px; }
        .diagram-step { min-width: 160px; text-align: center; }
        .diagram-step p { margin: 0; color: #eef1ff; font-size: 0.95rem; }
        .diagram-arrow { color: #8f9ad8; font-size: 1.8rem; }
        .report-footer { color: var(--muted); font-size: 0.95rem; line-height: 1.7; }
        .report-footer a { color: var(--accent); text-decoration: none; }
    </style>
</head>
<body>
    <div class="page">
        <div class="hero">
            <div>
                <h1>Survey Response Quality Report</h1>
                <p>Deep analytics for synthetic customer feedback, focusing on response validity, distribution behavior, and persona-driven signal quality.</p>
                <div class="hero-meta">
                    <span class="badge">{{ total_responses }} responses</span>
                    <span class="badge highlight">Acceptance: {{ (acceptance_rate * 100) | round(1) }}%</span>
                    <span class="badge highlight">Persona accuracy: {{ (persona_results.accuracy * 100) | round(1) }}%</span>
                </div>
            </div>

            <div class="card-grid">
                <div class="metric-card"><strong>Acceptance rate</strong><p><span class="value">{{ (acceptance_rate * 100) | round(1) }}%</span></p></div>
                <div class="metric-card"><strong>Rejection rate</strong><p><span class="value">{{ (rejection_rate * 100) | round(1) }}%</span></p></div>
                <div class="metric-card"><strong>Duplicate feedback</strong><p><span class="value">{{ (text_metrics.duplicate_rate * 100) | round(1) }}%</span></p></div>
                <div class="metric-card"><strong>Average feedback length</strong><p><span class="value">{{ text_metrics.average_feedback_length | round(1) }}</span> words</p></div>
                <div class="metric-card"><strong>Unique feedback</strong><p><span class="value">{{ text_metrics.unique_feedback }}</span></p></div>
                <div class="metric-card"><strong>Median feedback</strong><p><span class="value">{{ text_metrics.median_feedback_length | round(1) }}</span> words</p></div>
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <div>
                    <h2>Executive summary</h2>
                    <p>Top-level findings from the synthetic survey generation pipeline, including quality checks, distribution behavior, and persona recovery strength.</p>
                </div>
            </div>
            <div class="insight-list">
                {% for insight in insights %}
                <div class="insight-card">
                    <span>→</span>
                    <p>{{ insight }}</p>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="section chart-grid">
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.correlation_heatmap }}" alt="Correlation heatmap"/></div>
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.persona_distribution }}" alt="Persona distribution"/></div>
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.satisfaction_distribution }}" alt="Satisfaction distribution"/></div>
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.nps_distribution }}" alt="NPS distribution"/></div>
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.category_distribution }}" alt="Category distribution"/></div>
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.delivery_pie }}" alt="Delivery pie chart"/></div>
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.funnel_chart }}" alt="Acceptance funnel"/></div>
            <div class="chart-card"><img src="data:image/png;base64,{{ charts.confusion_matrix }}" alt="Persona confusion matrix"/></div>
        </div>

        <div class="section">
            <div class="section-header">
                <div>
                    <h2>Validation metrics</h2>
                    <p>Detailed conditional probabilities and distribution summaries show where the synthetic responses align with expected customer behavior.</p>
                </div>
            </div>

            <div class="card-grid">
                <div class="table-card">
                    <h3>Conditional probability analysis</h3>
                    <table>
                        <tr><th>Condition</th><th>Value</th></tr>
                        <tr><td>P(NPS ≥ 8 | Satisfaction ≥ 4)</td><td>{{ conditional_probabilities.p_nps_high_given_satisfaction_high | round(2) }}</td></tr>
                        <tr><td>P(NPS ≥ 8 | Satisfaction ≤ 2)</td><td>{{ conditional_probabilities.p_nps_high_given_satisfaction_low | round(2) }}</td></tr>
                        <tr><td>P(Satisfaction ≥ 4 | Delivery = Yes)</td><td>{{ conditional_probabilities.p_satisfaction_high_given_delivery_yes | round(2) }}</td></tr>
                        <tr><td>P(Satisfaction ≥ 4 | Delivery = No)</td><td>{{ conditional_probabilities.p_satisfaction_high_given_delivery_no | round(2) }}</td></tr>
                    </table>
                </div>
                <div class="table-card">
                    <h3>Distribution summaries</h3>
                    <table>
                        <tr><th>Distribution</th><th>Counts</th></tr>
                        <tr><td>Satisfaction</td><td>{{ distributions.satisfaction }}</td></tr>
                        <tr><td>NPS</td><td>{{ distributions.nps }}</td></tr>
                        <tr><td>Category</td><td>{{ distributions.category }}</td></tr>
                        <tr><td>Delivery</td><td>{{ distributions.delivery }}</td></tr>
                    </table>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <div>
                    <h2>Representative feedback examples</h2>
                    <p>Selected comments from the generated dataset provide context for the quality metrics and highlight how sentiment is expressed with respect to category and delivery.</p>
                </div>
            </div>
            <div class="feedback-grid">
                {% for feedback in feedback_samples %}
                <div class="feedback-card">
                    <div>
                        <h3>{{ feedback.label }}</h3>
                        <p>“{{ feedback.feedback }}”</p>
                    </div>
                    <div class="meta">
                        <span class="badge">Satisfaction: {{ feedback.satisfaction }}</span>
                        <span class="badge">NPS: {{ feedback.nps }}</span>
                        <span class="badge">Category: {{ feedback.category }}</span>
                        <span class="badge">Delivery: {{ feedback.delivery }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="section">
            <h2>Architecture overview</h2>
            <div class="diagram">
                <div class="diagram-step"><p>Survey Definition</p></div>
                <div class="diagram-arrow">→</div>
                <div class="diagram-step"><p>Synthetic Population</p></div>
                <div class="diagram-arrow">→</div>
                <div class="diagram-step"><p>Latent Customer Simulation</p></div>
                <div class="diagram-arrow">→</div>
                <div class="diagram-step"><p>Structured Response Generation</p></div>
                <div class="diagram-arrow">→</div>
                <div class="diagram-step"><p>Open Text Generation</p></div>
                <div class="diagram-arrow">→</div>
                <div class="diagram-step"><p>Validation & Analysis</p></div>
            </div>
        </div>

        <div class="section report-footer">
            <p>The synthetic dataset is generated by a latent customer model, persona-driven feedback generation, deterministic consistency rules, and a critic stage. This report is designed to provide a concise, colorful, and structured overview of generation quality and model behavior.</p>
        </div>
    </div>
</body>
</html>
"""
    from jinja2 import Template
    html = Template(template).render(**context)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(html)
