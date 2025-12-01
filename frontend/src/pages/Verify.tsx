import { useState, useEffect } from "react";
import { Search, Loader2, AlertCircle, Calendar, Globe, ShieldAlert } from "lucide-react";
import { verifyLink, getHistory } from "../api";
import RiskCard from "../components/RiskCard";
import HistoryList from "../components/HistoryList";

export default function Verify() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      console.error("Failed to load history:", err);
    }
  };

  const handleVerify = async () => {
    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await verifyLink(url);
      setResult(data);
      loadHistory();
    } catch (err) {
      setError("Failed to verify link. Please check the URL and try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleHistorySelect = (item: any) => {
    setUrl(item.url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 pt-24 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Verify Job Link
            </span>
          </h1>
          <p className="text-gray-600 text-lg">Check if a job or internship posting is legitimate.</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">

          {/* LEFT SIDE */}
          <div className="lg:col-span-2 space-y-6">

            {/* Input Section */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <div className="space-y-4">
                <label className="block text-sm font-semibold text-gray-700">Job/Internship URL</label>

                <div className="flex space-x-3">
                  <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://example.com/job"
                    className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-600 transition"
                    onKeyPress={(e) => e.key === "Enter" && handleVerify()}
                  />

                  <button
                    onClick={handleVerify}
                    disabled={loading}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:shadow-lg transition disabled:opacity-50 flex items-center space-x-2"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Verifying...</span>
                      </>
                    ) : (
                      <>
                        <Search className="w-5 h-5" />
                        <span>Verify</span>
                      </>
                    )}
                  </button>
                </div>

                {error && (
                  <div className="flex items-center space-x-2 text-red-600 bg-red-50 px-4 py-3 rounded-lg border border-red-200">
                    <AlertCircle className="w-5 h-5" />
                    <span>{error}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Loading */}
            {loading && (
              <div className="bg-white rounded-2xl shadow-xl p-12">
                <div className="flex flex-col items-center justify-center space-y-4">
                  <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
                  <p className="text-gray-600 text-lg">Analyzing the link...</p>
                </div>
              </div>
            )}

            {/* RESULT */}
            {result && !loading && (
              <div className="space-y-6 animate-fadeIn">

                {/* Scorecard */}
                <RiskCard score={result.risk_score} verdict={result.verdict} />

                {/* RISK FLAGS */}
                <div className="bg-white p-6 rounded-2xl shadow-xl">
                  <h3 className="text-xl font-bold mb-4 flex items-center">
                    <ShieldAlert className="w-6 h-6 text-red-600 mr-2" />
                    Risk & Trust Indicators
                  </h3>

                  <h4 className="font-semibold text-red-700">Risk Flags</h4>
                  <ul className="mb-4 space-y-2">
                    {result.risk_flags?.length > 0
                      ? result.risk_flags.map((f: string, i: number) => (
                          <li key={i} className="bg-red-50 border px-4 py-2 rounded-lg text-red-700">
                            {f}
                          </li>
                        ))
                      : <li className="text-gray-500">No risk indicators found.</li>}
                  </ul>

                  <h4 className="font-semibold text-green-700">Trust Flags</h4>
                  <ul className="space-y-2">
                    {result.trust_flags?.length > 0
                      ? result.trust_flags.map((f: string, i: number) => (
                          <li key={i} className="bg-green-50 border px-4 py-2 rounded-lg text-green-700">
                            {f}
                          </li>
                        ))
                      : <li className="text-gray-500">No trust indicators found.</li>}
                  </ul>
                </div>

                {/* DOMAIN INFO */}
                <div className="bg-white p-6 rounded-2xl shadow-xl">
                  <h3 className="text-xl font-bold mb-4 flex items-center">
                    <Globe className="w-6 h-6 text-blue-600 mr-2" /> Domain Information
                  </h3>

                  <p><strong>Domain:</strong> {result.domain}</p>
                  <p><strong>Age:</strong> {result.domain_info.domain_age_days ?? "Unknown"} days</p>
                  <p><strong>SSL Valid:</strong> {result.domain_info.ssl_valid ? "Yes" : "No"}</p>
                  <p><strong>Redirects:</strong> {result.domain_info.redirect_count ?? 0}</p>

                  <p><strong>Emails:</strong> {result.domain_info.contacts?.emails?.join(", ") || "None"}</p>
                  <p><strong>Phones:</strong> {result.domain_info.contacts?.phones?.join(", ") || "None"}</p>
                </div>

                {/* COMPANY OSINT */}
                <div className="bg-white p-6 rounded-2xl shadow-xl">
                  <h3 className="text-xl font-bold mb-4">Company OSINT</h3>

                  <p><strong>LinkedIn:</strong> {result.osint_basic.linkedin_found ? "Yes" : "No"}</p>
                  <p><strong>Glassdoor:</strong> {result.osint_basic.glassdoor_found ? "Yes" : "No"}</p>
                  <p><strong>Scam Reports:</strong> {result.osint_basic.scam_reports_found ? "Yes" : "No"}</p>

                  <p><strong>MCA Registered:</strong> {result.osint_company.mca_found ? "Yes" : "No"}</p>
                  <p><strong>GST Found:</strong> {result.osint_company.gst_found ? "Yes" : "No"}</p>
                  <p><strong>Office Location Verified:</strong> {result.osint_company.location_found ? "Yes" : "No"}</p>
                </div>

                {/* TIMESTAMP */}
                <div className="bg-white p-6 rounded-2xl shadow-xl">
                  <div className="flex items-center space-x-2 text-gray-600">
                    <Calendar className="w-5 h-5" />
                    <span>Verified on {new Date(result.timestamp).toLocaleString()}</span>
                  </div>
                </div>

              </div>
            )}
          </div>

          {/* HISTORY */}
          <div className="lg:col-span-1">
            <HistoryList history={history} onSelect={handleHistorySelect} />
          </div>

        </div>
      </div>
    </div>
  );
}
