import React, { useState, useEffect } from 'react';

interface BrokerProfile {
  name: string;
  description: string;
  priority: number;
  estimated_time: string;
  broker_count: number;
  color: string;
  icon: string;
}

interface BrokerProfileSelectorProps {
  selectedProfile: string;
  onProfileSelect: (profileId: string) => void;
}

export const BrokerProfileSelector: React.FC<BrokerProfileSelectorProps> = ({
  selectedProfile,
  onProfileSelect
}) => {
  const [profiles, setProfiles] = useState<Record<string, BrokerProfile>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfiles = async () => {
      try {
        const response = await fetch('http://localhost:5179/broker-profiles');
        if (response.ok) {
          const data = await response.json();
          setProfiles(data);
        }
      } catch (error) {
        console.error('Failed to fetch broker profiles:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfiles();
  }, []);

  const getPriorityStars = (priority: number) => {
    return '⭐'.repeat(priority);
  };

  const getProfileOrder = () => {
    // Order profiles by priority (descending) and specific order
    const order = [
      'quick_scan',
      'people_search', 
      'financial_credit',
      'marketing_advertising',
      'healthcare_medical',
      'real_estate_property',
      'professional_b2b',
      'tech_data_analytics'
      // Removed 'all_brokers' from main list since it's too time-intensive
    ];
    
    return order.filter(key => profiles[key]);
  };

  if (loading) {
    return (
      <div style={{ padding: "20px", textAlign: "center" }}>
        <div>Loading broker profiles...</div>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      <div style={{ marginBottom: "24px" }}>
        <h3 style={{ 
          fontSize: "1.125rem", 
          fontWeight: "600", 
          marginBottom: "8px",
          color: "#1f2937"
        }}>
          Select Broker Profile
        </h3>
        <p style={{ 
          color: "#6b7280", 
          fontSize: "0.875rem",
          margin: "0"
        }}>
          Choose a targeted broker set for faster discovery. Start with Quick Scan for immediate results.
        </p>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        {getProfileOrder().map((profileId) => {
          const profile = profiles[profileId];
          const isSelected = selectedProfile === profileId;
          
          return (
            <div
              key={profileId}
              style={{
                padding: "16px",
                border: `2px solid ${isSelected ? '#3b82f6' : '#e5e7eb'}`,
                borderRadius: "8px",
                cursor: "pointer",
                transition: "all 0.2s ease",
                backgroundColor: isSelected ? '#eff6ff' : 'white',
                boxShadow: isSelected ? '0 4px 6px -1px rgba(0, 0, 0, 0.1)' : '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
              }}
              onClick={() => onProfileSelect(profileId)}
              onMouseOver={(e) => {
                if (!isSelected) {
                  e.currentTarget.style.borderColor = '#9ca3af';
                  e.currentTarget.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
                }
              }}
              onMouseOut={(e) => {
                if (!isSelected) {
                  e.currentTarget.style.borderColor = '#e5e7eb';
                  e.currentTarget.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
                }
              }}
            >
              <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
                <div style={{ display: "flex", alignItems: "flex-start", gap: "12px", flex: "1" }}>
                  <div style={{ fontSize: "2rem", flexShrink: "0" }}>
                    {profile.icon}
                  </div>
                  
                  <div style={{ flex: "1", minWidth: "0" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
                      <h4 style={{ 
                        fontWeight: "600", 
                        color: "#111827",
                        margin: "0",
                        fontSize: "1rem"
                      }}>
                        {profile.name}
                      </h4>
                      <span style={{ fontSize: "0.875rem" }} title={`Priority: ${profile.priority}/5`}>
                        {getPriorityStars(profile.priority)}
                      </span>
                    </div>
                    
                    <p style={{ 
                      fontSize: "0.875rem", 
                      color: "#6b7280", 
                      marginBottom: "8px",
                      margin: "0 0 8px 0",
                      lineHeight: "1.25"
                    }}>
                      {profile.description}
                    </p>
                    
                    <div style={{ 
                      display: "flex", 
                      flexWrap: "wrap", 
                      gap: "12px", 
                      fontSize: "0.75rem", 
                      color: "#6b7280"
                    }}>
                      <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                        <span>⏱️</span>
                        <span>{profile.estimated_time}</span>
                      </span>
                      <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                        <span>🎯</span>
                        <span>{profile.broker_count} brokers</span>
                      </span>
                    </div>
                  </div>
                </div>

                <div style={{ flexShrink: "0", marginLeft: "12px" }}>
                  <div style={{
                    width: "16px",
                    height: "16px",
                    borderRadius: "50%",
                    border: `2px solid ${isSelected ? '#3b82f6' : '#d1d5db'}`,
                    backgroundColor: isSelected ? '#3b82f6' : 'transparent',
                    transition: "all 0.2s ease",
                    position: "relative"
                  }}>
                    {isSelected && (
                      <div style={{
                        width: "6px",
                        height: "6px",
                        borderRadius: "50%",
                        backgroundColor: "white",
                        position: "absolute",
                        top: "50%",
                        left: "50%",
                        transform: "translate(-50%, -50%)"
                      }} />
                    )}
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              {profileId === 'quick_scan' && (
                <div style={{
                  marginTop: "8px",
                  fontSize: "0.75rem",
                  backgroundColor: "#dcfce7",
                  color: "#166534",
                  padding: "4px 8px",
                  borderRadius: "4px"
                }}>
                  ✅ Recommended for first-time users
                </div>
              )}
              {profile.priority === 5 && profileId !== 'quick_scan' && (
                <div style={{
                  marginTop: "8px",
                  fontSize: "0.75rem",
                  backgroundColor: "#fecaca",
                  color: "#991b1b",
                  padding: "4px 8px",
                  borderRadius: "4px"
                }}>
                  🔒 High privacy impact
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Profile Comparison */}
      <div style={{
        marginTop: "24px",
        padding: "16px",
        backgroundColor: "#f9fafb",
        borderRadius: "8px"
      }}>
        <h4 style={{ 
          fontWeight: "500", 
          color: "#111827", 
          marginBottom: "8px",
          fontSize: "1rem"
        }}>
          💡 Smart Discovery Tips
        </h4>
        <ul style={{ 
          fontSize: "0.875rem", 
          color: "#6b7280", 
          margin: "0",
          paddingLeft: "0",
          listStyle: "none"
        }}>
          <li style={{ marginBottom: "4px" }}>• <strong>Start with Quick Scan</strong> (15 min) for immediate results</li>
          <li style={{ marginBottom: "4px" }}>• <strong>People Search</strong> covers the most visible public exposure</li>
          <li style={{ marginBottom: "4px" }}>• <strong>Financial & Healthcare</strong> profiles have the highest privacy impact</li>
          <li>• Run <strong>multiple targeted profiles</strong> for better time management</li>
        </ul>
      </div>
    </div>
  );
};