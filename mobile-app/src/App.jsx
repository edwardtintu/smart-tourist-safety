import { useState } from 'react';
import RegistrationForm from './components/RegistrationForm';
import Dashboard from './components/Dashboard';

function App() {
  const [digitalId, setDigitalId] = useState(null);

  if (!digitalId) {
    return <RegistrationForm onRegister={setDigitalId} />;
  }

  return <Dashboard digitalId={digitalId} />;
}

export default App;