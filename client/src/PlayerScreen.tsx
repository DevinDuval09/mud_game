
import HealthScreen from "./HealthScreen.tsx";
import EquipmentPanel from './EquipmentScreen.tsx';
import StatScreen from './StatScreen.tsx';
import InventoryList from './InventoryDiv.tsx';

function PlayerScreen(props)
{
    return(
        <div style={{display: "grid", gridTemplateColumns: "15% 35% 35% 15%"}}>
            <EquipmentPanel key={"PlayerEquip"} equipment={props.equipment} />
            <HealthScreen key={"PlayerHealth"}
                                maxHealth={props.maxHealth}
                                currentHealth={props.currentHealth} />
            <StatScreen key={"PlayerStats"} stats={props.stats} />
            <InventoryList key={"PlayerInventory"} inventory={props.inventory} />
        </div>
    );
}

export default PlayerScreen;