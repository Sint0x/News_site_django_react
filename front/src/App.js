import React from "react";
import MembersRouter from "./routes/Routing";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

export default function App() {
  return (  
    <Router>
      <MembersRouter />
      <Routes>
      </Routes>
    </Router>
  );
}