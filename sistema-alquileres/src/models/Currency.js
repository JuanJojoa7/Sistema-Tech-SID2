module.exports = (sequelize, DataTypes) => {
    const Currency = sequelize.define('Currency', {
      name: {
        type: DataTypes.STRING,
        allowNull: false
      },
      code: {
        type: DataTypes.STRING,
        allowNull: false
      },
      symbol: {
        type: DataTypes.STRING,
        allowNull: false
      }
    }, {
      tableName: 'currencies',  // nombre de la tabla en la base de datos
      timestamps: false         // si no quieres que Sequelize agregue 'createdAt' y 'updatedAt'
    });
  
    return Currency;
  };
  