const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ProductStockSchema = new Schema({
  product_stock_id: { type: Schema.Types.ObjectId, required: true },
  product_id: { type: Schema.Types.ObjectId, ref: 'Product', required: true },
  shop_id: { type: Schema.Types.ObjectId, ref: 'Shop', required: true },
  quantity: { type: Number, required: true },
  last_updated: { type: Date, default: Date.now }
});

module.exports = {
    ProductStock: mongoose.model('ProductStock', ProductStockSchema)
};