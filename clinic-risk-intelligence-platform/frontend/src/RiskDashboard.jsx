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
  "#8884d8",
  "#82ca9d",
  "#ffc658",
  "#ff7f7f",
  "#00C49F",
  "#0088FE",
  "#FFBB28",
  "#FF8042"
];

export default function RiskDashboard() {
  const [summary, setSummary] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedRule, setSelectedRule] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/risk/summary")
      .then((res) => res.json())
      .then((data) => {
        console.log("SUMMARY RESPONSE:", data);
        setSummary(data);
      })
      .catch((err) => console.error(err));
  }, []);

  if (!summary) return <div>Loading...</div>;

  // -----------------------------
  // SAFE BREAKDOWN HANDLING
  // -----------------------------
  const breakdown = Array.isArray(summary.breakdown)
    ? summary.breakdown
    : [];

  // -----------------------------
  // CATEGORY AGGREGATION
  // -----------------------------
  const categoryMap = {};

  breakdown.forEach((item) => {
    const cat = item.category || "UNKNOWN";
    categoryMap[cat] = (categoryMap[cat] || 0) + (item.weighted_score || 0);
  });

  const chartData = Object.keys(categoryMap).map((key) => ({
    name: key,
    value: categoryMap[key]
  }));

  // -----------------------------
  // RULE AGGREGATION (DRILLDOWN LEVEL 1)
  // -----------------------------
  const buildRuleData = (items, category) => {
    const ruleMap = {};

    items
      .filter((i) => !category || i.category === category)
      .forEach((item) => {
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

  const filteredRules = selectedCategory
    ? buildRuleData(breakdown, selectedCategory)
    : [];

  const selectedRuleData =
    selectedRule &&
    filteredRules.find((r) => r.rule === selectedRule.rule);

  // -----------------------------
  // COLOR MAPPING
  // -----------------------------
  const colorMap = {};
  chartData.forEach((entry, index) => {
    colorMap[entry.name] = COLORS[index % COLORS.length];
  });

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Risk Dashboard</h2>

      <h3>
        Risk Score:{" "}
        {summary?.risk_score !== undefined ? summary.risk_score : "N/A"}
      </h3>
      <h4>
        Risk Level:{" "}
        {summary?.risk_level ? summary.risk_level : "N/A"}
      </h4>

      {/* -----------------------------
          LEVEL 0 - CATEGORY VIEW
      ----------------------------- */}
      {!selectedCategory && (
        <>
          <BarChart width={650} height={300} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />

            <Bar
              dataKey="value"
              onClick={(data) => {
                setSelectedCategory(data.name);
                setSelectedRule(null);
              }}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`bar-${index}`}
                  fill={colorMap[entry.name]}
                />
              ))}
            </Bar>
          </BarChart>

          <PieChart width={450} height={350}>
            <Pie
              data={chartData}
              dataKey="value"
              nameKey="name"
              outerRadius={130}
              label={({ name, percent }) =>
                `${name} ${(percent * 100).toFixed(0)}%`
              }
              onClick={(data) => {
                setSelectedCategory(data.name);
                setSelectedRule(null);
              }}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`pie-${index}`}
                  fill={colorMap[entry.name]}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </>
      )}

      {/* -----------------------------
          LEVEL 1 - RULE VIEW
      ----------------------------- */}
      {selectedCategory && !selectedRule && (
        <div style={{ marginTop: "20px" }}>
          <button onClick={() => setSelectedCategory(null)}>
            ← Back to Categories
          </button>

          <h3>Rules in {selectedCategory}</h3>

          <table
            border="1"
            cellPadding="8"
            style={{ borderCollapse: "collapse", marginTop: "10px" }}
          >
            <thead>
              <tr>
                <th>Rule</th>
                <th>Severity</th>
                <th>Occurrences</th>
                <th>Total Score</th>
              </tr>
            </thead>
            <tbody>
              {filteredRules.map((rule, idx) => (
                <tr
                  key={idx}
                  onClick={() => setSelectedRule(rule)}
                  style={{ cursor: "pointer" }}
                >
                  <td>{rule.rule}</td>
                  <td>{rule.severity}</td>
                  <td>{rule.occurrences}</td>
                  <td>{rule.total_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* -----------------------------
          LEVEL 2 - RULE DETAILS
      ----------------------------- */}
      {selectedRule && selectedRuleData && (
        <div style={{ marginTop: "20px" }}>
          <button onClick={() => setSelectedRule(null)}>
            ← Back to Rules
          </button>

          <h3>Rule Details</h3>

          <p><b>Rule:</b> {selectedRuleData.rule}</p>
          <p><b>Category:</b> {selectedRuleData.category}</p>
          <p><b>Severity:</b> {selectedRuleData.severity}</p>
          <p><b>Occurrences:</b> {selectedRuleData.occurrences}</p>
          <p><b>Total Score:</b> {selectedRuleData.total_score}</p>

          <h4>Event IDs</h4>
          <ul>
            {selectedRuleData.events.slice(0, 25).map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}