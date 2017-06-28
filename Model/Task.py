class task():
    def __init__(self, taskstr, id):
        self.id = id
        self.legend = ''
        self.taskstr = taskstr
        self.original = taskstr
        self.cs = []
        self.relationships = []
    def treat(self):
        c = self.taskstr[0]
        if c == 'x': # paralell
            self.legend = 'paralell'
            #print('paralell')
        elif c == 'o': # or
            self.legend = 'or'
            #print('or')
        elif c == 'd':
            self.legend = 'domain'
        elif c == '<':
            self.legend = 'dependence'
        bkp = self.taskstr[1:]
        bkp = bkp.replace('(', '')
        bkp = bkp.replace(')', '')
        bkp = bkp.split(';')
        self.cs = bkp
        #print(bkp)
    def get_groupsets(self):
        if len(self.relationships) > 0:
            return self.relationships
        else:
            return -1
    def __repr__(self):
        return self.taskstr