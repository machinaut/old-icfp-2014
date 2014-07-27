/** @jsx React.DOM */
/* global React, Backbone, $ */

var ExampleModel = Backbone.Model.extend({
    initialize: function() {
        var self = this;
        var socket = io.connect('ws://localhost:8080');

        socket.on('init_response', function (data) {
            var moves = JSON.parse(data);
            socket.emit("get_board_state", { tick: moves[0] });
            self.set({
                moves: moves,
                selectedMove: moves[0]
            });
        });

        socket.on('frameResponse', function (data) {
            var moves = JSON.parse(data);
            console.log(moves.board);

            self.set({
                board: moves.board,
            });
        });
        
        // Hack for testing the board
        //var board = [];
        
        //_.each(_.range(80), function(y) {
        //    var row = [];
        //    _.each(_.range(80), function(x) {
        //        row.push(Math.floor((Math.random() * 10)));
        //    });
        //    board.push(row);
        //});

        //self.set({
        //    board: board
        //});
    },
});

var DisplayView = React.createClass({
    componentDidMount: function() {
        this.props.model.on('change', function() {
            this.forceUpdate();
            console.log("forcing update");
        }.bind(this));
    },
    getInitialState: function() {
        return {
        };
    },
    render: function() {
        var board = this.props.model.get('board');

        // If we aren't set to anything
        if (board === undefined) {
            board = [[]];
        }

        return (
            <div>
                <div className="boardGrid centered">
                    {board.map(function(row, y) {
                        var boardRow = "boardRow boardRow" + y;
                        return (
                            <div className={boardRow}>
                                {row.map(function(cell, x) {
                                    var boardCell = "boardCell boardCell" + y + "-" + x + " "; 
                                    
                                    switch (cell) {
                                        case 0: 
                                            boardCell += "wall ";
                                            break;
                                        case 2: 
                                            boardCell += "food ";
                                            break;
                                        case 3: 
                                            boardCell += "pill ";
                                            break;
                                        case 5: 
                                            boardCell += "lambda ";
                                            break;
                                        case 6: 
                                            boardCell += "ghost ";
                                            break;
                                    }

                                    return ( 
                                        <div className={boardCell}>
                                            {cell}
                                        </div>
                                    );
                                })}
                            </div>
                        );
                    })}
                </div>
                <h3>
                    Selected Move: {this.props.model.get('selectedMove')}
                </h3>
            </div>
        );
    }
});

var ToggleView = React.createClass({
    handleClick: function() {
        this.props.model.set('name', 'React');
    },
    render: function() {
        return (
            <div  className="centered">
                <button onClick={this.handleClick}
                        className="btn btn-default">
                    Does Nothing
                </button>
            </div>
        );
    }
});

var model = new ExampleModel();

React.renderComponent((
    <div className="centered reactContainer">
        <DisplayView model={model} />
        <ToggleView model={model} />
    </div>
), $("#maincontainer")[0]);