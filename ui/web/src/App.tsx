
import DiscoveryPanel from "./components/DiscoveryPanel"

export default function App(){
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
        <main style={{
          background: "rgba(255, 255, 255, 0.95)",
          borderRadius: "15px",
          padding: "30px",
          color: "#333",
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.1)"
        }}>
          <DiscoveryPanel />
        </main>
      </div>
    </div>
  )
}
