import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const API = 'http://localhost:8000'

export default function Resources() {
  const [resources, setResources] = useState([])

  useEffect(() => {
    axios.get(`${API}/api/v1/resources`).then(r => setResources(r.data))
  }, [])

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Resources</h1>
        <Link to="/add" className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded text-sm">+ Add Resource</Link>
      </div>
      {resources.length === 0 ? (
        <div className="text-center text-gray-500 py-20">No resources yet. Add one to get started.</div>
      ) : (
        <table className="w-full text-sm">
          <thead><tr className="text-left text-gray-400 border-b border-gray-800">
            <th className="py-2">Name</th><th>Account</th><th>Status</th><th></th>
          </tr></thead>
          <tbody>
            {resources.map(r => (
              <tr key={r.id} className="border-b border-gray-800 hover:bg-gray-900">
                <td className="py-3">{r.resource_name}</td>
                <td>{r.account_name}</td>
                <td>
                  <span className={`px-2 py-1 rounded text-xs ${r.validated ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'}`}>
                    {r.validated ? 'Validated' : 'Not Validated'}
                  </span>
                </td>
                <td><Link to={`/resources/${r.id}`} className="text-indigo-400 hover:underline">View →</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}