const BASE_URL = "http://localhost:8000";

export const api = {
  async listIncidents() {
    const response = await fetch(`${BASE_URL}/api/incidents/`);
    return response.json();
  },
  async createIncident(payload) {
    const response = await fetch(`${BASE_URL}/api/incidents/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  async updateIncident(id, payload) {
    const response = await fetch(`${BASE_URL}/api/incidents/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  async listLogs(incidentId) {
    const query = incidentId ? `?incident_id=${incidentId}` : "";
    const response = await fetch(`${BASE_URL}/api/logs/${query}`);
    return response.json();
  },
  async createLog(payload) {
    const response = await fetch(`${BASE_URL}/api/logs/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  async listKnowledge() {
    const response = await fetch(`${BASE_URL}/api/kb/`);
    return response.json();
  },
  async createKnowledge(payload) {
    const response = await fetch(`${BASE_URL}/api/kb/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  async listAgents() {
    const response = await fetch(`${BASE_URL}/api/agents/status`);
    return response.json();
  },
  async chat(query) {
    const response = await fetch(`${BASE_URL}/api/chat/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(query),
    });
    return response.json();
  },
  async embedKnowledge(payload) {
    const response = await fetch(`${BASE_URL}/api/kb/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  async simulationCommand(action) {
    const response = await fetch(`${BASE_URL}/api/simulation/control`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action }),
    });
    return response.json();
  },
  async listSlaTimers() {
    const response = await fetch(`${BASE_URL}/api/sla/`);
    return response.json();
  },
  async serviceNowUpdate(payload) {
    const response = await fetch(`${BASE_URL}/api/servicenow/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
};

export const connectEventStream = (onMessage) => {
  const socket = new WebSocket("ws://localhost:8000/ws/events");
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage?.(data);
  };
  return socket;
};
