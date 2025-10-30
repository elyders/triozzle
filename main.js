import { createRoot } from 'react-dom/client'
import './shadcn.css'
import App from './App.js'
import React from 'react'

const root = createRoot(document.getElementById('app'))
root.render(React.createElement(App))
