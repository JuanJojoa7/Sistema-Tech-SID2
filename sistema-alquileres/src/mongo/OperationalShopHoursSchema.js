const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const OperationalShopHoursSchema = new Schema({
  operational_shop_hours_id: { type: Schema.Types.ObjectId, required: true },
  operational_shop_id: { type: Schema.Types.ObjectId, ref: 'OperationalShop', required: true },
  day_of_week: { type: Number, required: true },
  open_time: { type: String, required: true },
  close_time: { type: String, required: true }
});

module.exports = {
    OperationalShopHours: mongoose.model('OperationalShopHours', OperationalShopHoursSchema)
};