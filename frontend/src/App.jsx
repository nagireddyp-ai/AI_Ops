import React from "react";
import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import ITSMPanel from "./pages/ITSMPanel.jsx";
import KnowledgeBase from "./pages/KnowledgeBase.jsx";
import Chatbot from "./pages/Chatbot.jsx";
import SimulationControl from "./pages/SimulationControl.jsx";

const App = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/itsm" element={<ITSMPanel />} />
        <Route path="/kb" element={<KnowledgeBase />} />
        <Route path="/chat" element={<Chatbot />} />
        <Route path="/simulation" element={<SimulationControl />} />
      </Routes>
    </Layout>
  );
};

export default App;
