// /models/index.js
const Sequelize = require('sequelize');
const config = require('../config/config.json');

// Inicializa Sequelize con la configuración de desarrollo
const sequelize = new Sequelize(config.development);

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

// Define las asociaciones entre los modelos
Object.keys(models).forEach((modelName) => {
  if (models[modelName].associate) {
    models[modelName].associate(models);
  }
});

models.sequelize = sequelize;
models.Sequelize = Sequelize;

module.exports = models;
