print('test')
class testing():
    def __init__ (self, a):
        self.a = a
    def printA(self):
        print(self.a)

import testingFile as tf
test = tf.testing('Hello world')
test.printA()
    




