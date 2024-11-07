module.exports = (sequelize, DataTypes) => {
    const Product = sequelize.define('Product', {
      category_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
          model: 'Categories',  // La tabla a la que hace referencia
          key: 'id'
        }
      },
      name: {
        type: DataTypes.STRING,
        allowNull: false
      },
      description: {
        type: DataTypes.STRING,
        allowNull: false
      },
      price: {
        type: DataTypes.DECIMAL(10, 2),  // Precio con 2 decimales
        allowNull: false
      }
    }, {
      tableName: 'products',  // nombre de la tabla en la base de datos
      timestamps: true         // Sequelize añadirá 'createdAt' y 'updatedAt'
    });
  
    Product.associate = (models) => {
      // Relación de un producto con una categoría
      Product.belongsTo(models.Category, {
        foreignKey: 'category_id', 
        as: 'category'
      });
    };
  
    return Product;
  };
  