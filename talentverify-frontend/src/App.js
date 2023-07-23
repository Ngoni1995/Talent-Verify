import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/employees/')
      .then((response) => setEmployees(response.data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      <h1>Employee List</h1>
      <ul>
      {employees.map((employee) => (
  <li key={employee.id}>
    ID: {employee.id}<br />
    Name: {employee.name}<br />
    Employee ID: {employee.employee_id}<br />
    Department: {employee.department}<br />
    Role: {employee.role}<br />
    Date Started: {employee.date_started}<br />
    Date Left: {employee.date_left}<br />
    Duties: {employee.duties}<br />
  </li>
))}

      </ul>
    </div>
  );
}

export default App;
