import api from "../api";
import "../App.css";

function Dashboard(){

const addFingerprint = async () => {

try{

const res = await api.post("/add-fingerprint",{
user_id: 1,
fingerprint_id: Math.floor(Math.random()*1000)
});

alert(res.data.message);

}catch(err){
alert("Failed to add fingerprint");
}

};

const deleteFingerprint = async () => {

try{

const res = await api.post("/remove-fingerprint",{
fingerprint_id: 1
});

alert(res.data.message);

}catch(err){
alert("Failed to delete fingerprint");
}

};

return(

<div className="container">

<h2>Smart Door Lock Dashboard</h2>

<button onClick={addFingerprint}>
Add Fingerprint
</button>

<br/><br/>

<button onClick={deleteFingerprint}>
Delete Fingerprint
</button>

</div>

);

}

export default Dashboard;