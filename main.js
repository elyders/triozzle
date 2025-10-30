import React from 'react';
import { createRoot } from 'react-dom/client';
import './shadcn.css';
import App from "https://cdn.jsdelivr.net/gh/elyders/triozzle/App.js";

const root = createRoot(document.getElementById('app'));
root.render(React.createElement(App, null));
