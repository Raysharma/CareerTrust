import { Link } from 'react-router-dom';
import { Shield } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 fixed w-full top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Shield className="w-8 h-8 text-blue-600" />
            <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              CareerTrust
            </span>
          </Link>
          <div className="flex items-center space-x-6">
            <Link to="/" className="text-gray-700 hover:text-blue-600 transition">
              Home
            </Link>
            <Link to="/verify" className="text-gray-700 hover:text-blue-600 transition">
              Verify
            </Link>
            <Link
              to="/verify"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg hover:shadow-lg transition"
            >
              Start Verification
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
