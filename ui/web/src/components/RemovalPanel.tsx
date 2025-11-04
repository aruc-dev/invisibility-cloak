
import React from 'react'

type RemovalJob = {
  job_id: string
  status: string
  profile_id: string
  broker_ids: number[]
  progress: number
  items: RemovalItem[]
  created_at: string
}

type RemovalItem = {
  broker_name: string
  broker_id: number
  method: string
  status: string
  transcript: string
  evidence_path?: string
}

type RemovalPanelProps = {
  selectedBrokers: number[]
  profileId: string
  onBack: () => void
}

export default function RemovalPanel({ selectedBrokers, profileId, onBack }: RemovalPanelProps) {
  const [currentJob, setCurrentJob] = React.useState<RemovalJob | null>(null)
  const [pastJobs, setPastJobs] = React.useState<RemovalJob[]>([])
  const [isStarting, setIsStarting] = React.useState(false)

  React.useEffect(() => {
    loadPastJobs()
  }, [])

  React.useEffect(() => {
    if (currentJob && (currentJob.status === "running" || currentJob.status === "queued")) {
      const interval = setInterval(() => {
        fetchJobStatus(currentJob.job_id)
      }, 2000)
      return () => clearInterval(interval)
    }
  }, [currentJob])

  const loadPastJobs = async () => {
    try {
      const response = await fetch('http://localhost:5179/removals')
      const jobs = await response.json()
      const jobList = Object.entries(jobs).map(([id, job]: [string, any]) => ({
        job_id: id,
        ...job
      }))
      setPastJobs(jobList.sort((a, b) => parseFloat(b.created_at) - parseFloat(a.created_at)))
    } catch (error) {
      console.error('Failed to load past jobs:', error)
    }
  }

  const fetchJobStatus = async (jobId: string) => {
    try {
      const response = await fetch(`http://localhost:5179/removals/${jobId}`)
      const job = await response.json()
      setCurrentJob({ job_id: jobId, ...job })
      
      if (job.status === "completed" || job.status === "error") {
        loadPastJobs()
      }
    } catch (error) {
      console.error('Failed to fetch job status:', error)
    }
  }

  const startRemoval = async () => {
    if (!profileId || selectedBrokers.length === 0) return

    setIsStarting(true)
    try {
      const response = await fetch('http://localhost:5179/removals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          profile_id: profileId,
          brokers: selectedBrokers
        })
      })

      if (response.ok) {
        const result = await response.json()
        setCurrentJob({ 
          job_id: result.job_id, 
          status: 'queued', 
          profile_id: profileId,
          broker_ids: selectedBrokers,
          progress: 0,
          items: [],
          created_at: String(Date.now() / 1000)
        })
      } else {
        alert('Failed to start removal process')
      }
    } catch (error) {
      console.error('Error starting removal:', error)
      alert('Error starting removal process')
    } finally {
      setIsStarting(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return '#10b981'
      case 'running': return '#3b82f6'
      case 'queued': return '#f59e0b'
      case 'error': return '#ef4444'
      case 'cancelled': return '#6b7280'
      case 'drafted': return '#8b5cf6'
      case 'submitted': return '#06b6d4'
      case 'manual_required': return '#f97316'
      default: return '#6b7280'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅'
      case 'running': return '⏳'
      case 'queued': return '⏸️'
      case 'error': return '❌'
      case 'cancelled': return '⛔'
      case 'drafted': return '📧'
      case 'submitted': return '🚀'
      case 'manual_required': return '👤'
      default: return '❓'
    }
  }

  const buttonStyle = {
    padding: "12px 24px",
    borderRadius: "8px",
    border: "none",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "all 0.3s ease",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
  }

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: "15px", marginBottom: "30px" }}>
        <button
          onClick={onBack}
          style={{
            ...buttonStyle,
            background: "linear-gradient(135deg, #6b7280 0%, #4b5563 100%)",
            color: "white",
            padding: "10px 20px",
            fontSize: "14px"
          }}
        >
          ← Back to Discovery
        </button>
        <h3 style={{
          color: "#2d3748",
          fontSize: "1.5rem",
          margin: 0,
          display: "flex",
          alignItems: "center",
          gap: "10px"
        }}>
          🛡️ Data Removal Center
        </h3>
      </div>

      {/* Current Removal Job */}
      {selectedBrokers.length > 0 && !currentJob && (
        <div style={{
          background: "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)",
          borderRadius: "12px",
          padding: "25px",
          marginBottom: "25px",
          border: "1px solid #bae6fd"
        }}>
          <h4 style={{
            color: "#0369a1",
            fontSize: "1.2rem",
            marginBottom: "15px",
            display: "flex",
            alignItems: "center",
            gap: "8px"
          }}>
            🎯 Ready to Start Removal
          </h4>
          <p style={{ marginBottom: "20px", color: "#0369a1" }}>
            {selectedBrokers.length} broker(s) selected for data removal. This process will:
          </p>
          <ul style={{ marginBottom: "20px", color: "#0369a1", paddingLeft: "20px" }}>
            <li>🤖 Generate AI-powered opt-out emails where applicable</li>
            <li>📝 Attempt automated form submissions for available opt-out forms</li>
            <li>📋 Create manual instructions for complex cases</li>
            <li>📊 Track progress and provide detailed results</li>
          </ul>
          <button
            onClick={startRemoval}
            disabled={isStarting}
            style={{
              ...buttonStyle,
              background: isStarting ? "#94a3b8" : "linear-gradient(135deg, #10b981 0%, #059669 100%)",
              color: "white",
              opacity: isStarting ? 0.6 : 1
            }}
          >
            {isStarting ? "⏳ Starting..." : "🚀 Start Removal Process"}
          </button>
        </div>
      )}

      {/* Active Job Progress */}
      {currentJob && (
        <div style={{
          background: "white",
          borderRadius: "12px",
          padding: "25px",
          marginBottom: "25px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.05)",
          border: "1px solid #e2e8f0"
        }}>
          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px"
          }}>
            <h4 style={{
              color: "#2d3748",
              fontSize: "1.2rem",
              margin: 0,
              display: "flex",
              alignItems: "center",
              gap: "8px"
            }}>
              {getStatusIcon(currentJob.status)} Current Removal Job
            </h4>
            <span style={{
              padding: "6px 12px",
              borderRadius: "20px",
              fontSize: "14px",
              fontWeight: "600",
              background: getStatusColor(currentJob.status),
              color: "white"
            }}>
              {currentJob.status.toUpperCase()}
            </span>
          </div>

          {/* Progress Bar */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "8px"
            }}>
              <span style={{ fontSize: "14px", fontWeight: "600", color: "#4a5568" }}>
                Progress: {currentJob.progress}%
              </span>
              <span style={{ fontSize: "14px", color: "#6b7280" }}>
                {currentJob.items.length} / {currentJob.broker_ids.length} brokers processed
              </span>
            </div>
            <div style={{
              width: "100%",
              height: "8px",
              background: "#e2e8f0",
              borderRadius: "4px",
              overflow: "hidden"
            }}>
              <div style={{
                width: `${currentJob.progress}%`,
                height: "100%",
                background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                borderRadius: "4px",
                transition: "width 0.3s ease"
              }} />
            </div>
          </div>

          {/* Results */}
          {currentJob.items.length > 0 && (
            <div>
              <h5 style={{ marginBottom: "15px", color: "#4a5568" }}>Results:</h5>
              <div style={{ maxHeight: "300px", overflowY: "auto" }}>
                {currentJob.items.map((item, index) => (
                  <div key={index} style={{
                    background: "#f8fafc",
                    borderRadius: "8px",
                    padding: "15px",
                    marginBottom: "10px",
                    border: "1px solid #e2e8f0"
                  }}>
                    <div style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      marginBottom: "8px"
                    }}>
                      <strong style={{ color: "#2d3748" }}>{item.broker_name}</strong>
                      <span style={{
                        padding: "3px 8px",
                        borderRadius: "12px",
                        fontSize: "12px",
                        fontWeight: "600",
                        background: getStatusColor(item.status),
                        color: "white"
                      }}>
                        {getStatusIcon(item.status)} {item.status.replace('_', ' ').toUpperCase()}
                      </span>
                    </div>
                    <p style={{
                      margin: "0 0 8px 0",
                      fontSize: "14px",
                      color: "#6b7280"
                    }}>
                      Method: {item.method.toUpperCase()}
                    </p>
                    <p style={{
                      margin: 0,
                      fontSize: "14px",
                      color: "#4a5568"
                    }}>
                      {item.transcript}
                    </p>
                    {item.evidence_path && (
                      <p style={{
                        margin: "8px 0 0 0",
                        fontSize: "12px",
                        color: "#059669",
                        fontWeight: "500"
                      }}>
                        📄 Evidence: {item.evidence_path}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Past Jobs */}
      {pastJobs.length > 0 && (
        <div style={{
          background: "white",
          borderRadius: "12px",
          padding: "25px",
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.05)",
          border: "1px solid #e2e8f0"
        }}>
          <h4 style={{
            color: "#2d3748",
            fontSize: "1.2rem",
            marginBottom: "20px",
            display: "flex",
            alignItems: "center",
            gap: "8px"
          }}>
            📋 Removal History
          </h4>
          <div style={{ maxHeight: "400px", overflowY: "auto" }}>
            {pastJobs.map((job) => (
              <div key={job.job_id} style={{
                background: "#f8fafc",
                borderRadius: "8px",
                padding: "15px",
                marginBottom: "15px",
                border: "1px solid #e2e8f0"
              }}>
                <div style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "10px"
                }}>
                  <span style={{
                    fontSize: "14px",
                    fontWeight: "600",
                    color: "#2d3748"
                  }}>
                    {new Date(parseFloat(job.created_at) * 1000).toLocaleString()}
                  </span>
                  <span style={{
                    padding: "3px 8px",
                    borderRadius: "12px",
                    fontSize: "12px",
                    fontWeight: "600",
                    background: getStatusColor(job.status),
                    color: "white"
                  }}>
                    {getStatusIcon(job.status)} {job.status.toUpperCase()}
                  </span>
                </div>
                <p style={{
                  margin: 0,
                  fontSize: "14px",
                  color: "#6b7280"
                }}>
                  {job.broker_ids.length} brokers • {job.items.length} processed • {job.progress}% complete
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {selectedBrokers.length === 0 && !currentJob && pastJobs.length === 0 && (
        <div style={{
          textAlign: "center",
          padding: "60px 20px",
          color: "#6b7280",
          fontSize: "16px"
        }}>
          <div style={{ fontSize: "48px", marginBottom: "20px" }}>🛡️</div>
          <h4 style={{ color: "#4a5568", marginBottom: "10px" }}>No Removal Jobs Yet</h4>
          <p>Use the Discovery panel to find your data, then proceed to removal.</p>
        </div>
      )}
    </div>
  )
}
