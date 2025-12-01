// frontend/src/components/HistoryList.tsx
import { Clock, ExternalLink } from "lucide-react";
import { HistoryItem } from "../api";

interface Props {
  history: HistoryItem[];
  onSelect: (h: HistoryItem) => void;
}

export default function HistoryList({ history, onSelect }: Props) {
  const getScoreColor = (score: number) => {
    if (score <= 30) return "text-green-600 bg-green-100";
    if (score <= 60) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  if (!history || history.length === 0) {
    return (
      <div className="bg-white rounded-xl p-8 text-center text-gray-500">
        <Clock className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No verification history yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4">
        <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
          <Clock className="w-5 h-5" />
          <span>Verification History</span>
        </h3>
      </div>

      <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
        {history.map((item) => (
          <div key={item.id} className="p-4 hover:bg-gray-50 transition cursor-pointer" onClick={() => onSelect(item)}>
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0 mr-4">
                <div className="flex items-center space-x-2 mb-2">
                  <ExternalLink className="w-4 h-4 text-gray-400 flex-shrink-0" />
                  <p className="text-sm text-gray-600 truncate">{item.url}</p>
                </div>
                <div className="flex items-center space-x-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getScoreColor(item.risk_score)}`}>
                    Score: {item.risk_score}
                  </span>
                  <span className="text-xs text-gray-500">{new Date(item.timestamp).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="text-right flex-shrink-0">
                <span className="text-sm font-semibold text-gray-700">{item.verdict}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
