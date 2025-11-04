
import React from 'react'
import FindingsTable from './FindingsTable'
import ProfileForm from './ProfileForm'

export default function DiscoveryPanel(){
  const [profileId, setProfileId] = React.useState<string>("")
  const [profiles, setProfiles] = React.useState<any[]>([])
  const [job, setJob] = React.useState<string|undefined>(undefined)
  const [progress, setProgress] = React.useState<number>(0)
  const [findings, setFindings] = React.useState<any[]>([])
  const [showProfileForm, setShowProfileForm] = React.useState<boolean>(false)

  React.useEffect(()=>{
    loadProfiles()
  }, [])

  function loadProfiles(){
    fetch("http://127.0.0.1:5179/pii-profiles").then(r=>r.json()).then(setProfiles)
  }

  function startDiscovery(){
    if(!profileId){ alert("Create/select a PII profile first"); return; }
    fetch(`http://127.0.0.1:5179/discovery?profile_id=${profileId}`, {method:"POST"})
    .then(r=>r.json()).then(({job_id})=>{
      setJob(job_id)
      const t = setInterval(async ()=>{
        const s = await fetch(`http://127.0.0.1:5179/discovery/${job_id}`).then(r=>r.json())
        setProgress(s.progress||0)
        setFindings(s.items||[])
        if(s.status === "completed"){ clearInterval(t) }
      }, 800)
    })
  }

  function createDummyProfile(){
    fetch("http://127.0.0.1:5179/pii-profiles", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({label:"Demo Profile", names:["John Q Public"], emails:["john@example.com"], phones:["(555) 123-4567"], addresses:[{city:"Oakland"}]})
    }).then(()=> loadProfiles())
  }

  function saveProfile(profileData: any) {
    fetch("http://127.0.0.1:5179/pii-profiles", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(profileData)
    })
    .then(response => {
      if (response.ok) {
        setShowProfileForm(false)
        loadProfiles()
        return response.json()
      }
      throw new Error('Failed to save profile')
    })
    .then(newProfile => {
      // Auto-select the new profile
      setProfileId(newProfile.id)
    })
    .catch(error => {
      console.error('Error saving profile:', error)
      alert('Failed to save profile. Please try again.')
    })
  }

  function planRemoval(ids:number[]){
    fetch("http://127.0.0.1:5179/removals", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({profile_id: profileId, brokers: ids})
    }).then(r=>r.json()).then(plan => alert("Removal plan drafted for "+plan.items.length+" brokers."))
  }

  const buttonStyle = {
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    color: "white",
    border: "none",
    padding: "10px 20px",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "14px",
    fontWeight: "500",
    transition: "all 0.3s ease",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
  }

  const selectStyle = {
    padding: "10px 15px",
    borderRadius: "8px",
    border: "2px solid #e2e8f0",
    fontSize: "14px",
    background: "white",
    color: "#333",
    cursor: "pointer",
    minWidth: "200px"
  }

  return (
    <div>
      <h3 style={{
        color: "#2d3748",
        fontSize: "1.5rem",
        marginBottom: "20px",
        display: "flex",
        alignItems: "center",
        gap: "10px"
      }}>
        🔍 Discovery & Search
      </h3>
      
      <div style={{
        display: "flex", 
        gap: "15px", 
        alignItems: "center",
        flexWrap: "wrap",
        marginBottom: "20px",
        padding: "20px",
        background: "linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)",
        borderRadius: "12px",
        border: "1px solid #e2e8f0"
      }}>
        <select 
          value={profileId} 
          onChange={e=>setProfileId(e.target.value)}
          style={selectStyle}
        >
          <option value="">Select profile...</option>
          {profiles.map((p:any)=> <option key={p.id} value={p.id}>{p.label}</option>)}
        </select>
        
        <button 
          onClick={createDummyProfile}
          style={{
            ...buttonStyle,
            background: "linear-gradient(135deg, #48bb78 0%, #38a169 100%)"
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.transform = "translateY(-2px)"
            e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.15)"
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = "translateY(0)"
            e.currentTarget.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)"
          }}
        >
          📝 Quick Demo Profile
        </button>
        
        <button 
          onClick={() => setShowProfileForm(true)}
          style={{
            ...buttonStyle,
            background: "linear-gradient(135deg, #9f7aea 0%, #805ad5 100%)"
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.transform = "translateY(-2px)"
            e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.15)"
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = "translateY(0)"
            e.currentTarget.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)"
          }}
        >
          ➕ Create New Profile
        </button>
        
        <button 
          onClick={startDiscovery}
          style={{
            ...buttonStyle,
            background: "linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)",
            fontSize: "16px",
            fontWeight: "600"
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.transform = "translateY(-2px)"
            e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.15)"
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = "translateY(0)"
            e.currentTarget.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)"
          }}
        >
          🚀 Run Discovery
        </button>
        
        {job && (
          <div style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            padding: "8px 16px",
            background: progress === 100 ? "#48bb78" : "#667eea",
            color: "white",
            borderRadius: "20px",
            fontSize: "14px",
            fontWeight: "500"
          }}>
            <span>📊 Progress: {progress}%</span>
            {progress < 100 && (
              <div style={{
                width: "100px",
                height: "6px",
                background: "rgba(255,255,255,0.3)",
                borderRadius: "3px",
                overflow: "hidden"
              }}>
                <div style={{
                  width: `${progress}%`,
                  height: "100%",
                  background: "white",
                  borderRadius: "3px",
                  transition: "width 0.3s ease"
                }} />
              </div>
            )}
          </div>
        )}
      </div>

      {/* Selected Profile Info */}
      {profileId && (
        <div style={{
          background: "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)",
          borderRadius: "12px",
          padding: "16px",
          marginBottom: "20px",
          border: "1px solid #bae6fd"
        }}>
          {(() => {
            const selectedProfile = profiles.find(p => p.id === profileId)
            if (!selectedProfile) return null
            
            return (
              <div>
                <h4 style={{
                  color: "#0369a1",
                  fontSize: "1.1rem",
                  marginBottom: "10px",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px"
                }}>
                  👤 Selected Profile: {selectedProfile.label}
                </h4>
                <div style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                  gap: "12px",
                  fontSize: "14px"
                }}>
                  {selectedProfile.names?.length > 0 && (
                    <div>
                      <strong style={{color: "#0369a1"}}>Names:</strong> {selectedProfile.names.join(", ")}
                    </div>
                  )}
                  {selectedProfile.emails?.length > 0 && (
                    <div>
                      <strong style={{color: "#0369a1"}}>Emails:</strong> {selectedProfile.emails.join(", ")}
                    </div>
                  )}
                  {selectedProfile.phones?.length > 0 && (
                    <div>
                      <strong style={{color: "#0369a1"}}>Phones:</strong> {selectedProfile.phones.join(", ")}
                    </div>
                  )}
                  {selectedProfile.addresses?.length > 0 && (
                    <div>
                      <strong style={{color: "#0369a1"}}>Addresses:</strong> {selectedProfile.addresses.map((addr: any) => 
                        Object.values(addr).filter(Boolean).join(", ")
                      ).join(" | ")}
                    </div>
                  )}
                </div>
              </div>
            )
          })()}
        </div>
      )}

      <div style={{marginTop: "20px"}}>
        <FindingsTable 
          data={findings}
          jobId={job}
          onProceed={(selectedIds: number[]) => {
            console.log('Proceeding with', selectedIds)
            planRemoval(selectedIds)
          }}
        />
      </div>

      {/* Profile Creation Form Modal */}
      {showProfileForm && (
        <ProfileForm
          onSave={saveProfile}
          onCancel={() => setShowProfileForm(false)}
        />
      )}
    </div>
  )
}
