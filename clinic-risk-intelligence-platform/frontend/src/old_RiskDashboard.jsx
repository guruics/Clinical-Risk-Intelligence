import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

const COLORS = [
  "#8884d8", // purple
  "#82ca9d", // green
  "#ffc658", // yellow
  "#ff7f7f", // red
  "#00C49F", // teal
  "#0088FE", // blue
  "#FFBB28", // gold
  "#FF8042"  // orange
];

export default function RiskDashboard() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/risk/summary")
      .then((res) => res.json())
      .then((data) => setSummary(data))
      .catch((err) => console.error(err));
  }, []);

  if (!summary) return <div>Loading...</div>;

  // -----------------------------
  // CATEGORY AGGREGATION
  // -----------------------------
  const categoryMap = {};

  summary.breakdown.forEach((item) => {
    const cat = item.category || "UNKNOWN";

    if (!categoryMap[cat]) {
      categoryMap[cat] = 0;
    }

    categoryMap[cat] += item.weighted_score || 0;
  });

  const buildRuleData = (breakdown) => {
  const ruleMap = {};

  breakdown.forEach((item) => {
    const key = item.rule;

    if (!ruleMap[key]) {
      ruleMap[key] = {
        rule: item.rule,
        category: item.category,
        severity: item.severity,
        total_score: 0,
        occurrences: 0,
        events: []
      };
    }

    ruleMap[key].total_score += item.weighted_score || 0;
    ruleMap[key].occurrences += 1;

    if (item.event_id) {
      ruleMap[key].events.push(item.event_id);
    }
  });

  return Object.values(ruleMap);
};



  const chartData = Object.keys(categoryMap).map((key) => ({
    name: key,
    value: categoryMap[key]
  }));

  // -----------------------------
  // COLOR MAPPING (consistent)
  // -----------------------------
  const colorMap = {};
  chartData.forEach((entry, index) => {
    colorMap[entry.name] = COLORS[index % COLORS.length];
  });

  return (
    <div style={{ padding: "20px" }}>
      <h2>Risk Dashboard</h2>

      <h3>Risk Score: {summary.risk_score}</h3>
      <h4>Risk Level: {summary.risk_level}</h4>

      {/* -----------------------------
          BAR CHART
      ----------------------------- */}
      <BarChart width={600} height={300} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />

        <Bar dataKey="value">
          {chartData.map((entry, index) => (
            <Cell key={`bar-${index}`} fill={colorMap[entry.name]} />
          ))}
        </Bar>
      </BarChart>

      {/* -----------------------------
          PIE CHART
      ----------------------------- */}
      <PieChart width={400} height={400}>
        <Pie
          data={chartData}
          dataKey="value"
          nameKey="name"
          outerRadius={150}
          label
        >
          {chartData.map((entry, index) => (
            <Cell key={`pie-${index}`} fill={colorMap[entry.name]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}