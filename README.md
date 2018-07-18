# cheat.sh-sublime-plugin


## How To Install

1. To install this plugin, clone this repository in the Packages folder of your Sublime Text 3 installation and rename the folder as CheatSheet. 
Hint : You can open the Packages folder from "Preferences -> Browse Packages".
```
git clone https://github.com/gauravk-in/cheat.sh-sublime-plugin.git CheatSheet
```
2. Then using the Package Control plugin, install the missing dependencies. To do this, you must open the 
Command Palette from "Tools -> Command Palette" and write "Package Control: Satisfy Dependencies". 
3. You can open the console from "View -> Show Console" to check for any errors.

Meanwhile, we are working on publishing this plugin using Package Control, which will make it easy to install and update. Stay tuned for updates on this.

## Demos

### Insert answer in editor

1. Write your query string.
2. Select the query string.
3. Press "Cmd + Shift + B" to replace the selected query string by the answer generated from cht.sh.

![Preview](/contrib/cheat_demo_1.gif)

### List top 3 answers in a new tab

1. Press "Cmd + Shift + N" to launch the input panel in Sublime Text.
2. Enter your query and press Enter.
3. A new tab will be opened, and the top 3 best answers for the query will be listed in this page.

![Preview](/contrib/cheat_demo_2.gif)

### Another way to insert answer directly in the editor

1. Press "Cmd + Shift + M" to launch the input panel in Sublime Text.
2. Enter your query and press Enter.
3. The answer will be pasted in the open editor.

![Preview](/contrib/cheat_demo_3.gif)