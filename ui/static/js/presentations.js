var React = require('react');
var ReactDOM = require('react-dom');

var Presentation = React.createClass({
  openDetailModal: function(e) {
    e.preventDefault();
  },

  render: function(){
    return (
      <div className="col-md-6 presentation">
        <div>
        <h2 className={"title"}>
          {this.props.presentation.name}
        </h2>
        <img
          className={"image img-circle img-responsive center-block"}
          src={this.props.presentation.thumbnail}
          alt="Loading the thumbnail"/>
        </div>
      </div>
    );
  }
});

var Presentations = React.createClass({
  render: function(){
    var chunk = this.props.chunkSize;
    var results2by2 = [];
    for (var i=0; i<this.props.results.length; i+=chunk) {
      var presentations = this.props.results.slice(i,i+chunk).map(
        function(presentation, index){
          return <Presentation  key={presentation.presentation_id}
                  presentation={presentation} />
      });
      results2by2.push(<div key={i + "root"}>
        <div key={i + "child"} className="row text-center">
          {presentations}
        </div>
        <hr/>
        </div>);
    }
    return (<div className="presentations">{results2by2}</div>)
  }
});

module.exports = {presentation: Presentation, presentations: Presentations};
