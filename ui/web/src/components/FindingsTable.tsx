
import React from 'react'

type Finding = {
  broker_name: string
  domain: string
  confidence: number
  evidence_url?: string
  found: boolean
  broker_id: number
  screenshot_path?: string
}

export default function FindingsTable({data, onProceed}:{ data: Finding[], onProceed:(ids:number[])=>void }){
  const [selected, setSelected] = React.useState<number[]>([])
  const foundItems = data.filter(d=>d.found)
  const toggle = (id:number)=> setSelected(s=> s.includes(id)? s.filter(x=>x!==id): [...s,id])
  const selectAll = ()=> setSelected(foundItems.map(f=>f.broker_id))
  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        <button onClick={selectAll} className="px-3 py-1 rounded" style={{background:"#eee"}}>Select All Found</button>
        <button disabled={!selected.length} onClick={()=>onProceed(selected)} className="px-3 py-1 rounded" style={{background: selected.length? "#2563eb":"#94a3b8", color:"#fff"}}>Proceed to Removal</button>
      </div>
      <table style={{width:"100%", fontSize:14}}>
        <thead>
          <tr style={{textAlign:"left", borderBottom:"1px solid #ddd"}}>
            <th>Broker</th><th>Domain</th><th>Found</th><th>Confidence</th><th>Evidence</th><th>Select</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r)=> (
            <tr key={r.broker_id} style={{borderBottom:"1px solid #f0f0f0"}}>
              <td>{r.broker_name}</td>
              <td>{r.domain}</td>
              <td>{r.found? 'Yes':'No'}</td>
              <td>{Math.round((r.confidence||0)*100)}%</td>
              <td>{r.screenshot_path? <a href="#" onClick={(e)=>{e.preventDefault(); alert('Screenshot stored locally: '+r.screenshot_path)}}>screenshot</a> : (r.evidence_url? <a href={r.evidence_url} target="_blank">link</a> : '-')}</td>
              <td>{r.found && (<input type="checkbox" checked={selected.includes(r.broker_id)} onChange={()=>toggle(r.broker_id)} />)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
