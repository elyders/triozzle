import React from 'react';
import { createRoot } from 'react-dom/client';
import './shadcn.css';
import App from "https://raw.githubusercontent.com/elyders/triozzle/refs/heads/main/App.js";

const root = createRoot(document.getElementById('app'));
root.render(React.createElement(App, null));
