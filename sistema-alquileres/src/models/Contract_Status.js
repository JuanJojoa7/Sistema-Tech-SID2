module.exports = (sequelize, DataTypes) => {
    const ContractStatus = sequelize.define('ContractStatus', {
      contract_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
          model: 'Contracts',  // La tabla a la que hace referencia
          key: 'id'
        }
      },
      status: {
        type: DataTypes.STRING,
        allowNull: false
      },
      updated_at: {
        type: DataTypes.DATE,
        defaultValue: sequelize.NOW
      }
    }, {
      tableName: 'contract_statuses',  // nombre de la tabla en la base de datos
      timestamps: false                // No se requiere 'createdAt' y 'updatedAt'
    });
  
    ContractStatus.associate = (models) => {
      // Relación con Contrato
      ContractStatus.belongsTo(models.Contract, {
        foreignKey: 'contract_id',
        as: 'contract'
      });
    };
  
    return ContractStatus;
  };
  