import React, { useEffect, useState } from "react";

import { api } from "../services/api.js";

const sampleIncident = () => ({
  title: "CPU spike on core-payment",
  type: "CPU spike",
  hostname: `srv-pay-${Math.floor(Math.random() * 50) + 1}`,
  region: "us-east-1",
  environment: "prod",
  severity: "P2",
});

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [slaTimers, setSlaTimers] = useState([]);

  const refresh = async () => {
    const [incidentData, slaData] = await Promise.all([
      api.listIncidents(),
      api.listSlaTimers(),
    ]);
    setIncidents(incidentData);
    setSlaTimers(slaData);
  };

  useEffect(() => {
    refresh();
  }, []);

  const handleSimulate = async () => {
    await api.createIncident(sampleIncident());
    refresh();
  };

  return (
    <div>
      <div className="page-header">
        <h1>Realtime Dashboard</h1>
        <div className="actions">
          <button onClick={handleSimulate}>Simulate Incident</button>
          <button onClick={() => api.simulationCommand("pause")}>Pause Simulation</button>
          <button onClick={() => api.simulationCommand("reset")}>Reset System</button>
          <button onClick={() => api.simulationCommand("escalate")}>Trigger Escalation</button>
        </div>
      </div>
      <div className="grid">
        <section>
          <h2>Live Incident Feed</h2>
          <ul>
            {incidents.length === 0 ? (
              <li>No incidents yet.</li>
            ) : (
              incidents.map((incident) => (
                <li key={incident.id}>
                  <strong>{incident.title}</strong>
                  <span>{incident.status}</span>
                  <span>{incident.severity}</span>
                </li>
              ))
            )}
          </ul>
        </section>
        <section>
          <h2>SLA Countdown Timers</h2>
          <ul>
            {slaTimers.length === 0 ? (
              <li>No active SLAs.</li>
            ) : (
              slaTimers.map((timer) => (
                <li key={timer.incident_id}>
                  {timer.incident_id} · {timer.remaining_minutes} min
                </li>
              ))
            )}
          </ul>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
