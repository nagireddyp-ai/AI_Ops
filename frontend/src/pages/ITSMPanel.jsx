import React, { useEffect, useState } from "react";

import { api } from "../services/api.js";

const ITSMPanel = () => {
  const [incidents, setIncidents] = useState([]);
  const [selected, setSelected] = useState(null);
  const [status, setStatus] = useState("in_progress");
  const [engineer, setEngineer] = useState("Alex Morgan");
  const [logs, setLogs] = useState([]);
  const [ragSuggestion, setRagSuggestion] = useState(null);

  const refresh = async () => {
    const data = await api.listIncidents();
    setIncidents(data);
    if (data.length && !selected) {
      setSelected(data[0]);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const handleUpdate = async () => {
    if (!selected) return;
    const updated = await api.updateIncident(selected.id, {
      status,
      assigned_engineer: engineer,
    });
    setSelected(updated);
    refresh();
  };

  const handleResolve = async () => {
    if (!selected) return;
    const updated = await api.updateIncident(selected.id, {
      status: "resolved",
      assigned_engineer: engineer,
    });
    setSelected(updated);
    refresh();
  };

  const handleServiceNow = async () => {
    if (!selected) return;
    await api.serviceNowUpdate({
      incident_id: selected.id,
      status,
      notes: "Updated via ITSM panel",
    });
  };

  const handleViewLogs = async () => {
    if (!selected) return;
    const data = await api.listLogs(selected.id);
    setLogs(data);
  };

  const handleRagSuggestion = async () => {
    if (!selected) return;
    const response = await api.chat({
      question: `Suggest remediation for ${selected.title} (${selected.severity})`,
    });
    setRagSuggestion(response);
  };

  return (
    <div>
      <div className="page-header">
        <h1>ITSM Panel</h1>
      </div>
      <div className="grid">
        <section>
          <h2>Incident List</h2>
          <ul>
            {incidents.map((incident) => (
              <li key={incident.id}>
                <button className="link" onClick={() => setSelected(incident)}>
                  {incident.title}
                </button>
              </li>
            ))}
          </ul>
        </section>
        <section>
          <h2>Incident Details</h2>
          {!selected ? (
            <p>Select an incident.</p>
          ) : (
            <div className="card">
              <p>
                <strong>ID:</strong> {selected.id}
              </p>
              <p>
                <strong>Status:</strong> {selected.status}
              </p>
              <p>
                <strong>Severity:</strong> {selected.severity}
              </p>
              <label>
                Update status
                <select value={status} onChange={(event) => setStatus(event.target.value)}>
                  <option value="new">new</option>
                  <option value="triaged">triaged</option>
                  <option value="in_progress">in_progress</option>
                  <option value="resolved">resolved</option>
                </select>
              </label>
              <label>
                Assign engineer
                <input value={engineer} onChange={(event) => setEngineer(event.target.value)} />
              </label>
              <div className="actions">
                <button onClick={handleUpdate}>Update Status</button>
                <button onClick={handleResolve}>Resolve Ticket</button>
                <button onClick={handleServiceNow}>Sync ServiceNow</button>
                <button onClick={handleViewLogs}>View Logs</button>
                <button onClick={handleRagSuggestion}>View RAG Suggestions</button>
              </div>
            </div>
          )}
        </section>
        <section>
          <h2>Incident Logs</h2>
          {logs.length === 0 ? (
            <p>No logs loaded.</p>
          ) : (
            <ul>
              {logs.map((log) => (
                <li key={log.id}>
                  <strong>{log.level}</strong> {log.message}
                </li>
              ))}
            </ul>
          )}
        </section>
        <section>
          <h2>RAG Suggestions</h2>
          {!ragSuggestion ? (
            <p>Run suggestions to see guidance.</p>
          ) : (
            <div className="card">
              <p>{ragSuggestion.answer}</p>
              <small>Sources: {ragSuggestion.sources.join(", ")}</small>
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default ITSMPanel;
