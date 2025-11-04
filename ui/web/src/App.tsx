
import React from "react"
import DiscoveryPanel from "./components/DiscoveryPanel"
import RemovalPanel from "./components/RemovalPanel"

export default function App(){
  const [activeTab, setActiveTab] = React.useState<'discovery' | 'removal'>('discovery')
  const [selectedBrokers, setSelectedBrokers] = React.useState<number[]>([])
  const [profileId, setProfileId] = React.useState<string>("")
  
  // Discovery state managed at App level to persist across tab switches
  const [discoveryJob, setDiscoveryJob] = React.useState<string|undefined>(undefined)
  const [discoveryProgress, setDiscoveryProgress] = React.useState<number>(0)
  const [discoveryFindings, setDiscoveryFindings] = React.useState<any[]>([])
  const [discoveryBrokerCount, setDiscoveryBrokerCount] = React.useState<{current: number, total: number, currentName?: string}>({current: 0, total: 0})

  const handleProceedToRemoval = (brokerIds: number[], profileId: string) => {
    setSelectedBrokers(brokerIds)
    setProfileId(profileId)
    setActiveTab('removal')
  }

  const tabStyle = {
    padding: "12px 24px",
    borderRadius: "8px 8px 0 0",
    border: "none",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "all 0.3s ease",
    marginRight: "4px"
  }

  return (
    <div style={{
      fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
      minHeight: "100vh",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      color: "#ffffff",
      margin: 0,
      padding: 0
    }}>
      <div style={{
        padding: "40px 20px",
        maxWidth: "1200px",
        margin: "0 auto"
      }}>
        <header style={{
          textAlign: "center",
          marginBottom: "40px",
          padding: "20px",
          background: "rgba(255, 255, 255, 0.1)",
          borderRadius: "15px",
          backdropFilter: "blur(10px)",
          border: "1px solid rgba(255, 255, 255, 0.2)"
        }}>
          <h1 style={{
            fontSize: "2.5rem",
            margin: "0 0 10px 0",
            background: "linear-gradient(45deg, #ffd700, #ffec8c)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
            textShadow: "0 2px 4px rgba(0,0,0,0.3)"
          }}>
            🕵️‍♂️ Invisibility Cloak
          </h1>
          <p style={{
            fontSize: "1.1rem",
            opacity: 0.9,
            margin: 0,
            fontWeight: "300"
          }}>
            Privacy-First Data Discovery & Removal Platform
          </p>
        </header>

        {/* Tab Navigation */}
        <div style={{
          marginBottom: "0",
          display: "flex",
          justifyContent: "center"
        }}>
          <button
            onClick={() => setActiveTab('discovery')}
            style={{
              ...tabStyle,
              background: activeTab === 'discovery' 
                ? "rgba(255, 255, 255, 0.95)" 
                : "rgba(255, 255, 255, 0.1)",
              color: activeTab === 'discovery' ? "#333" : "#ffffff",
              borderBottom: activeTab === 'discovery' ? "none" : "1px solid rgba(255, 255, 255, 0.2)"
            }}
          >
            🔍 Discovery
          </button>
          <button
            onClick={() => setActiveTab('removal')}
            style={{
              ...tabStyle,
              background: activeTab === 'removal' 
                ? "rgba(255, 255, 255, 0.95)" 
                : "rgba(255, 255, 255, 0.1)",
              color: activeTab === 'removal' ? "#333" : "#ffffff",
              borderBottom: activeTab === 'removal' ? "none" : "1px solid rgba(255, 255, 255, 0.2)"
            }}
          >
            🛡️ Removal {selectedBrokers.length > 0 && `(${selectedBrokers.length})`}
          </button>
        </div>

        <main style={{
          background: "rgba(255, 255, 255, 0.95)",
          borderRadius: "0 0 15px 15px",
          padding: "30px",
          color: "#333",
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.1)",
          minHeight: "600px"
        }}>
          {activeTab === 'discovery' && (
            <DiscoveryPanel 
              onProceedToRemoval={handleProceedToRemoval}
              job={discoveryJob}
              progress={discoveryProgress}
              findings={discoveryFindings}
              brokerCount={discoveryBrokerCount}
              onDiscoveryStateChange={{
                setJob: setDiscoveryJob,
                setProgress: setDiscoveryProgress,
                setFindings: setDiscoveryFindings,
                setBrokerCount: setDiscoveryBrokerCount
              }}
            />
          )}
          {activeTab === 'removal' && (
            <RemovalPanel 
              selectedBrokers={selectedBrokers}
              profileId={profileId}
              onBack={() => setActiveTab('discovery')}
            />
          )}
        </main>
      </div>
    </div>
  )
}
