export type AgentStep = {
  name: string;
  status: "started" | "completed" | "blocked";
  summary: string;
  payload: Record<string, unknown>;
};

export function AgentTimeline({ steps, loading }: { steps: AgentStep[]; loading: boolean }) {
  if (steps.length === 0) {
    return (
      <div className="step">
        <div className="step-header">
          <span>{loading ? "Running agent graph" : "No triage run yet"}</span>
          <span className="pill">{loading ? "active" : "idle"}</span>
        </div>
        <p className="muted">Submit a member request to inspect the final recommendation.</p>
      </div>
    );
  }

  return (
    <div className="timeline">
      {steps.map((step, index) => (
        <article className="step" key={`${step.name}-${index}`}>
          <div className="step-header">
            <span>{step.name}</span>
            <span className="pill">{step.status}</span>
          </div>
          <p>{step.summary}</p>
          <pre>{JSON.stringify(step.payload, null, 2)}</pre>
        </article>
      ))}
    </div>
  );
}
