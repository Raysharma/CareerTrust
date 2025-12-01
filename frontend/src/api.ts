// frontend/src/api.ts
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export interface VerifyLinkResponse {
  id?: string;
  url: string;
  domain: string;
  company?: string;
  risk_score: number;
  verdict: string;
  risk_flags: string[];
  trust_flags: string[];
  details?: any;
  domain_info?: any;
  osint_basic?: any;
  osint_company?: any;
  timestamp: string;
}

export interface HistoryItem {
  id: string;
  url: string;
  risk_score: number;
  verdict: string;
  timestamp: string;
}

export const verifyLink = async (url: string): Promise<VerifyLinkResponse> => {
  const res = await api.post("/verify/link", { url });
  return res.data;
};

export const getHistory = async (): Promise<HistoryItem[]> => {
  const res = await api.get("/verify/history");
  return res.data;
};

export default api;
