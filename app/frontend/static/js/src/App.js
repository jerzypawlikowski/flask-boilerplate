'use strict';

import React, { Component } from 'react';

export default class App extends Component {
    constructor(props) {
    super(props);

    this.state = {
      articles: []
    };
  }

  componentDidMount() {
    fetch('/api/example/').then(
        response => response.json()
    ).then(responseData => {
      if(responseData.success === true) {
        this.setState(responseData.data);
      }
    }).catch(function(err) {
      alert('Oh dear! An error occurred!')
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
