import React, { useEffect } from 'react';
import axios from 'axios';

function HomePage() {
  useEffect(() => {
    axios.get('http://localhost:5000')
      .then(response => {
        console.log('Respuesta del servidor:', response.data);
      })
      .catch(error => {
        console.error('Error al conectar con el servidor:', error);
      });
  }, []);

  return (
    <div>
      <h1>Bienvenido al Sistema de Alquileres</h1>
    </div>
  );
}

export default HomePage;
