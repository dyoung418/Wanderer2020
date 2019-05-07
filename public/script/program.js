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
        async newLevel(level)
        {
            this.level = parseInt(level, 10);
            let payload = {level: this.level};
            let res = await axios.put('/wanderer/level', payload);
            this.updateBoard(res.data);
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