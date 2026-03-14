import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";
import "../App.css";

function Login(){

const navigate = useNavigate();

const [email,setEmail] = useState("");
const [password,setPassword] = useState("");

const loginUser = async () => {

try{

const res = await api.post("/login",{
email,
password
});

if(res.status === 200){
alert("Login successful");
navigate("/dashboard");
}

}catch(err){

alert("Invalid email or password");

}

};

return(

<div className="container">

<h2>Login</h2>

<input
type="email"
placeholder="Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
/>

<input
type="password"
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
/>

<button onClick={loginUser}>
Login
</button>

<div className="link">
<Link to="/register">Create Account</Link>
</div>

</div>

);

}

export default Login;