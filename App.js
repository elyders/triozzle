import React from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import HomePage from './Home';

export default function App() {
  return React.createElement(
    HashRouter,
    null,
    React.createElement(
      Routes,
      null,
      React.createElement(Route, { path: '/', element: React.createElement(HomePage, null) })
    )
  );
}
