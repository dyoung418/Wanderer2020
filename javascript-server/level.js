const mongoose = require('mongoose');
const express = require("express");
const router = express.Router();
const auth = require("./auth.js");

const users = require("./users.js");
const User = users.model;

const levelSchema = new mongoose.Schema({
    user: {
      type: mongoose.Schema.ObjectId,
      ref: 'User'
    },

    grid: String,
    time: Number,
    level_num: Number,
    solution_count: Number,
    under_objects: [],
    cols: Number,
    title: String,
    rows: Number,
    solution: String,
    author: String,

    likes: Number,
    likedBy: [],

    official: Boolean,
    
    created: {
        type: Date,
        default: Date.now
    },
});
  
const Level = mongoose.model('Level', levelSchema);


router.post("/", auth.verifyToken, User.verify, async (req, res) => {
    const level = new Level({
      user: req.user,

      grid: req.body.grid,
      time: req.body.time,
      level_num: 0,
      solution_count: req.body.solution_count,
      under_objects: req.body.under_objects,
      cols: req.body.cols,
      title: req.body.title,
      rows: req.body.rows,
      solution: req.body.solution,
      author: req.body.username,
  
      likes: 0,
      likedBy: [],
  
      official: 0,

      created: {
          type: Date,
          default: Date.now
      },
    });
    try {
      await level.save();
      return res.sendStatus(200);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
});

router.get("/official/page/:num", async (req, res) => {
  try {
    let start = (req.param.num - 1) * 9;
    if (req.param.num == 1)
    {
      start = 0;
    }
    let end = start + 10;
    let levels = await Level.find({
        official: 1,
        level_num: { $gt: start, $lt: end}
    }).sort({
      level_num: 1
    });
    return res.send(levels);
  } catch (error) {
      console.log(error);
      return res.sendStatus(500);
  }
});

router.get("/official/:num", async (req, res) => {
    try {
        let level = await Level.findOne({
            official: 1,
            level_num: req.param.num
        });
        return res.send(level);
    } catch (error) {
        console.log(error);
        return res.sendStatus(500);
    }
});

router.get("/community/page/:num", async (req, res) => {
  try {
    let start = (req.param.num - 1) * 9;
    if (req.param.num == 1)
    {
      start = 0;
    }
    let end = start + 10;
    let levels = await Level.find({
        official: 0,
    }).sort({
      likes: -1
    });
    let sendLevels = [];
    for (var i = start + 1; i < end; i++)
    {
      sendLevels.push(levels[i]);
    }
    return res.send(sendLevels);
  } catch (error) {
      console.log(error);
      return res.sendStatus(500);
  }
});
  
router.get("/community/:id", async (req, res) => {
    try {
      let level = await Level.findOne({
        _id: req.params.id,
        official: 0,
      });
      return res.send(level);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
  });

  router.get("/all/liked", async (req, res) => {
    try {
        let levels = await Levels.find({
            official: 0
        }).sort({
            likes: -1
          });
      return res.send(levels);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
  });

  router.get("/all/newest", async (req, res) => {
    try {
        let levels = await Levels.find({
            official: 0
        }).sort({
            created: -1
          });
      return res.send(levels);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
  });

  router.post("/ajdsf0a8d7babdf8bj348q-qg=-ega0-u324j-g/post", async (req, res) => {
    const level = new Level({
      user: null,

      grid: req.body.grid,
      time: req.body.time,
      level_num: req.body.level_num,
      solution_count: req.body.solution_count,
      under_objects: req.body.under_objects,
      cols: req.body.cols,
      title: req.body.title,
      rows: req.body.rows,
      solution: req.body.solution,
      author: req.body.username,
  
      likes: 0,
      likedBy: [],
  
      official: 1,

      created: null,
    });
    try {
      await level.save();
      return res.sendStatus(200);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
});

  module.exports = {
    model: Level,
    routes: router,
  }