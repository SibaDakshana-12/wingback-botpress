import { Routes, Route, Link } from 'react-router-dom'
import Resources from './pages/Resources'
import AddResource from './pages/AddResource'
import ResourceDetail from './pages/ResourceDetail'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <Link to="/" className="text-xl font-bold text-indigo-400">Wingback Scanner</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Resources />} />
        <Route path="/add" element={<AddResource />} />
        <Route path="/resources/:id" element={<ResourceDetail />} />
      </Routes>
    </div>
  )
}