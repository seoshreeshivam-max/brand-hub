"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [selectedBrandId, setSelectedBrandId] = useState<string | null>(null);
  const [brands, setBrands] = useState<any[]>([]);
  const [auditResults, setAuditResults] = useState<any>(null);
  const [investigationResults, setInvestigationResults] = useState<any>({});
  const [fixSuggestions, setFixSuggestions] = useState<any>({});
  const [activityLogs, setActivityLogs] = useState<any[]>([
    { id: 1, time: "Just now", msg: "brandHub v1.0 Professional initialized", type: "system" }
  ]);
  const [loading, setLoading] = useState(false);
  const [investigating, setInvestigating] = useState<string | null>(null);
  const [fixing, setFixing] = useState<string | null>(null);

  const addLog = (msg: string, type: string = "info") => {
    setActivityLogs((prev: any[]) => [{ id: Date.now(), time: new Date().toLocaleTimeString(), msg, type }, ...prev].slice(0, 15));
  };

  useEffect(() => {
    fetch("/brands")
      .then((res) => res.json())
      .then((data) => {
        setBrands(data);
        if (data.length > 0 && !selectedBrandId) {
          setSelectedBrandId(data[0].id); // Auto-select first brand
        }
      })
      .catch((err) => console.error("Error fetching brands:", err));
  }, []);

  // Effect to auto-sync when brand changes
  useEffect(() => {
    if (selectedBrandId) {
      runAudit();
    }
  }, [selectedBrandId]);

  const runAudit = async () => {
    setLoading(true);
    addLog(`Syncing global performance for all brands...`, "agent");
    try {
      const res = await fetch("/agents/monitor/audit");
      const data = await res.json();
      setAuditResults(data);
      addLog("Global sync complete.", "success");
    } catch (err) {
      addLog("Sync failed. Check backend connection.", "error");
    } finally {
      setLoading(false);
    }
  };

  const currentBrand = brands.find(b => b.id === selectedBrandId);
  const currentAudit = auditResults?.[selectedBrandId || ""];
  const currentInvestigation = investigationResults?.[selectedBrandId || ""];
  const currentSuggestion = fixSuggestions?.[selectedBrandId || ""];

  const runInvestigation = async () => {
    if (!selectedBrandId) return;
    setInvestigating(selectedBrandId);
    addLog(`Running deep diagnostic for ${selectedBrandId}...`, "agent");
    try {
      const res = await fetch(`/agents/auditor/investigate/${selectedBrandId}`);
      const data = await res.json();
      setInvestigationResults((prev: any) => ({ ...prev, [selectedBrandId]: data }));
      addLog(`Diagnostic for ${selectedBrandId} complete.`, "success");
    } catch (err) {
      addLog(`Diagnostic failed.`, "error");
    } finally {
      setInvestigating(null);
    }
  };

  const runFix = async () => {
    if (!selectedBrandId) return;
    setFixing(selectedBrandId);
    addLog(`Content Agent drafting strategic fix (Fable 5)...`, "agent");
    try {
      const res = await fetch(`/agents/content/draft-fix/${selectedBrandId}/12345`);
      const data = await res.json();
      setFixSuggestions((prev: any) => ({ ...prev, [selectedBrandId]: data }));
      addLog(`Strategic draft ready for review.`, "success");
    } catch (err) {
      addLog(`AI drafting failed.`, "error");
    } finally {
      setFixing(null);
    }
  };

  return (
    <main className="min-h-screen bg-[#F8FAFC] flex font-sans text-slate-900">
      {/* PROFESSIONAL SIDEBAR */}
      <aside className="w-72 bg-slate-900 flex flex-col shadow-2xl">
        <div className="p-8">
          <h1 className="text-2xl font-black text-white tracking-tighter">brand<span className="text-blue-500">Hub</span></h1>
          <p className="text-slate-500 text-[10px] font-bold uppercase tracking-widest mt-1">SEO Orchestration</p>
        </div>

        <nav className="flex-1 px-4 space-y-2">
          {[
            { id: "dashboard", label: "Overview", icon: "📊" },
            { id: "diagnostics", label: "Diagnostics", icon: "🩺" },
            { id: "planner", label: "Content Planner", icon: "📅" },
            { id: "injectors", label: "Bulk Injectors", icon: "💉" },
            { id: "history", label: "Agent History", icon: "📜" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl text-sm font-bold transition-all ${
                activeTab === tab.id 
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-900/50" 
                  : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
              }`}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>

        <div className="p-6 bg-slate-800/50 mt-auto">
          <div className="flex items-center gap-3">
             <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
             <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">System Live</span>
          </div>
        </div>
      </aside>

      {/* MAIN WORKSPACE */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* TOP COMMAND HEADER */}
        <header className="h-20 bg-white border-b border-slate-200 px-12 flex justify-between items-center shrink-0">
          <div className="flex items-center gap-6">
            <div className="flex flex-col">
              <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Active Brand</span>
              <select 
                className="font-black text-lg text-slate-900 focus:outline-none cursor-pointer bg-transparent"
                value={selectedBrandId || ""}
                onChange={(e) => setSelectedBrandId(e.target.value)}
              >
                {brands.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
              </select>
            </div>
            <div className="h-8 w-px bg-slate-200"></div>
            <div className="flex flex-col">
              <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Context</span>
              <span className="font-bold text-sm text-blue-600 uppercase">{activeTab}</span>
            </div>
          </div>

          <div className="flex gap-4">
            <button 
              onClick={runAudit}
              disabled={loading}
              className="bg-slate-100 hover:bg-slate-200 text-slate-600 px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all"
            >
              {loading ? "Syncing..." : "Refresh Data"}
            </button>
            <button className="bg-blue-600 text-white px-8 py-2 rounded-xl text-xs font-black uppercase tracking-widest shadow-lg shadow-blue-100 hover:bg-blue-700 transition-all">
              Execute Agent
            </button>
          </div>
        </header>

        {/* SCROLLABLE VIEWPORT */}
        <div className="flex-1 overflow-y-auto p-12 bg-slate-50/50">
          <div className="max-w-6xl mx-auto">
            
            {activeTab === "dashboard" && (
              <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4">
                <div className="grid grid-cols-3 gap-8">
                  <StatCard title="Total Visibility" value={currentAudit?.seo?.latest_clicks ?? "—"} label="Last 7d Clicks" color="slate" />
                  <StatCard title="Gross Revenue" value={currentAudit?.retail ? `₹${Math.round(currentAudit.retail.total_sales/1000)}k` : "—"} label="30d Shopify" color="blue" />
                  <StatCard title="SEO Health" value={currentAudit?.status === "healthy" ? "100%" : "Critical"} label="System Scan" color={currentAudit?.status === "healthy" ? "emerald" : "red"} />
                </div>

                <div className="bg-white p-10 rounded-[40px] border border-slate-100 shadow-xl shadow-slate-200/50">
                   <h3 className="text-xl font-black mb-8 flex items-center gap-3">
                     <span className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center text-sm">📈</span>
                     Performance Analytics
                   </h3>
                   <div className="h-64 bg-slate-50 rounded-3xl flex items-center justify-center border-2 border-dashed border-slate-200">
                      <p className="text-slate-400 font-bold text-sm italic">GSC Sparkline Data Loading...</p>
                   </div>
                </div>
              </div>
            )}

            {activeTab === "diagnostics" && (
              <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
                <header className="flex justify-between items-center mb-8">
                   <div>
                      <h2 className="text-3xl font-black tracking-tight italic">SEO Diagnostics</h2>
                      <p className="text-slate-400 font-bold">Deep product and inventory audit for {currentBrand?.name}</p>
                   </div>
                   <button 
                     onClick={runInvestigation}
                     disabled={!!investigating}
                     className="bg-slate-900 text-white px-10 py-4 rounded-2xl font-black uppercase tracking-widest text-xs shadow-2xl shadow-slate-200"
                   >
                     {investigating ? "Scanning Store..." : "Run Full Diagnostic"}
                   </button>
                </header>

                {currentInvestigation ? (
                  <div className="grid grid-cols-2 gap-8">
                    <div className="bg-slate-900 p-10 rounded-[40px] shadow-2xl">
                      <h4 className="text-amber-500 font-black uppercase tracking-widest text-[10px] mb-4 flex items-center gap-2">
                        <span className="w-2 h-2 bg-amber-500 rounded-full animate-ping"></span>
                        Agent Hypothesis
                      </h4>
                      <p className="text-2xl font-bold text-white leading-tight mb-8">
                        {currentInvestigation.hypothesis}
                      </p>
                      <div className="flex gap-4">
                        <button className="flex-1 bg-white text-slate-900 py-3 rounded-2xl font-black uppercase text-[10px]">View 34 Products</button>
                        <button onClick={runFix} className="flex-1 bg-blue-600 text-white py-3 rounded-2xl font-black uppercase text-[10px]">Start AI Fix</button>
                      </div>
                    </div>
                    
                    <div className="bg-white p-10 rounded-[40px] border border-slate-100 shadow-xl">
                      <h4 className="text-slate-400 font-black uppercase tracking-widest text-[10px] mb-6">Issue Breakdown</h4>
                      <ul className="space-y-4">
                        <li className="flex justify-between items-center py-3 border-b border-slate-50">
                          <span className="font-bold text-slate-600">Out of Stock & Live</span>
                          <span className="bg-red-50 text-red-600 px-3 py-1 rounded-full font-black text-xs">{currentInvestigation.findings.out_of_sync_count}</span>
                        </li>
                        <li className="flex justify-between items-center py-3 border-b border-slate-50">
                          <span className="font-bold text-slate-600">Thin Content</span>
                          <span className="bg-amber-50 text-amber-600 px-3 py-1 rounded-full font-black text-xs">{currentInvestigation.findings.thin_content_count}</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                ) : (
                  <div className="py-20 text-center bg-white border-2 border-dashed border-slate-200 rounded-[40px]">
                    <p className="text-slate-400 font-bold">No diagnostic data available. Start an investigation to begin.</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === "planner" && (
              <div className="animate-in fade-in slide-in-from-bottom-4">
                 <div className="flex justify-between items-center mb-12">
                   <div>
                      <h2 className="text-3xl font-black tracking-tight">Content Planner</h2>
                      <p className="text-slate-400 font-bold italic">Strategic keyword targeting for {currentBrand?.name}</p>
                   </div>
                   <button className="bg-blue-600 text-white px-8 py-3 rounded-xl font-black text-xs uppercase tracking-widest">New Strategy</button>
                 </div>
                 
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-lg shadow-slate-200/50">
                       <h3 className="font-black uppercase tracking-widest text-[10px] text-indigo-500 mb-6 underline decoration-2 underline-offset-8">Keyword Gaps</h3>
                       <div className="space-y-4">
                          {["Silk Saree trends 2026", "Designer Wedding Wear", "Luxury Ethnic Sets"].map(kw => (
                            <div key={kw} className="flex justify-between items-center">
                              <span className="text-xs font-bold text-slate-700">{kw}</span>
                              <span className="text-[10px] text-slate-400">High Volume</span>
                            </div>
                          ))}
                       </div>
                    </div>
                    <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-lg shadow-slate-200/50 md:col-span-2">
                       <h3 className="font-black uppercase tracking-widest text-[10px] text-blue-500 mb-6 underline decoration-2 underline-offset-8">Production Queue</h3>
                       <p className="text-slate-300 text-sm italic font-bold">Connect your Notion Content Calendar to sync tasks...</p>
                    </div>
                 </div>
              </div>
            )}

            {activeTab === "injectors" && (
              <div className="animate-in fade-in slide-in-from-bottom-4">
                <h2 className="text-3xl font-black mb-8">Bulk Execution Engine</h2>
                <div className="grid grid-cols-2 gap-8">
                   <InjectorCard 
                      title="SEO Metadata Injector" 
                      desc="Bulk rewrite Titles and Descriptions for the entire 'Lehenga' collection using Fable 5."
                      action="Start Bulk Inject"
                      icon="💉"
                   />
                   <InjectorCard 
                      title="Inventory Sync" 
                      desc="Force 0-stock products to Draft status across the entire store catalog."
                      action="Run Global Sync"
                      icon="🔄"
                   />
                </div>
              </div>
            )}

            {activeTab === "history" && (
              <div className="bg-white p-10 rounded-[40px] shadow-xl border border-slate-100 animate-in fade-in slide-in-from-bottom-4">
                <h2 className="text-xl font-black mb-10 flex items-center gap-3">
                  <span className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center text-sm">📜</span>
                  Audit Trail
                </h2>
                <div className="space-y-6">
                  {activityLogs.map(log => (
                    <div key={log.id} className="flex gap-6 items-start pb-6 border-b border-slate-50 last:border-0">
                       <span className="text-[10px] font-mono text-slate-400 shrink-0 w-20">{log.time}</span>
                       <div className="flex-1">
                          <p className={`text-xs font-bold ${
                            log.type === "error" ? "text-red-500" : 
                            log.type === "success" ? "text-emerald-600" : 
                            log.type === "agent" ? "text-indigo-600" : "text-slate-700"
                          }`}>
                            {log.msg}
                          </p>
                       </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        </div>
      </div>
    </main>
  );
}

function StatCard({ title, value, label, color }: any) {
  const colorMap: any = {
    slate: "text-slate-900",
    blue: "text-blue-600",
    emerald: "text-emerald-600",
    red: "text-red-600"
  };
  
  return (
    <div className="bg-white p-8 rounded-[40px] border border-slate-100 shadow-xl shadow-slate-200/50 flex flex-col justify-between">
      <div>
        <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-4">{title}</p>
        <p className={`text-4xl font-black ${colorMap[color]} tracking-tighter tabular-nums`}>{value}</p>
      </div>
      <p className="text-[10px] font-bold text-slate-300 mt-4 italic">{label}</p>
    </div>
  );
}

function InjectorCard({ title, desc, action, icon }: any) {
  return (
    <div className="bg-white p-10 rounded-[40px] border border-slate-100 shadow-xl hover:shadow-2xl transition-all group">
      <div className="w-12 h-12 bg-slate-50 rounded-2xl flex items-center justify-center text-xl mb-6 group-hover:bg-blue-600 group-hover:text-white transition-colors">
        {icon}
      </div>
      <h3 className="text-xl font-black text-slate-900 mb-3">{title}</h3>
      <p className="text-sm text-slate-500 font-medium leading-relaxed mb-8">{desc}</p>
      <button className="w-full bg-slate-900 text-white py-3 rounded-2xl font-black uppercase text-[10px] tracking-widest hover:bg-blue-600 transition-all">
        {action}
      </button>
    </div>
  );
}
