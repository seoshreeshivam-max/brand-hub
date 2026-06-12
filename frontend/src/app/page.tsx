"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [brands, setBrands] = useState<any[]>([]);
  const [auditResults, setAuditResults] = useState<any>(null);
  const [investigationResults, setInvestigationResults] = useState<any>({});
  const [fixSuggestions, setFixSuggestions] = useState<any>({});
  const [activityLogs, setActivityLogs] = useState<any[]>([
    { id: 1, time: "Just now", msg: "brandHub v.0.0 Online", type: "system" }
  ]);
  const [loading, setLoading] = useState(false);
  const [investigating, setInvestigating] = useState<string | null>(null);
  const [fixing, setFixing] = useState<string | null>(null);
  const [selectedBrand, setSelectedBrand] = useState("all");

  const addLog = (msg: string, type: string = "info") => {
    setActivityLogs((prev: any[]) => [{ id: Date.now(), time: new Date().toLocaleTimeString(), msg, type }, ...prev].slice(0, 10));
  };

  useEffect(() => {
    fetch("/brands")
      .then((res) => res.json())
      .then((data) => setBrands(data))
      .catch((err) => console.error("Error fetching brands:", err));
  }, []);

  const runAudit = async () => {
    setLoading(true);
    addLog("Starting global multi-brand audit...", "agent");
    try {
      const res = await fetch("/agents/monitor/audit");
      const data = await res.json();
      setAuditResults(data);
      addLog("Global audit complete. Status: Active", "success");
    } catch (err) {
      addLog("Audit failed. Check backend connection.", "error");
    } finally {
      setLoading(false);
    }
  };

  const runInvestigation = async (brandId: string) => {
    setInvestigating(brandId);
    addLog(`Auditor Agent starting investigation for ${brandId}...`, "agent");
    try {
      const res = await fetch(`/agents/auditor/investigate/${brandId}`);
      const data = await res.json();
      setInvestigationResults((prev: any) => ({ ...prev, [brandId]: data }));
      addLog(`Investigation for ${brandId} complete. Hypothesis formulated.`, "success");
    } catch (err) {
      addLog(`Investigation for ${brandId} failed.`, "error");
    } finally {
      setInvestigating(null);
    }
  };

  const runFix = async (brandId: string) => {
    setFixing(brandId);
    addLog(`Content Agent drafting AI fix for ${brandId} (Fable 5)...`, "agent");
    try {
      const res = await fetch(`/agents/content/draft-fix/${brandId}/12345`);
      const data = await res.json();
      setFixSuggestions((prev: any) => ({ ...prev, [brandId]: data }));
      addLog(`AI content draft ready for ${brandId}.`, "success");
    } catch (err) {
      addLog(`AI fix drafting failed for ${brandId}.`, "error");
    } finally {
      setFixing(null);
    }
  };

  return (
    <main className="min-h-screen bg-[#F8FAFC] flex font-sans">
      {/* Sidebar Log */}
      <aside className="w-80 bg-white border-r border-slate-200 hidden lg:flex flex-col shadow-[4px_0_24px_rgba(0,0,0,0.02)]">
        <div className="p-8 border-b border-slate-100">
          <h2 className="font-black text-slate-900 flex items-center gap-3 text-xs uppercase tracking-widest">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            Live Operations
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {activityLogs.map(log => (
            <div key={log.id} className="group">
              <span className="text-[10px] text-slate-400 font-mono block mb-1 opacity-0 group-hover:opacity-100 transition-opacity">{log.time}</span>
              <p className={`text-xs font-semibold leading-relaxed ${
                log.type === "error" ? "text-red-500" : 
                log.type === "success" ? "text-emerald-600" : 
                log.type === "agent" ? "text-indigo-600" : "text-slate-600"
              }`}>
                {log.msg}
              </p>
            </div>
          ))}
        </div>
        <div className="p-6 bg-slate-50 border-t border-slate-100 text-[10px] text-slate-400 font-mono text-center tracking-tighter">
          HUB.SHREESHIVAM.COM // SYSTEM_V0.0_ACTIVE
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 p-12 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          <header className="flex justify-between items-end mb-16">
            <div>
              <span className="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded mb-2 inline-block tracking-widest">ENTERPRISE</span>
              <h1 className="text-5xl font-black text-slate-900 tracking-tighter mb-1">brand<span className="text-blue-600">Hub</span></h1>
              <p className="text-slate-400 font-bold text-sm tracking-tight">Autonomous Multi-Brand Orchestration</p>
            </div>
            <div className="flex gap-4">
              <select 
                className="bg-white border-2 border-slate-100 rounded-2xl px-6 py-3 text-sm font-bold text-slate-700 shadow-sm focus:border-blue-500 outline-none transition-all cursor-pointer"
                value={selectedBrand}
                onChange={(e) => setSelectedBrand(e.target.value)}
              >
                <option value="all">Full Portfolio</option>
                {brands.map((b) => (
                  <option key={b.id} value={b.id}>{b.name}</option>
                ))}
              </select>
              <button 
                onClick={runAudit}
                disabled={loading}
                className="bg-slate-900 hover:bg-black text-white px-10 py-3 rounded-2xl text-sm font-black transition-all shadow-[0_20px_40px_rgba(0,0,0,0.1)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.2)] disabled:opacity-50 active:scale-95"
              >
                {loading ? "SYNCING..." : "SYNC ALL"}
              </button>
            </div>
          </header>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-10">
            {brands.map((brand) => {
              const audit = auditResults?.[brand.id];
              const investigation = investigationResults?.[brand.id];
              const suggestion = fixSuggestions?.[brand.id];
              const isAnomaly = audit?.status === "anomaly_detected";
              
              return (
                <div key={brand.id} className="group">
                  <div className={`h-full bg-white p-10 rounded-[40px] border-2 ${isAnomaly ? 'border-red-100 shadow-[0_20px_50px_rgba(239,68,68,0.05)]' : 'border-slate-50 shadow-[0_20px_50px_rgba(0,0,0,0.02)]'} group-hover:shadow-[0_30px_60px_rgba(0,0,0,0.05)] transition-all duration-500 relative overflow-hidden`}>
                    
                    {/* Status Bar */}
                    <div className={`absolute top-0 left-0 right-0 h-1.5 ${
                      audit ? (isAnomaly ? 'bg-red-500' : 'bg-emerald-500') : 'bg-slate-100'
                    }`}></div>

                    <div className="flex justify-between items-start mb-10">
                      <div>
                        <h3 className="font-black text-3xl text-slate-900 tracking-tighter">{brand.name}</h3>
                        <p className="text-[10px] font-black text-slate-300 uppercase tracking-[0.2em] mt-1">{brand.domain}</p>
                      </div>
                      <div className={`w-3 h-3 rounded-full ${
                        audit ? (isAnomaly ? 'bg-red-500 shadow-[0_0_12px_rgba(239,68,68,0.5)]' : 'bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.5)]') : 'bg-slate-200'
                      }`}></div>
                    </div>

                    <div className="space-y-8">
                      <div className="grid grid-cols-2 gap-6">
                        <div>
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Visibility</p>
                          <p className="text-3xl font-black text-slate-900 tabular-nums">{audit?.seo?.latest_clicks ?? "—"}</p>
                          <p className="text-[10px] font-bold text-slate-300 mt-1 italic">Last 7d Clicks</p>
                        </div>
                        <div>
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Revenue</p>
                          <p className="text-3xl font-black text-blue-600 tabular-nums">
                            {audit?.retail ? `${Math.round(audit.retail.total_sales/1000)}k` : "—"}
                          </p>
                          <p className="text-[10px] font-bold text-blue-300 mt-1 italic">30d Gross (INR)</p>
                        </div>
                      </div>

                      {investigation && (
                        <div className="bg-slate-900 p-6 rounded-3xl space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                          <div className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-pulse"></span>
                            <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Diagnostic Alert</h4>
                          </div>
                          <p className="text-sm text-white font-bold leading-snug">{investigation.hypothesis}</p>
                          <button 
                            onClick={() => runFix(brand.id)}
                            disabled={fixing === brand.id}
                            className="w-full bg-white text-slate-900 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-200 transition-all active:scale-95 shadow-xl shadow-black/20"
                          >
                            {fixing === brand.id ? "THINKING..." : "DEPLOY AI FIX"}
                          </button>
                        </div>
                      )}

                      {suggestion && (
                        <div className="bg-indigo-600 p-6 rounded-3xl space-y-5 animate-in fade-in slide-in-from-bottom-4 duration-700 shadow-[0_20px_40px_rgba(79,70,229,0.3)]">
                          <div className="flex justify-between items-center">
                            <h4 className="text-[10px] font-black text-indigo-200 uppercase tracking-[0.2em]">Fable 5 Proposal</h4>
                            <span className="text-[8px] bg-white/20 text-white px-2 py-0.5 rounded font-black tracking-widest">COMPETITOR_AWARE</span>
                          </div>
                          <div className="bg-white/10 p-4 rounded-2xl border border-white/10">
                            <p className="text-[9px] text-indigo-100 font-black uppercase opacity-60 mb-2">Optimized SEO Title</p>
                            <p className="text-sm text-white font-bold leading-tight italic">"{suggestion.suggested_title}"</p>
                          </div>
                          <div className="flex gap-3">
                            <button className="flex-1 bg-white text-indigo-600 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:shadow-lg transition-all active:scale-95">Push to Store</button>
                            <button className="w-12 h-12 flex items-center justify-center bg-indigo-500 text-white rounded-2xl hover:bg-indigo-400 transition-colors">
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                            </button>
                          </div>
                        </div>
                      )}
                    </div>

                    {!investigation && (
                      <button 
                        onClick={() => runInvestigation(brand.id)}
                        disabled={investigating === brand.id}
                        className="w-full mt-10 py-4 bg-transparent border-2 border-slate-100 rounded-[28px] text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] hover:border-slate-900 hover:text-slate-900 hover:shadow-lg transition-all active:scale-95 disabled:opacity-50"
                      >
                        {investigating === brand.id ? "ANALYZING..." : "START INVESTIGATION"}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </main>
  );
}
