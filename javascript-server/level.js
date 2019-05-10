const mongoose = require('mongoose');
const express = require("express");
const router = express.Router();
const auth = require("./auth.js");

// Configure multer so that it will upload to '/public/images'

const users = require("./users.js");
const User = users.model;

const levelSchema = new mongoose.Schema({
    author: String,

    width: Number,
    height: Number,

    map: String,

    time: Number,
    title: String,
    solution:
    {
        score: Number,
        movecount: Number,
        moves: String,
    },

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
        author: req.body.username,

        width: req.body.width,
        height: req.body.height,
    
        map: req.body.map,
    
        time: req.body.time,
        title: req.body.title,
        solution:
        {
            score: req.body.solution.score,
            movecount: req.body.solution.movecount,
            moves: req.body.solution.moves,
        },
    
        likes: 0,
        likedBy: [],
    
        official: req.body.official,
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

router.get("/official/:num", async (req, res) => {
    try {
        let level = await Level.findOne({
            official: req.param.num
        });
        return res.send(level);
    } catch (error) {
        console.log(error);
        return res.sendStatus(500);
    }
  });
  
router.get("/custom/:id", async (req, res) => {
    try {
      let level = await Level.findOne({
        _id: req.params.id
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
        author: req.body.username,

        width: req.body.width,
        height: req.body.height,
    
        map: req.body.map,
    
        time: req.body.time,
        title: req.body.title,
        solution:
        {
            score: req.body.solution.score,
            movecount: req.body.solution.movecount,
            moves: req.body.solution.moves,
        },
    
        likes: 0,
        likedBy: [],
    
        official: req.body.official,
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

  module.exports = {
    model: profile,
    routes: router,
  }