var path = require('path');
var webpack = require('webpack');

module.exports = {
  devtool: 'cheap-module-eval-source-map',
  entry: [
    './src'
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  module: {
    loaders: [{
      include: path.join(__dirname, 'src'),
      loader: "babel",
      presets: ['es2015', 'react', "stage-0"]
    }]
  }
};
