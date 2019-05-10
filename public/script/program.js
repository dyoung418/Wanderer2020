var game = new Vue({ // Vue is used for the front end.
    el: '#game', // Selects item from DOM
    data:   // Collection of variables.
    {
        about: 0,
        page: 1,
        menuData: {
            menuNum: 1,
        },
        levelData: {
            level: 0,
            gameId: "",
            chests: 0,
            totalChests: 0,
            time: 0,
            score: 0,
            leveltitle: "",
            levelauthor: "",

            levelPage: 1,
        },
    },
    methods:
    {
        // GAME FUNCTIONS
        async newLevel(level)
        {
            this.levelData.level = level;
            pauseMusic();
            songSelection = 1;
            this.playSound(5,0);
            playMusic();

            this.levelData.title = LEVELS["level" + this.levelData.level].title;
            this.levelData.author = LEVELS["level" + this.levelData.level].author;

            let payload = 
            {
                level: this.level
            };
            let res = await axios.post('/wanderer/newlevel', payload);
            this.levelData.gameId = res.data.gameId;
            this.updateBoard(res.data);
        },
        async sendMove(key) {
            let payload = 
            {
                key: key,
                gameId: this.levelData.gameId,
            };
            let res = await axios.put('/wanderer/move', payload);
            this.updateBoard(res.data);
        },
        updateBoard(data)
        {
            for (var i = 0; i < data.updates.length; i++)
            {
                for (var j = 0; j < data.updates[i].length; j++)
                {
                    var id = this.getId(data.updates[i][j].row, data.updates[i][j].col);
                    var element = document.getElementById(id);
                    if (data.updates[i][j].add != "")
                    {
                        element.classList.add(data.updates[i][j].add);
                    }
                    if (data.updates[i][j].sub != "")
                    {
                        if (element.classList.contains(data.updates[i][j].sub))
                        {
                            element.classList.remove(data.updates[i][j].sub);
                        }
                    }
                }
            }
        },
        // MENU FUNCTIONS
        menuButton(page)
        {
            this.page = page;
            this.levelData.levelPage = 1;
            if (page == 1)
            {
                this.playSound(1,0);
            }
            else
            {
                this.playSound(0,0);
            }
            if (page == 3)
            {
                this.about = 0;
            }
        },
        aboutPages(page)
        {
            if (this.about != page)
            {
                this.about = page;
                this.levelData.levelPage = 1;
                this.playSound(0,0);
            }
            else
            {
                this.playSound(3,0);
            }
            
        },
        hover()
        {
            this.playSound(2,0);
        },
        getId(item)
        {
            let string = "";
            if (item.row < 10)
            {
                string += "0";
            }
            string += item.row;
            if (item.col < 10)
            {
                string += "0";
            }
            string += item.col;
            return string;
        },
        createItem(row, col)
        {
            let item = {row: row, col: col};
            return item;
        },

        levelPageToStart()
        {
            this.levelData.levelPage = 1;
            this.playSound(0,0);
            console.log("to start");
        },
        levelPagePrevious()
        {
            this.levelData.levelPage -= 1;
            this.playSound(0,0);
            console.log("to previous");
        },
        levelPageNext()
        {
            this.levelData.levelPage += 1;
            this.playSound(0,0);
            console.log("to next");
        },
        levelPageToEnd()
        {
            this.levelData.levelPage = 6;
            this.playSound(0,0);
            console.log("to end");
        },
        hoverLevel(id)
        {
            this.hover();
            var element = document.getElementById("level-title");
            element.innerHTML = LEVELS["level" + id].title;
            element.style.color = "rgba(255, 255, 255, 0.527)";
            element = document.getElementById("level-author");
            element.innerHTML = LEVELS["level" + id].author;
            element.style.color = "rgba(150, 150, 150,.4)";
        },
        unHoverLevel()
        {
            var element = document.getElementById("level-title");
            element.innerText = "Hover for Details";
            element.style.color = "rgba(255, 255, 255, 0)";
            element = document.getElementById("level-author");
            element.innerHTML = "EMPTY";
            element.style.color = "rgba(160, 160, 160,0)";
        },
        deny()
        {
            this.playSound(3,0);
            console.log("Denied");
        },
        levelmenu(button)
        {
            if (button == 0)
            {
                this.page = 1;
                this.menuData.menuNum = 1;
                this.levelData.levelPage = 1;
                this.playSound(1,0);
            }
            else if (button == 1)
            {
                this.page = 2;
                this.levelData.level = 0;
                this.levelData.levelPage = 1;
                this.menuData.menuNum = 1;
                this.playSound(0,0);
            }
            else if (button == 2)
            {
                this.page = 3;
                this.levelData.levelPage = 1;
                this.menuData.menuNum = 1;
                this.playSound(0,0);
                this.about = 0;
            }
            this.deleteData();
        },
        deleteData()
        {
            this.menuData = 1;
            this.levelData.level = 0;
            this.levelData.gameId = "";
            this.levelData.chests = 0;
            this.levelData.totalChests = 0;
            this.levelData.time = 0;
            this.levelData.score = 0;
            this.levelData.leveltitle = "";
            this.levelData.levelauthor = "";
        },
        playSound(sound, volume)
        {
            var media = document.getElementById(SOUNDS[sound].tag);
            if (volume == 0)
            {
                media.volume = SOUNDS[sound].volume;
                console.log(SOUNDS[sound].volume);
            }
            else
            {
                media.volume = volume;
            }
            const playPromise = media.play();
            if (playPromise !== null) 
                playPromise.catch(() => {media.play();})
        }
    },
    computed:
    {
        timeAvailable()
        {
            if (this.levelData.time >= 1)
            {
                return this.levelData.time;
            }
            else if (this.levelData.time == -1)
            {
                return "Unlimited";
            }
            else
            {
                return "Unsure";
            }
        },
        currentScore()
        {
            return this.levelData.score;
        },
        chestCollected()
        {
            var string = "";
            string += this.levelData.chests;
            string += " / ";
            string += this.levelData.totalChests;
            return string;
        }
    },
    created()
    {
    }
});