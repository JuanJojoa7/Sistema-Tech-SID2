const { Client } = require('pg');
const mongoose = require('mongoose');

// Conexión a PostgreSQL
const pgClient = new Client({
  user: process.env.PG_USER,
  host: process.env.PG_HOST,
  database: process.env.PG_DATABASE,
  password: process.env.PG_PASSWORD,
  port: process.env.PG_PORT,
  ssl: { rejectUnauthorized: false } // Agrega SSL para conexiones seguras
});

pgClient.connect()
  .then(() => {
    console.log('Conectado a PostgreSQL');
  })
  .catch(err => {
    console.error('Error al conectar a PostgreSQL:', err);
    process.exit(1);  // Sale del proceso si hay un error crítico
  });

// Conexión a MongoDB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => {
    console.log('Conectado a MongoDB');
  })
  .catch(err => {
    console.error('Error al conectar a MongoDB:', err);
    process.exit(1);  // Sale del proceso si hay un error crítico
  });

module.exports = { pgClient, mongoose };
