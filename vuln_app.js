const express = require("express");
const child_process = require("child_process");
const app = express();
app.use(express.json());

app.get("/cmd", (req, res) => {
  child_process.exec("ls " + req.query.input); // OS Command Injection
  res.send("ok");
});

app.get("/xss", (req, res) => {
  document.write(req.query.q); // XSS sink
  res.send("ok");
});

app.get("/proto", (req, res) => {
  Object.assign({}, req.body); // Prototype Pollution
  res.send("ok");
});

app.get("/buffer", (req, res) => {
  Buffer.allocUnsafe(req.query.size); // Buffer Overflow
  res.send("ok");
});

app.get("/graphql", (req, res) => {
  execute_graphql(req.body.query); // GraphQL Injection
  res.send("ok");
});

app.get("/nosql", (req, res) => {
  db.collection.find({ $where: req.query.q }); // NoSQL Injection
  res.send("ok");
});

app.get("/eval", (req, res) => {
  eval(req.query.code); // Code Injection via eval
  new Function(req.query.code)(); // Code Injection
  res.send("ok");
});

app.get("/redirect", (req, res) => {
  res.redirect(req.query.next); // Unvalidated Redirect
});

app.get("/cookie", (req, res) => {
  res.cookie("session", "abc"); // Insecure Cookie
  res.send("ok");
});

console.log = null; // Logging Disabled
console.log("password=" + (process.env.PASS || "secret")); // Sensitive Log
