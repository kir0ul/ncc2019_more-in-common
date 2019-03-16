import React, { Component } from 'react'

const API = 'https://hn.algolia.com/api/v1/search?query=';
const DEFAULT_QUERY = 'redux';



class TryJson extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          hits: [],
        };
      }

    componentDidMount(){
        fetch(API + DEFAULT_QUERY)
            .then(response => response.json())
            .then(data => this.setState({ hits: data.hits }));
    }
     
      render() {
        const { hits } = this.state;
    
        return (
          <ul>
              {hits.length}
            {hits.map(hit =>
              <li key={hit.objectID}>
                <a href={hit.url}>{hit.title}</a>
              </li>
            )}
          </ul>
        );
      }
}




export default TryJson;

