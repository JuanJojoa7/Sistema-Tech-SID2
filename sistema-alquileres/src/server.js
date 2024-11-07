const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();
require('./utils/db');

const app = express();
app.use(cors());
app.use(express.json()); // Para parsear el cuerpo de las solicitudes como JSON

// Ruta básica
app.get('/', (_req, res) => {
  res.send('Bienvenido al Sistema de Alquileres');
});

// Puerto del servidor
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});

// src/server.js
const express = require('express');
const { sequelize } = require('./models'); // Importa la conexión y modelos desde index.js

sequelize.sync({ alter: true })
  .then(() => {
    console.log('Conectado y sincronizado con la base de datos de PostgreSQL');
  })
  .catch((err) => {
    console.error('Error al sincronizar con la base de datos:', err);
  });

app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});


