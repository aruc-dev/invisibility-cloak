
import React from 'react'
import FindingsTable from './FindingsTable'

export default function DiscoveryPanel(){
  const [profileId, setProfileId] = React.useState<string>("")
  const [profiles, setProfiles] = React.useState<any[]>([])
  const [job, setJob] = React.useState<string|undefined>(undefined)
  const [progress, setProgress] = React.useState<number>(0)
  const [items, setItems] = React.useState<any[]>([])

  React.useEffect(()=>{
    fetch("http://127.0.0.1:5179/pii-profiles").then(r=>r.json()).then(setProfiles)
  }, [])

  function startDiscovery(){
    if(!profileId){ alert("Create/select a PII profile first"); return; }
    fetch(`http://127.0.0.1:5179/discovery?profile_id=${profileId}`, {method:"POST"})
    .then(r=>r.json()).then(({job_id})=>{
      setJob(job_id)
      const t = setInterval(async ()=>{
        const s = await fetch(`http://127.0.0.1:5179/discovery/${job_id}`).then(r=>r.json())
        setProgress(s.progress||0)
        setItems(s.items||[])
        if(s.status === "completed"){ clearInterval(t) }
      }, 800)
    })
  }

  function createDummyProfile(){
    fetch("http://127.0.0.1:5179/pii-profiles", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({label:"Me", names:["John Q Public"], emails:["john@example.com"], phones:["(555) 123-4567"], addresses:[{city:"Oakland"}]})
    }).then(()=> fetch("http://127.0.0.1:5179/pii-profiles").then(r=>r.json()).then(setProfiles))
  }

  function planRemoval(ids:number[]){
    fetch("http://127.0.0.1:5179/removals", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({profile_id: profileId, brokers: ids})
    }).then(r=>r.json()).then(plan => alert("Removal plan drafted for "+plan.items.length+" brokers."))
  }

  return (
    <div>
      <h3>Discovery</h3>
      <div style={{display:"flex", gap:8, alignItems:"center"}}>
        <select value={profileId} onChange={e=>setProfileId(e.target.value)}>
          <option value="">Select profile...</option>
          {profiles.map((p:any)=> <option key={p.id} value={p.id}>{p.label}</option>)}
        </select>
        <button onClick={createDummyProfile}>Quick Create Dummy Profile</button>
        <button onClick={startDiscovery}>Run Discovery</button>
        {job && <span>Progress: {progress}%</span>}
      </div>

      <div style={{marginTop:16}}>
        <FindingsTable data={items} onProceed={planRemoval} />
      </div>
    </div>
  )
}
