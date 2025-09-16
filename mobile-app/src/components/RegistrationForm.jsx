import { useState } from 'react';
import axios from 'axios';

export default function RegistrationForm({ onRegister }) {
  const [name, setName] = useState('');
  const [idNumber, setIdNumber] = useState('');
  const [emergencyContact, setEmergencyContact] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post('http://10.169.7.122:5000/register', {
        name: name.trim(),
        idNumber: idNumber.trim(),
        emergencyContact: emergencyContact.trim()
      });
      onRegister(res.data.digitalId); // ✅ This is the ONLY place onRegister should be called
    } catch (err) {
      alert("Registration failed: " + err.message);
      console.error("Full error:", err);
    }
  };

  return (
    <div style={{ padding: '30px', maxWidth: '450px', margin: '50px auto' }}>
      <h2 style={{ textAlign: 'center' }}>:Register as Tourist</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <input placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input placeholder="ID (Passport/Aadhaar)" value={idNumber} onChange={(e) => setIdNumber(e.target.value)} required />
        <input placeholder="Emergency Contact" value={emergencyContact} onChange={(e) => setEmergencyContact(e.target.value)} required />
        <button type="submit" style={{ padding: '12px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
          Register
        </button>
      </form>
    </div>
  );
}