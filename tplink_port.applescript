-- Change occurrences of '1' to the port number you want to control.
-- Load this into the script editor, and export as an app, then put the app on your desktop somewhere.

set homeDir to POSIX path of (path to home folder)
set commandPath to homeDir & "tplink_port.py"

set currentValue to do shell script commandPath & " 1"

set dialogText to "Port control is currently " & currentValue

set choice to display dialog dialogText buttons {"Enable Port", "Disable Port", "Cancel"} default button "Cancel"

set command to ""
if button returned of choice is "Enable Port" then
	set command to commandPath & " 1 enable"
else if button returned of choice is "Disable Port" then
	set command to commandPath & " 1 disable"
end if

if command is not "" then
	try
		set output to do shell script command
		display dialog output buttons {"OK"} default button "OK"
	on error errMsg
		display dialog "Error: " & errMsg buttons {"OK"} default button "OK"
	end try
end if
