import { HashRouter, Route, Routes } from 'react-router-dom'
import HomePage from './Home'

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </HashRouter>
  )
}
