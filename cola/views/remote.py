from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from cola.views import standard


class RemoteView(standard.StandardDialog):
    """A dialog for choosing branches."""

    def __init__(self, parent, action):
        """Customizes the dialog based on the remote action
        """
        standard.StandardDialog.__init__(self, parent=parent)

        self.resize(666, 606)
        self._main_vbox_layt = QtGui.QVBoxLayout(self)

        # Local branch section
        self._local_branch_hbox_layt = QtGui.QHBoxLayout()
        # Exposed
        self.local_label = QtGui.QLabel(self)
        self.local_label.setText(self.tr('Local Branches'))
        # Exposed
        self.local_branch = QtGui.QLineEdit(self)
        # Exposed
        self.local_branches = QtGui.QListWidget(self)

        # Remote branch section
        self._remote_branch_hbox_layt = QtGui.QHBoxLayout()
        self._remote_label = QtGui.QLabel(self)
        self._remote_label.setText(self.tr('Remote'))
        # Exposed
        self.remotename = QtGui.QLineEdit(self)
        # Exposed
        self.remotes = QtGui.QListWidget(self)

        self._remote_branches_hbox_layt = QtGui.QHBoxLayout()
        # Exposed
        self.remote_label = QtGui.QLabel(self)
        self.remote_label.setText(self.tr('Remote Branch'))
        # Exposed
        self.remote_branch = QtGui.QLineEdit(self)
        self.remote_branches = QtGui.QListWidget(self)

        self._options_hbox_layt = QtGui.QHBoxLayout()
        # Exposed
        self.ffwd_only_checkbox = QtGui.QCheckBox(self)
        self.ffwd_only_checkbox.setText(self.tr('Fast Forward Only'))
        self.ffwd_only_checkbox.setChecked(True)
        self.ffwd_only_checkbox.setObjectName("ffwd_only_checkbox")

        # Exposed
        self.tags_checkbox = QtGui.QCheckBox(self)
        self.tags_checkbox.setText(self.tr('Include tags'))

        self.rebase_checkbox = QtGui.QCheckBox(self)
        self.rebase_checkbox.setText(self.tr('Rebase'))

        self._options_spacer = QtGui.QSpacerItem(1, 1,
                                           QtGui.QSizePolicy.Expanding,
                                           QtGui.QSizePolicy.Minimum)
        self._options_hbox_layt.addItem(self._options_spacer)
        # Exposed
        self.action_button = QtGui.QPushButton(self)
        self.action_button.setText(self.tr('Push'))
        # Exposed
        self.cancel_button = QtGui.QPushButton(self)
        self.cancel_button.setText(self.tr('Cancel'))

        # connections
        self.connect(self.cancel_button, SIGNAL('released()'), self.reject)

        if action:
            self.action_button.setText(action.title())
            self.setWindowTitle(action.title())
        if action == 'pull':
            self.tags_checkbox.hide()
            self.ffwd_only_checkbox.hide()
            self.local_label.hide()
            self.local_branch.hide()
            self.local_branches.hide()
        if action != 'pull':
            self.rebase_checkbox.hide()

        if action == 'fetch':
            self.layout_remotes()
            self.layout_remote_branches()
            self.layout_local_branches()
        elif action == 'pull':
            self.layout_remote_branches()
            self.layout_remotes()
            self.layout_local_branches()
        else:
            self.layout_local_branches()
            self.layout_remotes()
            self.layout_remote_branches()

        self.layout_options()

    def layout_options(self):
        self._options_hbox_layt.addWidget(self.ffwd_only_checkbox)
        self._options_hbox_layt.addWidget(self.tags_checkbox)
        self._options_hbox_layt.addWidget(self.rebase_checkbox)
        self._options_hbox_layt.addWidget(self.action_button)
        self._options_hbox_layt.addWidget(self.cancel_button)
        self._main_vbox_layt.addLayout(self._options_hbox_layt)

    def layout_local_branches(self):
        self._local_branch_hbox_layt.addWidget(self.local_label)
        self._local_branch_hbox_layt.addWidget(self.local_branch)
        self._main_vbox_layt.addLayout(self._local_branch_hbox_layt)
        self._main_vbox_layt.addWidget(self.local_branches)

    def layout_remotes(self):
        self._remote_branch_hbox_layt.addWidget(self._remote_label)
        self._remote_branch_hbox_layt.addWidget(self.remotename)
        self._main_vbox_layt.addLayout(self._remote_branch_hbox_layt)
        self._main_vbox_layt.addWidget(self.remotes)

    def layout_remote_branches(self):
        self._remote_branches_hbox_layt.addWidget(self.remote_label)
        self._remote_branches_hbox_layt.addWidget(self.remote_branch)
        self._main_vbox_layt.addLayout(self._remote_branches_hbox_layt)
        self._main_vbox_layt.addWidget(self.remote_branches)

    def select_first_remote(self):
        """Selects the first remote in the list view"""
        return self.select_remote(0)

    def select_remote(self, idx):
        """Selects a remote by index"""
        item = self.remotes.item(idx)
        if item:
            self.remotes.setItemSelected(item, True)
            self.remotes.setCurrentItem(item)
            self.remotename.setText(item.text())
            return True
        else:
            return False

    def select_local_branch(self, idx):
        """Selects a local branch by index in the list view"""
        item = self.local_branches.item(idx)
        if not item:
            return False
        self.local_branches.setItemSelected(item, True)
        self.local_branches.setCurrentItem(item)
        self.local_branch.setText(item.text())
        return True


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    remote = RemoteView()
    remote.show()
    sys.exit(app.exec_())
