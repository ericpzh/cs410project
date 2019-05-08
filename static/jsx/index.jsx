class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fish : "Start a search to view results",
      input : '',
      example: {
        "axios": "^0.18.0",
        "gh-pages": "^2.0.1",
        "node-sass": "^4.11.0",
        "prop-types": "^15.7.2",
        "react": "^16.8.3",
        "react-dom": "^16.8.3",
        "react-router-dom": "^4.3.1",
        "react-scripts": "2.1.5",
        "semantic-ui-css": "^2.4.1",
        "semantic-ui-react": "^0.85.0"
      },
      parsedList: [],
      loading: false,
    };
    this.becomeChicken = this.becomeChicken.bind(this);
    this.becomeChickenByTopic = this.becomeChickenByTopic.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleTab = this.handleTab.bind(this);
  }
  handleChange(e){
    this.setState({input: e.target.value});
    if (e.target.getAttribute("id")==="list") {
      this.setState({parsedList: Object.keys(JSON.parse(e.target.value))});
    }
    else {
        this.setState({parsedList: e.target.value.split(" ")});
    }
  }
  becomeChicken(){
    if (this.state.parsedList.length === 0){
      return;
    }
    var args = '?data='+this.state.parsedList;
    console.log(this.state.parsedList);
    this.setState({loading: true});
    fetch('https://metapypy.herokuapp.com/api/package'+args, {
      mode: 'cors',
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
      },
    })
    .then(res => res.json())
    .then(res => {
        console.log(res);
        let fish = res=="" ? "No relevant package found" : res;
        this.setState({fish: fish, loading: false});
        return res;
    })
    .catch(error => {
    });
  }
  becomeChickenByTopic(){
    if (this.state.parsedList.length === 0){
      return;
    }
    var args = '?data='+this.state.parsedList;
    this.setState({loading: true});
    fetch('https://metapypy.herokuapp.com/api/description'+args, {
      mode: 'cors',
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
            .then(res => res.json())
            .then(res => {
              console.log(res);
              let fish = res=="" ? "No relevant package found" : res;
              this.setState({fish: fish, loading: false});
              return res;
            })
            .catch(error => {
            });
  }
  handleTab(e){
    // reset contents
    this.setState({input: "", parsedList: [], fish: "Start a search to view results"});
    let tabmenu = document.querySelectorAll(".tabmenu");
    tabmenu.forEach(tab => {
      tab.classList.remove("active");
      if(tab.getAttribute("data-tab") === e.target.getAttribute("data-tab")){
        tab.classList.add("active");
      }
    });
    let tabs = document.querySelectorAll(".tab");
    tabs.forEach(tab => {
      tab.classList.remove("active");
      if(tab.getAttribute("data-tab") === e.target.getAttribute("data-tab")){
        tab.classList.add("active");
      }
    })
  }
  render() {
    let pkgList = this.state.parsedList.map(pkg => <li>{pkg}</li>);
    let result = this.state.loading ? (<div>
              <div className="ui active inverted dimmer">
                <div className="ui large text loader">Searching for similar packages...</div>
              </div>
              <br/>
              <br/>
              <br/>
              <br/>
    </div>): (typeof this.state.fish === "string" ? <p>{this.state.fish}</p>
            :(<ul className="list">
      {this.state.fish.map(word => {
        if (typeof word == "string"){
          return <li><a href={"https://www.npmjs.com/package/"+word}>{word}</a></li>
        }
        else {
          return <div style={{marginBottom: 5}}><li><a href={"https://www.npmjs.com/package/"+word.title}>{word.title}</a></li><p>{word.des}</p></div>
        }
      })}
    </ul>));
    return (
            <div className="ui container">
              <br/>
              <div className="ui raised very padded container">
                <div className="ui huge header">NPM Package Recommender</div>
                <div className="ui pointing secondary menu">
                  <a className="active item tabmenu" onClick={this.handleTab} data-tab="first">Search By Package List</a>
                  <a className="item tabmenu" onClick={this.handleTab} data-tab="second">Search By Keywords</a>                    </div>
                <div className="ui active tab segment" data-tab="first">
                  <div className="ui message">
                    <div className="header">
                      Find Similar Packages By Package List
                    </div>
                    <ul className="list">
                      <li>You can use your current package list in your package.json to find similar packages.</li>
                      <li>Copy the "dependencies" field in your package.json.</li>
                      <li>Example Input:</li>
                      <p>{JSON.stringify(this.state.example)}</p>
                    </ul>
                  </div>
                  <div className="ui divider"/>
                  <div className="ui action left icon input">
                    <i className="list icon"/>
                    <input type="text" id="list" onChange={this.handleChange} value={this.state.input} placeholder="Enter a Package List"/>
                    <button onClick={this.becomeChicken} className="ui icon button"><i className="search icon"/></button>
                  </div>
                  <div className="ui header">Parsed Package List:</div>
                  <ul className="list">
                    {pkgList}
                  </ul>
                </div>
                <div className="ui tab segment" data-tab="second">
                  <div className="ui message">
                    <div className="header">
                      Find Similar Packages By Keywords
                    </div>
                    <ul className="list">
                      <li>In this mode you can enter some keywords to find the most related packages, just like google search.</li>
                      <li>Enter some keywords below, separated by space</li>
                      <li>Example Input:</li>
                      <p>react visualization</p>
                    </ul>
                  </div>
                  <div className="ui divider"/>
                  <div className="ui action left icon input">
                    <i className="tags icon"/>
                    <input type="text" id="topic" onChange={this.handleChange} value={this.state.input} placeholder="Enter a Topic (List)"/>
                    <button onClick={this.becomeChickenByTopic} className="ui icon button">
                      <i className="search icon"/>
                    </button>
                  </div>
                  <div className="ui header">Parsed Keywords:</div>
                  <ul className="list">
                    {pkgList}
                  </ul>
                </div>
              <div>
                <br/>
                <div className="ui large header">Results</div>
                <div className="ui segment">
                {result}
                </div>
              </div>
                <br/>
                <br/>
                <br/>
                <br/>
                <br/>
              </div>
            </div>
    );
  }
}
ReactDOM.render(<App/>, document.getElementById('app'));
