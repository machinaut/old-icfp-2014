/** @jsx React.DOM */
/* global React, Backbone, $ */

var ExampleModel = Backbone.Model.extend({
    initialize: function() {
        var self = this;
        var socket = io.connect('ws://localhost:8080');
        socket.on('init_response', function (data) {
            //console.log(data);
            self.set({name: data});
            //socket.emit('my other event', { my: 'data' });
        });
         
    },
});

var DisplayView = React.createClass({
    componentDidMount: function() {
        this.props.model.on('change', function() {
            this.forceUpdate();
        }.bind(this));
    },

    render: function() {
        return (
            <p>
                {this.props.model.get('name')}
            </p>
        );
    }
});

var ToggleView = React.createClass({
    handleClick: function() {
        this.props.model.set('name', 'React');
    },
    render: function() {
        return (
            <button onClick={this.handleClick}>
                model.set('name', 'React');
            </button>
        );
    }
});

var model = new ExampleModel();

React.renderComponent((
    <div>
        <DisplayView model={model} />
        <ToggleView model={model} />
    </div>
), document.body);