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

pgClient.connect().then(() => console.log('Conectado a PostgreSQL'));

// Conexión a MongoDB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => console.log('Conectado a MongoDB'))
  .catch(err => console.log('Error al conectar a MongoDB:', err));

module.exports = { pgClient, mongoose };
