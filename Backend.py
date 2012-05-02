
import shelve
import Command



def approved(cmd,approvals,cfg):
    """
        command has been approved according to this set of approvers
        @param cmd : command to approve
        @param approvals : set of approvals
        @param cfg : ruleset
    """

    for g in cmd.groups:

        try:
            rules = cfg['classes'][g]
        except:
            return "Invalid class provided:", g

        # Count number of valid approvers
        napprovers = 0
        for u in rules['approvers']:
            if u in approvals:
                napprovers += 1

        # Make sure number of valid approvers is met
        if napprovers < rules['required']:
            return "Doesn't meet number of approvers required", rules['required']
            
        # Ensure mandatory approvers are met
        for u in rules['mandatory']:
            if u not in approvals:
                return "Don't have mandatory approver:", u

    return "YES"


class Backend(object):
    def __init__(self,fname,cfg,new=False):
        self.file = fname
        self.pending = []
        self.cfg = cfg

        if new:
            flags = 'n'
        else:
            flags = 'w'

        self.d = shelve.open(fname,flags,writeback=True)

        try:
            self.d['commands']
        except KeyError:
            self.d['seqn'] = 0
            self.d['commands'] = dict()
            # (cmdid, uid)
            self.d['approvals'] = {}

#        self.d = dbm.open("test.db","c")

    def getPendingCommands(self,ci=None):
        s = ""
        if ci:
            cmd = self.d['commands'][ci]

            s += ci
            s += "Groups:", cmd.groups

        else:
            for c in self.d['commands'].itervalues():
                s += str(c) + '\n'
        return s
     
    def addCommand(self,cmd,uid,groups=['root']):
        self.d['seqn'] += 1
        cmd = Command.Command(id=self.d['seqn'], cmd=cmd, groups=groups)
        self.d['commands'][cmd.id] = cmd
        self.d.sync()

    def removeCommand(self,cmd,uid):
        self.d['commands']

    def approveCommand(self,ci,uid):
        """ @param ci: cmdid """
        
        if ci not in self.d['approvals']:
            self.d['approvals'][ci] = set()

        self.d['approvals'][ci].add(uid)

        cmd = self.d['commands'][int(ci)]

        ret = approved(cmd,self.d['approvals'][ci],self.cfg)

        if ret == "Yes":
            return "Yes", ret
        else:
            return ret

               

import unittest

class TestBackend(unittest.TestCase):

    def setUp(self):
        pass

    def test_addCommandAddsAsPending(self):
        """ Make sure commands are added """
        b = Backend("test.db")

        b.addCommand("test")

        self.assertTrue("test" in b.getPendingCommands())

    def test_addCommandGivesCommandID(self):
        b = Backend("test.db")
        self.assertTrue(1 == b.addCommand("test"))

if __name__ == '__main__':
    unittest.main()
	

# vim: set expandtab sw=4 ts=4:
