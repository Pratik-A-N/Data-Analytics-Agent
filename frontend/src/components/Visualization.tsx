// Visualization.tsx
import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import { Bar, Line, Pie } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
  Title
);

interface VisualizationData {
  labels: string[];
  values: Array<{
    data: number[];
    label: string;
  }>;
}

interface VisualizationProps {
  type: string;
  data: VisualizationData;
}

const COLORS = [
  "#8884d8", "#82ca9d", "#ffc658", "#ff7300", "#a4de6c",
  "#d0ed57", "#83a6ed", "#8dd1e1", "#82ca9d", "#c49c94"
];

function buildChartDatasets(values: VisualizationData["values"]) {
  return values.map((series, idx) => {
    const backgroundColor = COLORS[idx % COLORS.length];
    const borderColor = backgroundColor;
    return {
      label: series.label,
      data: series.data,
      backgroundColor: backgroundColor,
      borderColor: borderColor,
      borderWidth: 1,
      fill: false,
      // Chart.js uses different props for bar/line; common set is fine
    };
  });
}

function Visualization({ type, data }: VisualizationProps) {
  // Defensive checks
  if (!data || !Array.isArray(data.labels) || data.labels.length === 0) {
    return <div className="text-gray-400 p-4">No data to visualize</div>;
  }
  if (!Array.isArray(data.values) || data.values.length === 0) {
    return <div className="text-gray-400 p-4">No series to visualize</div>;
  }
  // ensure lengths are consistent (pad with zeros if necessary)
  const maxLen = Math.max(...data.values.map((s) => s.data.length), data.labels.length);
  const labels = data.labels.slice(0, maxLen);
  while (labels.length < maxLen) labels.push("");

  const normalizedValues = data.values.map((s) => {
    const arr = s.data.slice();
    while (arr.length < maxLen) arr.push(0);
    return { ...s, data: arr };
  });

  const datasets = buildChartDatasets(normalizedValues);

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false as const,
    plugins: {
      legend: { position: "top" as const },
      title: { display: false },
      tooltip: {
        // style with inline CSS classes or let Chart.js default
      },
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
          color: "#9ca3af",
        },
      },
      y: {
        ticks: {
          color: "#9ca3af",
        },
      },
    },
  };

  const barData = { labels, datasets };
  const lineData = { labels, datasets };
  // Pie uses a single dataset (use first series)
  const pieData = {
    labels,
    datasets: [
      {
        label: normalizedValues[0].label,
        data: normalizedValues[0].data,
        backgroundColor: labels.map((_, i) => COLORS[i % COLORS.length]),
      },
    ],
  };

  // render container with fixed height (so ChartJS can compute)
  return (
    <div className="w-full mt-4 bg-gray-800/30 rounded-lg p-4 border border-gray-700" style={{ height: 420 }}>
      {type === "bar" && <Bar data={barData} options={commonOptions} />}
      {type === "line" && <Line data={lineData} options={commonOptions} />}
      {type === "pie" && <Pie data={pieData} options={{ ...commonOptions, maintainAspectRatio: true }} />}
      {!["bar", "line", "pie"].includes(type) && (
        <div className="text-gray-300 p-4">Unsupported visualization type: {type}</div>
      )}
    </div>
  );
}

export default Visualization;
