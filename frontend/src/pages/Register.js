import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";
import "../App.css";

function Register() {

  const navigate = useNavigate();

  const [name,setName] = useState("");
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const registerUser = async () => {

    if(!name || !email || !password){
      alert("Please fill all fields");
      return;
    }

    try{

      const res = await api.post("/register",{
        name,
        email,
        password
      });

      alert(res.data.message);

      // redirect to login page
      navigate("/");

    }catch(err){

      if(err.response && err.response.status === 400){
        alert("User already exists with this email");
      }
      else{
        alert("Registration failed");
      }

    }

  };

  return (

    <div className="container">

      <h2>User Registration</h2>

      <input
        type="text"
        placeholder="Full Name"
        value={name}
        onChange={(e)=>setName(e.target.value)}
      />

      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e)=>setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e)=>setPassword(e.target.value)}
      />

      <button onClick={registerUser}>
        Register
      </button>

      <div className="link">
        Already registered?  
        <Link to="/"> Login here</Link>
      </div>

    </div>

  );

}

export default Register;