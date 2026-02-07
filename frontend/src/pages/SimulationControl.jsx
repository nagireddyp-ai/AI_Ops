import React from "react";

import { api } from "../services/api.js";

const SimulationControl = () => {
  return (
    <div>
      <div className="page-header">
        <h1>Simulation Control Panel</h1>
      </div>
      <div className="grid">
        <section className="card">
          <h2>Simulation Controls</h2>
          <div className="actions">
            <button onClick={() => api.simulationCommand("start")}>Start Simulation</button>
            <button onClick={() => api.simulationCommand("stop")}>Stop Simulation</button>
            <button onClick={() => api.simulationCommand("generate_10")}>Generate 10 Incidents</button>
          </div>
        </section>
        <section className="card">
          <h2>Advanced Scenarios</h2>
          <div className="actions">
            <button onClick={() => api.simulationCommand("trigger_outage")}>Trigger Outage</button>
            <button onClick={() => api.simulationCommand("simulate_sla_breach")}>
              Simulate SLA Breach
            </button>
            <button onClick={() => api.simulationCommand("inject_log_spike")}>
              Inject Log Spike
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default SimulationControl;
