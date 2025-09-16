import React, { useEffect, useState } from "react";
import axios from "axios";

interface Tourist {
  name: string;
  digital_id: string;
  contact: string;
}

const TouristTable: React.FC = () => {
  const [tourists, setTourists] = useState<Tourist[]>([]);

  const fetchTourists = async () => {
    try {
      const res = await axios.get("http://<10.169.7.122>:5000/tourists");
      setTourists(res.data);
    } catch (err) {
      console.error("Error fetching tourists:", err);
    }
  };

  useEffect(() => {
    fetchTourists();
    const interval = setInterval(fetchTourists, 5000); // refresh every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>Tourist List</h2>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          border: "1px solid black",
        }}
      >
        <thead>
          <tr>
            <th style={{ border: "1px solid black", padding: "8px" }}>Name</th>
            <th style={{ border: "1px solid black", padding: "8px" }}>
              Digital ID
            </th>
            <th style={{ border: "1px solid black", padding: "8px" }}>
              Contact
            </th>
          </tr>
        </thead>
        <tbody>
          {tourists.map((t, index) => (
            <tr key={index}>
              <td style={{ border: "1px solid black", padding: "8px" }}>
                {t.name}
              </td>
              <td style={{ border: "1px solid black", padding: "8px" }}>
                {t.digital_id}
              </td>
              <td style={{ border: "1px solid black", padding: "8px" }}>
                {t.contact}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TouristTable;
