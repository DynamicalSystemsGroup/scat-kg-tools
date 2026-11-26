# SCAT Chat's window or menu-bar item: which macOS mechanism (WP22 spike, G2 and G3)

WP22-G2 to G5. macOS 15.7.7, 26 November 2026. Test applets were built in a scratch folder; no real key, vault or address was used. Full test sources are in the appendix.

## Recommendation

Use **(a), AppleScriptObjC inside the existing applet, as a menu-bar item only**: an `NSStatusItem` whose title is a coloured dot, and a menu of State, Vault and Address lines (disabled, read-only) above Copy address, Copy key, Change vault and Stop. A menu-bar item needs no minimising (G2): it is out of the way and always there. No window closes on a click, so there should be no flicker (G4; Inferred, it needs a screen at the sitting). The build adds two lines: `plutil -insert LSUIElement -bool true` and `codesign --force --sign -` (ad hoc).

- **Talk:** the launcher writes `$STATE/ui` (three lines: state, vault, address; the key never) with a rename; the applet reads it in `on idle`. Menu items run `scat-chat.sh copy-key|copy-address|change-vault|stop`; `copy-key` and `copy-address` are new verbs (today only start, stop, status, change-vault exist); arguments are verbs only, so the session key never reaches any argument (WP21-R5, D-115) and is never shown. `copy_key` stays the one clipboard path.
- **Vault (G5):** before the server starts, one `ui_choice` says "Serve <vault>?" with "Use it" and "Choose another" (first run: folder chooser). It is one-shot, so no flicker; Change vault in the menu runs `stop` then `start` (`change-vault` is redefined; today it only deletes `$STATE/vault`), since the container mounts the vault.
- **Stop:** menu Stop and quitting the app both run the existing `stop` as today.
- **Fallback:** the same applet with an `NSWindow`.

## Evidence

Reproduce (a): `S=$(mktemp -d)`, save the script as `$S/t.applescript`, then
`osacompile -s -o $S/t.app $S/t.applescript && (SCAT_TEST_OUT=$S/out.txt $S/t.app/Contents/MacOS/applet & sleep 6; kill $!; cat $S/out.txt)` (re-run here: compile rc 0, output `fired`)

```
use framework "AppKit"
use scripting additions
property si : missing value
property n : 0
on run
  set si to current application's NSStatusBar's systemStatusBar()'s statusItemWithLength:-1
  si's button()'s setTitle:"● SCAT Chat"
  set m to current application's NSMenu's alloc()'s init()
  (m's addItemWithTitle:"Copy key" action:"k:" keyEquivalent:"")'s setTarget:me
  si's setMenu:m
  m's performActionForItemAtIndex:0
end run
on k_(s)
  do shell script "echo fired >> " & quoted form of (system attribute "SCAT_TEST_OUT")
end k_
on idle
  set n to n + 1
  if n > 3 then quit
  return 1
end idle
```

| Mechanism | What was tested | Result | Needs |
|---|---|---|---|
| (a) ASObjC status item | Appendix A command (four items, red dot, window button, `copy-key` stand-in, state file in `on idle`) | Tested: item action fired; stand-in got argv `copy-key` only; state file read | Nothing beyond macOS and `osacompile` |
| (a) NSWindow | Appendix A, same run (`isVisible`, `miniaturize:`, `deminiaturize:`) | Tested: stayed visible after the click; minimised and restored | As above |
| (a) as a menu-bar-only app | Appendix A, then `plutil -insert LSUIElement -bool true $S/t.app/Contents/Info.plist && codesign --force --sign - $S/t.app && codesign --verify --strict $S/t.app`; `lsappinfo info -only applicationType -app <pid>` (run while the applet is up) | Tested: signature valid, UIElement (no Dock icon), idle ran | No certificate |
| (a) stay open | Appendix A with `osacompile -o` (no `-s`) | Tested: quit after `on run`; with `-s` it ran (`build-app.sh` has `-s`) | Keep `-s` |
| (a) screenshot of the dot | `screencapture -x -R0,0,1800,40 $S/bar.png` | Tested, inconclusive: the capture shows no status items (not even the clock), so the dot's look and a real click are untested | Sitting |
| (b) one `display dialog` | `osascript -e 'display dialog "x" buttons {"Copy address","Copy key","Stop"} giving up after 2'` | Tested: returns on any button (here, after 2 s), so a Copy button cannot keep it open; any loop re-shows it. Inferred (from memory, not re-read in the dictionary): at most three buttons, no minimise | Nothing |
| (c) JXA helper | Appendix B: `osascript -l JavaScript h.js` | Tested, failed: `NSAttributedString` initialisers did not bridge in four tries; one variant hung and was killed | macOS |
| (c) Swift helper | Appendix C: `swiftc t.swift -o t && ./t` | Tested: compiles, but only because Command Line Tools are installed here. Inferred: a clean Mac lacks `swiftc` | Extra install |

## Isolation and CI

- macOS-only: the applet, `osacompile`, `plutil`, `codesign`, behind the launcher's own verbs; record them beside `security` in MISSION Platforms.
- Linux CI (Inferred, not run): add `ui_state()` to the launcher, called by every start step, writing `$STATE/ui` in both modes; a test starts under `SCAT_CHAT_UI=plain` with stand-ins and asserts the file's three lines and that the key is in no line. `copy-address` uses the `PBCOPY` stand-in. A grep test checks every applet verb is one the launcher accepts. Skip the built-app test off macOS.
- The Mac dry run checks the dot, a click and `ps -ww -o args` (WP22-R6).

## Open questions

1. Menu-bar item only, or a window too? A notch can hide a crowded menu bar's item (Inferred).
2. Is "Change vault" meaning stop and restart acceptable, since a running server cannot change vault?
3. May the build edit `Info.plist` and re-sign ad hoc (needs the ACE's log, ORG new mechanism)?
4. A problem: red dot with the reason in the menu, or the error dialog?

## Appendix (test sources, not counted in the prose limit)

**A. Full applet.** `S=$(mktemp -d); cd $S`; save as `asobjc.applescript`; then
```
printf '#!/bin/sh\nprintf "argv=%%s\\n" "$*" >> "$SCAT_TEST_OUT"\n' > fake.sh; chmod +x fake.sh
printf 'running\nVAULT-X\nhttps://example.test/mcp\n' > state.txt
osacompile -s -o u.app asobjc.applescript
SCAT_TEST_OUT=$S/out.txt SCAT_TEST_LAUNCHER=$S/fake.sh SCAT_TEST_STATE=$S/state.txt u.app/Contents/MacOS/applet & P=$!
sleep 12; kill $P; cat out.txt
plutil -insert LSUIElement -bool true u.app/Contents/Info.plist && codesign --force --sign - u.app && codesign --verify --strict u.app
```
Run the last line before a second launch, and `lsappinfo info -only applicationType -app $!` two seconds after it starts.

```
use AppleScript version "2.4"
use framework "Foundation"
use framework "AppKit"
use scripting additions

property sItem : missing value
property theMenu : missing value
property theWin : missing value
property outPath : ""
property tick : 0

on logline(t)
	do shell script "printf '%s\\n' " & quoted form of t & " >> " & quoted form of outPath
end logline

on dot(c)
	set s to current application's NSMutableAttributedString's alloc()'s initWithString:"● SCAT Chat"
	(s's addAttribute:(current application's NSForegroundColorAttributeName) value:c range:{0, 1})
	return s
end dot

on run
	set outPath to system attribute "SCAT_TEST_OUT"
	current application's NSApplication's sharedApplication()
	-- status item with a coloured dot and a menu
	set sItem to current application's NSStatusBar's systemStatusBar()'s statusItemWithLength:(current application's NSVariableStatusItemLength)
	sItem's button()'s setAttributedTitle:(my dot(current application's NSColor's systemGreenColor()))
	set theMenu to current application's NSMenu's alloc()'s initWithTitle:"SCAT"
	repeat with t in {"Copy address", "Copy key", "Change vault", "Stop"}
		set mi to (theMenu's addItemWithTitle:(t as text) action:("menu" & (character 1 of (t as text)) & ":") keyEquivalent:"")
		mi's setTarget:me
	end repeat
	sItem's setMenu:theMenu
	-- a window with two buttons
	set theWin to current application's NSWindow's alloc()'s initWithContentRect:{{200, 200}, {320, 120}} styleMask:(1 + 2 + 4) backing:2 defer:false
	theWin's setTitle:"SCAT Chat"
	set b to current application's NSButton's buttonWithTitle:"Copy key" target:me action:"menuC:"
	b's setFrame:{{20, 20}, {120, 32}}
	theWin's contentView()'s addSubview:b
	theWin's makeKeyAndOrderFront:me
	try
		set w to sItem's button()'s |window|()
		my logline("statusitem window visible: " & ((w's isVisible()) as text) & " onscreen y=" & (item 2 of item 1 of (w's frame() as list)))
	on error e
		my logline("frame err: " & e)
	end try
	my logline("menu items: " & ((theMenu's numberOfItems()) as text))
	set tick to 0
end run

on menuC_(sender)
	try
		my logline("action fired: " & (sender's title() as text))
		do shell script (quoted form of (system attribute "SCAT_TEST_LAUNCHER")) & " copy-key"
		set stText to do shell script "cat " & quoted form of (system attribute "SCAT_TEST_STATE")
		my logline("state file read: " & (stText as text))
	on error e
		my logline("handler err: " & e)
	end try
end menuC_

on idle
	set tick to tick + 1
	my logline("idle " & (tick as text))
	if tick = 1 then
		theMenu's performActionForItemAtIndex:1 -- Copy key
		my logline("after click, window visible: " & ((theWin's isVisible()) as text))
		theWin's miniaturize:me
	else if tick = 2 then
		my logline("miniaturized: " & ((theWin's isMiniaturized()) as text))
		theWin's deminiaturize:me
	else if tick = 3 then
		my logline("deminiaturized, visible: " & ((theWin's isVisible()) as text) & " mini=" & ((theWin's isMiniaturized()) as text))
		sItem's button()'s setAttributedTitle:(my dot(current application's NSColor's systemRedColor()))
		my logline("title now: " & (sItem's button()'s attributedTitle()'s |string|() as text))
	else if tick >= 9 then
		quit
	end if
	return 1
end idle
```

**B. JXA, `h.js`** (failed as described; run `osascript -l JavaScript h.js`, kill it if it hangs):
```
ObjC.import('Cocoa');
$.NSApplication.sharedApplication;
$.NSApp.setActivationPolicy($.NSApplicationActivationPolicyAccessory);
var it = $.NSStatusBar.systemStatusBar.statusItemWithLength($.NSVariableStatusItemLength);
var d = $.NSDictionary.dictionaryWithObjectForKey($.NSColor.systemGreenColor, $.NSForegroundColorAttributeName);
var s = $.NSAttributedString.alloc.init.initWithStringAttributes($("● SCAT Chat"), d);
it.button.attributedTitle = s;
ObjC.registerSubclass({name:'H', methods:{'copyKey:':{types:['void',['id']], implementation:function(x){ $.NSFileHandle.fileHandleWithStandardOutput.writeData($.NSString.alloc.initWithUTF8String('fired\n').dataUsingEncoding($.NSUTF8StringEncoding)); }}}});
var h = $.H.alloc.init;
var m = $.NSMenu.alloc.initWithTitle('SCAT');
var mi = m.addItemWithTitleActionKeyEquivalent('Copy key', 'copyKey:', ''); mi.target = h;
it.menu = m;
m.performActionForItemAtIndex(0);
var n=0;
$.NSTimer.scheduledTimerWithTimeIntervalRepeatsBlock(1,true,function(t){ n++; if(n>=3){ $.NSApp.terminate(null);} });
$.NSApp.run;
```

**C. Swift, `t.swift`:**
```
import AppKit
print("ok")
```
