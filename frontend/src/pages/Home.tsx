import { Link } from 'react-router-dom';
import { Shield, Search, CheckCircle, AlertTriangle } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <h1 className="text-5xl font-bold leading-tight">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                CareerTrust
              </span>
              <br />
              <span className="text-gray-800">
                Verify Job & Internship Links in Seconds
              </span>
            </h1>

            <p className="text-xl text-gray-600 leading-relaxed">
              Paste any job or internship link. Our AI + OSINT scans the internet
              and tells you if it's safe.
            </p>

            <Link
              to="/verify"
              className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:shadow-xl transform hover:-translate-y-1 transition-all"
            >
              <span>Start Verification</span>
              <span>→</span>
            </Link>

            <div className="grid grid-cols-3 gap-4 pt-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">1000+</div>
                <div className="text-sm text-gray-600">Links Verified</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">95%</div>
                <div className="text-sm text-gray-600">Accuracy Rate</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-pink-600">24/7</div>
                <div className="text-sm text-gray-600">Protection</div>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="bg-white rounded-3xl shadow-2xl p-8 transform hover:scale-105 transition-transform">
              <div className="flex justify-center mb-6">
                <Shield className="w-32 h-32 text-blue-600" />
              </div>

              <div className="space-y-4">
                <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg border border-green-200">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                  <span className="text-gray-700">AI-Powered Detection</span>
                </div>

                <div className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <Search className="w-6 h-6 text-blue-600" />
                  <span className="text-gray-700">OSINT Intelligence</span>
                </div>

                <div className="flex items-center space-x-3 p-4 bg-purple-50 rounded-lg border border-purple-200">
                  <AlertTriangle className="w-6 h-6 text-purple-600" />
                  <span className="text-gray-700">Real-time Analysis</span>
                </div>
              </div>
            </div>

            <div className="absolute -z-10 top-10 right-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
            <div className="absolute -z-10 bottom-10 left-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
          </div>
        </div>

        <div className="mt-24">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            How It Works
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Paste Link</h3>
              <p className="text-gray-600">
                Copy and paste any job or internship URL you want to verify
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl font-bold text-purple-600">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">AI Analysis</h3>
              <p className="text-gray-600">
                Our system scans multiple databases and runs AI detection
              </p>
            </div>

            <div className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition">
              <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl font-bold text-pink-600">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Get Results</h3>
              <p className="text-gray-600">
                Receive instant verdict with detailed risk analysis and flags
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
