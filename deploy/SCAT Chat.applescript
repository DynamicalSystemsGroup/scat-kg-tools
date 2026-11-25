-- SCAT Chat: a thin shell around scat-chat.sh (in this app's Resources). Compile with build-app.sh.
-- Start: the script asks its own questions and shows its own windows. Quit: the script's stop runs.
property launcher : ""
property started : false

on run
	set launcher to quoted form of (POSIX path of (path to resource "scat-chat.sh"))
	do shell script launcher & " start > /dev/null 2>&1 &"
	delay 3
	set started to true
end run

on idle
	if started then
		try
			do shell script launcher & " status > /dev/null"
		on error
			quit
		end try
	end if
	return 3
end idle

on quit
	try
		do shell script launcher & " stop > /dev/null 2>&1"
	end try
	continue quit
end quit
