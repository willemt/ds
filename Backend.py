
import shelve
import Command



def approved(cmd,approvals,groups,cfg):
    """
        command has been approved according to this set of approvers
        @param cmd
        @param approvals set of approvals
        @param cfg ruleset
    """

    for g in cmd.groups:
        try:
            rules = cfg['classes'][g]
        except:
            return "does not have class", g

        napprovers = 0
        for u in rules['approvers']:
            if u in approvals:
                napprovers += 1

        if napprovers < rules['required']:
            return "doesn't meet number of approvers required", rules['required']
            
        for u in rules['mandatory']:
            if u not in approvals:
                return "don't have mandatory approver:", u

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
            self.d['commands'] = {}
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
        
        try:
            _ = self.d['approvals'][ci]
        except KeyError:
            self.d['approvals'][ci] = set()

        self.d['approvals'][ci].add(uid)

        print "approvers", self.d['approvals'][ci]

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
