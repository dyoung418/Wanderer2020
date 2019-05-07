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
        hoverLevel(id)
        {
            this.hover();
            var element = document.getElementById(id);
            var levelName = "";
            switch (id)
            {
                case "lev1":
                levelName = "Unplug the Cistern #1";
                break;
                case "lev2":
                levelName = "Unplug the Cistern #2";
                break;
                case "lev3":
                levelName = "My favorite one of the lot - Steve";
                break;
                case "lev4":
                levelName = "Hanging by a thread";
                break;
                case "lev6":
                levelName = "Yet another Beckett screen";
                break;
                case "lev10":
                levelName = "Meet the Baby Monsters!";
                break;
                case "lev11":
                levelName = "play@nl.cwi is responsible for this mess";
                break;
                case "lev12":
                levelName = "Get a load of this one then";
                break;
                case "lev13":
                levelName = "Return of the Dutch designer";
                break;
                case "lev14":
                levelName = "Is there no stopping these Dutchmen?  They'll be flying next";
                break;
                case "lev15":
                levelName = "The Aussies start to move in";
                break;
                case "lev16":
                levelName = "All but the one";
                break;
                case "lev18":
                levelName = "And another offering from Oz";
                break;
                case "lev19":
                levelName = "More from the Netherlands";
                break;
                case "lev20":
                levelName = "and still more (but this is the last of his)";
                break;
                case "lev21":
                levelName = "Max moves in Under:S,40,16,0,1 Under:S,40,16,0,1 Under:S,40,16,0,1 Under:S,40,16,0,1 Under:S,40,16,0,1";
                break;
                case "lev22":
                levelName = "and then moves out again";
                break;
                case "lev23":
                levelName = "Introducing THE BALLOONS!";
                break;
                case "lev24":
                levelName = "The Shrine of Quetzacoatl";
                break;
                case "lev26":
                levelName = "Revitalization of the Dutch";
                break;

                case "lev27":
                levelName = "Revived from the dead";
                break;
                case "lev29":
                levelName = "Kenton's swan song";
                break;
                case "lev30":
                levelName = "Who's is it?";
                break;
                case "lev31":
                levelName = "Alan Bland did this and the Amiga port";
                break;
                case "lev34":
                levelName = "Cause and Effect";
                break;
                case "lev26":
                levelName = "The Combination Lock";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;
                case "lev26":
                levelName = "";
                break;

                
                default:
                levelName = "Unnamed";
                break;
            }
            element.innerHTML = levelName;
        },
        unHoverLevel(id)
        {
            var element = document.getElementById(id);
            element.innerText = id.substring(3, id.length);
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