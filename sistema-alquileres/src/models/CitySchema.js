const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const CitySchema = new Schema({
  city_id: { type: Schema.Types.ObjectId, required: true },
  name: { type: String, required: true },
  country_id: { type: Schema.Types.ObjectId, ref: 'Country', required: true }
});

module.exports = {
    City: mongoose.model('City', CitySchema)
};