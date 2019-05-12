const mongoose = require('mongoose');
const express = require("express");
const router = express.Router();
const auth = require("./auth.js");

// Configure multer so that it will upload to '/public/images'

const users = require("./users.js");
const User = users.model;

const profileSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.ObjectId,
        ref: 'User'
    },
    username: String,

    level: Number,
    customLevels: Number,
    likes: Number,
    liked: [],
    medals: [],
    completion: [],

    picture: Number,

    created: {
        type: Date,
        default: Date.now
    },
});
  
const Profile = mongoose.model('Profile', profileSchema);


router.post("/", auth.verifyToken, User.verify, async (req, res) => {
    const profile = new Profile({
      user: req.user,
      username: req.body.username,

      level: 0.0,
      customLevels: 0,
      likes: 0,
      liked: [],
      medals: [],
      completion: [],
      
      picture: 0,
    });
    try {
      await profile.save();
      return res.sendStatus(200);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
});

router.get("/", auth.verifyToken, User.verify, async (req, res) => {
    try {
        let profile = await Profile.findOne({
            user: req.user
        });

        return res.send(profile);
    } catch (error) {
        console.log(error);
        return res.sendStatus(500);
    }
  });
  
router.get("/:username", async (req, res) => {
    try {
      let profile = await Profile.findOne({
        username: req.params.username
      });
      var count = 0;
      for (var i = 0; i < profile.completion.length; i++)
      {
          if (profile.completion[i])
          {
              count += 1;
          }
      }
      let adjustedProfile = {
          username: profile.username,
          level: profile.level,
          customLevels: profile.level,
          likes: profile.likes,
          medals: profile.medals,
          completion: count,
          picture: profile.picture
      };
      return res.send(adjustedProfile);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
  });

  router.get("/all", async (req, res) => {
    try {
        let profiles = await Profile.find({
        }).sort({
            likes: -1
          });
      return res.send(profiles);
    } catch (error) {
      console.log(error);
      return res.sendStatus(500);
    }
  });

  module.exports = {
    model: Profile,
    routes: router,
  }