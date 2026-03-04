const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(bodyParser.json());
app.use(cors());

let currentOTP = null;

const path = require("path");

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Base route
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Generate OTP
app.get("/generate-otp", (req, res) => {
  currentOTP = Math.floor(1000 + Math.random() * 9000).toString(); // 4-digit OTP
  console.log("OTP Generated:", currentOTP);
  res.json({ otp: currentOTP });
});

// Verify OTP
app.post("/verify-otp", (req, res) => {
  const { otp } = req.body;
  if (otp === currentOTP) {
    res.json({ status: "success", message: "OTP Correct" });
    currentOTP = null; // reset OTP
  } else {
    res.json({ status: "fail", message: "OTP Incorrect" });
  }
});

module.exports = app;
