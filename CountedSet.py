'''
*
*   Author: Nate Schriener 6/2017
*
*   Operation Overloading. Sends a Request to a URL and scrapes page.
*   Returns the most common word found on that page. 
*
'''

from functools import *
from collections import Counter
import collections
import operator

from functools import *
from random import randint
from collections import Counter
from urllib.request import Request, urlopen
import re  # regular expresions

class CountedSet:
    def __init__(self):
        self.data = {}
    def __iadd__(self,other):
        if isinstance(other,int):
            self.data[other] = self.data.get(other, 0) + 1
            return self
        elif isinstance(other,CountedSet):
            for key, value in other.data.items():
                if key in self.data:
                    self.data[key] = self.data[key] + other.data[key]
                else:
                    self.data[key] = value
            return self
        else:
            self.data[other] = self.data.get(other,0) + 1
            return self
    def __add__(self,obj):
        for key, value in obj.data.items():
            if len(self.data) == 0:
                self.data[key] = value
            elif self.data[key]:
                self.data[key] = self.data[key] + value
            else:
                self.data[key] = value
        return self
    def __getitem__(self,item):
        if item in self.data:
            return self.data.get(item)
        else:
            return 0
    def __str__(self):
        for key, value in self.data.items():
            items = []
            for key, value in self.data.items():
                items.append("{%s,%s}" % (key, value))
            return ' '.join(items)

    def most_common(self, other=0):
        counter = 0
        templist = [(k, v) for k, v in self.data.items()]
        mostcommon = []
        while counter != other:
            temp = None
            largestVal = 0

            for x in range(0, len(templist)):
                if templist[x][1] > largestVal:
                    largestVal = templist[x][1]
                    temp = templist[x]

            counter += 1
            mostcommon.append(temp)
            templist.remove(temp)

            if not templist:
                break

        return mostcommon




if __name__ == "__main__":
    # easy tests
    c1 = CountedSet()  # Make a CountedSet
    c1 += 4  # Add 4 to it
    assert c1[4] == 1  # There should be one 4
    c1 += 4  # Add another 4
    assert c1[4] == 2  # There should be two 4's
    c1 += c1  # Now there are four 4's
    c1 += c1  # Now there ate eight 8's
    assert c1[4] == 8
    assert c1[17] == 0  # There should be no 17's
    c1 += 17
    c1 += 17
    assert c1[17] == 2  # Now there is a 17
    assert c1[4] == 8  # And still eight 4's
    c1 += "fred"  # Add a word
    assert c1["fred"] == 1  # check the count

    # Can you make a set from a set
    c2 = CountedSet()
    c2 += c1
    c2 += c1
    c2 += 4
    assert c2[4] == 17
    assert c1[4] == 8

    # Does an empty set work
    c3 = CountedSet()
    assert c3[5] == 0
    assert c3[-10] == 0
    assert c3["fred"] == 0

    # Does most_common work
    assert c1.most_common(1) == [(4, 8)]
    assert c1.most_common(2) == [(4, 8), (17, 2)]
    assert c1.most_common(1000) == [(4, 8), (17, 2), ("fred", 1)]
    c2 = CountedSet()
    assert c2.most_common() == []

    print("All easy tests passed\n\n")

    # Do a bunch of random integers.  Make sure we get the same answers as the builtin Counter class
    for size in range(1, 10000, 173):
        c1 = CountedSet()
        ans = Counter()
        l = [randint(1, size) for x in range(1, 10000)]
        for x in l:
            r = randint(1, size)
            c1 += r  # add r into a CountedSet
            ans[r] += 1  # add r into a Counter
        double = CountedSet()
        double += c1
        double += c1
        for x in range(1, size):
            assert c1[x] * 2 == double[x]
            assert c1[x] == ans[x]
    print("All integer Tests Passed!\n\n")

    # Read a web page.  See if we get the same answers as the builtin Counter class with words
    c3 = CountedSet()
    ans = Counter()
    req = Request("http://www.nytimes.com/")
    try:
        responce = urlopen(req)
        text = responce.read().decode("utf-8")
        words = re.split(r"[<|>|\s]+", text)
        for word in words:
            c3 += word
            ans[word] += 1
        for word in words:
            assert c3[word] == ans[word]
        print("Processed {0} words".format(len(words)))
        for x in c3.most_common():
            print("\tAppeared {1} times:{0}".format(x[0], c3[x[0]]))
        print("All word tests passed\n\n")

        assert c3.most_common(1) == ans.most_common(1)
        assert c3.most_common(7) == ans.most_common(7)
        print("All word most_common tests passed")


    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        pass
