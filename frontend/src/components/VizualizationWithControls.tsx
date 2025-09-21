import React, { useMemo, useState } from "react";
import { saveAs } from "file-saver";
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
  type LinearScaleOptions,
  type ScatterDataPoint,
  type ChartOptions
} from "chart.js";
import { Bar, Line, Pie, Scatter } from "react-chartjs-2";

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

type Series = {
  label: string;
  data: number[];
};

type VisualizationData = {
  labels: string[];
  values: Series[];
};

type Props = {
  initialType?: "bar" | "horizontal_bar" | "line" | "pie" | "scatter";
  data: VisualizationData;
};

const COLORS = [
  "#8884d8", "#82ca9d", "#ffc658", "#ff7300", "#a4de6c",
  "#d0ed57", "#83a6ed", "#8dd1e1", "#82ca9d", "#c49c94"
];

function buildDatasets(values: Series[], active: Record<string, boolean>, forPie = false) {
  const maxLen = Math.max(...values.map(s => s.data.length), 0);
  const datasets = values
    .filter(s => active[s.label])
    .map((s, idx) => {
      const data = s.data.slice(0, maxLen).concat(Array(Math.max(0, maxLen - s.data.length)).fill(0));
      if (forPie) {
        return {
          label: s.label,
          data,
          backgroundColor: COLORS[idx % COLORS.length],
        };
      }
      return {
        label: s.label,
        data,
        backgroundColor: COLORS[idx % COLORS.length],
        borderColor: COLORS[idx % COLORS.length],
        borderWidth: 1,
        fill: false,
      };
    });
  return datasets;
}

export default function VisualizationWithControls({ initialType = "bar", data }: Props) {
  const [chartType, setChartType] = useState<typeof initialType>(initialType);
  // series visibility
  const initialActive = useMemo(() => {
    const map: Record<string, boolean> = {};
    data.values.forEach(v => (map[v.label] = true));
    return map;
  }, [data.values]);

  const [activeSeries, setActiveSeries] = useState<Record<string, boolean>>(initialActive);
  const [stacked, setStacked] = useState(false);

  // CSV download helper
  function downloadCsv() {
    const header = ["label", ...data.values.map(s => s.label)];
    const rows: string[][] = data.labels.map((lab, i) => {
      return [lab, ...data.values.map(s => String(s.data[i] ?? ""))];
    });
    const csv = [header.join(","), ...rows.map(r => r.join(","))].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    saveAs(blob, "visualization_data.csv");
  }

  // computed chart data
  const labels = data.labels;
  const activeDatasets = useMemo(() => buildDatasets(data.values, activeSeries, chartType === "pie"), [data.values, activeSeries, chartType]);

  // common options (tweakable)
  const commonOptions: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "top" },
      title: { display: false },
      tooltip: {},
    },
    scales: {
      x: { ticks: { color: "#9ca3af" } as any },
      y: { ticks: { color: "#9ca3af" } as any },
    },
  };

  // stacked/grouped modifications for bar charts
  const barOptions: ChartOptions = {
    ...commonOptions,
    scales: {
      ...commonOptions.scales,
      x: { stacked },
      y: { stacked },
    },
  };

  // scatter needs different dataset format
  const scatterData = useMemo(() => {
    // Use first active series for x, second active series for y OR convert labels to x
    const active = data.values.filter(s => activeSeries[s.label]);
    if (active.length === 0) return { datasets: [] };
    if (active.length === 1) {
      // plot index vs value
      const pts: ScatterDataPoint[] = active[0].data.map((v, i) => ({ x: i, y: v }));
      return { datasets: [{ label: active[0].label, data: pts, backgroundColor: COLORS[0] }] };
    } else {
      // pair first two active series
      const pts: ScatterDataPoint[] = active[0].data.map((v, i) => ({ x: v ?? 0, y: (active[1].data[i] ?? 0) }));
      return { datasets: [{ label: `${active[0].label} vs ${active[1].label}`, data: pts, backgroundColor: COLORS[0] }] };
    }
  }, [data.values, activeSeries]);

  // Chart renderers
  const renderChart = () => {
    switch (chartType) {
      case "bar":
        return <div style={{ height: 420 }}><Bar data={{ labels, datasets: activeDatasets }} options={barOptions} /></div>;
      case "horizontal_bar":
        // Chart.js v3 uses indexAxis = 'y' for horizontal bars
        return <div style={{ height: 420 }}>
          <Bar
            data={{ labels, datasets: activeDatasets }}
            options={{ ...barOptions, indexAxis: "y" as const }}
          />
        </div>;
      case "line":
        return <div style={{ height: 420 }}><Line data={{ labels, datasets: activeDatasets }} options={commonOptions} /></div>;
      case "pie":
        // pie uses single dataset - we sum/flatten across active series or use first
        const pieDataset = activeDatasets.length > 0 ? {
          labels,
          datasets: [{
            label: activeDatasets[0].label,
            data: activeDatasets[0].data,
            backgroundColor: labels.map((_, i) => COLORS[i % COLORS.length]),
          }]
        } : { labels: [], datasets: [] };
        return <div style={{ height: 420 }}><Pie data={pieDataset} options={{ ...commonOptions, maintainAspectRatio: true }} /></div>;
      case "scatter":
        return <div style={{ height: 420 }}><Scatter data={scatterData as any} options={commonOptions} /></div>;
      default:
        return <div>Unsupported chart type</div>;
    }
  };

  // UI controls
  return (
    <div className="p-4 bg-gray-800/30 rounded-lg border border-gray-700">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-300">Chart type</label>
          <select
            className="bg-gray-700 text-white p-1 rounded"
            value={chartType}
            onChange={(e) => setChartType(e.target.value as any)}
          >
            <option value="bar">Bar</option>
            <option value="horizontal_bar">Horizontal Bar</option>
            <option value="line">Line</option>
            <option value="pie">Pie</option>
            <option value="scatter">Scatter</option>
          </select>

          {chartType === "bar" && (
            <label className="ml-4 text-sm text-gray-300">
              <input type="checkbox" checked={stacked} onChange={() => setStacked(s => !s)} />
              <span className="ml-2">Stacked</span>
            </label>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={downloadCsv}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
          >
            Download CSV
          </button>
        </div>
      </div>

      <div className="mt-3 flex flex-col md:flex-row gap-4">
        <div className="flex-1">
          {renderChart()}
        </div>

        <div className="w-full md:w-64 p-2 bg-gray-900/40 rounded">
          <div className="text-sm text-gray-300 mb-2">Series</div>
          <div className="flex flex-col gap-2 max-h-56 overflow-auto">
            {data.values.map((s, idx) => (
              <label key={s.label} className="flex items-center gap-2 text-gray-200">
                <input
                  type="checkbox"
                  checked={!!activeSeries[s.label]}
                  onChange={() => setActiveSeries(prev => ({ ...prev, [s.label]: !prev[s.label] }))}
                />
                <span style={{ width: 12, height: 12, backgroundColor: COLORS[idx % COLORS.length], display: "inline-block", borderRadius: 2 }} />
                <span className="ml-2 text-sm">{s.label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
