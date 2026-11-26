-- SCAT Chat: a menu-bar item over scat-chat.sh (in this app's Resources). Compile with build-app.sh (which also
-- makes it menu-bar only: no Dock icon, no window).
-- The dot is grey (starting, stopped), green (running) or red (a problem). The menu shows what the launcher wrote
-- to its state file (`ui` in the launcher's state folder: state, vault, address, then a problem line) and runs the
-- launcher with verbs only. No value is ever an argument, and the session key is never read or shown here:
-- `copy-key` is the one path to the clipboard. Stop runs the launcher's stop and shows its sentence in one alert, then quits; if the stop is not confirmed it stays,
-- red, so Stop can be tried again. Any other quit runs the launcher's stop silently, once.
-- Test settings (unset in a double-clicked app): SCAT_CHAT_LAUNCHER (a stand-in launcher), SCAT_CHAT_HOME (the
-- state folder, as for the launcher) and SCAT_CHAT_APPLET_LOG (a file that receives the menu's lines).
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

on run
	set logPath to my envOf("SCAT_CHAT_APPLET_LOG")
	set launcher to my envOf("SCAT_CHAT_LAUNCHER")
	if launcher is "" then set launcher to POSIX path of (path to resource "scat-chat.sh")
	set launcher to quoted form of launcher
	set stateDir to my envOf("SCAT_CHAT_HOME")
	if stateDir is "" then set stateDir to (POSIX path of (path to application support folder from user domain)) & "SCAT Chat"
	set uiPath to stateDir & "/ui"

	current application's NSApplication's sharedApplication()
	set sItem to current application's NSStatusBar's systemStatusBar()'s statusItemWithLength:(current application's NSVariableStatusItemLength)
	set theMenu to current application's NSMenu's alloc()'s initWithTitle:"SCAT Chat"
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
			display alert "SCAT Chat stopped" message msg
		end try
		quit
	on error msg
		my logline("stop failed: " & msg)
		try
			activate
			display alert "SCAT Chat has a problem" message msg as critical
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
				display alert "SCAT Chat has a problem" message theProb as critical
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
