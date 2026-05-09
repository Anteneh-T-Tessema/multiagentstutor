import { useState } from 'react'
import './App.css'

interface ProposalResponse {
  proposal: string;
  constraints: string[];
  steps: string[];
  rag_context: string[];
  tool_data: any;
}

function App() {
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ProposalResponse | null>(null);
  const [currentStep, setCurrentStep] = useState<string | null>(null);
  const [isAwaitingReview, setIsAwaitingReview] = useState(false);
  const thread_id = "consultant_session_1";

  const generateProposal = async () => {
    setLoading(true);
    setResult(null);
    
    // Simulate steps for UI feel
    const steps = ['analyst', 'rag', 'tooling', 'architect'];
    for (const step of steps) {
      setCurrentStep(step);
      await new Promise(r => setTimeout(r, 800)); // Visual delay
    }

    try {
      const response = await fetch('http://localhost:7854/generate-proposal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes, thread_id }),
      });
      
      const data = await response.json();
      if (data.status === 'awaiting_review') {
        setIsAwaitingReview(true);
      }
      setResult(data);
    } catch (error) {
      console.error('Failed to generate proposal:', error);
      alert('Error connecting to backend.');
    } finally {
      setLoading(false);
      setCurrentStep(null);
    }
  };

  const approveProposal = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:7854/approve-proposal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes, thread_id }),
      });
      const data = await response.json();
      setResult(data);
      setIsAwaitingReview(false);
    } catch (error) {
      console.error('Failed to approve proposal:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-wrapper">
      <header className="header">
        <h1>Consulting Delivery Copilot</h1>
        <p className="subtitle">Agentic Solution Architecture Assistant (Powered by {import.meta.env.VITE_MODEL_NAME || 'Gemma 4:26b'})</p>
      </header>

      <main className="app-container">
        {/* Left Panel: Input & Reasoning */}
        <section className="card">
          <h3>1. Discovery Notes</h3>
          <textarea 
            placeholder="Paste messy client discovery notes here..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            disabled={loading}
          />
          
          <button 
            onClick={generateProposal} 
            disabled={loading || !notes}
          >
            {loading ? 'Processing Agent Workflow...' : 'Generate Architecture'}
          </button>

          <div className="reasoning-panel">
            <h3>2. Agent Reasoning Chain</h3>
            {[
              { id: 'analyst', label: 'Analyst: Constraint Extraction' },
              { id: 'rag', label: 'RAG: Reference Architecture Retrieval' },
              { id: 'tooling', label: 'MCP Tooling: Compliance & Governance' },
              { id: 'architect', label: 'Architect: Solution Synthesis' }
            ].map(step => (
              <div key={step.id} className={`status-step ${currentStep === step.id ? 'active' : ''} ${result?.steps.includes(step.id) ? 'complete' : ''}`}>
                {result?.steps.includes(step.id) ? '✅' : currentStep === step.id ? '⏳' : '⚪️'} {step.label}
              </div>
            ))}
          </div>
        </section>

        {/* Right Panel: Result */}
        <section className="card" style={{ overflowY: 'auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3>3. Technical Solution Proposal</h3>
            {isAwaitingReview && (
              <div style={{ background: '#f8514933', border: '1px solid #f85149', padding: '4px 12px', borderRadius: '4px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ color: '#f85149', fontSize: '0.8rem', fontWeight: 'bold' }}>⚠️ REVIEW REQUIRED</span>
                <button 
                  onClick={approveProposal}
                  style={{ background: '#238636', color: 'white', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer', fontSize: '0.7rem' }}
                >
                  Approve & Resume
                </button>
              </div>
            )}
          </div>
          <div className="proposal-view">
            {result ? (
              <div className="content-area">
                <div className="markdown-content" style={{ backgroundColor: '#0d1117', padding: '1rem', borderRadius: '8px' }}>
                  {result.proposal}
                </div>
                
                <div className="transparency-log" style={{ marginTop: '2rem', borderTop: '1px solid #30363d', paddingTop: '1rem' }}>
                  <h4 style={{ color: '#58a6ff' }}>🔍 Transparency Log (Internal Reasoning)</h4>
                  <div style={{ marginBottom: '1rem' }}>
                    <small style={{ color: '#8b949e' }}>Retrieved Context Snippets:</small>
                    {result.rag_context.map((ctx, i) => (
                      <pre key={i} style={{ fontSize: '0.7rem', background: '#000', padding: '0.5rem', borderRadius: '4px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{ctx}</pre>
                    ))}
                  </div>
                  <div>
                    <small style={{ color: '#8b949e' }}>MCP Tool Decisions:</small>
                    <pre style={{ fontSize: '0.7rem', background: '#000', padding: '0.5rem', borderRadius: '4px' }}>{JSON.stringify(result.tool_data, null, 2)}</pre>
                  </div>
                </div>
              </div>
            ) : loading ? (
              <p style={{ color: '#8b949e' }}>Generating comprehensive proposal based on retrieved context and tools...</p>
            ) : (
              <p style={{ color: '#8b949e' }}>Input discovery notes and generate to see the architectural proposal.</p>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
