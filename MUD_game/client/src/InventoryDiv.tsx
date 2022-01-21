import React from "react";

function InventoryList(props)
{
    var inventory = props.inventory.map((item) =>
        <li>{item}</li>
    )

    return (
        <div>
            <ul>Inventory:
                <ul>
                    {inventory}
                </ul>

            </ul>
        </div>
    )
}

export default InventoryList;