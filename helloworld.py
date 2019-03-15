#learning python
str = "hello world"

print(str[3:5], str[3:], str*2, str + "Addition")

int = 5

arr = [1, 2, 3, '4'] #mutable
print(arr[0], arr[0:3], arr[3:])

tuple = (1, 2, 3, '5') #immutable

map = {'one': 1, 'two': 2, 'three': 3, 'four': '4' } #like javascript
print(map['one'], map['two'], map['three'])

map['one'] = 'one got changed'
map['four'] = 'four got changed'
values = map.values()
print(list(values))

i = 0
for i in range(0, tuple.__len__()):
    if i > 2:
        print('third!')
    else:
        print("%s" % [i])

undefined = None
if undefined:
    print("this shouldn't work")
else:
    print("But this should")

undefined = 5
if undefined:
    print("now it should %s" % undefined)

mapReference = map
if mapReference is map:
    print("mapReference is actually a reference of map")

# how to know the datatypes???
def boringFunction(arg1, arg2, arg3):
    print("calling boringFunction with some args: %s %s %s" % (arg1, arg2, arg3))
    return

boringFunction('hello', 'world', 'function')

def interestingFunction(*args):
    print(args)
    return
someOtherArgs = ['dynamic arg3', 'dynamic arg4']
interestingFunction('dynamic arg 1', 'dynamic arg2', *someOtherArgs)

hasElements = lambda x: x.__len__() > 0

def referenceFunction(aInnocentList = [], aInnocentTuple = (), aInnocentDictionary = {}):
    if hasElements(aInnocentList):
        aInnocentList[0] = 'changed value'

    try:
        if hasElements(aInnocentTuple):
            aInnocentTuple[0] = 'changed value'
    except Exception:
        print("something went wrong ... you cant assign values to tuples, bu you can copy a tuple to a list")
        aInnocentCopy = [*aInnocentTuple]
        if hasElements(aInnocentCopy):
            aInnocentCopy[0] = 'got changed'
        print(aInnocentCopy)



    if 'one' in list(aInnocentDictionary.keys()):
        aInnocentDictionary['one'] = 'changed Value'

    return


aInnocentList = ['not changed']
aInnocentTuple = ('not changed',)
aInnocentDictionary = { 'one': 'not changed' }

referenceFunction(aInnocentList, aInnocentTuple, aInnocentDictionary)

print(aInnocentList, aInnocentTuple, aInnocentDictionary)

def callback(optionalArg = None):
    if optionalArg:
        print("called with the optional arg with value %s" % optionalArg)
    return "this is the value of the callback function"

def callbackCaller(callback):
    print("return value of callback function %s" % callback())
    return

callbackCaller(callback)

callbackWrapper = lambda: callback("heh i'm optional")

callbackCaller(callbackWrapper)

def strategy1():
    return "strategy1"

def strategy2():
    return "strategy2"

strategies = {'bestStrategy': strategy1, 'worstStrategy': strategy2}

print("the best strategy is now: %s" % strategies['bestStrategy']())

strategies['bestStrategy'] = strategy2

print("the best strategy has changed: %s" % strategies['bestStrategy']())

class Plane:
    # Static though
    publicMember = 40
    __privateMember = 5

    def publicMethod(self):
        self.publicMember = 6
        print("plane")
        return

    def __privateMethod(self):
        self.__privateMember = 8
        return

class BabyPlane(Plane):
    def publicMethod(self):
        print("baby plane")
        return

    def __init__(super):
        super.publicMember = 'test'
        print(super.publicMember)




