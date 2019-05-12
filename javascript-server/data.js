const axios = require("axios");

const fs = require('fs');

levels.forEach(async level => {
  try {
    fs.readFile(file, 'utf8', (err, fileContents) => {
        if (err) {
          console.error(err)
          return;
        }
        try {
          const data = JSON.parse(fileContents)
          let response = await axios.post("http://localhost:3000/api/wanderer/ajdsf0a8d7babdf8bj348q-qg=-ega0-u324j-g/post", data);
        } catch(err) {
          console.error(err);
        }
      })
    
  } catch (error) {
    console.log(error);
  }
});