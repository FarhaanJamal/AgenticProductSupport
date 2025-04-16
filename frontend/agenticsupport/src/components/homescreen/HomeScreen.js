import React from "react";
import { CardContent, Button } from "@mui/material";
import './homecss.css';
import images from '../../assets/scripts.js';

export default function HomeScreen({ handleQRImageCapture }) {
  return (
    <CardContent className="main-card">
      <div class='home-alignment'>
      <div>
          <h2 className="top-title">Welcome, I'm</h2>
          <h1 className="top-title">Agent Quask</h1>
        </div>
        <img src={images.logo} alt="My Logo" />
        <div>
      <div class="home-buttons">
        <div>
          <input
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleQRImageCapture}
          className="hidden"
          style={{ display: "none" }}
          id="capture-button"
          />
          <label htmlFor="capture-button">
          <Button
            variant="contained"
                  class="home-individual-buttons"
                  onClick={() => document.getElementById('capture-button').click()}
            >
            Scan QR Code
            </Button>
          </label>
            </div>
            <p style={{marginTop:'-1.75rem', paddingLeft:'1rem', fontStyle:"italic", color:"#375932"}}>Check the product for the QR code</p>
        </div>
      </div>
      </div>
      <h3 class="footer">I am developed by Raghava and Farhaan</h3>
    </CardContent>
  );
}
