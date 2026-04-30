import React, { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell
} from "recharts";

const API_BASE = "http://127.0.0.1:8000";

// Simple UI replacements (no shadcn dependency)
const Card = ({ children }) => (
  <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16, background: "#fff" }}>
    {children}
  </div>
);

const CardContent = ({ children }) => <div>{children}</div>;

const Button = ({ children, onClick, disabled }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    style={{
      padding: "10px 14px",
      borderRadius: 6,
      border: "1px solid #333",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.6 : 1
    }}
  >
    {children}
  </button>
);

export default function RiskDashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSummary = async () => {
    const res = await fetch(`${API_BASE}/risk/summary`);
    const data = await res.json();
    setSummary(data);
  };

  const runPipeline = async () => {
    setLoading(true);
    await fetch(`${API_BASE}/risk/run`, { method: "POST" });
    await fetchSummary();
    setLoading(false);
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const breakdownData = summary?.breakdown || [];

  const pieData = breakdownData.map((b) => ({
    name: b.category,
    value: b.weighted_score || 0
  }));

  return (
    <div style={{ padding: 24, display: "grid", gap: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Risk Intelligence Dashboard</h1>
        <Button onClick={runPipeline} disabled={loading}>
          {loading ? "Running..." : "Run Risk Pipeline"}
        </Button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
        <Card>
          <CardContent>
            <div>Risk Score</div>
            <h2>{summary?.risk_score ?? 0}</h2>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div>Risk Level</div>
            <h2>{summary?.risk_level ?? "LOW"}</h2>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div>Findings</div>
            <h2>{breakdownData.length}</h2>
          </CardContent>
        </Card>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Card>
          <CardContent>
            <h3>Risk Breakdown</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={breakdownData}>
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="weighted_score" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <h3>Risk Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={100}
                  label
                >
                  {pieData.map((_, index) => (
                    <Cell key={index} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent>
          <h3>Findings</h3>
          <div style={{ maxHeight: 300, overflow: "auto" }}>
            {(summary?.breakdown || []).map((f, i) => (
              <div key={i} style={{ borderBottom: "1px solid #f70f0f", padding: 8 }}>
                <strong>{f.rule || f.rule_name}</strong>
                <div style={{ fontSize: 12 }}>
                  {f.category} • {f.severity}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
