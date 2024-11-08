// Cargar las variables de entorno desde el archivo .env
require('dotenv').config();

const Sequelize = require('sequelize');

// Inicializa Sequelize con las variables de entorno
const sequelize = new Sequelize({
  username: process.env.PG_USER,
  password: process.env.PG_PASSWORD,
  database: process.env.PG_DATABASE,
  host: process.env.PG_HOST,
  port: process.env.PG_PORT,
  dialect: 'postgres',
  ssl: process.env.PG_SSL === 'true',  // Asegurando que el valor booleano sea correcto
  dialectOptions: {
    ssl: process.env.PG_SSL === 'true' ? { rejectUnauthorized: false } : null
  }
});

// Importa los modelos
const models = {
  Company: require('./Company')(sequelize, Sequelize.DataTypes),
  Shop: require('./Shop')(sequelize, Sequelize.DataTypes),
  Operational_Shop: require('./Operational_Shop')(sequelize, Sequelize.DataTypes),
  Operational_Shop_Hours: require('./Operational_Shop_Hours')(sequelize, Sequelize.DataTypes),
  Operational_Shop_Media: require('./Operational_Shop_Media')(sequelize, Sequelize.DataTypes),
  City: require('./City')(sequelize, Sequelize.DataTypes),
  Country: require('./Country')(sequelize, Sequelize.DataTypes),
  Contact: require('./Contact')(sequelize, Sequelize.DataTypes),
  Contract: require('./Contract')(sequelize, Sequelize.DataTypes),
  Contract_Status: require('./Contract_Status')(sequelize, Sequelize.DataTypes),
  Currency: require('./Currency')(sequelize, Sequelize.DataTypes),
  Product: require('./Product')(sequelize, Sequelize.DataTypes),
  Product_Stock: require('./Product_Stock')(sequelize, Sequelize.DataTypes),
  Category: require('./Category')(sequelize, Sequelize.DataTypes),
};

// Sincroniza los modelos con la base de datos (esto crea las tablas si no existen)
sequelize.sync({ force: false }) // force: false no elimina las tablas existentes
  .then(() => {
    console.log('Tablas sincronizadas correctamente');
  })
  .catch((error) => {
    console.error('Error al sincronizar tablas:', error);
  });

// Define las asociaciones entre los modelos
Object.keys(models).forEach((modelName) => {
  if (models[modelName].associate) {
    models[modelName].associate(models);
  }
});

// Exporta los modelos y la conexión de Sequelize
models.sequelize = sequelize;
models.Sequelize = Sequelize;

module.exports = models;
