const MUSIC = [
    {tag: "song11", volume: 0.2},
    {tag: "song04", volume: 0.1},
    {tag: "song25", volume: 0.1},
];

var songSelection = 0;

const SOUNDS = [
    {tag: "click", volume: 0.05},
    {tag: "back", volume: 0.05},
    {tag: "hover", volume: 0.25},
    {tag: "err", volume: 0.05},
    {tag: "monsterdeath", volume: 0.1},
    {tag: "level-start", volume: 0.2},
];

function playMusic()
{
    var media = document.getElementById(MUSIC[songSelection].tag);
	media.volume = MUSIC[songSelection].volume;
	const playPromise = media.play();
	if (playPromise !== null){
		playPromise.catch(() => { media.play(); })
	}
}

function pauseMusic()
{
    var media = document.getElementById(MUSIC[songSelection].tag);
    const playPromise = media.pause();
}

function playSound(sound, volume)
{
    var media = document.getElementById(sound);
    media.volume = volume;
    const playPromise = media.play();
    if (playPromise !== null) 
        playPromise.catch(() => {media.play();})
}