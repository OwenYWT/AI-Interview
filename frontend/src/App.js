// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import WelcomePage from './components/WelcomePage';
import JobSelectionPage from './components/JobSelectionPage';
import ChatPage from './components/ChatPage';
import FeedbackPage from "./components/FeedbackPage";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<WelcomePage />} />
                <Route path="/job-selection" element={<JobSelectionPage />} />
                <Route path="/feedback" element={<FeedbackPage />} />
                <Route path="/chat" element={<ChatPage />} />
            </Routes>
        </Router>
    );
};

export default App;