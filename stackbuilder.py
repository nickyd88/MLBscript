


class Stack:

    def __init__(self, player1, player2, player3, player4):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.stackpos = '0-0-0-0-0-0'
        self.pairpos = '0-0-0-0-0-0'

        positions = ['C', '1B', '2B', '3B', 'SS', 'OF']
        pos = {}
        for item in positions:
            pos[item] = 0
        pos[player1.position] += 1
        pos[player2.position] += 1
        pos[player3.position] += 1
        pos[player4.position] += 1

        p1 = pos['C']
        p2 = pos['1B']
        p3 = pos['2B']
        p4 = pos['SS']
        p5 = pos['3B']
        p6 = pos['OF']

        # Create simple string definition for position combination of stack #
        self.stackpos = '%d-%d-%d-%d-%d-%d' % (p1, p2, p3, p4, p5, p6)

        pos['C'] = 1 - p1
        pos['1B'] = 1 - p2
        pos['2B'] = 1 - p3
        pos['SS'] = 1 - p4
        pos['3B'] = 1 - p5
        pos['OF'] = 3 - p6

        p1 = pos['C']
        p2 = pos['1B']
        p3 = pos['2B']
        p4 = pos['SS']
        p5 = pos['3B']
        p6 = pos['OF']

        # Creating simple string of position requirements to complete 8-player stack #
        self.pairpos = '%d-%d-%d-%d-%d-%d' % (p1, p2, p3, p4, p5, p6)