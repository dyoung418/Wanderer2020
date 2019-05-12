// Request
let req = 
{
    playerMove: "",
    gameId: "",
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


=======
>>>>>>> 6e00ed3d12cf725d40b48fbed157a7d1fc608fce
*/
let LEVEL_JSON =
{
    width: 40,
    height: 17,
    author: "Steven Shipway",
    map: "=======================\OOO*OOOO/#OO####*O       O:#         O/ \OOOOOO/# ::A**## O #### #:#       **/   \OOOO/   ####### #  O  *#:#              \OO/   ##    -# #* * ###:# OOO           O/    ##    -# ######:::#*****         :/  *###* O  -#    #*                 @     *<*###*< -#*#! ###                  \   *###*    -###              !     ::  \     ##    -# #          \ /=O=   ::::   \O     / O/#*           O O  =    ::   / \*   / */-###         #***# =        /   \    O/ -X < !!!     #\*/# =       /    O*O*O*O ->*   *   *<  # #  =      /     =**O*O= -    !!!   ! !# #! =! \    /    =:O*O:= -          ! *#T#*:::::\**/     =::::::*-########################################",
    time: 1000,
    title: "Unplug the Cistern #1",
    solution_score: 501,
    solution_movecount: 320,
    soloution_moves: "JJJLJHHKKHJJJJJLJJLHKHKHHJJLHHHHHLLLLKKKKKKKKKHHHHHHHHHHKHHJHHLLJJHHHHKKHHHJKLLLJJJHJHHLLJJJLLHHHHJJLLLLLLLLKKKLLJJJLHKKKKKKLKLLJJHJLKLJHJJJJLLHHHHHJHJJHHJJJKLLHHJJLLJJJJJJJLLLLLLHHKHHHKLKJLLKHKLKLKKKKHLKHHHLLJJHHLJJHJHHHKKHKHKHHHKKHLLKKKKJJJJHHHHHHHKKHHJJJHHHHHHJHHKKKKKHHHHHHHJJJLLLKLLHHHHHKKHLHHHLJJJJJLLLJJJHJJJHJHHK",
    official: 1,
};