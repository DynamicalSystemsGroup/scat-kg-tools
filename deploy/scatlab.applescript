-- SCATLAB: a menu-bar item over scatlab.sh (in this app's Resources). Compile with build-app.sh (which also
-- makes it menu-bar only: no Dock icon, no window).
-- The dot is grey (starting, stopped), green (running) or red (a problem). The menu shows what the launcher wrote
-- to its state file (`ui` in the launcher's state folder: state, vault, address, then a problem line) and runs the
-- launcher with verbs only. No value is ever an argument, and the session key is never read or shown here:
-- `copy-key` is the one path to the clipboard. Stop runs the launcher's stop and shows its sentence in one alert, then quits; if the stop is not confirmed it stays,
-- red, so Stop can be tried again. Any other quit runs the launcher's stop silently, once.
-- Settings for tests (unset in a double-clicked app): SCATLAB_LAUNCHER (another launcher to call), SCATLAB_HOME (the
-- state folder, as for the launcher) and SCATLAB_APPLET_LOG (a file that receives the menu's lines).
use AppleScript version "2.4"
use framework "Foundation"
use framework "AppKit"
use scripting additions

property launcher : ""
property uiPath : ""
property logPath : ""
property sItem : missing value
property theMenu : missing value
property stateItem : missing value
property vaultItem : missing value
property addrItem : missing value
property probItem : missing value
property copyAddrItem : missing value
property copyKeyItem : missing value
property changeItem : missing value
property stopItem : missing value
property ticks : 0
property alerted : false
property lastDump : ""
property stopDone : false -- the Stop item already ran the launcher's stop: quitting must not run it again

on logline(t)
	if logPath is "" then return
	try
		do shell script "printf '%s\\n' " & quoted form of t & " >> " & quoted form of logPath
	end try
end logline

on envOf(n)
	try
		return system attribute n
	on error
		return ""
	end try
end envOf

on addLine(t)
	set mi to theMenu's addItemWithTitle:t action:(missing value) keyEquivalent:""
	mi's setEnabled:false
	return mi
end addLine

on addAction(t, sel)
	set mi to theMenu's addItemWithTitle:t action:sel keyEquivalent:""
	mi's setTarget:me
	return mi
end addAction

-- Outside the Applications folder, offer to move the app there, as many Mac apps do. Returns true when the person chose
-- to move it (moved, or told how), so this copy quits without starting a session. Skipped under tests
-- (SCATLAB_LAUNCHER set).
on offerMove()
	set here to POSIX path of (path to me)
	if here ends with "/" then set here to text 1 thru -2 of here
	if here starts with "/Applications/" then return false
	set target to "/Applications/SCATLAB.app"
	activate -- a menu-bar app's dialog would otherwise open behind other windows
	set answer to button returned of (display dialog "SCATLAB is not in your Applications folder. Move it there? It then opens from Applications, like your other apps." buttons {"Not now", "Move to Applications"} default button "Move to Applications" with title "SCATLAB" with icon note)
	if answer is not "Move to Applications" then return false
	if here contains "/AppTranslocation/" then
		display alert "SCATLAB can't move itself from here." message "macOS is running it from a temporary place. Quit it, then drag SCATLAB.app into your Applications folder in Finder and open it from there."
		return true
	end if
	try
		do shell script "rm -rf " & quoted form of target & " && mv " & quoted form of here & " " & quoted form of target
	on error
		display alert "SCATLAB couldn't move itself." message "Drag SCATLAB.app into your Applications folder in Finder, then open it from there."
		return true
	end try
	display dialog "SCATLAB is now in your Applications folder. Open it from there when you start a session." buttons {"OK"} default button "OK" with title "SCATLAB" with icon note
	return true
end offerMove

on run
	set logPath to my envOf("SCATLAB_APPLET_LOG")
	set launcher to my envOf("SCATLAB_LAUNCHER")
	if launcher is "" and my offerMove() then
		set stopDone to true -- this copy started nothing, so its quit has nothing to stop
		quit
		return
	end if
	if launcher is "" then set launcher to POSIX path of (path to resource "scatlab.sh")
	set launcher to quoted form of launcher
	set stateDir to my envOf("SCATLAB_HOME")
	if stateDir is "" then set stateDir to (POSIX path of (path to application support folder from user domain)) & "SCATLAB"
	set uiPath to stateDir & "/ui"

	current application's NSApplication's sharedApplication()
	set sItem to current application's NSStatusBar's systemStatusBar()'s statusItemWithLength:(current application's NSVariableStatusItemLength)
	set theMenu to current application's NSMenu's alloc()'s initWithTitle:"SCATLAB"
	theMenu's setAutoenablesItems:false
	set stateItem to my addLine("State: starting")
	set vaultItem to my addLine("Vault:")
	set addrItem to my addLine("Address:")
	set probItem to my addLine("Problem:")
	theMenu's addItem:(current application's NSMenuItem's separatorItem())
	set copyAddrItem to my addAction("Copy address", "copyAddress:")
	set copyKeyItem to my addAction("Copy key", "copyKey:")
	set changeItem to my addAction("Change vault", "changeVault:")
	set stopItem to my addAction("Stop", "stopIt:")
	sItem's setMenu:theMenu
	my render("starting", "", "", "")

	-- an old state file must not be read as this session's
	try
		do shell script "rm -f " & quoted form of uiPath
	end try
	do shell script launcher & " start > /dev/null 2>&1 &"
end run

on dot(c)
	set s to current application's NSMutableAttributedString's alloc()'s initWithString:"●"
	s's addAttribute:(current application's NSForegroundColorAttributeName) value:c range:{0, 1}
	return s
