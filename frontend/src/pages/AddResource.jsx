import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API = 'https://wingback-botpress.onrender.com'

export default function AddResource() {
  const nav = useNavigate()
  const [form, setForm] = useState({ account_name:'', resource_name:'', webhook_id:'', encryption_key:'', user_id:'', description:'' })
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const update = e => setForm({...form, [e.target.name]: e.target.value})

  const validate = async () => {
    setLoading(true)
    setStatus(null)
    try {
      const r = await axios.post(`${API}/api/v1/resources`, form)
      const id = r.data.id
      const v = await axios.post(`${API}/api/v1/resources/${id}/validate`)
      setStatus(v.data.validated ? 'success' : 'fail')
      if (v.data.validated) setTimeout(() => nav(`/resources/${id}`), 1000)
    } catch(e) {
      setStatus('error')
    }
    setLoading(false)
  }

  const fields = [
    {name:'account_name', label:'Account Name', required:true},
    {name:'resource_name', label:'Resource Name', required:true},
    {name:'webhook_id', label:'Webhook ID', required:true},
    {name:'encryption_key', label:'Encryption Key', required:false},
    {name:'user_id', label:'User ID', required:false},
    {name:'description', label:'Description', required:false},
  ]

  return (
    <div className="max-w-lg mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Add Resource</h1>
      <div className="space-y-4">
        {fields.map(f => (
          <div key={f.name}>
            <label className="block text-sm text-gray-400 mb-1">{f.label}{f.required && <span className="text-red-400"> *</span>}</label>
            <input name={f.name} value={form[f.name]} onChange={update}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
          </div>
        ))}
      </div>
      {status === 'success' && <div className="mt-4 text-green-400">✅ Connected! Redirecting...</div>}
      {status === 'fail' && <div className="mt-4 text-red-400">❌ Validation failed. Check webhook ID.</div>}
      {status === 'error' && <div className="mt-4 text-red-400">❌ Error. Check backend.</div>}
      <button onClick={validate} disabled={loading}
        className="mt-6 w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 py-2 rounded font-medium">
        {loading ? 'Connecting...' : 'Validate & Save'}
      </button>
    </div>
  )
}