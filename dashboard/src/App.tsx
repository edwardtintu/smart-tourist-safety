import TouristTable from "./components/TouristTable";
import AlertsPanel from "./components/AlertsPanel";
import MapVisualization from "./components/MapView";

function App() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: "20px", padding: "20px" }}>
      {/* Sidebar */}
      <div>
        <TouristTable />
        <AlertsPanel />
      </div>

      {/* Map Area */}
      <div>
        <MapVisualization />
      </div>
    </div>
  );
}

export default App;