end dot

on render(theState, theVault, theAddr, theProb)
	set c to current application's NSColor's systemGrayColor()
	if theState is "running" then set c to current application's NSColor's systemGreenColor()
	if theState is "problem" then set c to current application's NSColor's systemRedColor()
	sItem's button()'s setAttributedTitle:(my dot(c))
	stateItem's setTitle:("State: " & theState)
	vaultItem's setTitle:("Vault: " & theVault)
	addrItem's setTitle:("Address: " & theAddr)
	probItem's setTitle:("Problem: " & theProb)
	probItem's setHidden:(theState is not "problem")
	copyAddrItem's setEnabled:(theState is "running")
	copyKeyItem's setEnabled:(theState is "running")
	set dump to theState & "|" & theVault & "|" & theAddr & "|" & theProb
	if dump is not lastDump then
		set lastDump to dump
		my logline("menu (dot " & theState & "):")
		repeat with i from 0 to ((theMenu's numberOfItems()) as integer) - 1
			set mi to theMenu's itemAtIndex:i
			if (mi's isSeparatorItem()) as boolean then
				my logline("  ---")
			else
				my logline("  " & (mi's title() as text) & "  [enabled=" & ((mi's isEnabled()) as boolean) & " hidden=" & ((mi's isHidden()) as boolean) & "]")
			end if
		end repeat
	end if
end render

on readState()
	-- returns {state, vault, address, problem}; no file yet means starting
	try
		set raw to do shell script "cat " & quoted form of uiPath
	on error
		return {"starting", "", "", ""}
	end try
	set ps to paragraphs of raw
	set theState to "starting"
	set theVault to ""
	set theAddr to ""
	set theProb to ""
	if (count of ps) ≥ 1 then set theState to item 1 of ps
	if (count of ps) ≥ 2 then set theVault to item 2 of ps
	if (count of ps) ≥ 3 then set theAddr to item 3 of ps
	if (count of ps) ≥ 4 then set theProb to item 4 of ps
	return {theState, theVault, theAddr, theProb}
end readState

on copyAddress_(sender)
	try
		do shell script launcher & " copy-address > /dev/null 2>&1"
	end try
end copyAddress_

on copyKey_(sender)
	try
		do shell script launcher & " copy-key > /dev/null 2>&1"
	end try
end copyKey_

on changeVault_(sender)
	try
		do shell script launcher & " change-vault > /dev/null 2>&1 &"
	end try
end changeVault_

on stopIt_(sender)
	-- Stop runs the launcher's stop and shows its sentence in one alert. Confirmed (exit 0): quit. Not confirmed
	-- (the launcher exits non-zero and has written the problem state): show it as the problem and stay, so Stop can
	-- be chosen again. `do shell script` blocks the run loop meanwhile; `alerted` keeps the idle timer from alerting too.
	set alerted to true
	try
		set msg to do shell script launcher & " stop 2>&1"
		set stopDone to true
		my logline("stop: " & msg)
		try
			activate
			display alert "SCATLAB stopped" message msg
		end try
		quit
	on error msg
		my logline("stop failed: " & msg)
		try
			activate
			display alert "SCATLAB has a problem" message msg as critical
		end try
	end try
end stopIt_

on idle
	set ticks to ticks + 1
	set {theState, theVault, theAddr, theProb} to my readState()
	my render(theState, theVault, theAddr, theProb)
	if theState is "problem" then
		if not alerted then
			set alerted to true
			try
				activate
				display alert "SCATLAB has a problem" message theProb as critical
			end try
		end if
	else
		set alerted to false
		-- the launcher is gone and there is nothing to show: quit (after a few seconds' grace at the start)
		if ticks > 2 then
			try
				do shell script launcher & " status > /dev/null"
			on error
				quit
			end try
		end if
	end if
	return 2
end idle

on quit
	-- other routes (Cmd-Q, the system, a quit mid-start) stop silently, once
	if not stopDone then
		set stopDone to true
		try
			do shell script launcher & " stop > /dev/null 2>&1"
		end try
	end if
	continue quit
end quit
