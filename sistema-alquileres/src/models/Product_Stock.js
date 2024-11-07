module.exports = (sequelize, DataTypes) => {
    const ProductStock = sequelize.define('ProductStock', {
      product_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
          model: 'Products',  // La tabla a la que hace referencia
          key: 'id'
        }
      },
      shop_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
          model: 'Shops',  // La tabla a la que hace referencia
          key: 'id'
        }
      },
      quantity: {
        type: DataTypes.INTEGER,
        allowNull: false
      },
      last_updated: {
        type: DataTypes.DATE,
        defaultValue: sequelize.NOW
      }
    }, {
      tableName: 'product_stocks',  // nombre de la tabla en la base de datos
      timestamps: false             // No se requiere 'createdAt' y 'updatedAt'
    });
  
    ProductStock.associate = (models) => {
      // Relación con Producto
      ProductStock.belongsTo(models.Product, {
        foreignKey: 'product_id',
        as: 'product'
      });
  
      // Relación con Tienda
      ProductStock.belongsTo(models.Shop, {
        foreignKey: 'shop_id',
        as: 'shop'
      });
    };
  
    return ProductStock;
  };
  