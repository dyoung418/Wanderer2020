// Request
let req = 
{
    playerMove: "",
}


//Response
let res = 
{
    updates: [ // List of Refreshed Screens
        [ // First screen
            {row: 0, col: 0, add: "", sub: ""}, // List of Individual Updates
            {row: 0, col: 0, add: "", sub: ""}
        ]
    ],
    score: 10,
}

// NEW LEVEL

// Request
let req = 
{
    level: Number,
}

// Response
let res = 
{
    gameId: String,
    level: [
        {row: 0, col: 0, add: ""}
        ]
}

/*


*/