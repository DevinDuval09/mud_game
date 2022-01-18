import React from 'react';

const MAX_SIZE = 40;

function getMaxSize()
{
    return MAX_SIZE;
}

class MainScreen extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = {history: props.history};
    }

    addToHistory(event)
    {
        var tempHistory = this.state.history;
        tempHistory.push(event.target.value);
        if (tempHistory >= getMaxSize())
        {
            tempHistory.pop();
        }
        this.setState({history: tempHistory})

    }

    render()
    {
        var reversedHist = this.state.history.reverse();
        var histList = reversedHist.map((item) =>
            <li>{item}</li>
        );
        return (
            <div>
                <ul>
                    {histList}
                </ul>
            </div>
        )
    }
}

export default MainScreen;