const path = require('path');
const webpack = require('webpack');
const express = require('express');
const config = require('./webpack.config');

const app = express();

app.get('*', function(req, res) {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(3000, function(err) {
  if (err) {
    return console.error(err);
  }

  console.log('Listening at http://localhost:3000/');
});