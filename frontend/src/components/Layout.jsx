import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

import { api, connectEventStream } from "../services/api.js";

const Layout = ({ children }) => {
  const [events, setEvents] = useState([]);
  const [agents, setAgents] = useState([]);
  const [ticker, setTicker] = useState([]);

  useEffect(() => {
    let socket;
    const loadAgents = () => api.listAgents().then(setAgents).catch(() => setAgents([]));
    loadAgents();
    socket = connectEventStream((event) => {
      setEvents((prev) => [event, ...prev].slice(0, 12));
      if (event.event?.includes("incident")) {
        setTicker((prev) => [event, ...prev].slice(0, 8));
      }
    });
    const interval = setInterval(loadAgents, 15000);
    return () => {
      clearInterval(interval);
      socket?.close();
    };
  }, []);

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">SitePulse</div>
        <nav>
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/itsm">ITSM Panel</NavLink>
          <NavLink to="/kb">Knowledge Base</NavLink>
          <NavLink to="/chat">Chatbot</NavLink>
          <NavLink to="/simulation">Simulation Control</NavLink>
        </nav>
      </aside>
      <main>
        <header className="topbar">
          <div className="ticker">
            <span className="label">Live Incident Ticker</span>
            <div className="ticker-items">
              {ticker.length === 0 ? (
                <span>No incidents yet.</span>
              ) : (
                ticker.map((item, index) => (
                  <span key={`${item.event}-${index}`}>
                    {item.event} · {item.data?.title ?? item.data?.incident_id ?? "update"}
                  </span>
                ))
              )}
            </div>
          </div>
          <div className="agents">
            {agents.map((agent) => (
              <div key={agent.name} className="agent">
                <strong>{agent.name}</strong>
                <span>{agent.status}</span>
              </div>
            ))}
          </div>
        </header>
        <div className="content">
          <section className="panel">{children}</section>
          <aside className="activity">
            <h3>Agent Activity</h3>
            <ul>
              {events.length === 0 ? (
                <li>No activity yet.</li>
              ) : (
                events.map((event, index) => (
                  <li key={`${event.event}-${index}`}>
                    <strong>{event.event}</strong>
                    <span>{event.data?.status ?? event.data?.incident_id ?? ""}</span>
                  </li>
                ))
              )}
            </ul>
          </aside>
        </div>
      </main>
    </div>
  );
};

export default Layout;
