ShowRenamer App


About:

It is a TV series renamer app which renames all the episodes of the TV series according to the respective names given in IMDb, given the name and local directory path

How to use:

- Put the file showRenamer.py in any directory.
- Run the script using the command:
	python showRenamer.py
- A prompt will come, asking for the series name and the local path
- Enter the name of the Series and the local directory path in your PC.
- It will fetch the details from IMDb and then rename all the episodes and folders accordingly.

Note:
Currently, only those episodes will be renamed which have their name in the format:
<something><'S'/'s'><something><season num><something><'E'/'e'><something><episode num><something><extension>
Episodes named like 1x01.mkv, 1x02.mkv will not be affected.