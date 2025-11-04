
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

  const buttonStyle = {
    padding: "8px 16px",
    borderRadius: "6px",
    border: "none",
    fontSize: "14px",
    fontWeight: "500",
    cursor: "pointer",
    transition: "all 0.2s ease"
  }

  return (
    <div style={{marginTop: "20px"}}>
      {data.length > 0 && (
        <>
          <h4 style={{
            color: "#2d3748",
            fontSize: "1.2rem",
            marginBottom: "15px",
            display: "flex",
            alignItems: "center",
            gap: "8px"
          }}>
            📋 Discovery Results ({foundItems.length} found out of {data.length} searched)
          </h4>

          <div style={{display: "flex", gap: "10px", marginBottom: "15px"}}>
            <button 
              onClick={selectAll} 
              style={{
                ...buttonStyle,
                background: "linear-gradient(135deg, #48bb78 0%, #38a169 100%)",
                color: "white"
              }}
            >
              ✅ Select All Found ({foundItems.length})
            </button>
            <button 
              disabled={!selected.length} 
              onClick={()=>onProceed(selected)} 
              style={{
                ...buttonStyle,
                background: selected.length ? "linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)" : "#94a3b8",
                color: "white",
                opacity: selected.length ? 1 : 0.6,
                cursor: selected.length ? "pointer" : "not-allowed"
              }}
            >
              🚀 Proceed to Removal ({selected.length})
            </button>
          </div>

          <div style={{
            background: "white",
            borderRadius: "12px",
            overflow: "hidden",
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.05)",
            border: "1px solid #e2e8f0"
          }}>
            <table style={{width: "100%", fontSize: "14px", borderCollapse: "collapse"}}>
              <thead>
                <tr style={{
                  background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  color: "white"
                }}>
                  <th style={{padding: "12px", textAlign: "left", fontWeight: "600"}}>🏢 Broker</th>
                  <th style={{padding: "12px", textAlign: "left", fontWeight: "600"}}>🌐 Domain</th>
                  <th style={{padding: "12px", textAlign: "left", fontWeight: "600"}}>🔍 Found</th>
                  <th style={{padding: "12px", textAlign: "left", fontWeight: "600"}}>📊 Confidence</th>
                  <th style={{padding: "12px", textAlign: "left", fontWeight: "600"}}>📷 Evidence</th>
                  <th style={{padding: "12px", textAlign: "left", fontWeight: "600"}}>☑️ Select</th>
                </tr>
              </thead>
              <tbody>
                {data.map((r, index) => (
                  <tr 
                    key={r.broker_id} 
                    style={{
                      borderBottom: "1px solid #f1f5f9",
                      background: r.found ? 
                        (index % 2 === 0 ? "#fef5e7" : "#fff7ed") : 
                        (index % 2 === 0 ? "#f8fafc" : "#ffffff"),
                      transition: "background-color 0.2s ease"
                    }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.background = r.found ? "#fed7aa" : "#e2e8f0"
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.background = r.found ? 
                        (index % 2 === 0 ? "#fef5e7" : "#fff7ed") : 
                        (index % 2 === 0 ? "#f8fafc" : "#ffffff")
                    }}
                  >
                    <td style={{padding: "12px", fontWeight: r.found ? "600" : "400"}}>
                      {r.broker_name}
                    </td>
                    <td style={{padding: "12px", color: "#6b7280", fontFamily: "monospace"}}>
                      {r.domain}
                    </td>
                    <td style={{padding: "12px"}}>
                      <span style={{
                        padding: "4px 8px",
                        borderRadius: "12px",
                        fontSize: "12px",
                        fontWeight: "600",
                        background: r.found ? "#dcfce7" : "#fef2f2",
                        color: r.found ? "#166534" : "#991b1b"
                      }}>
                        {r.found ? '✅ Yes' : '❌ No'}
                      </span>
                    </td>
                    <td style={{padding: "12px"}}>
                      <div style={{display: "flex", alignItems: "center", gap: "8px"}}>
                        <div style={{
                          width: "60px",
                          height: "6px",
                          background: "#e2e8f0",
                          borderRadius: "3px",
                          overflow: "hidden"
                        }}>
                          <div style={{
                            width: `${(r.confidence || 0) * 100}%`,
                            height: "100%",
                            background: r.confidence > 0.7 ? "#10b981" : r.confidence > 0.4 ? "#f59e0b" : "#ef4444",
                            borderRadius: "3px"
                          }} />
                        </div>
                        <span style={{fontSize: "12px", fontWeight: "500"}}>
                          {Math.round((r.confidence || 0) * 100)}%
                        </span>
                      </div>
                    </td>
                    <td style={{padding: "12px"}}>
                      {r.screenshot_path ? (
                        <button 
                          onClick={(e)=>{e.preventDefault(); alert('Screenshot stored locally: '+r.screenshot_path)}}
                          style={{
                            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            color: "white",
                            border: "none",
                            padding: "4px 8px",
                            borderRadius: "4px",
                            fontSize: "12px",
                            cursor: "pointer"
                          }}
                        >
                          📷 screenshot
                        </button>
                      ) : r.evidence_url ? (
                        <a 
                          href={r.evidence_url} 
                          target="_blank" 
                          style={{
                            color: "#667eea",
                            textDecoration: "none",
                            fontSize: "12px",
                            fontWeight: "500"
                          }}
                        >
                          🔗 link
                        </a>
                      ) : (
                        <span style={{color: "#9ca3af", fontSize: "12px"}}>-</span>
                      )}
                    </td>
                    <td style={{padding: "12px"}}>
                      {r.found && (
                        <input 
                          type="checkbox" 
                          checked={selected.includes(r.broker_id)} 
                          onChange={()=>toggle(r.broker_id)}
                          style={{
                            width: "16px",
                            height: "16px",
                            cursor: "pointer"
                          }}
                        />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
      
      {data.length === 0 && (
        <div style={{
          textAlign: "center",
          padding: "40px",
          color: "#6b7280",
          fontSize: "16px"
        }}>
          🔍 No results yet. Run discovery to search for your data across brokers.
        </div>
      )}
    </div>
  )
}
