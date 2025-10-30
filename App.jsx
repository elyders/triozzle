import { HashRouter, Route, Routes } from 'react-router-dom'
import HomePage from './Home.jsx'

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </HashRouter>
  )
}
