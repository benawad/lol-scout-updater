# lol-scout-updater
A small python script that accesses the Riot Games API and retrieves stats on a random challenger player. It then formats the stats and writes it to a file. I use the program to pick the featured player for my [LoL Scout app](https://play.google.com/store/apps/details?id=benawad.com.lolscout&hl=en). 

## How to run it on your computer

1. Get an API key at the developer page at [Riot](https://developer.riotgames.com/) and create a free account.
2. Change the API key in the program to yours
3. Change the `filepath` variable to the path of where you want the program to write the text file to. 

## Running the program
The player information is printed in the terminal and written to the file. A output should look like this:

`15,51,34,17,7.6,4.1,9,EnmaDaiO,na,Sivir,4,7,1055,3087,3031,1038,3006,1053,(9)[r_1_3.png]#+0.95 attack damage!,(9)[b_3_3.png]#+1.34 magic resist!,(9)[y_1_3.png]#+1 armor!,(3)[bl_3_3.png]#+4.5% attack speed!`
