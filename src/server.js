const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();

app.use(express.json());
app.use(cors());


// ===== Temporary OTP Storage =====
let currentOTP = null;
let otpExpiry = null;

app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ===== Generate OTP (Called from Web Page) =====
app.get("/generate-otp", (req, res) => {

  currentOTP = Math.floor(1000 + Math.random() * 9000).toString();
  otpExpiry = Date.now() + (2 * 60 * 1000); // 2 minutes expiry

  console.log("OTP Generated:", currentOTP);

  res.json({
    otp: currentOTP,
    expiresIn: "2 minutes"
  });
});

// ===== Verify OTP (Called from ESP32) =====
app.post("/verify-otp", (req, res) => {

  const { otp } = req.body;

  if (!currentOTP) {
    return res.json({
      status: "fail",
      message: "No OTP generated"
    });
  }

  if (Date.now() > otpExpiry) {
    currentOTP = null;
    return res.json({
      status: "fail",
      message: "OTP expired"
    });
  }

  if (otp === currentOTP) {
    currentOTP = null; // delete after use
    return res.json({
      status: "success",
      message: "OTP correct"
    });
  }

  return res.json({
    status: "fail",
    message: "Incorrect OTP"
  });
});

module.exports = app;