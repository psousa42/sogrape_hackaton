const express = require('express');
const mongoose = require('mongoose');
const app = express();
const PORT = 3000; // or any port you prefer
const DB_URL = 'mongodb+srv://opc:L5xJt6oXMKrCRiBv@cluster0.0xb5fg2.mongodb.net/?retryWrites=true&w=majority';

mongoose.connect(DB_URL, { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

app.get('/data', async (req, res) => {
  // Fetch data from MongoDB
  try {
    const data = await YourMongoDBModel.find(); // Replace YourMongoDBModel with your Mongoose model
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});