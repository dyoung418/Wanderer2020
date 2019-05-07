const music = "song04";

function playMusic()
{
	var media = document.getElementById(music);
	media.volume = .2;
	const playPromise = media.play();
	if (playPromise !== null){
		playPromise.catch(() => { media.play(); })
	}
}

function pauseMusic()
{
    var media = document.getElementById(music);
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