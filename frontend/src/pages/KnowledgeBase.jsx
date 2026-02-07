import React, { useEffect, useState } from "react";

import { api } from "../services/api.js";

const KnowledgeBase = () => {
  const [articles, setArticles] = useState([]);
  const [query, setQuery] = useState("");

  const refresh = async () => {
    const data = await api.listKnowledge();
    setArticles(data);
  };

  useEffect(() => {
    refresh();
  }, []);

  const filtered = articles.filter((article) =>
    article.title.toLowerCase().includes(query.toLowerCase())
  );

  const handleCreate = async () => {
    await api.createKnowledge({
      title: "Disk full remediation",
      summary: "Clear cache and extend volume.",
      content: "Steps: 1) identify large files 2) clear tmp 3) expand volume",
      tags: ["disk", "storage"],
      incident_id: articles[0]?.incident_id ?? "manual",
    });
    refresh();
  };

  return (
    <div>
      <div className="page-header">
        <h1>Knowledge Base</h1>
        <div className="actions">
          <button onClick={handleCreate}>Regenerate Article</button>
          <button onClick={() => api.simulationCommand("embed_kb")}>Embed into RAG</button>
        </div>
      </div>
      <div className="filters">
        <input
          placeholder="Search KB"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </div>
      <ul>
        {filtered.length === 0 ? (
          <li>No knowledge articles yet.</li>
        ) : (
          filtered.map((article) => (
            <li key={article.id}>
              <h3>{article.title}</h3>
              <p>{article.summary}</p>
              <small>Tags: {article.tags.join(", ")}</small>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default KnowledgeBase;
