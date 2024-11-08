// Cargar las variables de entorno desde el archivo .env
require('dotenv').config();

const mongoose = require('mongoose');

// Conectar a MongoDB usando las variables de entorno
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  ssl: true,  // Si tienes SSL habilitado
})
  .then(() => {
    console.log('Conectado correctamente a MongoDB');
  })
  .catch((error) => {
    console.error('Error al conectar a MongoDB:', error);
  });
