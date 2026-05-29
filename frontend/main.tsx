import React from "react";
import ReactDOM from "react-dom";
import App from "./app";
// @ts-ignore: allow side-effect import of CSS in TSX
import "./styles.css";

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);