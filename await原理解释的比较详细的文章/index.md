# python3异步编程async/await原理解释的比较详细的文章




身为`Python`核心开发组的成员，我对于这门语言的各种细节充满好奇。尽管我很清楚自己不可能对这门语言做到全知全能，但哪怕是为了能够解决各种issue和参与常规的语言设计工作，我也觉得有必要试着接触和理解`Python`的内核，弄清楚在底层它是怎么工作的。

话虽如此，直到最近我才理解了[Python3.5中`async/await`的工作机制](https://docs.python.org/3/whatsnew/3.5.html#whatsnew-pep-492)。在此之前，对于`async/await`语法，我只知道[Python3.3中的`yield from`](https://docs.python.org/3/whatsnew/3.3.html#pep-380)和[Python3.4中的`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio)让这个新语法得以在Python3.5中实现。由于日常工作中没有接触多少网络编程--`asyncio`的主要应用领域，虽然它可以做的远不止于此--我对`async/await`并没有关注太多。以代码来说，我知道：

```python
yield from iterator
```

(大体)等价于:

```python
from x in iterator:
    yield x
```

而且我知道`asyncio`是个事件循环的框架，支持异步编程，还有这些术语所表示的(基本)意义。但未曾真正的深入研究`async/await`语法，分析从最基础的指令到实现代码语法功能的过程，我觉得并没有理解Python中的异步编程，这一点甚至让我心烦意乱。因此我决定花点时间弄明白这个语法的工作机制。鉴于我听到许多人说他们也不理解异步编程的工作机制，我写出了这篇论文(是的，这篇博文耗费时间之长，字数之多，让我妻子把它叫做论文)。

由于我希望对这个语法的工作机制有一个完整的理解，这篇论文中会出现涉及CPython的底层技术细节。如果你不关心这些细节，或者无法通过这篇文章完全理解这些细节--限于篇幅，我不可能详细解释CPython的每个细节，否则这篇文章就要变成一本书了(例如，如果你不知道代码对象具有标识位，那就别在意代码对象是什么，这不是这篇文章的重点)--那也没什么关系。在每个章节的最后，我都添加了一个概念明确的小结，因此如果你对某个章节的内容不感兴趣，那么可以跳过前面的长篇大论，直接阅读结论。

Python中协程(coroutine)的历史

根据[维基百科](https://www.wikipedia.org/)，“[协程](https://en.wikipedia.org/wiki/Coroutine)是将多个低优先级的任务转换成统一类型的子任务，以实现在多个节点之间停止或唤醒程序运行的程序模块”。这句专业论述翻译成通俗易懂的话就是，“协程就是可以人为暂停执行的函数”。如果你觉得，“这听起来像是生成器(generators)”，那么你是对的。

生成器的概念在[Python2.2](https://docs.python.org/3/whatsnew/2.2.html)时的[PEP 255](https://www.python.org/dev/peps/pep-0255/)中(由于实现了[遍历器的协议](https://docs.python.org/3/library/stdtypes.html#iterator-types)，生成器也被成为生成器遍历器)第一次被引入。主要受到了[Icon语言](http://www.cs.arizona.edu/icon/)的影响，生成器允许用户创建一个特殊的遍历器，在生成下一个值时，不会占用额外的内存，并且实现方式非常简单(当然，在自定义类中实现`__iter__()`和`__next__()`方法也可以达到不存储遍历器中所有值的效果，但也带来了额外的工作量)。举例来说，如果你想实现自己的`range()`函数，最直接的方式是创建一个整数数组：

```python
def eager_range(up_to):
    """创建一个从0到变量up_to的数组，不包括up_to"""
    sequence = []
    index = []
    while index < up_to:
        sequence.append(index)
        index += 1
    return sequence
```

简单直白，但这个函数的问题是，如果你需要的序列很大，比如0到一百万，你必须创建一个包含了所有整数的长度是一百万的数组。如果使用生成器，你就可以毫不费力的创建一个从0到上限前一个整数的生成器。所占用的内存也只是每次生成的一个整数。

```python
def lazy_range(up_to):
    """一个从0到变量up_to，不包括up_to的生成器"""
    index = 0
    while index < up_to:
        yield index
        index += 1
```

函数可以在遇到`yield`表达式时暂停执行--尽管`yield`直到Python2.5才出现--然后在下次被调用时继续执行，这种特性对于节约内存使用有意义深远，可以用于实现无限长度的序列。

也许你已经注意到了，生成器所操作的都是遍历器。多一种更好的创建遍历器的语法的确不错(当你为一个对象定义`__iter__()`方法作为生成器时，也会收到类似的提升)，但如果我们把生成器的“暂停”功能拿出来，再加上“把事物传进去”的功能，Python就有了自己的协程功能(暂且把这个当成Python的一个概念，真正的Python中的协程会在后面详细讨论)。[Python 2.5](https://docs.python.org/3/whatsnew/2.5.html)中引入了把对象传进一个被暂停的生成器的功能，这要归功于[PEP 342](https://www.python.org/dev/peps/pep-0342/)。抛开与本文无关的内容不看，PEP 342引入了生成器的`send()`方法。这样就不光可以暂停生成器，更可以在生成器停止时给它传回一个值。在上文`range()`函数的基础上更近一步，你可以让函数产生的序列前进或后退：

```python
def jumping_range(up_to):
    """一个从0到变量up_to，不包括up_to的生成器
    传入生成器的值会让序列产生对应的位移
    """
    index = 0
    while index < up_to:
        jump = yield index
        if jump is None: ##原文这里是 if jump is Not None, 应该是笔误，此处已做修改
            jump = 1
        index += jump
 
if __name__ == '__main__':
    iterator = jumping_range(5)
    print(next(iterator))  # 0
    print(iterator.send(2))  # 2
    print(next(iterator))  # 3
    print(iterator.send(-1))  # 2
    for x in iterator:
        print(x)  # 3, 4
```

直到[Python 3.3](https://docs.python.org/3/whatsnew/3.3.html)中[PEP 380](https://www.python.org/dev/peps/pep-0380/)引入`yield from`之前，生成器都没有太大的变化。严格的说，`yield from`让用户可以轻松便捷的从遍历器(生成器最常见的应用场景)里提取每一个值，进而重构生成器。

```python
def lazy_range(up_to):
    """一个从0到变量up_to，不包括up_to的生成器"""
    index = 0
    def gratuitous_refactor():
        nonlocal index
        while index < up_to:
            yield index
            index += 1
    yield from gratuitous_refactor()
```

同样出于简化重构操作的目的，`yield from`也支持将生成器串连起来，这样再不同的调用栈之间传递值时，不需要对原有代码做太大的改动。

```python
def bottom():
    """返回yield表达式来允许值通过调用栈进行传递"""
    return (yield 42)
 
def middle():
    return (yield from bottom())
 
def top():
    return (yield from middle())
 
# 获取生成器
gen = top()
value = next(gen)
print(value)  # Prints '42'
 
try:
    value = gen.send(value * 2)
except StopIteration as exc:
    print("Error!")  # Prints 'Error!'
    value = exc.value
print(value)  # Prints '84'
```

总结

Python2.2引入的生成器使代码的执行可以被暂停。而在Python2.5中引入的允许传值给被暂停的生成器的功能，则让Python中协程的概念成为可能。在Python3.3中引入的`yield from`让重构和连接生成器变得更加简单。

### **事件循环是什么？**

如果你想理解`async/await`语法，那么理解事件循环的定义，知道它如何支持的异步编程，是不可或缺的基础知识。如果你曾经做过GUI编程--包括网页前端工作--那么你已经接触过事件循环了。但在Python的语言体系中，异步编程的概念还是第一次出现，所以如果不知道事件循环是什么，也情有可原。

让我们回到维基百科，[事件循环](https://en.wikipedia.org/wiki/Event_loop)是“在程序中等待、分发事件或消息的编程结构”。简而言之，事件循环的作用是，“当A发生后，执行B”。最简单的例子可能是每个浏览器中都有的JavaScript事件循环，当你点击网页某处("当A发生后")，点击事件被传递给JavaScript的事件循环，然后事件循环检查网页上该位置是否有注册了处理这次点击事件的`onclick`回调函数("执行B")。如果注册了回调函数，那么回调函数就会接收点击事件的详细信息，被调用执行。事件循环会不停的收集发生的事件，循环已注册的事件操作来找到对应的操作，因此被称为“循环”。

Python标准库中的`asyncio`库可以提供事件循环。`asyncio`在网络编程里的一个重要应用场景，就是以连接到socket的I/O准备好读/写(通过[selector模块](https://docs.python.org/3/library/selectors.html#module-selectors)实现)事件作为事件循环中的“当A发生后”事件。除了GUI和I/O，事件循环也经常在执行多线程或多进程代码时充当调度器(例如[协同式多任务处理](https://en.wikipedia.org/wiki/Cooperative_multitasking))。如果你知道Python中的GIL(General Interpreter Lock)，事件循环在规避GIL限制方面也有很大的作用。

总结

事件循环提供了一个让你实现“当事件A发生后，执行事件B”功能的循环。简单来说，事件循环监视事件的发生，如果发生的是事件循环关心(“注册”过)的事件，那么事件循环会执行所有被关联到该事件的操作。在Python3.4中加入标准库的`asyncio`使Python也有了事件循环。

### `async`和`await`是怎么工作的

在Python3.4中的工作方式

在Python3.3推动生成器的发展和Python3.5中事件循环以`asyncio`的形式出现之间，Python3.4以[并发编程](https://en.wikipedia.org/wiki/Concurrent_computing)的形式实现了异步编程。从本质上说，异步编程就是无法预知执行时间的计算机程序(也就是异步，而非同步)。并发编程的代码即使运行在同一个线程中，执行时也互不干扰([并发**不是**并行](http://blog.golang.org/concurrency-is-not-parallelism))。例如，以下Python3.4的代码中，并发两个异步的函数调用，每秒递减计数，互不干扰。

```python
import asyncio
 
# Borrowed from http://curio.readthedocs.org/en/latest/tutorial.html.
 
def countdown(number, n):
    while n > 0:
        print('T-minus', n, '({})'.format(number))
        yield from asyncio.sleep(1)
        n -= 1
 
loop = asyncio.get_event_loop()
tasks = [
    asyncio.ensure_future(countdown('A', 2)),
    asyncio.ensure_future(countdown('B', 3))
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
```

在Python3.4中，[`asyncio.coroutine`装饰器](https://docs.python.org/3/library/asyncio-task.html#asyncio.coroutine)被用于修饰使用`asyncio`库并且作为[协程](https://docs.python.org/3/reference/datamodel.html?#coroutine-objects)在它的事件循环中运行的函数。这是Python中第一次出现明确的协程定义：一种实装了[PEP 342](https://www.python.org/dev/peps/pep-0342/)中添加给生成器的方法，基类是[抽象类`collections.abc.Coroutine`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Coroutine)的对象。这个定义让那些原本没有异步执行意图的生成器也带上了协程的特征。而为了解决这种混淆，`asyncio`规定所有作为协程执行的函数都需要以[`asyncio.coroutine`装饰器](https://docs.python.org/3/library/asyncio-task.html#asyncio.coroutine)进行修饰。

有了这样一个明确的协程的定义(同时符合生成器的接口规范)，你可以使用`yield from`将任何[`asyncio.Future`对象](https://docs.python.org/3/library/asyncio-task.html#future)传入事件循环，在等待事件发生时暂停程序执行(future对象是`asyncio`中的一种对象，此处不再详述)。future对象进入事件循环后就处于事件循环的监控之下，一旦future对象完成了自身任务，事件循环就会唤醒原本被暂停的协程继续执行，future对象的返回结果则通过`send()`方法由事件循环传递给协程。

以上文代码为例，事件循环启动了两个调用`call()`函数的协程，运行到某个协程中包含`yield from`和`asyncio.sleep()`语句处，这条语句将一个`asyncio.Future`对象返回事件循环，暂停协程的执行。这时事件循环会为future对象等待一秒(并监控其他程序，例如另外一个协程)，一秒后事件循环唤醒传出了future对象的被暂停的`countdown()`协程继续执行，并把future对象的执行结果归还给原协程。这个循环过程会持续到`countdown()`协程结束执行，事件循环中没有被监控的事件为止。稍后我会用一个完整的例子详细解释协程/事件循环结构的工作流程，但首先，我要解释一下`async`和`await`是如何工作的。

从`yield from`到Python3.5中的`await`

在Python3.4中，一个用于异步执行的协程代码会被标记成以下形式：

```python
# 这种写法在Python3.5中同样有效
@asyncio.coroutine
def py34_coro():
    yield from stuff()
```

Python3.5也添加了一个作用和`asyncio.coroutine`相同，用于修饰协程函数的[装饰器`types.coroutine`](https://docs.python.org/3/library/types.html#types.coroutine)。也可以使用`async def`语法定义协程函数，但是这样定义的协程函数中不能使用`yield`语句，只允许使用`return`或`await`语句返回数据。

```python
async def py35_coro():
    await stuff()
```

对同一个协程概念添加的不同语法，是为了规范协程的定义。这些陆续补充的语法使协程从抽象的接口变成了具体的对象类型，让普通的生成器和协程用的生成器有了明显的区别([`inspect.iscoroutine()`方法](https://docs.python.org/3/library/inspect.html#inspect.iscoroutine)的判断标准则比`async`还要严格)。

另外，除了`async`，Python3.5也引入了`await`语法(只能在`async def`定义的函数中使用)。虽然`await`的使用场景与`yield from`类似，但是`await`接收的对象不同。作为由于协程而产生的语法，`await`接收协程对象简直理所当然。但是当你对某个对象使用`await`语法时，技术上说，这个对象必须是[可等待对象(awaitable object)](https://docs.python.org/3/reference/datamodel.html?#awaitable-objects)：一种定义了`__await__()`方法(返回非协程本身的遍历器)的对象。协程本身也被视作可等待对象(体现在Python语言设计中，就是`collections.abc.Coroutine`继承了`collections.abc.Awaitable`抽象类)。可等待对象的定义沿用了Python中将大多数语法结构在底层转换成方法调用的传统设计思想，例如`a + b`等价于`a.__add__(b)`或`b.__radd__(a)`。

那么在编译器层面，`yield from`和`await`的运行机制有什么区别(例如`types.coroutine`修饰的生成器和`async def`语法定义的函数)呢？让我们看看上面两个例子在Python3.5环境下执行时的字节码细节有什么不同，`py34_coro()`执行时的字节码是：

```python
In [31]: dis.dis(py34_coro)
  3           0 LOAD_GLOBAL              0 (stuff)
              3 CALL_FUNCTION            0 (0 positional, 0 keyword pair)
              6 GET_YIELD_FROM_ITER
              7 LOAD_CONST               0 (None)
             10 YIELD_FROM
             11 POP_TOP
             12 LOAD_CONST               0 (None)
             15 RETURN_VALUE
```

`py35_coro()`执行时的字节码是：

```python
In [33]: dis.dis(py35_coro)
  2           0 LOAD_GLOBAL              0 (stuff)
              3 CALL_FUNCTION            0 (0 positional, 0 keyword pair)
              6 GET_AWAITABLE
              7 LOAD_CONST               0 (None)
             10 YIELD_FROM
             11 POP_TOP
             12 LOAD_CONST               0 (None)
             15 RETURN_VALUE
```

除了`py34_coro`代码中多了一行装饰器而导致的行号不同，两组字节码的区别集中在[`GET_YIELD_FROM_ITER`操作符](https://docs.python.org/3/library/dis.html#opcode-GET_YIELD_FROM_ITER)和[`GET_AWAITABLE`操作符](https://docs.python.org/3/library/dis.html#opcode-GET_AWAITABLE)。两个函数都是以协程的语法声明的。对于`GET_YIELD_FROM_ITER`，编译器只检查参数是否生成器或者协程，如果不是，就调用`iter()`函数遍历参数(`types.coroutine`装饰器修饰了生成器，让代码对象在C代码层面附带了`CO_ITERABLE_COROUTINE`标识，因此`yield from`语句可以在协程中接收协程对象)。

`GET_AWAITABLE`则是另外一番光景。虽然同`GET_YIELD_FROM_ITER`操作符一样，字节码也接收协程对象，但它不会接收没有协程标记的生成器。而且，正如前文所述，字节码不止接收协程对象，也可以接收可等待对象。这样，`yield from`语句和`await`语句都可以实现协程概念，但一个接收的是普通的生成器，另一个是可等待对象。

也许你会好奇，为什么基于`async`的协程和基于生成器的协程在暂停时接收的对象会不同？这种设计的主要目的是让用户不至于混淆两种类型的协程实现，或者不小心弄错类似的API的参数类型，甚而影响Python最重要的特性的使用体验。例如生成器继承了协程的API，在需要协程时很容易犯使用了普通的生成器的错误。生成器的使用场景不限于通过协程实现流程控制的情况，因此很容易的辨别普通生成器和协程也非常重要。可是，Python不是需要预编译的静态语言，在使用基于生成器的协程时编译器只能做到在运行时进行检查。换句话说，就算使用了`types.coroutine`装饰器，编译器也无法确定生成器会充当本职工作还是扮演协程的角色(记住，即使代码中明明白白使用了`types.coroutine`装饰器，依然有在之前的代码中类似`types = spam`这样的语句存在的可能)，编译器会根据已知的信息，在不同的上下文环境下调用不同的操作符。

对于基于生成器的协程和`async`定义的协程的区别，我的一个非常重要的观点是，只有基于生成器的协程可以真正的暂停程序执行，并把外部对象传入事件循环。当你使用事件循环相关的函数，如[`asyncio.sleep()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep)时，这些函数与事件循环的交互所用的是框架内部的API，事件循环究竟如何变化，并不需要用户操心，因此也许你很少看到这种关注底层概念的说法。我们大多数人其实并不需要真正实现一个事件循环，而只需要使用`async`这样的语法来通过事件循环实现某个功能。但如果你像我一样，好奇为什么我们不能使用`async`协程实现类似`asnycio.sleep()`的功能，那么答案就在这里。

总结

让我们总结一下这两个相似的术语，使用`async def`可以定义协程，使用`types.coroutine`装饰器可以将一个生成器--返回一个不是协程本身的遍历器--声明为协程。`await`语句只能用于可等待对象(`await`不能作用于普通的生成器)，除此之外就和`yield from`的功能基本相同。`async`函数定义的协程中一定会有`return`语句--包括每个Python函数都有的默认返回语句`return None`--和/或`await`语句(不能使用`yield`语句)。对`async`函数所添加的限制，是为了保证用户不会混淆它和基于生成器的协程，两者的期望用途差别很大。

### 请把`async/await`视为异步编程的API

[David Bzazley的Python Brasil 2015 keynote](https://www.youtube.com/watch?v=lYe8W04ERnY)让我发现自己忽略了一件很重要的事。在那个演讲中，David指出，`async/await`其实是一种异步编程的API(他在Twitter上[对我说过同样的话](https://twitter.com/dabeaz/status/696028946220056576))。我想David的意思是，我们不应该把`async/await`当成`asnycio`的一种别名，而应该利用`async/await`，让`asyncio`成为异步编程的通用框架。

David对将`async/await`作为异步编程API的想法深信不疑，甚至在他的[`curio`项目](https://pypi.python.org/pypi/curio)中实现了自己的事件循环。这也侧面证明了Python中`async/await`作为异步编程语法的作用(不像其他集成了事件循环的语言那样，用户需要自己实现事件循环和底层细节)。`async/await`语法让像`curio`这样的项目可以进行不同的底层操作(`asyncio`使用future对象与事件循环进行交互，而`curio`使用元祖对象)，还让它们可以有不同的侧重和性能优化(为了更广泛的适用性，`asyncio`实现了完整的传输和协议层框架，而相对简单的`curio`则需要用户实现那些框架，但也因此获得了更快的运行速度)。

看完了Python中异步编程的(简略)历史，很容易得出`async/await` == `asyncio`的结论。我想说的是，`asyncio`导致了Python3.4中异步编程的出现，并且对Python3.5中`async/await`的产生居功至伟，但是，`async/await`的灵活的设计，甚至到了可以_不使用_`asyncio`的地步，也不需要为了应用`asyncio`框架而修改架构。简而言之，`async/await`语法延续了Python在保证实用性的同时尽可能的让设计灵活的传统。

### 一个例子

看到这里，你的脑子里应该已经装满了各种新术语和新概念，但对于这些新事物如何实现异步编程却仍一知半解。为了加深理解，以下是一个(略显做作的)异步编程的例子，包括完整的从事件循环到相关业务函数的代码。在这个例子中，协程的用途是实现独立的火箭发射倒计时器，产生的效果是同步进行的倒计时。这是通过异步编程而实现的函数并发，程序执行是有三个协程运行在在同一个线程中，却可以彼此互不干扰。

```python
import datetime
import heapq
import types
import time
 
 
class Task:
 
    """Represent how long a coroutine should wait before starting again.
    Comparison operators are implemented for use by heapq. Two-item
    tuples unfortunately don't work because when the datetime.datetime
    instances are equal, comparison falls to the coroutine and they don't
    implement comparison methods, triggering an exception.
    
    Think of this as being like asyncio.Task/curio.Task.
    """
 
    def __init__(self, wait_until, coro):
        self.coro = coro
        self.waiting_until = wait_until
 
    def __eq__(self, other):
        return self.waiting_until == other.waiting_until
 
    def __lt__(self, other):
        return self.waiting_until < other.waiting_until
 
 
class SleepingLoop:
 
    """An event loop focused on delaying execution of coroutines.
    Think of this as being like asyncio.BaseEventLoop/curio.Kernel.
    """
 
    def __init__(self, *coros):
        self._new = coros
        self._waiting = []
 
    def run_until_complete(self):
        # Start all the coroutines.
        for coro in self._new:
            wait_for = coro.send(None)
            heapq.heappush(self._waiting, Task(wait_for, coro))
        # Keep running until there is no more work to do.
        while self._waiting:
            now = datetime.datetime.now()
            # Get the coroutine with the soonest resumption time.
            task = heapq.heappop(self._waiting)
            if now < task.waiting_until:
                # We're ahead of schedule; wait until it's time to resume.
                delta = task.waiting_until - now
                time.sleep(delta.total_seconds())
                now = datetime.datetime.now()
            try:
                # It's time to resume the coroutine.
                wait_until = task.coro.send(now)
                heapq.heappush(self._waiting, Task(wait_until, task.coro))
            except StopIteration:
                # The coroutine is done.
                pass
 
 
@types.coroutine
def sleep(seconds):
    """Pause a coroutine for the specified number of seconds.
    Think of this as being like asyncio.sleep()/curio.sleep().
    """
    now = datetime.datetime.now()
    wait_until = now + datetime.timedelta(seconds=seconds)
    # Make all coroutines on the call stack pause; the need to use `yield`
    # necessitates this be generator-based and not an async-based coroutine.
    actual = yield wait_until
    # Resume the execution stack, sending back how long we actually waited.
    return actual - now
 
 
async def countdown(label, length, *, delay=0):
    """Countdown a launch for `length` seconds, waiting `delay` seconds.
    This is what a user would typically write.
    """
    print(label, 'waiting', delay, 'seconds before starting countdown')
    delta = await sleep(delay)
    print(label, 'starting after waiting', delta)
    while length:
        print(label, 'T-minus', length)
        waited = await sleep(1)
        length -= 1
    print(label, 'lift-off!')
 
 
def main():
    """Start the event loop, counting down 3 separate launches.
    This is what a user would typically write.
    """
    loop = SleepingLoop(countdown('A', 5), countdown('B', 3, delay=2),
                        countdown('C', 4, delay=1))
    start = datetime.datetime.now()
    loop.run_until_complete()
    print('Total elapsed time is', datetime.datetime.now() - start)
 
 
if __name__ == '__main__':
    main()
```

正如前文所说，这个例子是有意为之，如果在Python3.5下运行，你会发现虽然三个协程在同一线程中互不干扰，但总运行时间是5秒左右。你可以把`Task`，`SleepingLoop`和`sleep()`看成`asyncio`和`curio`这样生成事件循环的框架提供的接口函数，对普通用户来说，只有`countdown()`和`main()`函数才需要关注。到此为止，你应该已经明白，`async`，`await`语句，甚至整个异步编程，都不是完全无法理解的魔术，`async/await`只是Python为了让异步编程更简便易用而添加的API。

### 我对未来的愿景

我已经理解了Python中的异步编程，我想把它用到所有地方！这个精巧高效的概念完全可以替代原本线程的作用。问题是，Python3.5和`async/await`都是面世不久的新事物，这就意味着支持异步编程的库数量不会太多。例如，要发送HTTP请求，你要么手动构造HTTP请求对象(麻烦透顶)，然后用一个类似[`aiohttp`](https://pypi.python.org/pypi/aiohttp)的框架把HTTP放进另外的事件循环(对于`aiohttp`，是`asyncio`)开始操作；要么就等着哪天出现一个像[`hyper`](https://pypi.python.org/pypi/hyper)这样的项目对HTTP这类I/O进行抽象，让你可以使用任意的I/O库(遗憾的是，到目前为止`hyper`只支持HTTP/2)。

我的个人观点是希望像`hyper`这样的项目可以继续发展，分离从I/O获取二进制数据和解析二进制数据的逻辑。Python中大部分的I/O库都是包揽进行I/O操作和处理从I/O接收的数据，因此对操作分离进行抽象意义重大。Python标准库的[`http`包](https://docs.python.org/3/library/http.html#module-http)也存在同样的问题，有处理I/O的连接对象，却没有HTTP解析器。而如果你希望`requests`库支持异步编程，那么[你可能要失望了](https://github.com/kennethreitz/requests/issues/2801)，因为`requests`从设计上就是同步编程。拥有异步编程能力让Python社区有机会弥补Python语言中没有多层网络栈抽象的缺点。现在Python的优势是可以像运行同步代码那样运行异步代码，因此填补异步编程空白的工具，可以应用在同步异步两种场景中。

我还希望Python可以增加`async`协程对`yield`语句的支持。这可能需要一个新的关键字(也许是`anticipate`?)，但只使用`async`语法就不能实现事件循环的情况实在不尽人意。幸运的是，[在这一点上我不是一个人](https://twitter.com/dabeaz/status/696014754557464576)，[PEP 492](https://www.python.org/dev/peps/pep-0492/)的作者与我观点相同，我觉得这个愿望很有可能成为现实。

# 总结

总而言之，`async`和`await`出现的目的就是为了协程，顺便支持可等待对象，也可以把普通生成器转换成协程。所有这些都是为了实现并发操作，来提升Python中的异步编程体验。相比使用多线程的编程体验，协程功能强大并且更为易用--只用了包括注释在内的不到100行代码就实现了一个完整的异步编程实例--兼具良好的适用性和运行效率(curio的FAQ里说它的运行速度比`twisted`快30-40%，比`gevent`慢10-15%，别忘了，在Python2+版本中，Twisted用的内存更少而且调试比Go简单，想想我们可以做到什么程度！)。能在Python 3中看到`async/await`的引入，我非常高兴，并且期待Python社区接纳这个新语法，希望有更多的库和框架支持`async/await`语法，让所有的Python开发者都可以从异步编程中受益。

# 来源
https://blog.csdn.net/permike/article/details/110821246
