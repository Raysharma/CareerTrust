// frontend/src/components/RiskCard.tsx
import { CheckCircle, AlertTriangle, XCircle } from "lucide-react";

interface RiskCardProps {
  score: number;
  verdict: string;
}

export default function RiskCard({ score, verdict }: RiskCardProps) {
  const getColor = () => {
    if (score <= 30) return { bg: "bg-green-100", text: "text-green-600", border: "border-green-300", stroke: "stroke-green-600" };
    if (score <= 60) return { bg: "bg-yellow-100", text: "text-yellow-600", border: "border-yellow-300", stroke: "stroke-yellow-600" };
    return { bg: "bg-red-100", text: "text-red-600", border: "border-red-300", stroke: "stroke-red-600" };
  };

  const getIcon = () => {
    if (score <= 30) return <CheckCircle className="w-16 h-16 text-green-600" />;
    if (score <= 60) return <AlertTriangle className="w-16 h-16 text-yellow-600" />;
    return <XCircle className="w-16 h-16 text-red-600" />;
  };

  const colors = getColor();
  const circumference = 2 * Math.PI * 70;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className={`${colors.bg} border-2 ${colors.border} rounded-2xl p-8`}>
      <div className="flex items-center justify-between">
        <div className="space-y-4">
          <div className="flex items-center space-x-3">
            {getIcon()}
            <div>
              <h3 className="text-2xl font-bold text-gray-800">{verdict}</h3>
              <p className={`${colors.text} font-semibold`}>Risk Score: {score}/100</p>
            </div>
          </div>
        </div>

        <div className="relative w-40 h-40">
          <svg className="transform -rotate-90 w-40 h-40">
            <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="10" fill="transparent" className="text-gray-300" />
            <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="10" fill="transparent"
                    strokeDasharray={circumference} strokeDashoffset={offset}
                    className={`${colors.stroke} transition-all duration-1000 ease-out`} strokeLinecap="round" />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={`text-3xl font-bold ${colors.text}`}>{score}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
