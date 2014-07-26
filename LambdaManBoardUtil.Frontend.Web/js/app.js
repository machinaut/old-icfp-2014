/** @jsx React.DOM */
/* global React, Backbone, $ */

var ExampleModel = Backbone.Model.extend({
    initialize: function() {
        var self = this;
        var socket = io.connect('ws://localhost:8080');
        socket.on('news', function (data) {
            //console.log(data);
            self.set({name: data});
            socket.emit('my other event', { my: 'data' });
        });
         
    },
});

var DisplayView = React.createClass({displayName: 'DisplayView',
    componentDidMount: function() {
        this.props.model.on('change', function() {
            this.forceUpdate();
        }.bind(this));
    },

    render: function() {
        return (
            React.DOM.p(null, 
                this.props.model.get('name')
            )
        );
    }
});

var ToggleView = React.createClass({displayName: 'ToggleView',
    handleClick: function() {
        this.props.model.set('name', 'React');
    },
    render: function() {
        return (
            React.DOM.button({onClick: this.handleClick}, 
                "model.set('name', 'React');"
            )
        );
    }
});

var model = new ExampleModel();

React.renderComponent((
    React.DOM.div(null, 
        DisplayView({model: model}), 
        ToggleView({model: model})
    )
), document.body);