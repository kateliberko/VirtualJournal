class Counter:
    count1 = 1
    count2 = 1

    jpc = 0

    def increment1(self):
        self.count1 += 1
        return ''

    def increment2(self):
        self.count2 += 1
        return ''

    def jcount(self):
        self.jpc += 1
        return ''
    
    def jreset(self):
        self.jpc = 0
        return ''


