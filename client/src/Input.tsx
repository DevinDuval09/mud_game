import React from "react";

class UserInput extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = {inputValue: "", url: props.url, character: props.character};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    };

    handleChange(event)
    {
        this.setState({inputValue: event.target.value});
    }

    handleSubmit(event)
    {
        var command = this.state.inputValue;
        this.setState({inputValue: ""})
        var response = new XMLHttpRequest();
        var params = "character=" + this.state.character + "&command=" + command;
        response.open("POST", this.state.url, true);
        response.setRequestHeader("Content-type", "text/plain");
        response.send(params);
        console.log(params);
        event.preventDefault();

    };

    render(){
        return(
            <div>
                <form>
                    <input value={this.state.inputValue} onChange={evt=>this.handleChange(evt)}></input>
                    <button onClick={this.handleSubmit}>
                        Input Command
                    </button>
                </form>
            </div>
        )
    };
};

export default UserInput;