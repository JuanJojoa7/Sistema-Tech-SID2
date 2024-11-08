const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const CountrySchema = new Schema({
  country_id: { type: Schema.Types.ObjectId, required: true },
  name: { type: String, required: true },
  code: { type: String, required: true }
});

module.exports = {
    Country: mongoose.model('Country', CountrySchema)
};