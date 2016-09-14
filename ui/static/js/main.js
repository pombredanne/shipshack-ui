var React = require('react');
var ReactDOM = require('react-dom');
var Loading = require('react-loading');
var rest = require('rest');
var mime = require('rest/interceptor/mime');
var vars = require('./vars');
var Presentations = require('./presentations').presentations;

var client = rest.wrap(mime);


var Contents = React.createClass({
  getInitialState: function(){
    return {
      response: null,
      baseUrl: vars.baseUrl}
  },

  load: function(url){
    client({path: url}).then(function(response) {
      window.scrollTo(0, 0);
      this.setState({response: response});
    }.bind(this));
  },

  componentWillMount: function(){
    var url = this.state.baseUrl + window.location.pathname.substr(4) + '/?format=json';
    console.log(url);
    this.load(url);
  },

  render: function() {
    if (!this.state.response){
      return <div><img src="/static/images/loading.gif"/></div>
    }
    return (<Presentations results={this.state.response.entity} chunkSize={2}/>);
  }
});

var Main = React.createClass({
  refresh: function(){
    window.location = '/app/';
  },

  render: function() {
    return (
      <div>
        <div className="home circle" onClick={this.refresh}>
          <div className="home-text glyphicon glyphicon-home"></div>
        </div>
        <div className="container-fluid">
          <div className="jumbotron">
            <div className="row">
              <div className="col-md-12">
                <h1>ShipShack</h1>
              </div>
            </div>
          </div>
        </div>
        <div className="container">
          <Contents />
        </div>
      </div>
    );
  }

});

module.exports = Main;
