var React = require('react');
var ReactDOM = require('react-dom');

var Image = React.createClass({
  render: function(){
    return (
      <div className="col-md-6 presentation">
        <div>
        <h2 className={"title"}>
          {this.props.image.name}
        </h2>
        <div>
          <ul className="list-inline">
            <li>
              <a href={this.props.image.source}>source</a>
            </li>
            <li>
              <a href={this.props.image.url}>original</a>
            </li>
          </ul>
        </div>
        <img
          className={"image img-circle img-responsive center-block"}
          src={this.props.image.thumbnail}
          alt="Loading the thumbnail"/>
        </div>
      </div>
    );
  }
});

var Directory = React.createClass({
  render: function(){
    return (
      <div className="col-md-6 presentation">
        <div>
        <h2 className={"title"}>
          <a href={"/app/" + this.props.directory.name}>
            {this.props.directory.name}
          </a>
        </h2>
        </div>
      </div>
    );
  }
});

var Presentation = React.createClass({
  render: function(){
    if (this.props.presentation.is_directory){
      return <Directory directory={this.props.presentation}/>
    }
    return <Image image={this.props.presentation}/>
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
