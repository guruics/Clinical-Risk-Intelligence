import React, { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
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
    value: b.score || 0
  }));

  return (
    <div className="p-6 grid gap-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Risk Intelligence Dashboard</h1>
        <Button onClick={runPipeline} disabled={loading}>
          {loading ? "Running..." : "Run Risk Pipeline"}
        </Button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Card>
          <CardContent>
            <div className="text-sm">Risk Score</div>
            <div className="text-3xl font-bold">
              {summary?.risk_score ?? 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div className="text-sm">Risk Level</div>
            <div className="text-3xl font-bold">
              {summary?.risk_level ?? "LOW"}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div className="text-sm">Findings</div>
            <div className="text-3xl font-bold">
              {breakdownData.length}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardContent>
            <h2 className="font-semibold mb-2">Risk Breakdown</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={breakdownData}>
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <h2 className="font-semibold mb-2">Risk Distribution</h2>
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
          <h2 className="font-semibold mb-2">Findings</h2>
          <div className="max-h-96 overflow-auto text-sm">
            {(summary?.breakdown || []).map((f, i) => (
              <div key={i} className="border-b py-2">
                <div className="font-medium">{f.rule || f.rule_name}</div>
                <div className="text-xs">
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
