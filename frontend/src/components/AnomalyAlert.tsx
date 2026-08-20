import React from "react";
import { AnomalyReport } from "@/types";
import { AlertTriangle, TrendingDown, TrendingUp, ShieldAlert } from "lucide-react";

interface AnomalyAlertProps {
  report: AnomalyReport;
}

export const AnomalyAlert: React.FC<AnomalyAlertProps> = ({ report }) => {
  if (!report.is_anomaly) {
    return null;
  }

  const priceDiff = report.current_price - report.expected_price;
  const isDrop = priceDiff < 0;
  const pctChange = Math.abs((priceDiff / report.expected_price) * 100).toFixed(1);
  const severityPercentage = Math.round(report.severity_score * 100);

  return (
    <div className="bg-[#1c0f12] border border-[#5c1d24] rounded-xl p-5 shadow-lg">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4 pb-3 border-b border-[#3d161a]">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400 shrink-0">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold text-rose-400 font-mono tracking-wider block mb-0.5">
              02 — AI RISK MANAGER ANOMALY FLAG
            </span>
            <h4 className="text-lg font-bold text-[#f5f0eb] tracking-tight">
              Significant Price Deviation ({isDrop ? "-" : "+"}{pctChange}%)
            </h4>
          </div>
        </div>

        <div className="bg-[#0e0b08] border border-[#5c1d24] rounded-lg px-3.5 py-1.5 flex items-center gap-2 text-xs font-semibold shrink-0">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          <span className="text-[#a8a29e]">Severity Score:</span>
          <span className="text-rose-400 font-mono font-bold text-sm">
            {report.severity_score.toFixed(2)} ({severityPercentage}%)
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 my-3 p-3.5 bg-[#0e0b08] rounded-lg border border-[#3d161a] text-xs">
        <div>
          <span className="text-[#a8a29e] block mb-0.5 font-medium">Scraped Live Price</span>
          <span className="text-base font-extrabold text-rose-300 font-mono">
            ${report.current_price.toFixed(2)}
          </span>
        </div>
        <div>
          <span className="text-[#a8a29e] block mb-0.5 font-medium">Expected Baseline Price</span>
          <span className="text-base font-extrabold text-emerald-400 font-mono">
            ${report.expected_price.toFixed(2)}
          </span>
        </div>
        <div>
          <span className="text-[#a8a29e] block mb-0.5 font-medium">Variance Delta</span>
          <span className="text-base font-extrabold text-amber-300 font-mono flex items-center gap-1">
            {isDrop ? <TrendingDown className="w-4 h-4 text-rose-400" /> : <TrendingUp className="w-4 h-4 text-amber-400" />}
            {priceDiff < 0 ? "-" : "+"}${Math.abs(priceDiff).toFixed(2)}
          </span>
        </div>
      </div>

      <div className="mt-3">
        <div className="flex justify-between text-xs text-rose-300/90 mb-1 font-semibold">
          <span>Anomaly Risk Threshold</span>
          <span className="font-mono">{severityPercentage}% Confidence</span>
        </div>
        <div className="w-full bg-[#0e0b08] rounded-full h-2 overflow-hidden border border-[#3d161a]">
          <div
            className="bg-rose-500 h-full rounded-full transition-all duration-500"
            style={{ width: `${severityPercentage}%` }}
          />
        </div>
      </div>
    </div>
  );
};
