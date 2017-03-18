import React, { Component } from 'react';

export default class App extends Component {
    constructor(props) {
    super(props);

    this.state = {
      articles: []
    };
  }

  componentDidMount() {
    var that = this;
    fetch('/api/example/').then(function(response){
      return response.json();
    }).then(function(response_data) {
      if(response_data.success === true) {
        that.setState(response_data.data);
      }
    }).catch(function(err) {
      alert("Oh dear! An error occurred!")
    });
  }

  render() {
    const articles = this.state.articles.map((article) =>
      <li key={article.id}>
        {article.title}
      </li>
    );
    return <ul>{articles}</ul>
  }
}
