


class Command(object):
    def __init__(self,id,cmd,groups=None,preq=None):
        self.id = id
        self.cmd = cmd
        self.groups = groups
        self.preq = preq

    def __repr__(self):
        #return "%6.6d %-50s groups:%s preq:%s" % (self.id, self.cmd,self.groups,self.preq)
        return "%6.6d %-50s %s" % (self.id, self.cmd, self.groups)

# vim: set expandtab sw=4 ts=4:
