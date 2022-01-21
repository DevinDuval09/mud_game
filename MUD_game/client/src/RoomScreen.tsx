import React from "react";

function ListItems(props)
{
    return <li key={props.value} style={Object.assign({}, {style: props.alignment}, {listStyleType: "none"})}>{props.value}</li>
}

function RoomDescription(props)
{
    return (
        <div>
            <p>Room Description:</p>
            <p>
                {props.description}
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
        <div key={"RoomItems"}>
            <p>Items in Room</p>
            <ul key={"RoomItemList"}>{items}</ul>
        </div>
    )
}

function CharactersList(props)
{
    var chars = props.characters.map((character) =>
            <ListItems alignment={props.alignment} value={character} />
    );

    return (
        <div key={"RoomChars"}>
            <p>People in Room:</p>
            <ul key="RoomCharList">{chars}</ul>
        </div>
        );
    }

function RoomScreen(props)
{
    return(
        <div style={{display: "grid", gridTemplateColumns: "20% 60% 20%"}}>
            <ItemsList key={"RoomItems"} items={props.items} alignment={props.itemAlignment} />
            <RoomDescription key={"RoomDesc"} description={props.description} />
            <CharactersList key={"RoomChars"} characters={props.characters} alignment={props.charAlignment} />
        </div>
    )
}

export default RoomScreen;