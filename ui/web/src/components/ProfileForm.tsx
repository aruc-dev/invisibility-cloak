import React from 'react'

type ProfileData = {
  label: string
  names: string[]
  emails: string[]
  phones: string[]
  addresses: Array<{
    street?: string
    city?: string
    state?: string
    zip?: string
    country?: string
  }>
  birth_dates: string[]
  ssn_last4: string[]
  usernames: string[]
  other_info: string[]
}

type ProfileFormProps = {
  onSave: (profile: ProfileData) => void
  onCancel: () => void
}

export default function ProfileForm({ onSave, onCancel }: ProfileFormProps) {
  const [formData, setFormData] = React.useState<ProfileData>({
    label: '',
    names: [''],
    emails: [''],
    phones: [''],
    addresses: [{ street: '', city: '', state: '', zip: '', country: '' }],
    birth_dates: [''],
    ssn_last4: [''],
    usernames: [''],
    other_info: ['']
  })

  const [errors, setErrors] = React.useState<string[]>([])

  const addField = (field: keyof ProfileData) => {
    setFormData(prev => ({
      ...prev,
      [field]: field === 'addresses' 
        ? [...prev[field], { street: '', city: '', state: '', zip: '', country: '' }]
        : [...(prev[field] as string[]), '']
    }))
  }

  const removeField = (field: keyof ProfileData, index: number) => {
    setFormData(prev => ({
      ...prev,
      [field]: (prev[field] as any[]).filter((_, i) => i !== index)
    }))
  }

  const updateField = (field: keyof ProfileData, index: number, value: string | object) => {
    setFormData(prev => ({
      ...prev,
      [field]: (prev[field] as any[]).map((item, i) => i === index ? value : item)
    }))
  }

  const updateAddress = (index: number, key: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      addresses: prev.addresses.map((addr, i) => 
        i === index ? { ...addr, [key]: value } : addr
      )
    }))
  }

  const validateForm = (): boolean => {
    const newErrors: string[] = []
    
    if (!formData.label.trim()) {
      newErrors.push('Profile label is required')
    }

    // Check if at least one field has data
    const hasData = [
      ...formData.names,
      ...formData.emails,
      ...formData.phones,
      ...formData.birth_dates,
      ...formData.ssn_last4,
      ...formData.usernames,
      ...formData.other_info,
      ...formData.addresses.flatMap(addr => Object.values(addr))
    ].some(value => value && value.toString().trim())

    if (!hasData) {
      newErrors.push('At least one field must be filled out')
    }

    setErrors(newErrors)
    return newErrors.length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return

    // Clean up empty fields
    const cleanedProfile: ProfileData = {
      ...formData,
      names: formData.names.filter(n => n.trim()),
      emails: formData.emails.filter(e => e.trim()),
      phones: formData.phones.filter(p => p.trim()),
      birth_dates: formData.birth_dates.filter(d => d.trim()),
      ssn_last4: formData.ssn_last4.filter(s => s.trim()),
      usernames: formData.usernames.filter(u => u.trim()),
      other_info: formData.other_info.filter(o => o.trim()),
      addresses: formData.addresses.filter(addr => 
        Object.values(addr).some(v => v && v.trim())
      ).map(addr => 
        Object.fromEntries(
          Object.entries(addr).filter(([_, v]) => v && v.trim())
        )
      )
    }

    onSave(cleanedProfile)
  }

  const inputStyle = {
    padding: "8px 12px",
    borderRadius: "6px",
    border: "2px solid #e2e8f0",
    fontSize: "14px",
    width: "100%",
    outline: "none",
    transition: "border-color 0.2s ease"
  }

  const buttonStyle = {
    padding: "8px 16px",
    borderRadius: "6px",
    border: "none",
    fontSize: "14px",
    fontWeight: "500",
    cursor: "pointer",
    transition: "all 0.2s ease"
  }

  const sectionStyle = {
    background: "white",
    borderRadius: "12px",
    padding: "20px",
    marginBottom: "16px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
    border: "1px solid #e2e8f0"
  }

  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: "rgba(0,0,0,0.5)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000,
      padding: "20px"
    }}>
      <div style={{
        background: "white",
        borderRadius: "16px",
        padding: "30px",
        maxWidth: "800px",
        width: "100%",
        maxHeight: "90vh",
        overflow: "auto",
        boxShadow: "0 20px 40px rgba(0,0,0,0.1)"
      }}>
        <h2 style={{
          color: "#2d3748",
          fontSize: "1.8rem",
          marginBottom: "20px",
          display: "flex",
          alignItems: "center",
          gap: "10px"
        }}>
          👤 Create New Profile
        </h2>

        {errors.length > 0 && (
          <div style={{
            background: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: "8px",
            padding: "12px",
            marginBottom: "20px"
          }}>
            {errors.map((error, i) => (
              <p key={i} style={{margin: 0, color: "#dc2626", fontSize: "14px"}}>
                ❌ {error}
              </p>
            ))}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Profile Label */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              📋 Profile Information
            </h3>
            <div style={{marginBottom: "16px"}}>
              <label style={{display: "block", marginBottom: "6px", fontWeight: "500", color: "#4a5568"}}>
                Profile Name *
              </label>
              <input
                type="text"
                value={formData.label}
                onChange={(e) => setFormData(prev => ({...prev, label: e.target.value}))}
                placeholder="e.g., My Personal Info, John Doe, Work Profile"
                style={inputStyle}
              />
            </div>
          </div>

          {/* Names */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              🏷️ Names & Aliases
            </h3>
            {formData.names.map((name, index) => (
              <div key={index} style={{display: "flex", gap: "8px", marginBottom: "12px"}}>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => updateField('names', index, e.target.value)}
                  placeholder="Full name, nickname, or alias"
                  style={{...inputStyle, flex: 1}}
                />
                {formData.names.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('names', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('names')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add Name
            </button>
          </div>

          {/* Emails */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              📧 Email Addresses
            </h3>
            {formData.emails.map((email, index) => (
              <div key={index} style={{display: "flex", gap: "8px", marginBottom: "12px"}}>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => updateField('emails', index, e.target.value)}
                  placeholder="email@example.com"
                  style={{...inputStyle, flex: 1}}
                />
                {formData.emails.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('emails', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('emails')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add Email
            </button>
          </div>

          {/* Phone Numbers */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              📱 Phone Numbers
            </h3>
            {formData.phones.map((phone, index) => (
              <div key={index} style={{display: "flex", gap: "8px", marginBottom: "12px"}}>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => updateField('phones', index, e.target.value)}
                  placeholder="(555) 123-4567"
                  style={{...inputStyle, flex: 1}}
                />
                {formData.phones.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('phones', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('phones')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add Phone
            </button>
          </div>

          {/* Addresses */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              🏠 Addresses
            </h3>
            {formData.addresses.map((address, index) => (
              <div key={index} style={{
                border: "1px solid #e2e8f0",
                borderRadius: "8px",
                padding: "16px",
                marginBottom: "16px",
                background: "#f9fafb"
              }}>
                <div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", marginBottom: "12px"}}>
                  <input
                    type="text"
                    value={address.street || ''}
                    onChange={(e) => updateAddress(index, 'street', e.target.value)}
                    placeholder="Street address"
                    style={inputStyle}
                  />
                  <input
                    type="text"
                    value={address.city || ''}
                    onChange={(e) => updateAddress(index, 'city', e.target.value)}
                    placeholder="City"
                    style={inputStyle}
                  />
                </div>
                <div style={{display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px", marginBottom: "12px"}}>
                  <input
                    type="text"
                    value={address.state || ''}
                    onChange={(e) => updateAddress(index, 'state', e.target.value)}
                    placeholder="State"
                    style={inputStyle}
                  />
                  <input
                    type="text"
                    value={address.zip || ''}
                    onChange={(e) => updateAddress(index, 'zip', e.target.value)}
                    placeholder="ZIP code"
                    style={inputStyle}
                  />
                  <input
                    type="text"
                    value={address.country || ''}
                    onChange={(e) => updateAddress(index, 'country', e.target.value)}
                    placeholder="Country"
                    style={inputStyle}
                  />
                </div>
                {formData.addresses.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('addresses', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌ Remove Address
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('addresses')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add Address
            </button>
          </div>

          {/* Birth Dates */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              🎂 Birth Dates
            </h3>
            {formData.birth_dates.map((date, index) => (
              <div key={index} style={{display: "flex", gap: "8px", marginBottom: "12px"}}>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => updateField('birth_dates', index, e.target.value)}
                  style={{...inputStyle, flex: 1}}
                />
                {formData.birth_dates.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('birth_dates', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('birth_dates')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add Birth Date
            </button>
          </div>

          {/* SSN Last 4 */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              🔢 SSN Last 4 Digits
            </h3>
            {formData.ssn_last4.map((ssn, index) => (
              <div key={index} style={{display: "flex", gap: "8px", marginBottom: "12px"}}>
                <input
                  type="text"
                  value={ssn}
                  onChange={(e) => updateField('ssn_last4', index, e.target.value)}
                  placeholder="1234"
                  maxLength={4}
                  pattern="[0-9]{4}"
                  style={{...inputStyle, flex: 1}}
                />
                {formData.ssn_last4.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('ssn_last4', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('ssn_last4')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add SSN Last 4
            </button>
          </div>

          {/* Usernames */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              👤 Usernames & Handles
            </h3>
            {formData.usernames.map((username, index) => (
              <div key={index} style={{display: "flex", gap: "8px", marginBottom: "12px"}}>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => updateField('usernames', index, e.target.value)}
                  placeholder="social media handle, forum username, etc."
                  style={{...inputStyle, flex: 1}}
                />
                {formData.usernames.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('usernames', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('usernames')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add Username
            </button>
          </div>

          {/* Other Info */}
          <div style={sectionStyle}>
            <h3 style={{color: "#4a5568", fontSize: "1.2rem", marginBottom: "15px"}}>
              📝 Other Information
            </h3>
            {formData.other_info.map((info, index) => (
              <div key={index} style={{display: "flex", gap: "8px", marginBottom: "12px"}}>
                <input
                  type="text"
                  value={info}
                  onChange={(e) => updateField('other_info', index, e.target.value)}
                  placeholder="license plate, company name, other identifiers"
                  style={{...inputStyle, flex: 1}}
                />
                {formData.other_info.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField('other_info', index)}
                    style={{...buttonStyle, background: "#ef4444", color: "white"}}
                  >
                    ❌
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField('other_info')}
              style={{...buttonStyle, background: "#10b981", color: "white"}}
            >
              ➕ Add Other Info
            </button>
          </div>

          {/* Action Buttons */}
          <div style={{
            display: "flex",
            gap: "12px",
            justifyContent: "flex-end",
            marginTop: "30px",
            paddingTop: "20px",
            borderTop: "1px solid #e2e8f0"
          }}>
            <button
              type="button"
              onClick={onCancel}
              style={{
                ...buttonStyle,
                background: "#6b7280",
                color: "white",
                padding: "12px 24px"
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              style={{
                ...buttonStyle,
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                color: "white",
                padding: "12px 24px",
                fontSize: "16px",
                fontWeight: "600"
              }}
            >
              💾 Save Profile
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}