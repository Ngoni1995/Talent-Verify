import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EmployeeList = () => {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    // Fetch employee data from Django backend
    axios.get('http://127.0.0.1:8000/api/employees/')
      .then((response) => {
        // Update the state with the fetched data
        setEmployees(response.data);
      })
      .catch((error) => {
        console.error('Error fetching employee data:', error);
      });
  }, []);

  return (
    <div>
      <h1>Employee List</h1>
      <ul>
        {employees.map((employee) => (
          <li key={employee.id}>
            {employee.name} - {employee.role} - {employee.department}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmployeeList;
