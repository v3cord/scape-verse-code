import React from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
} from "recharts";

interface PriceChartProps {
  currentPrice: number;
  expectedPrice: number;
  isAnomaly: boolean;
}

export const PriceChart: React.FC<PriceChartProps> = ({
  currentPrice,
  expectedPrice,
  isAnomaly,
}) => {
  const chartData = [
    { day: "Day 1", price: Number((expectedPrice * 0.98).toFixed(2)) },
    { day: "Day 2", price: Number((expectedPrice * 0.99).toFixed(2)) },
    { day: "Day 3", price: Number((expectedPrice * 1.01).toFixed(2)) },
    { day: "Day 4", price: Number((expectedPrice * 1.00).toFixed(2)) },
    { day: "Day 5", price: Number((expectedPrice * 1.01).toFixed(2)) },
    { day: "Day 6", price: Number((expectedPrice * 1.02).toFixed(2)) },
    { day: "Today", price: currentPrice },
  ];

  const mainColor = isAnomaly ? "#f43f5e" : "#f59e0b";
  const gradientId = isAnomaly ? "anomalyGradient" : "normalGradient";

  return (
    <div className="bg-[#16120e] border border-[#261f18] rounded-xl p-5 shadow-md flex flex-col justify-between">
      <div>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-[#261f18]">
          <div>
            <span className="text-xs font-bold text-[#f59e0b] font-mono tracking-wider block mb-0.5">
              03 — REVENUE & PRICE TRAJECTORY
            </span>
            <h3 className="text-base font-bold text-[#f5f0eb] tracking-tight">
              7-Day Market Baseline
            </h3>
          </div>

          <div className="flex items-center gap-3 text-xs font-semibold">
            <div className="flex items-center gap-1.5 text-[#a8a29e]">
              <span className="w-2.5 h-0.5 bg-slate-500 rounded" />
              <span>Historical</span>
            </div>
            <div className="flex items-center gap-1.5 text-[#a8a29e]">
              <span className="w-2.5 h-0.5 bg-[#f59e0b] border border-[#f59e0b]" />
              <span>Expected (${expectedPrice.toFixed(2)})</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span
                className={`w-2 h-2 rounded-full ${
                  isAnomaly ? "bg-rose-500" : "bg-[#f59e0b]"
                }`}
              />
              <span className={isAnomaly ? "text-rose-400 font-bold" : "text-[#f59e0b] font-bold"}>
                Current
              </span>
            </div>
          </div>
        </div>

        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="anomalyGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="normalGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#261f18" opacity={0.8} />
              <XAxis
                dataKey="day"
                stroke="#a8a29e"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: "#261f18" }}
              />
              <YAxis
                stroke="#a8a29e"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: "#261f18" }}
                domain={["auto", "auto"]}
                tickFormatter={(value) => `$${value}`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0e0b08",
                  borderColor: "#261f18",
                  borderRadius: "0.5rem",
                  color: "#f5f0eb",
                  fontSize: "0.8125rem",
                  boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)",
                }}
                formatter={(value: any) => [`$${Number(value).toFixed(2)}`, "Price"]}
              />
              <ReferenceLine
                y={expectedPrice}
                stroke="#f59e0b"
                strokeDasharray="4 4"
                label={{
                  value: `Expected: $${expectedPrice.toFixed(2)}`,
                  fill: "#f59e0b",
                  fontSize: 10,
                  position: "insideTopLeft",
                }}
              />
              <Area
                type="monotone"
                dataKey="price"
                stroke={mainColor}
                strokeWidth={2.5}
                fillOpacity={1}
                fill={`url(#${gradientId})`}
                activeDot={{ r: 6, stroke: mainColor, strokeWidth: 2, fill: "#0e0b08" }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
