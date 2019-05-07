var game = new Vue({
    el: '#game',
    data:
    {
        page: 1,
        menuData: {
            menuNum: 1,
        },
        levelData: {
            level: 0,
            levelPage: 1,
            gameId: "",
        }
    },
    methods:
    {
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
        },
        hover()
        {
            this.playSound(2,0);
        },
        async newLevel(level)
        {
            this.levelData.level = level;
            pauseMusic();
            songSelection = 1;
            this.playSound(5,0);
            playMusic();
            
            let payload = {level: this.level};
            //let res = await axios.put('/wanderer/level', payload);
            //this.updateBoard(res.data);
        },
        async sendMove() {
            let payload = {key: "r"};
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
        deny()
        {
            this.playSound(3,0);
            console.log("Denied");
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

    },
    created()
    {
        console.log("script");
        //let res = axios.post('/wanderer/', payload);
    }
});