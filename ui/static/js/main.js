var React = require('react');
var ReactDOM = require('react-dom');
var Loading = require('react-loading');
var rest = require('rest');
var mime = require('rest/interceptor/mime');
var vars = require('./vars');
var Presentations = require('./presentations').presentations;

var client = rest.wrap(mime);


var Main = React.createClass({
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
    var url = this.state.baseUrl + window.location.pathname + '/?format=json';
    console.log(url);
    this.load(url);
  },

  refresh: function(){
    window.location = '/';
  },

  render: function() {
    if (!this.state.response){
      console.log('no response');
      return <Loading type='balls' />
    }
    console.log(this.state.response);
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
          <Presentations results={this.state.response.entity}
                         chunkSize={2}/>
        </div>
      </div>
    );
  }
});

module.exports = Main;
