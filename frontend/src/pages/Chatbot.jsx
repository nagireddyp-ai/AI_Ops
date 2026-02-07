import React, { useState } from "react";

import { api } from "../services/api.js";

const Chatbot = () => {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = await api.chat({ question });
    setResponse(data);
  };

  const handleUpdateTicket = async () => {
    await api.simulationCommand("chat_update_ticket");
  };

  return (
    <div>
      <div className="page-header">
        <h1>RAG Chat Assistant</h1>
      </div>
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask about an incident, KB article, or log"
        />
        <button type="submit">Send</button>
      </form>
      {response && (
        <div className="card">
          <p>{response.answer}</p>
          <p>
            <strong>Sources:</strong> {response.sources.join(", ")}
          </p>
          <button onClick={handleUpdateTicket}>Update Ticket</button>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
