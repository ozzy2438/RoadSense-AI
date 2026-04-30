"use client";

import { useState } from "react";
import { SendHorizonal } from "lucide-react";
import { AgentTimeline, AgentStep } from "../components/AgentTimeline";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [memberId, setMemberId] = useState("M-10042");
  const [message, setMessage] = useState(
    "I hit debris near Ballarat and need a tow. Is this covered?"
  );
  const [steps, setSteps] = useState<AgentStep[]>([]);
  const [loading, setLoading] = useState(false);

  async function runTriage() {
    setLoading(true);
    setSteps([]);

    const response = await fetch(`${API_URL}/triage`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ member_id: memberId, channel: "chat", message }),
    });
    const finalStep = (await response.json()) as AgentStep;
    setSteps([finalStep]);
    setLoading(false);
  }

  return (
    <main>
      <section className="sidebar">
        <h1 className="brand">RoadSense AI</h1>
        <p className="muted">Claims and roadside triage console</p>

        <label htmlFor="member">Member ID</label>
        <input id="member" value={memberId} onChange={(event) => setMemberId(event.target.value)} />

        <label htmlFor="message">Incoming request</label>
        <textarea id="message" value={message} onChange={(event) => setMessage(event.target.value)} />

        <button disabled={loading} onClick={runTriage}>
          <SendHorizonal size={16} /> {loading ? "Running triage" : "Run triage"}
        </button>
      </section>

      <section className="workspace">
        <AgentTimeline steps={steps} loading={loading} />
      </section>
    </main>
  );
}
