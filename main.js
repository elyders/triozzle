import React from 'react';
import { createRoot } from 'react-dom/client';
import './shadcn.css';
import App from './main/App';

const root = createRoot(document.getElementById('app'));
root.render(React.createElement(App, null));
