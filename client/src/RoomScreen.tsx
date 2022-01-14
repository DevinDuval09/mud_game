import React from "react";

function ListItems(props)
{
    return <li style={Object.assign({}, {style: props.alignment}, {listStyleType: "none"})}>{props.value}</li>
}

function RoomDescription(props)
{
    return (
        <div>
            <p>Room Description:</p>
            <p>
                props.description
            </p>
        </div>
    )
}

function ItemsList(props)
{
    var items = props.items.map((item) =>
            <ListItems alignment={props.alignment} value={item} />
    );

    return (
        <div>
            <p>Items in Room</p>
            <ul>{items}</ul>
        </div>
    )
}

function CharactersList(props)
{
    var chars = props.characters.map((character) =>
            <ListItems alignment={props.alignment} value={character} />
    );

    return (
        <div>
            <p>People in Room:</p>
            <ul>{chars}</ul>
        </div>
        );
    }

function RoomScreen(props)
{
    console.log(props.items);
    console.log(props.characters);
    return(
        <div style={{display: "grid", gridTemplateColumns: "33% 33% 33%"}}>
            <ItemsList items={props.items} alignment={props.itemAlignment} />
            <RoomDescription description={props.description} />
            <CharactersList characters={props.characters} alignment={props.charAlignment} />
        </div>
    )
}

export default RoomScreen;