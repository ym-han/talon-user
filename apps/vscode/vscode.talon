app: vscode
-
tag(): user.find
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs
tag(): user.zoom

# Language features
comment:                         code.toggle_comment()
suggest:                         code.complete()
format document:                 user.format_document()
suggest param:                   user.vscode("editor.action.triggerParameterHints")
imports organize:                user.vscode("editor.action.organizeImports")
problem next:                    user.vscode("editor.action.marker.nextInFiles")
problem last:                    user.vscode("editor.action.marker.prevInFiles")
problem fix:                     user.vscode("problems.action.showQuickFixes")
refactor this:                   user.vscode("editor.action.refactor")

# Split
split up:                        user.vscode("workbench.action.moveEditorToAboveGroup")
split down:                      user.vscode("workbench.action.moveEditorToBelowGroup")
split left:                      user.vscode("workbench.action.moveEditorToLeftGroup")
split right:                     user.vscode("workbench.action.moveEditorToRightGroup")
focus up:                        user.vscode("workbench.action.focusAboveGroup")
focus down:                      user.vscode("workbench.action.focusBelowGroup")
focus left:                      user.vscode("workbench.action.focusLeftGroup")
focus right:                     user.vscode("workbench.action.focusRightGroup")
split flip:                      user.vscode("workbench.action.toggleEditorGroupLayout")
split clear:                     user.vscode("workbench.action.joinTwoGroups")
split clear all:                 user.vscode("workbench.action.editorLayoutSingle")
cross:                           user.vscode("workbench.action.focusNextGroup")
open cross:                      key(ctrl-enter)

# Sidebar
bar (show | hide):               user.vscode("workbench.action.toggleSidebarVisibility")
bar explorer:                    user.vscode("workbench.view.explorer")
bar extensions:                  user.vscode("workbench.view.extensions")
bar outline:                     user.vscode("outline.focus")
bar debug:                       user.vscode("workbench.view.debug")
bar search:                      user.vscode("workbench.view.search")
bar source:                      user.vscode("workbench.view.scm")
bar file:                        user.vscode("workbench.files.action.showActiveFileInExplorer")
bar collapse:                    user.vscode("workbench.files.action.collapseExplorerFolders")
ref last:                        user.vscode("references-view.prev")
ref next:                        user.vscode("references-view.next")

# Panel
panel (show | hide):             user.vscode("workbench.action.togglePanel")
panel (large | small):           user.vscode("workbench.action.toggleMaximizedPanel")
panel control:                   user.vscode("workbench.panel.repl.view.focus")
panel output:                    user.vscode("workbench.panel.output.focus")
panel problems:                  user.vscode("workbench.panel.markers.view.focus")
panel terminal:                  user.vscode("workbench.action.terminal.focus")
panel debug:                     user.vscode("workbench.debug.action.toggleRepl")
panel clear:                     user.vscode("workbench.debug.panel.action.clearReplAction")

# Focus editor
focus editor:                    user.vscode("workbench.action.focusActiveEditorGroup")

# Hide sidebar and panel
hide all:
    user.vscode("workbench.action.closeSidebar")
    user.vscode("workbench.action.closePanel")
    user.vscode("closeFindWidget")

# Files / Folders
folder open:                     user.vscode("workbench.action.files.openFolder")
folder add:                      user.vscode("workbench.action.addRootFolder")
folder new:                      user.vscode("explorer.newFolder")
file open:                       user.vscode("workbench.action.files.openFile")
file new:                        user.vscode("explorer.newFile")
file open folder:                user.vscode("revealFileInOS")
file copy path:                  user.vscode("copyFilePath")

# Folding
fold this:                       user.vscode("editor.fold")
unfold this:                     user.vscode("editor.unfold")
fold recursive:                  user.vscode("editor.foldAllMarkerRegions")
unfold recursive:                user.vscode("editor.unfoldRecursively")
fold all:                        user.vscode("editor.foldAll")
unfold all:                      user.vscode("editor.unfoldAll")
fold comments:                   user.vscode("editor.foldAllBlockComments")

# Navigation
take last:                       user.vscode("editor.action.addSelectionToPreviousFindMatch")
take all these:                  user.vscode("editor.action.selectHighlights")
cursor nope:                     user.vscode("cursorUndo")
cursor redo:                     user.vscode("cursorRedo")
cursor up:                       user.vscode("editor.action.insertCursorAbove")
cursor down:                     user.vscode("editor.action.insertCursorBelow")
cursor lines:                    user.vscode("editor.action.insertCursorAtEndOfEachLineSelected")
cursor expand:                   user.vscode("editor.action.smartSelect.expand")
cursor shrink:                   user.vscode("editor.action.smartSelect.shrink")

# Find session
scout sesh [<user.text>]$:
    user.vscode_find_recent(text or "")

pop sesh <user.text>$:
    user.vscode_find_recent(text)
    key(enter)

pop sesh:
    user.vscode_find_recent("", 1)
    key(enter)

# Find a symbol
scout symbol [<user.text>]$:
    user.vscode("workbench.action.gotoSymbol")
    "{text}"

scout all symbol [<user.text>]$:
    user.vscode("workbench.action.showAllSymbols")
    "{text}"

# Misc
install extension:               user.vscode("workbench.extensions.action.installVSIX")
window reload:                   user.vscode("workbench.action.reloadWindow")
open settings json:              user.vscode("workbench.action.openSettingsJson")
trim trailing:                   user.vscode("editor.action.trimTrailingWhitespace")
cursorless record:               user.vscode("cursorless.recordTestCase")
inspect scope:                   user.vscode("editor.action.inspectTMScopes")

snip last:                       user.vscode("jumpToPrevSnippetPlaceholder")
[snip] next:                     user.vscode("jumpToNextSnippetPlaceholder")

please [<user.text>]$:
    user.vscode("workbench.action.showCommands")
    "{user.text or ''}"