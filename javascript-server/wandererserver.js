const express = require('express');
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: false
}));

const mongoose = require('mongoose');

// connect to the database
mongoose.connect('mongodb://localhost:27017/wanderer', {
  useNewUrlParser: true
});

const cookieParser = require("cookie-parser");
app.use(cookieParser());

const users = require("./users.js");
app.use("/api/users", users.routes);

const photos = require("./profile.js");
app.use("/api/profile", profile.routes);


const level = require("./level.js");
app.use("/api/level", level.routes);

app.listen(3005, () => console.log('Server listening on port 3001!'));