// Day 06 Chat App — minimal Express static server
// Serves public/index.html on http://localhost:3000
// The HTML page calls the FastAPI backend at http://localhost:8000

const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, "public")));

app.listen(PORT, () => {
  console.log(`Frontend running at http://localhost:${PORT}`);
});
