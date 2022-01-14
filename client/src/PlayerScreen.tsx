
import HealthScreen from "./HealthScreen.tsx";
import EquipmentPanel from './EquipmentScreen.tsx';
import StatScreen from './StatScreen.tsx';
//add inventory

function PlayerScreen(props)
{
    return(
        <div style={{display: "grid", gridTemplateColumns: "25% 25% 25% 25%"}}>
            <EquipmentPanel key={"PlayerEquip"} equipment={props.equipment} />
            <HealthScreen key={"PlayerHealth"} maxHealth={props.maxHealth} currentHealth={props.currentHealth} />
            <StatScreen key={"PlayerStats"} stats={props.stats} />
        </div>
    );
}

export default PlayerScreen;